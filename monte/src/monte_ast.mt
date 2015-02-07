module unittest
export (makeLiteralExpr, makeNounExpr, makeFinalPattern)

def idStart := 'a'..'z' | 'A'..'Z' | '_'..'_'
def idPart := idStart | '0'..'9'
def INDENT := "    "
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
     "prim" => 16,

     "pattern" => 0]

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
            return makeStaticScope(namesRead, namesSet, [], [],
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

def printSuiteOn(leaderFn, suite, cuddle, out, priority):
    def indentOut := out.indent(INDENT)
    if (priority >= priorities["braceExpr"]):
        if (cuddle):
            out.print(" ")
        leaderFn()
        indentOut.println(" {")
        suite.subPrintOn(indentOut, priorities["braceExpr"])
        out.println("")
        out.print("}")
    else:
        if (cuddle):
            out.println("")
        leaderFn()
        indentOut.println(":")
        suite.subPrintOn(indentOut, priorities["indentExpr"])


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

def makeTempNounExpr(namePrefix, span):
    object name extends namePrefix:
        to _printOn(out):
            out.print("$<temp ")
            out.print(namePrefix)
            out.print(">")
    def scope := makeStaticScope([name], [], [], [], false)
    object tempNounExpr:
        to getName():
            return name
        to subPrintOn(out, priority):
            out.print(name)
    return astWrapper(tempNounExpr, makeTempNounExpr, [name], span,
         scope, term`TempNounExpr`, fn f {[namePrefix]})

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
    def scope := union([e.getStaticScope() for e in imports], emptyScope) + union([x.getStaticScope() for x in exports], emptyScope)
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
            out.println("")
            if (exports.size() > 0):
                out.print("export ")
                printListOn("(", exports, ", ", ")", out, priorities["braceExpr"])
                out.println("")
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
            if (verb != "run" && verb != "get"):
                out.print(".")
                if (isIdentifier(verb)):
                    out.print(verb)
                else:
                    out.quote(verb)
            if (verb == "get"):
                printListOn("[", arglist, ", ", "]", out, priorities["braceExpr"])
            else:
                printListOn("(", arglist, ", ", ")", out, priorities["braceExpr"])
            if (priorities["call"] < priority):
                out.print(")")
    return astWrapper(methodCallExpr, makeMethodCallExpr,
        [rcvr, verb, arglist], span, scope, term`MethodCallExpr`,
        fn f {[rcvr.transform(f), verb, [a.transform(f) for a in arglist]]})

def makeVarPattern(noun, guard, span):
    def scope := makeStaticScope([], [], [], [noun.getName()], false)
    object varPattern:
        to getNoun():
            return noun
        to getGuard():
            return guard
        to subPrintOn(out, priority):
            out.print("var ")
            noun.subPrintOn(out, priority)
            if (guard != null):
                out.print(" :")
                guard.subPrintOn(out, priorities["order"])
    return astWrapper(varPattern, makeVarPattern, [noun, guard], span,
        scope, term`VarPattern`,
        fn f {[noun.transform(f), if (guard == null) {null} else {guard.transform(f)}]})

def makeDefExpr(pattern, exit_, expr, span):
    def scope := if (exit_ == null) {
        pattern.getStaticScope() + expr.getStaticScope()
    } else {
        pattern.getStaticScope() + exit_.getStaticScope() + expr.getStaticScope()
    }
    object defExpr:
        to getPattern():
            return pattern
        to getExit():
            return exit_
        to getExpr():
            return expr
        to subPrintOn(out, priority):
            if (priorities["assign"] < priority):
                out.print("(")
            if (pattern._uncall()[0] != makeVarPattern):
                out.print("def ")
            pattern.subPrintOn(out, priorities["pattern"])
            if (exit_ != null):
                out.print(" exit ")
                exit_.subPrintOn(out, priorities["call"])
            out.print(" := ")
            expr.subPrintOn(out, priorities["assign"])
            if (priorities["assign"] < priority):
                out.print(")")
    return astWrapper(defExpr, makeDefExpr, [pattern, exit_, expr], span,
        scope, term`DefExpr`, fn f {[pattern.transform(f), if (exit_ == null) {null} else {exit_.transform(f)}, expr.transform(f)]})

def makeAssignExpr(lvalue, rvalue, span):
    def [lmaker, _, largs] := lvalue._uncall()
    def lscope := if (lmaker == makeNounExpr || lmaker == makeTempNounExpr) {
        makeStaticScope([], [lvalue.getName()], [], [], false)
    } else {
        lvalue.getStaticScope()
    }
    def scope := lscope + rvalue.getStaticScope()
    object assignExpr:
        to getLvalue():
            return lvalue
        to getRvalue():
            return rvalue
        to subPrintOn(out, priority):
            if (priorities["assign"] < priority):
                out.print("(")
            lvalue.subPrintOn(out, priorities["call"])
            out.print(" := ")
            rvalue.subPrintOn(out, priorities["assign"])
            if (priorities["assign"] < priority):
                out.print(")")
    return astWrapper(assignExpr, makeAssignExpr, [lvalue, rvalue], span,
        scope, term`AssignExpr`, fn f {[lvalue.transform(f), rvalue.transform(f)]})

def makeVerbAssignExpr(verb, lvalue, rvalues, span):
    def [lmaker, _, largs] := lvalue._uncall()
    def lscope := if (lmaker == makeNounExpr || lmaker == makeTempNounExpr) {
        makeStaticScope([], [lvalue.getName()], [], [], false)
    } else {
        lvalue.getStaticScope()
    }
    def scope := lscope + union([r.getStaticScope() for r in rvalues], emptyScope)
    object verbAssignExpr:
        to getLvalue():
            return lvalue
        to getRvalues():
            return rvalues
        to subPrintOn(out, priority):
            if (priorities["assign"] < priority):
                out.print("(")
            lvalue.subPrintOn(out, priorities["call"])
            out.print(" ")
            if (isIdentifier(verb)):
                out.print(verb)
            else:
                out.quote(verb)
            out.print("= ")
            printListOn("(", rvalues, ", ", ")", out, priorities["assign"])
            if (priorities["assign"] < priority):
                out.print(")")
    return astWrapper(verbAssignExpr, makeVerbAssignExpr, [verb, lvalue, rvalues], span,
        scope, term`VerbAssignExpr`, fn f {[verb, lvalue.transform(f), [ar.transform(f) for ar in rvalues]]})

def operatorsByName := [
    "add" => "+",
    "subtract" => "-",
    "multiply" => "*",
    "floorDivide" => "//",
    "approxDivide" => "/",
    "mod" => "%",
    "pow" => "**",
    "and" => "&",
    "or" => "|",
    "xor" => "^",
    "butNot" => "&!",
    "shiftLeft" => "<<",
    "shiftRight" => ">>",
]

def makeAugAssignExpr(verb, lvalue, rvalue, span):
    def [lmaker, _, largs] := lvalue._uncall()
    def lscope := if (lmaker == makeNounExpr || lmaker == makeTempNounExpr) {
        makeStaticScope([], [lvalue.getName()], [], [], false)
    } else {
        lvalue.getStaticScope()
    }
    def scope := lscope + rvalue.getStaticScope()
    object augAssignExpr:
        to getLvalue():
            return lvalue
        to getRvalue():
            return rvalue
        to subPrintOn(out, priority):
            if (priorities["assign"] < priority):
                out.print("(")
            lvalue.subPrintOn(out, priorities["call"])
            out.print(" ")
            out.print(operatorsByName[verb])
            out.print("= ")
            rvalue.subPrintOn(out, priorities["assign"])
            if (priorities["assign"] < priority):
                out.print(")")
    return astWrapper(augAssignExpr, makeAugAssignExpr, [verb, lvalue, rvalue], span,
        scope, term`AugAssignExpr`, fn f {[verb, lvalue.transform(f), rvalue.transform(f)]})

def makeMatcher(pattern, body, span):
    def scope := pattern.getStaticScope() + body.getStaticScope().hide()
    object matcher:
        to getPattern():
            return pattern
        to getBody():
            return body
        to subPrintOn(out, priority):
            printSuiteOn(fn {
                out.print("match ");
                pattern.subPrintOn(out, priorities["pattern"]);
            }, body, false, out, priority)
    return astWrapper(matcher, makeMatcher, [pattern, body], span,
        scope, term`Matcher`, fn f {[pattern.transform(f), body.transform(f)]})

def makeCatchExpr(body, pattern, catcher, span):
    def scope := body.getStaticScope().hide() + (pattern.getStaticScope() + catcher.getStaticScope()).hide()
    object catchExpr:
        to getBody():
            return body
        to getPattern():
            return pattern
        to getCatcher():
            return catcher
        to subPrintOn(out, priority):
            printSuiteOn(fn {out.print("try")}, body, false, out, priority)
            printSuiteOn(fn {
                out.print("catch ")
                pattern.subPrintOn(out, priorities["pattern"])
            }, catcher, true, out, priority)
    return astWrapper(catchExpr, makeCatchExpr, [body, pattern, catcher], span,
        scope, term`CatchExpr`, fn f {[body.transform(f), pattern.transform(f),
                                       catcher.transform(f)]})

def makeFinallyExpr(body, unwinder, span):
    def scope := body.getStaticScope().hide() + unwinder.getStaticScope().hide()
    object finallyExpr:
        to getBody():
            return body
        to getUnwinder():
            return unwinder
        to subPrintOn(out, priority):
            printSuiteOn(fn {out.print("try")}, body, false, out, priority)
            printSuiteOn(fn {out.print("finally")}, unwinder, true, out,
                         priority)
    return astWrapper(finallyExpr, makeFinallyExpr, [body, unwinder], span,
        scope, term`FinallyExpr`, fn f {[body.transform(f), unwinder.transform(f)]})

def makeTryExpr(body, catchers, finallyBlock, span):
    def baseScope := union([
        (m.getPattern().getStaticScope() + m.getBody().getStaticScope()).hide()
             for m in catchers],
        body.getStaticScope().hide())
    def scope := if (finallyBlock == null) {
        baseScope
    } else {
        baseScope + finallyBlock.getStaticScope().hide()
    }
    object tryExpr:
        to getBody():
            return body
        to getCatchers():
            return catchers
        to getFinally():
            return finallyBlock
        to subPrintOn(out, priority):
            printSuiteOn(fn {out.print("try")}, body, false, out, priority)
            for m in catchers:
                printSuiteOn(fn {
                    out.print("catch ")
                    m.getPattern().subPrintOn(out, priorities["pattern"])
                }, m.getBody(), true, out, priority)
            if (finallyBlock != null):
                printSuiteOn(fn {out.print("finally")},
                    finallyBlock, true, out, priority)
    return astWrapper(tryExpr, makeTryExpr, [body, catchers, finallyBlock], span,
        scope, term`TryExpr`, fn f {[body.transform(f), [m.transform(f) for m in catchers],if (finallyBlock == null) {null} else {finallyBlock.transform(f)}]})

def makeEscapeExpr(ejectorPattern, body, catchPattern, catchBody, span):
    def baseScope := (ejectorPattern.getStaticScope() + body.getStaticScope()).hide()
    def scope := if (catchPattern == null) {
        baseScope
    } else {
        baseScope + (catchPattern.getStaticScope() + catchBody.getStaticScope()).hide()
    }
    object escapeExpr:
        to getEjectorPattern():
            return ejectorPattern
        to getBody():
            return body
        to getCatchPattern():
            return catchPattern
        to getCatchBody():
            return catchBody
        to subPrintOn(out, priority):
            printSuiteOn(fn {
                out.print("escape ")
                ejectorPattern.subPrintOn(out, priorities["pattern"])
            }, body, false, out, priority)
            if (catchPattern != null):
                printSuiteOn(fn {
                    out.print("catch ")
                    catchPattern.subPrintOn(out, priorities["pattern"])
                }, catchBody, true, out, priority)
    return astWrapper(escapeExpr, makeEscapeExpr,
         [ejectorPattern, body, catchPattern, catchBody], span,
        scope, term`EscapeExpr`,
         fn f {[ejectorPattern.transform(f), body.transform(f),
                catchPattern.transform(f), catchBody.transform(f)]})

def makeIfExpr(test, consq, alt, span):
    def baseScope := test.getStaticScope() + consq.getStaticScope().hide()
    def scope := if (alt == null) {
        baseScope
    } else {
        baseScope + alt.getStaticScope().hide()
    }
    object ifExpr:
        to getTest():
            return test
        to getThen():
            return consq
        to getElse():
            return alt
        to subPrintOn(out, priority):
            printSuiteOn(fn {
                out.print("if (")
                test.subPrintOn(out, priorities["braceExpr"])
                out.print(")")
                }, consq, false, out, priority)
            if (alt != null):
                printSuiteOn(fn {out.print("else")}, alt, true, out, priority)

    return astWrapper(ifExpr, makeIfExpr, [test, consq, alt], span,
        scope, term`IfExpr`, fn f {[test.transform(f), consq.transform(f), alt.transform(f)]})

def makeHideExpr(body, span):
    def scope := body.getStaticScope().hide()
    object hideExpr:
        to getBody():
            return body
        to subPrintOn(out, priority):
            def indentOut := out.indent(INDENT)
            indentOut.println("{")
            body.subPrintOn(indentOut, priorities["braceExpr"])
            out.println("")
            out.print("}")

    return astWrapper(hideExpr, makeHideExpr, [body], span,
        scope, term`HideExpr`, fn f {[body.transform(f)]})

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
        fn f {[noun.transform(f), if (guard == null) {null} else {guard.transform(f)}]})

