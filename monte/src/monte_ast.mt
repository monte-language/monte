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

object makeScopeSet:
    to run(items):
        return makeScopeSet.fromKeys([k => null for k in items])
    to fromKeys(map):
        return object scopeset extends map:
            to _makeIterator():
                return super.getKeys()._makeIterator()
            to contains(k):
                return super.maps(k)
            to subtract(right):
                def new := super.diverge()
                for k in right:
                    if (super.maps(k)):
                        new.removeKey(k)
                return makeScopeSet.fromKeys(new.snapshot())
            to and(right):
                return makeScopeSet.fromKeys(super.and(right))
            to or(right):
                return makeScopeSet.fromKeys(super.or(right))
            to _conformTo(guard):
                return super
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

def union(additionalScopes, var scope):
    for sc in additionalScopes:
        scope += sc
    return scope

def all(iterable, pred):
    for item in iterable:
        if (!pred(item)):
            return false
    return true

def isIdentifier(name):
    return idStart(name[0]) && all(name.slice(1), idPart)

def printListOn(left, nodes, sep, right, out, priority):
    out.print(left)
    if (nodes.size() >= 1):
        for n in nodes.slice(0, nodes.size() - 1):
            n.subPrintOn(out, priority)
            out.print(sep)
        nodes.last().subPrintOn(out, priority)
    out.print(right)

def astWrapper(node, maker, args, span, scope, termFunctor, transformArgs):
    return object astNode extends node:
        to getStaticScope():
            return scope
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
        to subPrintOn(out, priority):
            out.quote(value)
    return astWrapper(literalExpr, makeLiteralExpr, [value], span,
        emptyScope, term`LiteralExpr`, fn f {[value]})

def makeNounExpr(name, span):
    def scope := makeStaticScope([name], [], [], [], false)
    object nounExpr:
        to getName():
            return name
        to subPrintOn(out, priority):
            if (isIdentifier(name)):
                out.print(name)
            else:
                out.print("::")
                out.quote(name)
    return astWrapper(nounExpr, makeNounExpr, [name], span,
         scope, term`NounExpr`, fn f {[name]})

def makeSlotExpr(name, span):
    def scope := makeStaticScope([name], [], [], [], false)
    object slotExpr:
        to getName():
            return name
        to subPrintOn(out, priority):
            out.print("&")
            if (isIdentifier(name)):
                out.print(name)
            else:
                out.print("::")
                out.quote(name)
    return astWrapper(slotExpr, makeSlotExpr, [name], span,
        scope, term`SlotExpr`, fn f {[name]})

def makeMetaContextExpr(span):
    def scope := emptyScope
    object metaContextExpr:
        to subPrintOn(out, priority):
            out.print("meta.getContext()")
    return astWrapper(metaContextExpr, makeMetaContextExpr, [], span,
        scope, term`MetaContextExpr`, fn f {[]})

def makeMetaStateExpr(span):
    def scope := makeStaticScope([], [], [], [], true)
    object metaStateExpr:
        to subPrintOn(out, priority):
            out.print("meta.getState()")
    return astWrapper(metaStateExpr, makeMetaStateExpr, [], span,
        scope, term`MetaStateExpr`, fn f {[]})

def makeBindingExpr(name, span):
    def scope := makeStaticScope([name], [], [], [], false)
    object bindingExpr:
        to getName():
            return name
        to subPrintOn(out, priority):
            out.print("&&")
            if (isIdentifier(name)):
                out.print(name)
            else:
                out.print("::")
                out.quote(name)
    return astWrapper(bindingExpr, makeBindingExpr, [name], span,
        scope, term`BindingExpr`, fn f {[name]})

def makeSeqExpr(exprs, span):
    def scope := union([e.getStaticScope() for e in exprs], emptyScope)
    object seqExpr:
        to getExprs():
            return exprs
        to subPrintOn(out, priority):
            if (priority > priorities["braceExpr"]):
                out.print("(")
            var first := true
            for e in exprs:
                if (!first):
                    out.println("")
                first := false
                e.subPrintOn(out, priority.min(priorities["braceExpr"]))
    return astWrapper(seqExpr, makeSeqExpr, [exprs], span,
        scope, term`SeqExpr`, fn f {[[e.transform(f) for e in exprs]]})

def makeModule(imports, exports, body, span):
    def scope := union(imports, emptyScope) + union(exports, emptyScope)
    object ::"module":
        to getImports():
            return imports
        to getExports():
            return exports
        to getBody():
            return body
        to subPrintOn(out, priority):
            out.print("module")
            if (imports.size() > 0):
                out.print(" ")
                printListOn("", imports, ", ", "", out, priorities["braceExpr"])
            if (exports.size() > 0):
                out.print("export ")
                printListOn("(", exports, ", ", ")", out, priorities["braceExpr"])
            body.subPrintOn(out, priorities["indentExpr"])
    return astWrapper(::"module", makeModule, [imports, exports, body], span,
        scope, term`Module`, fn f {[
            [e.transform(f) for e in imports],
            [e.transform(f) for e in exports],
            body.transform(f)]})

