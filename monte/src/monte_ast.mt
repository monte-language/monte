module unittest
export (makeLiteralExpr, makeNounExpr, makeFinalPattern)

def idStart := 'a'..'z' | 'A'..'Z' | '_'..'_'
def idPart := idStart | '0'..'9'

# note to future drunk self: lower precedence number means add parens when
# inside a higher-precedence-number expression
def priorities := [
     "indentExpr" => 0,
     "braceExpr" => 1,
     "assign" => 2,
     "logicalOr" => 3,
     "logicalAnd" => 4,
     "comp" => 5,
     "order" => 6,
     "interval" => 7,
     "shift" => 8,
     "addsub" => 9,
     "divmul" => 10,
     "exp" => 11,
     "prefix" => 12,
     "send" => 13,
     "coerce" => 14,
     "call" => 15,
     "prim" => 16]

def makeScopeSet(items):
    return object scopeset extends ([k => null for k in items]):
        to _makeIterator():
            return super.getKeys()._makeIterator()
        to contains(k):
            return super.maps(k)
        to subtract(right):
            def new := super.diverge()
            for k in right:
                if (super.maps(k)):
                    new.removeKey(k)
            return makeScopeSet(new.snapshot())
        to printOn(out):
            out.print(super.getKeys())

def makeStaticScope(read, set, defs, vars, metaStateExpr):
    def namesRead := makeScopeSet(read)
    def namesSet := makeScopeSet(set)
    def defNames := makeScopeSet(defs)
    def varNames := makeScopeSet(vars)
    return object staticScope:
        to getNamesRead():
            return namesRead

        to getNamesSet():
            return namesSet

        to getDefNames():
            return defNames

        to getVarNames():
            return varNames

        to getMetaStateExprFlag():
            return metaStateExpr

        to hide():
            return makeStaticScope(namesRead, namesSet, null, null,
                                   metaStateExpr)

        to add(right):
            if (right == null):
                return staticScope
            def rightNamesRead := (right.getNamesRead() - defNames) - varNames
            def rightNamesSet := right.getNamesSet() - varNames
            def badAssigns := rightNamesSet & defNames
            if (badAssigns.size() > 0):
                throw(`Can't assign to final nouns ${badAssigns}`)
            return makeStaticScope(namesRead | rightNamesRead,
                                   namesSet | rightNamesSet,
                                   defNames | right.getDefNames(),
                                   varNames | right.getVarNames(),
                                   metaStateExpr | right.getMetaStateExprFlag())
        to namesUsed():
            return namesRead | namesSet

        to outNames():
            return defNames | varNames

        to printOn(out):
            out.print("<")
            out.print(namesSet)
            out.print(" := ")
            out.print(namesRead)
            out.print(" =~ ")
            out.print(defNames)
            out.print(" + var ")
            out.print(varNames)
            out.print(" ")
            out.print(metaStateExpr)
            out.print(">")

def emptyScope := makeStaticScope([], [], [], [], false)

def astWrapper(node, maker, args, span, termFunctor, transformArgs):
    return object astNode extends node:
        to asTerm():
            def termit(subnode, maker, args, span):
                return subnode.asTerm()
            return term`$termFunctor(${transformArgs(termit)}*)`.withSpan(span)
        to transform(f):
            return f(astNode, maker, transformArgs(f), span)
        to _uncall():
            return [maker, "run", args + [span]]
        to _printOn(out):
            astNode.subPrintOn(out, 0)

def makeLiteralExpr(value, span):
    object literalExpr:
        to getValue():
            return value
        to getStaticScope():
            return emptyScope
        to subPrintOn(out, priority):
            out.quote(value)
    return astWrapper(literalExpr, makeLiteralExpr, [value], span,
        term`LiteralExpr`, fn f {[value]})

def all(iterable, pred):
    for item in iterable:
        if (!pred(item)):
            return false
    return true

def makeNounExpr(name, span):
    def scope := makeStaticScope([name], [], [], [], false)
    object nounExpr:
        to getName():
            return name
        to getStaticScope():
            return scope
        to subPrintOn(out, priority):
            if (idStart(name[0]) && all(name.slice(1), idPart)):
                out.print(name)
            else:
                out.print("::")
                out.quote(name)
    return astWrapper(nounExpr, makeNounExpr, [name], span,
         term`NounExpr`, fn f {[name]})


def makeFinalPattern(noun, guard, span):
    def scope := makeStaticScope([], [], [noun.getName()], [], false)
    object finalPattern:
        to getNoun():
            return noun
        to getGuard():
            return guard
        to getStaticScope():
            return scope
        to subPrintOn(out, priority):
            noun.subPrintOn(out, priority)
            if (guard != null):
                out.print(" :")
                guard.subPrintOn(out, priorities["order"])
    return astWrapper(finalPattern, makeFinalPattern, [noun, guard], span,
        term`FinalPattern`, fn f {[noun.transform(f), guard.transform(f)]})

def makeIgnorePattern(guard, span):
    def scope := if (guard != null) {guard.getStaticScope()} else {emptyScope}
    object ignorePattern:
        to getGuard():
            return guard
        to getSpan():
            return span
        to getStaticScope():
            return scope
        to subPrintOn(out, priority):
            out.print("_")
            if (guard != null):
                out.print(" :")
                guard.subPrintOn(out, priorities["order"])
    return astWrapper(ignorePattern, makeIgnorePattern, [guard], span,
        term`IgnorePattern`, fn f {[guard.transform(f)]})

def test_literalExpr(assert):
    def expr := makeLiteralExpr("one", null)
    assert.equal(expr._uncall(), [makeLiteralExpr, "run", ["one", null]])
    assert.equal(M.toString(expr), "\"one\"")
    assert.equal(expr.asTerm(), term`LiteralExpr("one")`)

def test_nounExpr(assert):
    def expr := makeNounExpr("foo", null)
    assert.equal(expr._uncall(), [makeNounExpr, "run", ["foo", null]])
    assert.equal(M.toString(expr), "foo")
    assert.equal(expr.asTerm(), term`NounExpr("foo")`)
    assert.equal(M.toString(makeNounExpr("unwind-protect", null)),
                 "::\"unwind-protect\"")

def test_finalPattern(assert):
    def [name, guard] := [makeNounExpr("blee", null), makeNounExpr("Int", null)]
    def patt := makeFinalPattern(name, guard, null)
    assert.equal(patt._uncall(), [makeFinalPattern, "run", [name, guard, null]])
    assert.equal(M.toString(patt), "blee :Int")
    assert.equal(patt.asTerm(), term`FinalPattern(NounExpr("blee"), NounExpr("Int"))`)

def test_ignorePattern(assert):
    def guard := makeNounExpr("List", null)
    def patt := makeIgnorePattern(guard, null)
    assert.equal(patt._uncall(), [makeIgnorePattern, "run", [guard, null]])
    assert.equal(M.toString(patt), "_ :List")
    assert.equal(patt.asTerm(), term`IgnorePattern(NounExpr("List"))`)
    assert.equal(M.toString(makeIgnorePattern(null, null)), "_")

unittest([test_literalExpr, test_nounExpr, test_finalPattern, test_ignorePattern])