def makeBindingPattern(noun, span):
    def scope := makeStaticScope([], [], [noun.getName()], [], false)
    object bindingPattern:
        to getNoun():
            return noun
        to subPrintOn(out, priority):
            out.print("&&")
            noun.subPrintOn(out, priority)
    return astWrapper(bindingPattern, makeBindingPattern, [noun], span,
        scope, term`BindingPattern`, fn f {[noun.transform(f)]})

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

def makeListPattern(patterns, tail, span):
    def scope := union([p.getStaticScope() for p in patterns] +
            if (tail == null) {[]} else {[tail.getStaticScope()]},
        emptyScope)
    object listPattern:
        to getPatterns():
            return patterns
        to getTail():
            return tail
        to subPrintOn(out, priority):
            printListOn("[", patterns, ", ", "]", out, priorities["pattern"])
            if (tail != null):
                out.print(" + ")
                tail.subPrintOn(out, priorities["pattern"])
    return astWrapper(listPattern, makeListPattern, [patterns, tail], span,
        scope, term`ListPattern`, fn f {[[p.transform(f) for p in patterns], if (tail == null) {null} else {tail.transform(f)}]})

def makeViaPattern(expr, subpattern, span):
    def scope := expr.getStaticScope() + subpattern.getStaticScope()
    object viaPattern:
        to getExpr():
            return expr
        to getPattern():
            return subpattern
        to subPrintOn(out, priority):
            out.print("via (")
            expr.subPrintOn(out, priorities["order"])
            out.print(") ")
            subpattern.subPrintOn(out, priority)
    return astWrapper(viaPattern, makeViaPattern, [expr, subpattern], span,
        scope, term`ViaPattern`, fn f {[expr.transform(f), subpattern.transform(f)]})

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