def makeMethodCallExpr(rcvr, verb, arglist, span):
    def scope := union([a.getStaticScope() for a in arglist],
                       rcvr.getStaticScope())
    object methodCallExpr:
        to getReceiver():
            return rcvr
        to getVerb():
            return verb
        to getArglist():
            return arglist
        to subPrintOn(out, priority):
            if (priorities["call"] < priority):
                out.print("(")
            rcvr.subPrintOn(out, priorities["call"])
            if (verb != "run"):
                out.print(".")
                if (isIdentifier(verb)):
                    out.print(verb)
                else:
                    out.quote(verb)
            printListOn("(", arglist, ", ", ")", out, priorities["braceExpr"])
            if (priorities["call"] < priority):
                out.print(")")
    return astWrapper(methodCallExpr, makeMethodCallExpr,
        [rcvr, verb, arglist], span, scope, term`MethodCallExpr`,
        fn f {[rcvr.transform(f), verb, [a.transform(f) for a in arglist]]})


def makeFinalPattern(noun, guard, span):
    def scope := makeStaticScope([], [], [noun.getName()], [], false)
    object finalPattern:
        to getNoun():
            return noun
        to getGuard():
            return guard
        to subPrintOn(out, priority):
            noun.subPrintOn(out, priority)
            if (guard != null):
                out.print(" :")
                guard.subPrintOn(out, priorities["order"])
    return astWrapper(finalPattern, makeFinalPattern, [noun, guard], span,
        scope, term`FinalPattern`,
        fn f {[noun.transform(f), guard.transform(f)]})

def makeIgnorePattern(guard, span):
    def scope := if (guard != null) {guard.getStaticScope()} else {emptyScope}
    object ignorePattern:
        to getGuard():
            return guard
        to subPrintOn(out, priority):
            out.print("_")
            if (guard != null):
                out.print(" :")
                guard.subPrintOn(out, priorities["order"])
    return astWrapper(ignorePattern, makeIgnorePattern, [guard], span,
        scope, term`IgnorePattern`, fn f {[guard.transform(f)]})

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

def test_slotExpr(assert):
    def expr := makeSlotExpr("foo", null)
    assert.equal(expr._uncall(), [makeSlotExpr, "run", ["foo", null]])
    assert.equal(M.toString(expr), "&foo")
    assert.equal(expr.asTerm(), term`SlotExpr("foo")`)
    assert.equal(M.toString(makeSlotExpr("unwind-protect", null)),
                 "&::\"unwind-protect\"")

def test_bindingExpr(assert):
    def expr := makeBindingExpr("foo", null)
    assert.equal(expr._uncall(), [makeBindingExpr, "run", ["foo", null]])
    assert.equal(M.toString(expr), "&&foo")
    assert.equal(expr.asTerm(), term`BindingExpr("foo")`)
    assert.equal(M.toString(makeBindingExpr("unwind-protect", null)),
                 "&&::\"unwind-protect\"")

def test_metaContextExpr(assert):
    def expr := makeMetaContextExpr(null)
    assert.equal(expr._uncall(), [makeMetaContextExpr, "run", [null]])
    assert.equal(M.toString(expr), "meta.getContext()")
    assert.equal(expr.asTerm(), term`MetaContextExpr()`)

def test_metaStateExpr(assert):
    def expr := makeMetaStateExpr(null)
    assert.equal(expr._uncall(), [makeMetaStateExpr, "run", [null]])
    assert.equal(M.toString(expr), "meta.getState()")
    assert.equal(expr.asTerm(), term`MetaStateExpr()`)

def test_seqExpr(assert):
    def exprs := [makeLiteralExpr(3, null), makeLiteralExpr("four", null)]
    def expr := makeSeqExpr(exprs, null)
    assert.equal(expr._uncall(), [makeSeqExpr, "run", [exprs, null]])
    assert.equal(M.toString(expr), "3\n\"four\"")
    assert.equal(expr.asTerm(), term`SeqExpr([LiteralExpr(3), LiteralExpr("four")])`)

def test_module(assert):
    def body := makeLiteralExpr(3, null)
    def imports := [makeFinalPattern(makeNounExpr("a", null), null, null), makeFinalPattern(makeNounExpr("b", null), null, null)]
    def exports := [makeNounExpr("c", null)]
    def expr := makeModule(imports, exports, body)
    assert.equal(expr._uncall(), [makeFinalPattern, "run", [imports, exports, body, null]])
    assert.equal(M.toString(expr), "module a, b\nexport (c)\n3")
    assert.equal(expr.asTerm(), term`Module([FinalPattern(NounExpr("a"), null), FinalPattern(NounExpr("b"), null)], [NounExpr("c")], LiteralExpr(3)`)

def test_methodCallExpr(assert):
    def args := [makeLiteralExpr(1, null), makeLiteralExpr("two", null)]
    def receiver := makeNounExpr("foo", null)
    def expr := makeMethodCallExpr(receiver, "doStuff",
         args, null)
    assert.equal(expr._uncall(), [makeMethodCallExpr, "run", [receiver, "doStuff", args, null]])
    assert.equal(M.toString(expr), "foo.doStuff(1, \"two\")")
    assert.equal(expr.asTerm(), term`MethodCallExpr(NounExpr("foo"), "doStuff", [LiteralExpr(1), LiteralExpr("two")])`)
    def fcall := makeMethodCallExpr(makeNounExpr("foo", null), "run",
         [makeNounExpr("a", null)], null)
    assert.equal(M.toString(fcall), "foo(a)")
    assert.equal(M.toString(makeMethodCallExpr(makeNounExpr("a", null), "+",
         [makeNounExpr("b", null)], null)),
             "a.\"+\"(b)")

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

unittest([test_literalExpr, test_nounExpr, test_bindingExpr, test_slotExpr, test_metaContextExpr, test_metaStateExpr, test_seqExpr, test_methodCallExpr, test_finalPattern, test_ignorePattern])