def test_tempNounExpr(assert):
    def expr := makeTempNounExpr("foo", null)
    assert.equal(M.toString(expr), "$<temp foo>")
    assert.equal(expr.asTerm(), term`TempNounExpr("foo")`)
    assert.notEqual(expr.getName(), makeTempNounExpr("foo", null).getName())

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
    def expr := makeModule(imports, exports, body, null)
    assert.equal(expr._uncall(), [makeModule, "run", [imports, exports, body, null]])
    assert.equal(M.toString(expr), "module a, b\nexport (c)\n3")
    assert.equal(expr.asTerm(), term`Module([FinalPattern(NounExpr("a"), null), FinalPattern(NounExpr("b"), null)], [NounExpr("c")], LiteralExpr(3))`)

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
    assert.equal(M.toString(makeMethodCallExpr(makeNounExpr("foo", null), "get",
         [makeNounExpr("a", null), makeNounExpr("b", null)], null)), "foo[a, b]")

def test_defExpr(assert):
    def patt := makeFinalPattern(makeNounExpr("a", null), null, null)
    def ej :=  makeNounExpr("ej", null)
    def body := makeLiteralExpr(1, null)
    def expr := makeDefExpr(patt, ej, body, null)
    assert.equal(expr._uncall(), [makeDefExpr, "run", [patt, ej, body, null]])
    assert.equal(M.toString(expr), "def a exit ej := 1")
    assert.equal(M.toString(makeDefExpr(patt, null, body, null)), "def a := 1")
    assert.equal(M.toString(makeDefExpr(makeVarPattern(makeNounExpr("a", null), null, null), null, body, null)), "var a := 1")
    assert.equal(expr.asTerm(), term`DefExpr(FinalPattern(NounExpr("a"), null), NounExpr("ej"), LiteralExpr(1))`)

def test_assignExpr(assert):
    def lval := makeNounExpr("a", null)
    def body := makeLiteralExpr(1, null)
    def expr := makeAssignExpr(lval, body, null)
    assert.equal(expr._uncall(), [makeAssignExpr, "run", [lval, body, null]])
    assert.equal(M.toString(expr), "a := 1")
    assert.equal(expr.asTerm(), term`AssignExpr(NounExpr("a"), LiteralExpr(1))`)
    assert.equal(M.toString(makeAssignExpr(makeMethodCallExpr(lval, "get", [makeLiteralExpr(0, null)], null), body, null)), "a[0] := 1")


def test_verbAssignExpr(assert):
    def lval := makeNounExpr("a", null)
    def body := makeLiteralExpr(1, null)
    def expr := makeVerbAssignExpr("blee", lval, [body], null)
    assert.equal(expr._uncall(), [makeVerbAssignExpr, "run", ["blee", lval, [body], null]])
    assert.equal(M.toString(expr), "a blee= (1)")
    assert.equal(expr.asTerm(), term`VerbAssignExpr("blee", NounExpr("a"), [LiteralExpr(1)])`)
    assert.equal(M.toString(makeVerbAssignExpr("blee", makeMethodCallExpr(lval, "get", [makeLiteralExpr(0, null)], null), [body], null)), "a[0] blee= (1)")

def test_augAssignExpr(assert):
    def lval := makeNounExpr("a", null)
    def body := makeLiteralExpr(1, null)
    def expr := makeAugAssignExpr("add", lval, body, null)
    assert.equal(expr._uncall(), [makeAugAssignExpr, "run", ["add", lval, body, null]])
    assert.equal(M.toString(expr), "a += 1")
    assert.equal(expr.asTerm(), term`AugAssignExpr("add", NounExpr("a"), LiteralExpr(1))`)
    assert.equal(M.toString(makeAugAssignExpr("shiftRight", makeMethodCallExpr(lval, "get", [makeLiteralExpr(0, null)], null), body, null)), "a[0] >>= 1")

def test_ifExpr(assert):
    def [test, consq, alt] := [makeNounExpr(n, null) for n in ["a", "b", "c"]]
    def expr := makeIfExpr(test, consq, alt, null)
    assert.equal(expr._uncall(), [makeIfExpr, "run", [test, consq, alt, null]])
    assert.equal(M.toString(expr), "if (a):\n    b\nelse:\n    c")
    assert.equal(M.toString(makeDefExpr(makeIgnorePattern(null, null), null, expr, null)),
         "def _ := if (a) {\n    b\n} else {\n    c\n}")
    assert.equal(expr.asTerm(), term`IfExpr(NounExpr("a"), NounExpr("b"), NounExpr("c"))`)

def test_catchExpr(assert):
    def [attempt, pattern, catcher] := [makeNounExpr("a", null), makeFinalPattern(makeNounExpr("b", null), null, null), makeNounExpr("c", null)]
    def expr := makeCatchExpr(attempt, pattern, catcher, null)
    assert.equal(expr._uncall(), [makeCatchExpr, "run", [attempt, pattern, catcher, null]])
    assert.equal(M.toString(expr), "try:\n    a\ncatch b:\n    c")
    assert.equal(M.toString(makeDefExpr(makeIgnorePattern(null, null), null, expr, null)),
        "def _ := try {\n    a\n} catch b {\n    c\n}")
    assert.equal(expr.asTerm(), term`CatchExpr(NounExpr("a"), FinalPattern(NounExpr("b"), null), NounExpr("c"))`)

def test_finallyExpr(assert):
    def [attempt, catcher] := [makeNounExpr("a", null), makeNounExpr("b", null)]
    def expr := makeFinallyExpr(attempt, catcher, null)
    assert.equal(expr._uncall(), [makeFinallyExpr, "run", [attempt, catcher, null]])
    assert.equal(M.toString(expr), "try:\n    a\nfinally:\n    b")
    assert.equal(M.toString(makeDefExpr(makeIgnorePattern(null, null), null, expr, null)),
        "def _ := try {\n    a\n} finally {\n    b\n}")
    assert.equal(expr.asTerm(), term`FinallyExpr(NounExpr("a"), NounExpr("b"))`)

def test_tryExpr(assert):
    def [body, catchers, fin] := [makeNounExpr("a", null),
        [makeMatcher(makeFinalPattern(makeNounExpr("b", null), null, null),
                     makeNounExpr("c", null), null),
         makeMatcher(makeFinalPattern(makeNounExpr("d", null), null, null),
                      makeNounExpr("e", null), null)],
        makeNounExpr("f", null)]
    def expr := makeTryExpr(body, catchers, fin, null)
    assert.equal(expr._uncall(), [makeTryExpr, "run", [body, catchers, fin, null]])
    assert.equal(M.toString(expr), "try:\n    a\ncatch b:\n    c\ncatch d:\n    e\nfinally:\n    f")
    assert.equal(M.toString(makeTryExpr(body, catchers, null, null)), "try:\n    a\ncatch b:\n    c\ncatch d:\n    e")
    assert.equal(M.toString(makeDefExpr(makeIgnorePattern(null, null), null, expr, null)),
        "def _ := try {\n    a\n} catch b {\n    c\n} catch d {\n    e\n} finally {\n    f\n}")
    assert.equal(expr.asTerm(), term`TryExpr(NounExpr("a"), [Matcher(FinalPattern(NounExpr("b"), null), NounExpr("c")), Matcher(FinalPattern(NounExpr("d"), null), NounExpr("e"))], NounExpr("f"))`)

def test_escapeExpr(assert):
    def [ejPatt, body, catchPattern, catchBlock] := [makeFinalPattern(makeNounExpr("a", null), null, null), makeNounExpr("b", null), makeFinalPattern(makeNounExpr("c", null), null, null), makeNounExpr("d", null)]
    def expr := makeEscapeExpr(ejPatt, body, catchPattern, catchBlock, null)
    assert.equal(expr._uncall(), [makeEscapeExpr, "run", [ejPatt, body, catchPattern, catchBlock, null]])
    assert.equal(M.toString(expr), "escape a:\n    b\ncatch c:\n    d")
    assert.equal(M.toString(makeDefExpr(makeIgnorePattern(null, null), null, expr, null)),
        "def _ := escape a {\n    b\n} catch c {\n    d\n}")
    assert.equal(M.toString(makeEscapeExpr(ejPatt, body, null, null, null)), "escape a:\n    b")
    assert.equal(expr.asTerm(), term`EscapeExpr(FinalPattern(NounExpr("a"), null), NounExpr("b"), FinalPattern(NounExpr("c"), null), NounExpr("d"))`)

def test_hideExpr(assert):
    def body := makeNounExpr("a", null)
    def expr := makeHideExpr(body, null)
    assert.equal(expr._uncall(), [makeHideExpr, "run", [body, null]])
    assert.equal(M.toString(expr), "{\n    a\n}")
    assert.equal(expr.asTerm(), term`HideExpr(NounExpr("a"))`)

def test_finalPattern(assert):
    def [name, guard] := [makeNounExpr("blee", null), makeNounExpr("Int", null)]
    def patt := makeFinalPattern(name, guard, null)
    assert.equal(patt._uncall(), [makeFinalPattern, "run", [name, guard, null]])
    assert.equal(M.toString(patt), "blee :Int")
    assert.equal(patt.asTerm(), term`FinalPattern(NounExpr("blee"), NounExpr("Int"))`)

def test_bindingPattern(assert):
    def name := makeNounExpr("blee", null)
    def patt := makeBindingPattern(name, null)
    assert.equal(patt._uncall(), [makeBindingPattern, "run", [name, null]])
    assert.equal(M.toString(patt), "&&blee")
    assert.equal(patt.asTerm(), term`BindingPattern(NounExpr("blee"))`)

def test_ignorePattern(assert):
    def guard := makeNounExpr("List", null)
    def patt := makeIgnorePattern(guard, null)
    assert.equal(patt._uncall(), [makeIgnorePattern, "run", [guard, null]])
    assert.equal(M.toString(patt), "_ :List")
    assert.equal(patt.asTerm(), term`IgnorePattern(NounExpr("List"))`)
    assert.equal(M.toString(makeIgnorePattern(null, null)), "_")

def test_varPattern(assert):
    def [name, guard] := [makeNounExpr("blee", null), makeNounExpr("Int", null)]
    def patt := makeVarPattern(name, guard, null)
    assert.equal(patt._uncall(), [makeVarPattern, "run", [name, guard, null]])
    assert.equal(M.toString(patt), "var blee :Int")
    assert.equal(patt.asTerm(), term`VarPattern(NounExpr("blee"), NounExpr("Int"))`)

def test_listPattern(assert):
    def patts := [makeFinalPattern(makeNounExpr("a", null), null, null), makeVarPattern(makeNounExpr("b", null), null, null)]
    def tail := makeFinalPattern(makeNounExpr("tail", null), null, null)
    def patt := makeListPattern(patts, tail, null)
    assert.equal(patt._uncall(), [makeListPattern, "run", [patts, tail, null]])
    assert.equal(M.toString(patt), "[a, var b] + tail")
    assert.equal(M.toString(makeListPattern(patts, null, null)), "[a, var b]")
    assert.equal(patt.asTerm(), term`ListPattern([FinalPattern(NounExpr("a"), null), VarPattern(NounExpr("b"), null)], FinalPattern(NounExpr("tail"), null))`)

def test_viaPattern(assert):
    def subpatt := makeFinalPattern(makeNounExpr("a", null), null, null)
    def expr := makeNounExpr("b", null)
    def patt := makeViaPattern(expr, subpatt, null)
    assert.equal(patt._uncall(), [makeViaPattern, "run", [expr, subpatt, null]])
    assert.equal(M.toString(patt), "via (b) a")
    assert.equal(patt.asTerm(), term`ViaPattern(NounExpr("b"), FinalPattern(NounExpr("a"), null))`)

unittest([test_literalExpr, test_nounExpr, test_tempNounExpr, test_bindingExpr, test_slotExpr,
          test_metaContextExpr, test_metaStateExpr, test_seqExpr, test_module,
          test_defExpr, test_methodCallExpr, test_assignExpr, test_verbAssignExpr,
          test_augAssignExpr, test_ifExpr, test_catchExpr, test_finallyExpr, test_tryExpr,
          test_escapeExpr, test_hideExpr,
          test_finalPattern, test_ignorePattern, test_varPattern,
          test_listPattern, test_bindingPattern, test_viaPattern])
