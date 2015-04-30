module parseModule, astBuilder, unittest
export (expand)

/** Maybe Python isn't so bad after all. */
object zip:
    match [=="run", iterables]:
        def its := [it._makeIterator() for it in iterables]
        return object ziperator:
            to _makeIterator():
                return ziperator
            to next(ej):
                return [it.next(ej) for it in its]

def reversed(it):
    def items := __makeList.fromIterable(it)
    return items.reversed()

def buildQuasi(name, inputs):
    def parts := ["text" => [].diverge(),
                  "expr" => [].diverge(),
                  "patt" => [].diverge()]
    for [typ, node] in inputs:
        parts[typ].push(node)
    return [p.snapshot() for p in parts]

def putVerb(verb, fail, span):
    switch (verb):
        match =="get":
            return "put"
        match =="run":
            return "setRun"
        match _:
            fail(["Unsupported verb for assignment", span])


def expand(node, builder, fail):
    def nouns := [].asMap().diverge()

    def emitList(items, span):
        return builder.MethodCallExpr(
            builder.NounExpr("__makeList", span),
            "run", items, span)

    def unaryOperator(verb, args, span):
        return builder.MethodCallExpr(args[0], verb, [], span)

    def binaryOperator(verb, args, span):
        return builder.MethodCallExpr(args[0], verb, [args[1]], span)

    def makeSlotPatt(n, span):
        return builder.ViaPattern(builder.NounExpr("__slotToBinding", span),
             builder.BindingPattern(n, span), span)

    def expandMatchBind(args, span, fail):
        def [spec, patt] := args
        def pattScope := patt.getStaticScope()
        def specScope := spec.getStaticScope()
        if ((pattScope.getOutNames() & specScope.getNamesUsed()).size() > 0):
            fail(["Use on left isn't really in scope of matchbind pattern: ${conflicts.getKeys()}", span])
        def [sp, ejector, result, problem, broken] := [builder.TempNounExpr(n, span)
            for n in ["sp", "fail", "result", "problem", "broken"]]
        def patternNouns := [builder.NounExpr(n, span) for n in pattScope.getOutNames()]
        return builder.SeqExpr([
            builder.DefExpr(builder.FinalPattern(sp, null, span), null, spec, span),
            builder.DefExpr(builder.ListPattern([builder.FinalPattern(result, null, span)] +
                                        [builder.BindingPattern(n, span) for n in patternNouns]),
                null,
                builder.EscapeExpr(
                    builder.FinalPattern(ejector, null, span),
                    builder.SeqExpr([
                        builder.DefExpr(patt, ejector, sp, span),
                        emitList([builder.NounExpr("true", span)] +
                            [builder.BindingExpr(n, span) for n in patternNouns],
                            span)], span),
                    builder.FinalPattern(problem, null, span),
                    builder.SeqExpr([
                        builder.DefExpr(builder.SlotPatt(broken, span),
                            builder.MethodCallExpr(builder.NounExpr("Ref", span),
                                "broken", [problem], span),
                            null,
                            emitList([builder.NounExpr("false", span)] +
                                [builder.BindingExpr(broken, span)] * patternNouns.size()),
                                    span)],
                                span),
                    span),
                span),
            result],
            span)

    def expandLogical(leftNames, rightNames, f, span):
        def both := [builder.NounExpr(n, span) for n in leftNames | rightNames]
        def result := builder.TempNounExpr("ok", span)
        def success := emitList([builder.NounExpr("true", span)] +
            [builder.BindingExpr(n, span) for n in both], span)
        def failure := builder.MethodCallExpr(builder.NounExpr("__booleanFlow", span),
            "failureList", [builder.LiteralExpr(both.size())], span)
        return builder.SeqExpr([
            builder.DefExpr(
                builder.ListPattern([builder.FinalPattern(result, null, span)] +
                    [builder.BindingPattern(n, span) for n in both], null, span),
                null,
                f(success, failure), span),
                result], span)

    def expandCallAssign([rcvr, verb, margs], right, fail, span):
        def ares := builder.TempNounExpr("ares", span)
        return builder.SeqExpr([
            builder.MethodCallExpr(rcvr, putVerb(verb, fail, span),
                margs + [builder.DefExpr(builder.FinalPattern(ares,
                        null, span),
                null, right, span)], span),
            ares], span)

    def expandVerbAssign(verb, target, vargs, fail, span):
        def [leftbuilder.r, _, leftargs] := target._uncall()
        switch (leftmaker.getNodeName()):
            match =="NounExpr":
                return builder.AssignExpr(target, builder.MethodCallExpr(target, verb, vargs))
            match =="MethodCallExpr":
                def [rcvr, methverb, margs] := subargs
                def recip := builder.TempNounExpr("recip", span)
                def seq := [builder.DefExpr(builder.FinalPattern(recip,
                                null, span),
                            null, rcvr, span)].diverge()
                def setArgs := [].diverge()
                for arg in margs:
                    def a := builder.TempNounExpr("arg")
                    seq.push(builder.DefExpr(builder.FinalPattern(a, null, span),
                         null, arg, span))
                    setArgs.push(a)
                seq.extend(expandCallAssign([recip, methverb, setArgs], builder.MethodCallExpr(builder.MethodCallExpr(recip, methverb, setArgs, span), verb, vargs, span), fail, span))
                return builder.SeqExpr(seq, span)
            match =="QuasiLiteralExpr":
                fail(["Can't use update-assign syntax on a \"$\"-hole. Use explicit \":=\" syntax instead.", span])
            match =="QuasiPatternExpr":
                fail(["Can't use update-assign syntax on a \"@\"-hole. Use explicit \":=\" syntax instead.", span])
            match _:
                fail(["Can only update-assign nouns and calls", span])

    def expandMessageDesc(doco, type, verb, paramDescs, resultGuard, span):
        def docExpr := if (doco == null) {null} else {builder.LiteralExpr(doco, span)}
        def guardExpr := if (guard == null) {null} else {builder.NounExpr("void", span)}
        return builder.HideExpr(builder.MethodCallExpr(builder.NounExpr("__makeMessageDesc", span),
            "run", [docExpr, builder.LiteralExpr(verb, span),
                 emitList(paramDescs, span), guardExpr],
             span), span)

    def expandObject(doco, name, auditors, [xtends, methods, matchers], span):
        if (xtends == null):
            return builder.ObjectExpr(doco, name, auditors, builder.Script(null, methods, matchers, span),
                 span)
        def p := builder.TempNounExpr("pair")
        def superExpr := if (xtends.getNodeName() == "NounExpr") {
            builder.DefExpr(builder.BindingPattern(builder.NounExpr("super", span), span), null,
                builder.BindingExpr(xtends, span))
            } else {
                builder.DefExpr(builder.FinalPattern(builder.NounExpr("super", span), span), null, xtends)
            }
        return builder.DefExpr(name, null, builder.HideExpr(builder.SeqExpr([superExpr,
            builder.ObjectExpr(doco, name, auditors, builder.Script(null, methods,
                matchers + [builder.Matcher(builder.FinalPattern(p, null, span),
                     builder.MethodCallExpr(builder.NounExpr("M", span), "callWithPair",
                          [builder.NounExpr("super", span), p], span), span)]), span)], span),
            span), span)

    def validateFor(left, right, fail, span):
        if ((left.getOutNames() & right.getNamesUsed()).size() > 0):
            fail(["Use on right isn't really in scope of definition", span])
        if ((right.getOutNames() & left.getNamesUsed()).size() > 0):
            fail(["Use on left would get captured by definition on right", span])

    def expandFor(optKey, value, coll, block, catchPatt, catchBlock, span):
        def key := if (optKey == null) {builder.IgnorePattern(null, span)} else {optKey}
        validateFor(key.getScope() + value.getScope(), coll.getScope(), fail, span)}
        def fTemp := builder.TempNounExpr("validFlag", span)
        def kTemp := builder.TempNounExpr("key", span)
        def vTemp := builder.TempNounExpr("value", span)
        def obj := builder.ObjectExpr("For-loop body",
            builder.IgnorePattern(null, span), [], builder.Script(
                null,
                [builder.Method(null, "run",
                    [builder.FinalPattern(kTemp, null, span),
                     builder.FinalPattern(kTemp, null, span)],
                null,
                builder.SeqExpr([
                    builder.MethodCallExpr(
                        builder.NounExpr("__validateFor", span),
                        "run", [fTemp], span),
                    builder.EscapeExpr(
                        builder.FinalPattern(builder.NounExpr("__continue", span), null, span),
                        builder.SeqExpr([
                            builder.DefExpr(key, null, kTemp, span),
                            builder.DefExpr(value, null, vTemp, span),
                            block,
                            builder.NounExpr("null", span)
                        ], span),
                    null, null)
                ], span))],
            []))
        return builder.EscapeExpr(
            builder.FinalPattern(builder.NounExpr("__break", span), null, span),
            builder.SeqExpr([
                builder.DefExpr(builder.VarPattern(fTemp, null, span), null,
                    builder.NounExpr("true", span), span),
                builder.FinallyExpr(
                    builder.MethodCallExpr(builder.NounExpr("__loop", span),
                        "run", [coll, obj], span),
                    builder.AssignExpr(fTemp, builder.NounExpr("false", span), span)),
                builder.NounExpr("null", span)
            ], span),
            catchPatt,
            catchBlock)

    def expandComprehension(optKey, value, coll, filter, exp, collector, span):
        def key := if (optKey == null) {builder.IgnorePattern(null, span)} else {optKey}
        validateFor(exp.getScope(), coll.getScope(), fail, span)
        validateFor(key.getScope() + value.getScope(), coll.getScope(), fail, span)
        def fTemp := builder.TempNounExpr("validFlag", span)
        def kTemp := builder.TempNounExpr("key", span)
        def vTemp := builder.TempNounExpr("value", span)
        def skip := builder.TempNounExpr("skip", span)
        def kv := []
        def maybeFilterExpr := if (filter != null) {
            builder.IfExpr(filter, exp, builder.MethodCallExpr(skip, "run", [], span), span)
        } else {exp}
        def obj := builder.ObjectExpr("For-loop body",
            builder.IgnorePattern(null, span), [], builder.Script(
                null,
                [builder.Method(null, "run",
                    [builder.FinalPattern(kTemp, null, span),
                     builder.FinalPattern(kTemp, null, span),
                     builder.FinalPattern(skip, null, span)],
                null,
                builder.SeqExpr([
                    builder.MethodCallExpr(
                        builder.NounExpr("__validateFor", span),
                        "run", [fTemp], span),
                    builder.DefExpr(key, null, kTemp, span),
                    builder.DefExpr(value, null, vTemp, span),
                    maybeFilterExpr
                ], span))],
            []))
        return builder.SeqExpr([
            builder.DefExpr(builder.VarPattern(fTemp, null, span), null,
                builder.NounExpr("true", span), span),
            builder.FinallyExpr(
                builder.MethodCallExpr(builder.NounExpr(collector, span),
                    "run", [coll, obj], span),
                builder.AssignExpr(fTemp, builder.NounExpr("false", span), span)),
            ], span)

    def expandTransformer(node, maker, args, span):
        switch (node.getNodeName()):
            match =="LiteralExpr":
                return maker(args[0], span)

            match =="NounExpr":
                def [name] := args
                nouns[name] := null
                return maker(name, span)
            match =="SlotExpr":
                def [noun] := args
                return builder.MethodCallExpr(builder.BindingExpr(noun, span), "get", [], span)
            mach =="BindingExpr":
                def [noun] := args
                return builder.BindingExpr(noun, span)
            match =="MethodCallExpr":
                def [rcvr, verb, arglist] := args
                return builder.MethodCallExpr(rcvr, verb, arglist, span)

            match =="ListExpr":
                def [items] := args
                return emitList(items, span)
            match =="MapExpr":
                def [assocs] := args
                return builder.MethodCallExpr(
                    builder.NounExpr("__makeMap", span), "fromPairs",
                    [emitList([emitList(a, span) for a in assocs], span)],
                    span)
            match =="MapExprAssoc":
                return args
            match =="MapExprExport":
                def [subnode] := args
                switch (subnode.getNodeName()):
                    match =="NounExpr":
                        return [builder.LiteralExpr(subargs[0]), subnode]
                    match =="SlotExpr":
                        return [builder.LiteralExpr("&" + subargs[0].getName()), subnode]
                    match =="BindingExpr":
                        return [builder.LiteralExpr("&&" + subargs[0].getName()), subnode]

            match =="QuasiText":
                def [text] := args
                return ["text", text]
            match =="QuasiExprHole":
                def [expr] := args
                return ["expr", expr]
            match =="QuasiPatternHole":
                def [patt] := args
                return ["patt", patt]
            match =="QuasiExpr":
                def [name, quasis] := args
                def qprefix := if (name == null) {"simple"} else {name}
                def qname := name + "__quasiParser"
                def [textParts, exprParts, _] := buildQuasi(qname, quasis)
                return builder.MethodCallExpr(
                    builder.MethodCallExpr(
                        builder.NounExpr(qname, span), "valueMaker",
                        [emitList(textParts, span)], span),
                    "substitute",
                    [emitList(exprParts, span)], span)
            match =="Module":
                def [imports, exports, expr] := args
                return builder.Module(imports, exports, expr, span)
            match =="SeqExpr":
                def [exprs] := args
                #XXX some parsers have emitted nested SeqExprs, should that
                #flattening be done here or in the parser?
                return builder.SeqExpr(exprs, span)
            match =="VerbCurryExpr":
                def [receiver, verb] := args
                return builder.MethodCallExpr(
                    builder.NounExpr("__makeVerbFacet", span),
                    "curryCall",
                    [receiver, builder.LiteralExpr(verb, span)],
                    span)
            match =="GetExpr":
                def [receiver, index] := args
                return builder.MethodCallExpr(receiver, "get", [index], span)
            match =="FunctionCallExpr":
                def [receiver, fargs] := args
                return builder.MethodCallExpr(receiver, "run", fargs, span)
            match =="FunctionSendExpr":
                def [receiver, fargs] := args
                return builder.MethodCallExpr(builder.NounExpr("M", span),
                    "send", [receiver, "run", fargs], span)
             match =="MethodSendExpr":
                 def [receiver, verb, margs] := args
                 return builder.MethodCallExpr(builder.NounExpr("M", span),
                     "send", [receiver, builder.LiteralExpr(verb, span),
                              emitList(margs, span)],
                      span)
            match =="SendCurryExpr":
                def [receiver, verb] := args
                return builder.MethodCallExpr(
                builder.NounExpr("__makeVerbFacet", span),
                    "currySend", [receiver, builder.LiteralExpr(verb, span)],
                    span)
            match =="MinusExpr":
                return unaryOperator("negate", args, span)
            match =="LogicalNotExpr":
                return unaryOperator("not", args, span)
            match =="BinaryNotExpr":
                return unaryOperator("complement", args, span)
            match =="PowExpr":
                return binaryOperator("pow", args, span)
            match =="MultiplyExpr":
                return binaryOperator("multiply", args, span)
            match =="DivideExpr":
                return binaryOperator("approxDivide", args, span)
            match =="FloorDivideExpr":
                return binaryOperator("floorDivide", args, span)
            match =="ModExpr":
                return binaryOperator("mod", args, span)
            # E's expander turns "x ** y % z" into x.modPow(y, z), but all the
            # things that's useful for should not be written in Monte, I
            # suspect.
            match =="AddExpr":
                return binaryOperator("add", args, span)
            match =="SubtractExpr":
                return binaryOperator("subtract", args, span)
            match =="ShiftRightExpr":
                return binaryOperator("shiftRight", args, span)
            match =="ShiftLeftExpr":
                return binaryOperator("shiftLeft", args, span)
            match =="TillExpr":
                return builder.MethodCallExpr(builder.NounExpr("__makeOrderedSpace", span),
                    "op__till", args, span)
            match =="ThruExpr":
                return builder.MethodCallExpr(builder.NounExpr("__makeOrderedSpace", span),
                    "op__thru", args, span)
            match =="GreaterThanExpr":
                return builder.MethodCallExpr(builder.NounExpr("__comparer", span),
                    "greaterThan", args, span)
            match =="LessThanExpr":
                return builder.MethodCallExpr(builder.NounExpr("__comparer", span),
                    "lessThan", args, span)
            match =="GreaterThanEqualExpr":
                return builder.MethodCallExpr(builder.NounExpr("__comparer", span),
                    "geq", args, span)
            match =="LessThanEqualExpr":
                return builder.MethodCallExpr(builder.NounExpr("__comparer", span),
                    "leq", args, span)
            match =="AsBigAsExpr":
                return builder.MethodCallExpr(builder.NounExpr("__comparer", span),
                    "asBigAs", args, span)
            match =="CoerceExpr":
                def [spec, guard] := args
                return builder.MethodCallExpr(
                    builder.MethodCallExpr(
                        builder.NounExpr("ValueGuard", span),
                            "coerce",
                            [guard, builder.NounExpr("throw", span)], span),
                         "coerce", [spec, builder.NounExpr("throw", span)], span)
            match =="MatchBindExpr":
                return expandMatchBind(args, span, fail)
            match =="MismatchExpr":
                return builder.MethodCallExpr(expandMatchBind(args, span, fail), "not", [], span)
            match =="SameExpr":
                return builder.MethodCallExpr(builder.NounExpr("__equalizer", span), "sameEver",
                    args, span)
            match =="NotSameExpr":
                return builder.MethodCallExpr(builder.MethodCallExpr(builder.NounExpr("__equalizer", span), "sameEver", args, span), "not", [], span)
            match =="ButNotExpr":
                return binaryOperator("butNot", args, span)
            match =="BinaryOrExpr":
                return binaryOperator("or", args, span)
            match =="BinaryAndExpr":
                return binaryOperator("and", args, span)
            match =="BinaryXorExpr":
                return binaryOperator("xor", args, span)
            match =="LogicalAndExpr":
                def [left, right] := args
                return expandLogical(
                    left.getStaticScope().getOutNames(),
                    right.getStaticScope().getOutNames(),
                    fn s, f {builder.IfExpr(left, builder.IfExpr(right, s, f, span), f, span)},
                    span)
            match =="LogicalOrExpr":
                def [left, right] := args
                def leftmap := left.getStaticScope().getOutNames()
                def rightmap := right.getStaticScope().getOutNames()
                def partialFail(failed):
                    return builder.SeqExpr([
                        builder.DefExpr(builder.BindingPattern(n, span), null, broken, span)
                        for n in failed] + [s])
                return expandLogical(
                    leftmap, rightmap,
                    fn s, f {
                        def broken := builder.MethodCallExpr(
                            builder.NounExpr("__booleanFlow", span),
                            "broken", [], span)
                        def rightOnly := [builder.NounExpr(n, span) for n in rightmap - leftmap]
                        def leftOnly := [builder.NounExpr(n, span) for n in leftmap - rightmap]
                        builder.IfExpr(left, partialFail(rightOnly),
                            builder.IfExpr(right, partialFail(leftOnly), f, span), span)},
                    span)
            match =="DefExpr":
                def [patt, ej, rval] := args
                def pattScope := patt.getStaticScope()
                def defPatts := pattScope.getDefNames()
                def varPatts := pattScope.getVarNames()
                def rvalScope := if (ej != null) {
                    rval.getStaticScope()
                } else {
                    ej.getStaticScope() + rval.getStaticScope()
                }
                def rvalUsed := rvalScope.namesUsed()
                if ((varPatts & rvalUsed).size() != 0):
                    fail(["Circular 'var' definition not allowed", span])
                if ((pattScope.namesUsed() & rvalScope.getOutNames()).size() != 0):
                    fail(["Pattern may not used var defined on the right", span])
                def conflicts := defPatts & rvalUsed
                if (size(conflicts) == 0):
                    return builder.DefExpr(patt, ej, rval)
                else:
                    def promises := [].diverge()
                    def resolvers := [].diverge()
                    def renamings := [].asMap().diverge()
                    for oldname in conflicts:
                        def newname := builder.TempNounExpr(oldname, span)
                        def newnameR := builder.TempNounExpr(oldname + "R", span)
                        renamings[oldname] := newname
                        def pair := [builder.FinalPattern(newname, null, span),
                                     builder.FinalPattern(newnameR, null, span)]
                        promises.push(builder.DefExpr(builder.ListPattern(pair, null, span),
                            null, builder.MethodCallExpr(builder.NounExpr("Ref", span), "promise",
                                [], span), span))
                        resolvers.push(builder.MethodCallExpr(newnamer, "resolve",
                             [builder.NounExpr(oldname, span)], span))
                    def resName := builder.TempNounExpr("value")
                    resolvers.push(resName)
                    def renamedRval := renameCycles(rval, renamings)
                    def resPatt := builder.FinalPattern(resName, null, span)
                    def resDef := builder.DefExpr(resPatt, null,
                         builder.DefExpr(patt, ej, renamedRval, span), span)
                    return builder.SeqExpr(promises.snapshot() + [resDef] + resolvers, span)
            match =="ForwardExpr":
                def [noun] := args
                def rname := builder.NounExpr(noun.getName() + "__Resolver", span)
                return builder.SeqExpr([
                    builder.DefExpr(builder.ListPattern([
                            builder.FinalPattern(name, null, span),
                            builder.FinalPattern(rname, null, span)],
                        null, span),
                        null,
                        builder.MethodCallExpr(builder.NounExpr("Ref", span), "promise", [], span)),
                        rname], span)
            match =="AssignExpr":
                def [left, right] := args
                def [leftmaker, _, leftargs] := left._uncall()
                switch (leftmaker):
                    match =="NounExpr":
                        return builder.AssignExpr(left, right, span)
                    match =="MethodCallExpr":
                        return expandCallAssign(leftargs, right, fail, span)
                    match _:
                        fail(["Assignment can only be done to nouns and collection elements",
                             span])
            match =="VerbAssignExpr":
                def [verb, target, vargs] := args
                return expandVerbAssign(verb, target, vargs, fail, span)
            match =="AugAssignExpr":
                def [verb, left, right] := args
                return expandVerbAssign(verb, left, [right], fail, span)
            match =="BreakExpr":
                if (args[0] == null):
                    return builder.MethodCallExpr(builder.NounExpr("__break", span), "run", [], span)
                else:
                    return builder.MethodCallExpr(builder.NounExpr("__break", span), "run", [expr], span)
            match =="ContinueExpr":
                if (args[0] == null):
                    return builder.MethodCallExpr(builder.NounExpr("__continue", span), "run", [], span)
                else:
                    return builder.MethodCallExpr(builder.NounExpr("__continue", span), "run", [expr], span)
            match =="ReturnExpr":
                if (args[0] == null):
                    return builder.MethodCallExpr(builder.NounExpr("__return", span), "run", [], span)
                else:
                    return builder.MethodCallExpr(builder.NounExpr("__return", span), "run", [expr], span)
            match =="GuardExpr":
                def [expr, subscripts] := args
                var e := expr
                for s in subscripts:
                    e := builder.MethodCallExpr(e, "get", [s], span)
                return e

            match =="IgnorePattern":
                return builder.IgnorePattern(args[0], span)
            match =="FinalPattern":
                def [noun, guard] := args
                return builder.FinalPattern(noun, guard, span)
            match =="SamePattern":
                def [value] := args
                return builder.ViaPattern(
                    builder.MethodCallExpr(builder.NounExpr("__matchSame", span),
                        "run", [value], span),
                    builder.IgnorePattern(null, span))
            match =="NotSamePattern":
                def [value] := args
                return builder.ViaPattern(
                    builder.MethodCallExpr(builder.NounExpr("__matchSame", span),
                        "different", [value], span),
                    builder.IgnorePattern(null, span))
            match =="VarPattern":
                return builder.VarPattern(args[0], args[1], span)
            match =="BindPattern":
                def [noun, guard] := args
                return builder.ViaPattern(
                    builder.MethodCallExpr(builder.NounExpr("__bind", span),
                        "run", [builder.NounExpr(noun.getName() + "__Resolver", span), guard],
                        span),
                    builder.BindingPattern(noun, span), span)
            match =="SlotPattern":
                def [noun, guard] := args
                if (guard == null):
                    return builder.ViaPattern(builder.NounExpr("__slotToBinding", span),
                        builder.BindingPattern(noun, span), span)
                else:
                    return builder.ViaPattern(
                        builder.MethodCallExpr(builder.NounExpr("__slotToBinding", span),
                            "run", [guard],
                            span),
                        builder.BindingPattern(noun, span), span)
            match =="MapPattern":
                def [assocs, tail] := args
                var nub := if (tail == null) {
                      builder.IgnorePattern(builder.NounExpr("__mapEmpty", span), span)
                      } else {tail}
                for [left, right, aspan] in assocs.reversed():
                    nub := builder.ViaPattern(
                        left,
                        builder.ListPattern([right, nub], null, aspan), aspan)
                return nub
            match =="MapPatternAssoc":
                return args
            match =="MapPatternImport":
                def [subbuilder.r, subargs, subspan] := subnode._uncall()
                switch (subbuilder.r):
                    match =="FinalPattern":
                        return [builder.LiteralExpr(subargs[0].getName(), span), subnode]
                    match =="SlotExpr":
                        return [builder.LiteralExpr("&" + subargs[0].getName(), span), subnode]
                    match =="BindingExpr":
                        return [builder.LiteralExpr("&&" + subargs[0].getName(), span), subnode]
            match =="MapPatternOptional":
                def [[k, v], default] := args
                return [builder.MethodCallExpr(builder.NounExpr("__mapExtract", span),
                        "depr", [k, default], span), v]
            match =="MapPatternRequired":
                def [[k, v]] := args
                return [builder.MethodCallExpr(builder.NounExpr("__mapExtract", span),
                        "run", [k], span), v]
            match =="ListPattern":
                def [patterns, tail] := args
                if (tail == null):
                    return builder.ListPattern(patterns, null, span)
                else:
                    return builder.ViaPattern(
                        builder.MethodCallExpr(builder.NounExpr("__splitList", span), "run",
                            [builder.LiteralExpr(patterns.size())], span),
                        builder.ListPattern(patterns + [tail], null, span), span)
            match =="SuchThatPattern":
                def [pattern, expr] := args
                return builder.ViaPattern(builder.NounExpr("__suchThat", span),
                    builder.ListPattern([pattern, builder.ViaPattern(
                        builder.MethodCallExpr(builder.NounExpr("_suchThat", span), "run",
                             [expr], span),
                        builder.IgnorePattern(null, span))], null, span), span)
            match =="QuasiPattern":
                def [name, quasis] := args
                def qprefix := if (name == null) {"simple"} else {name}
                def qname := name + "__quasiParser"
                def [textParts, exprParts, patternParts] := buildQuasi(qname, quasis)
                return builder.ViaPattern(
                    builder.MethodCallExpr(
                        builder.NounExpr("__quasiMatcher", span), "run",
                        [builder.MethodCallExpr(builder.NounExpr(qname, span), "matchMaker",
                            [emitList(textParts, span), emitList(exprParts, span)], span)]),
                    builder.ListPattern(patternParts, null, span), span)
            match =="InterfaceFunction":
                def [params, resultGuard] := args
                return [expandMessageDesc(null, "to", "run", params, resultGuard, span)]
            match =="InterfaceExpr":
                def [doco, name, guard, xtends, mplements, script] := args
                def verb := if (guard == null) {"run"} else {"makePair"}
                def docExpr := if (doco == null) { null } else {builder.LiteralExpr(doco, span)}
                def ifaceExpr := builder.HideExpr(builder.MethodCallExpr(
                    builder.NounExpr("__builder.ProtocolDesc", span), verb,
                        [docExpr, builder.MethodCallExpr(
                            builder.MethodCallExpr(
                                builder.MetaContextExpr(span),
                                "getFQNPrefix", [], span),
                            "add", [builder.LiteralExpr(name.getName() + "__T", span)], span),
                        emitList(xtends, span),
                        emitList(mplements, span),
                        emitList(script, span)], span), span)
                if (guard == null):
                    return builder.DefExpr(name, null, ifaceExpr, span)
                else:
                    return builder.MethodCallExpr(
                        builder.DefExpr(builder.ListPattern([builder.FinalPattern(name, null, span), guard],
                                     null, span),
                                 null, ifaceExpr, span),
                        "get", [builder.LiteralExpr(0)], span)
            match =="MessageDesc":
                def [doco, type, verb, params, resultGuard] := args
                return expandMessageDesc(doco, type, verb, params, resultGuard, span)
            match =="ParamDesc":
                def [name, guard] := args
                return builder.MethodCallExpr(builder.NounExpr("__makeParamDesc", span),
                    "run", [builder.LiteralExpr(name, span),
                        if (guard == null) {builder.NounExpr("any", span)} else {guard}], span)
            match =="LambdaExpr":
                def [doco, patterns, block] := args
                return builder.ObjectExpr(doco, builder.IgnorePattern(null, span), [],
                    builder.Script(null,
                         [builder.Method(null, "run", patterns, null, block, span)],
                         span), span)
            match =="ObjectExpr":
                def [doco, patt, auditors, script] := args
                def [pattMaker, pattArgs, pattSpan] := patt._uncall()
                def pattKind := node.getName()getNodeName()
                if (pattKind == "BindPattern"):
                    def name := builder.FinalPattern(node.getName().getName(), null, span)
                    def o := expandObject(doco, name, auditors, script, span)
                    return builder.DefExpr(patt, null, builder.HideExpr(o, span), span)
                if (pattKind == "FinalPattern" || pattKind == "IgnorePattern"):
                    return expandObject(doco, patt, auditors, script, span)
                fail(["Unknown pattern type in object expr", patt.getSpan()])
            match =="Script":
                #def [xtends, methods, matchers] := args
                return args
            match =="Function":
                def [params, guard, block] := args
                return [null, [builder.Method(null, "run", params, guard,
                    builder.EscapeExpr(builder.FinalPattern(builder.NounExpr("__return", span), null, span),
                        builder.SeqExpr([block, builder.NounExpr("null", span)], span), null, null, span),
                            span)], []]
            match =="To":
                def [doco, verb, params, guard, block] := args
                return builder.Method(doco, verb, params, guard,
                    builder.EscapeExpr(builder.FinalPattern(builder.NounExpr("__return", span), null, span),
                        builder.SeqExpr([block, builder.NounExpr("null", span)], span), null, null, span),
                            span)
            match =="Method":
                def [doco, verb, params, guard, block] := args
                return builder.Method(doco, verb, params, guard, block, span)
            match =="ForExpr":
                def [key, value, coll, block, [catchPatt, catchBlock]] := args
                return expandFor(key, value, coll, block, catchPatt, catchBlock, span)
            match =="ListCompExpr":
                def [key, value, coll, filter, exp] := args
                return expandComprehension(key, value, coll, filter, exp, "__accumulateList", span)
            match =="MapCompExpr":
                def [key, value, coll, filter, kExp, vExp] := args
                return expandComprehension(key, value, coll, filter,
                    emitList([kExp, vExp], span), "__accumulateMap", span)
            match =="SwitchExpr":
                def [expr, matchers] := args
                def sp := builder.TempNounExpr("specimen", span)
                def failures := [builder.TempNounExpr("failure", span) for _ in matchers]
                def ejs := [builder.TempNounExpr("ej") for _ in matchers]
                var block := builder.MethodCallExpr(builder.NounExpr("__switchFailed", span), "run",
                    [sp] + failures, span)
                for [m, fail, ej] in reversed(zip(matchers, falures, ejs)):
                    block := builder.EscapeExpr(
                        builder.FinalPattern(ej, null, span),
                        builder.SeqExpr([
                            builder.DefExpr(m.getPattern(), ej, sp, span),
                            m.getExpr()], span),
                        builder.FinalPattern(fail, null, span),
                        block, span)
                return builder.HideExpr(builder.SeqExpr([
                    builder.DefExpr(builder.FinalPattern(sp, null, span), null, expr, span),
                    block], span), span)
            match =="TryExpr":
                def [tryblock, catchers, finallyblock] := args
                var block := tryblock
                for [patt, catchblock] in catchers:
                    block := builder.KernelTryExpr(block, patt, catchblock, span)
                if (finallyblock != null):
                    block := builder.FinallyExpr(block, finallyblock, span)
                return block
            match =="Catch":
                return args
            match =="WhileExpr":
                def [test, block, [catchPatt, catchBlock]] := args
                return builder.EscapeExpr(
                    builder.FinallyExpr(builder.NounExpr("__break", span), null, span),
                        builder.MethodCallExpr(builder.NounExpr("__loop", span), "run",
                            [builder.MethodCallExpr(builder.NounExpr("__iterWhile", span), "run",
                                builder.ObjectExpr(null, builder.IgnorePattern(null, span), [],
                                    builder.Script(null,
                                        [builder.Method(null, "run", [], null, test, span)],
                                        [], span), span)),
                            builder.ObjectExpr(null, builder.IgnorePattern(null, span), [],
                                builder.Script(null,
                                    [builder.Method(null, "run",
                                         [builder.IgnorePattern(null, span),
                                         builder.IgnorePattern(null, span)],
                                         builder.NounExpr("boolean", span),
                                         builder.SeqExpr([
                                             builder.EscapeExpr(
                                                 builder.FinalPattern(
                                                     builder.NounExpr("__continue", span),
                                                     null, span),
                                                 block, null, null, span),
                                             builder.NounExpr("true", span)]))],
                                     [], span))], span),
                    catchPatt, catchBlock)
            match =="WhenExpr":
                def [var promiseExprs, var block, catchers, finallyblock] := args
                def expr := if (promiseExprs.size() > 1) {
                    builder.MethodCallExpr(builder.NounExpr("promiseAllFulfilled", span), "run",
                        [emitList(args, span)], span)
                } else {promiseExprs[0]}
                def resolution := builder.TempNounExpr("resolution", span)
                block := builder.IfExpr(
                    builder.MethodCallExpr(builder.NounExpr("Ref", span), "isBroken",
                         [resolution], span),
                    builder.MethodCallExpr(builder.NounExpr("Ref", span), "broken",
                        [builder.MethodCallExpr(builder.NounExpr("Ref", span), "optProblem",
                            [resolution], span)], span), block)
                for [patt, catchblock] in catchers:
                    block := builder.KernelTryExpr(block, patt, catchblock, span)
                if (finallyblock != null):
                    block := builder.FinallyExpr(block, finallyblock, span)
                return builder.HideExpr(builder.MethodCallExpr(builder.NounExpr("Ref", span),
                    "whenResolved", [expr,
                         builder.ObjectExpr("when-catch 'done' function",
                              builder.IgnorePattern(null, span), [],
                              builder.Script(null,
                                  [builder.Method(null, "run",
                                      [builder.FinalPattern(resolution, null, span)],
                                      null, block, span)], span),
                              span)], span), span)
            match _:
                return M.call(maker, args + [span])
    return node.transform(expandTransformer)


def tests := [].diverge()
def fixedPointSpecimens := [
    "x",
    "x := y",
    "x := y := z",
    "foo.bar(x, y)",
    "def [x, y] := z",
    "def x :y exit z := w",
    "def &&x := y",
    "def via (x) y := z",
    "if (x):
         y
     else:
         z",
    "
    if (x):
        y
    else if (z):
        w",
    "
    object x:
        method y:
            z
    ",
    "
    object x:
        match y:
            z
    ",
]
def specimens := [
    ["x[i] := y",
     "x.put(i, def ares__1 := y)
      ares__1"],

    ["x[i] := y; ares__1",
     "x.put(i, def ares__2 := y)
      ares__2
      ares__1"],

    ["x foo= (y, z)", "x := x.foo(y, z)"],

    ["x[i] foo= (y)",
     "def recip__1 := x
      def arg__2 := i
      recip__1.put(arg__2, def ares__3 := recip__1.get(arg__2).foo(y, z))
      ares__3"],

    ["x[i] += y",
     "def recip__1 := x
      def arg__2 := i
      recip__1.put(arg__2, def ares__3 := recip__1.get(arg__2).foo(y, z))
      ares__3"],

    ["x + y",
     "x.add(y)"],

    ["x - y",
     "x.subtract(y)"],

    ["x * y",
     "x.multiply(y)"],

    ["x / y",
     "x.approxDivide(y)"],

    ["x // y",
     "x.floorDivide(y)"],

    ["x % y",
     "x.mod(y)"],

    ["x ** y",
     "x.pow(y)"],

    ["x >> y",
     "x.shiftRight(y)"],

    ["x << y",
     "x.shiftLeft(y)"],

    ["x & y",
     "x.and(y)"],

    ["x | y",
     "x.or(y)"],

    ["x ^ y",
     "x.xor(y)"],

    ["x += y",
     "x := x.add(y)"],

    ["x -= y",
     "x := x.subtract(y)"],

    ["x *= y",
     "x := x.multiply(y)"],

    ["x /= y",
     "x := x.approxDivide(y)"],

    ["x //= y",
     "x := x.floorDivide(y)"],

    ["x %= y",
     "x := x.mod(y)"],

    ["x **= y",
     "x := x.pow(y)"],

    ["x >>= y",
     "x := x.shiftRight(y)"],

    ["x <<= y",
     "x := x.shiftLeft(y)"],

    ["x &= y",
     "x := x.and(y)"],

    ["x |= y",
     "x := x.or(y)"],

    ["x ^= y",
     "x := x.xor(y)"],

    ["!x", "x.not()"],
    ["-x", "x.negate()"],
    ["~x", "x.complement()"],

    ["x < y", "__comparer.lessThan(x, y)"]m
    ["x <= y", "__comparer.leq(x, y)"],
    ["x > y", "__comparer.greaterThan(x, y)"],
    ["x >= y", "__comparer.geq(x, y)"],
    ["x <=> y", "__comparer.asBigAs(x, y)"],

    ["x == y", "__equalizer.sameEver(x, y)"],
    ["x != y", "__equalizer.sameEver(x, y).not()"],

    ["x..y", "__makeOrderedSpace.op__thru(x, y)"],
    ["x..!y", "__makeOrderedSpace.op__till(x, y)"],

    ["foo <- bar(x, y)",
     "M.send(foo, \"bar\", __makeList.run(x, y))"],

    ["def [x, y] := [1, x]",
     "def [x__1, xR__2] := Ref.promise()
      def value__3 := def [x, y] := __makeList.run(1, x__1)
      xR__2.resolve(x, value__3)"],

    ["def x",
     "def [x, x__Resolver] := Ref.promise()
      x__Resolver"],

    ["x :y",
     "ValueGuard.coerce(y, throw).coerce(x, throw)"],

    ["def &x := y",
     "def via (__slotToBinding) &&x := y"],

    ["return",
     "__return.run()"],

    ["return 1",
     "__return.run(1)"],

    ["break",
     "__break.run()"],

    ["break 1",
     "__break.run(1)"],

    ["continue",
     "__continue.run()"],

    ["continue 1",
     "__continue.run(1)"],

    ["x && y",
     "
     def [ok__1] := if (x) {
         if (y) {
             __makeList.run(true)
         } else {
             __booleanFlow.failureList(0)
         }
     } else {
         __booleanFlow.failureList(0)
     }
     ok__1"],

    ["(def x := 1) && (def y := 2)",
     "
     def [ok__1, &&y, &&x] := if (def x := 1) {
         if (def y := 2) {
             __makeList.run(true, &&y, &&x)
         } else {
             __booleanFlow.failureList(2)
         }
     } else {
         __booleanFlow.failureList(2)
     }
     ok__1"],

    ["x || y",
     "
     def [ok__1] := if (x) {
         __makeList.run(true)
     } else if (y) {
         __makeList.run(true)
     } else {
         __booleanFlow.failureList(0)
     }
     ok__1"],

    ["(def x := 1) || (def y := 2)",
     "
     def [ok__1, &&y, &&x] := if (def x := 1) {
         def &&y := __booleanFlow.broken()
          __makeList.run(true, &&y, &&x)
     } else if (def y := 2) {
         def &&x := __booleanFlow.broken()
         __makeList.run(true, &&y, &&x)
     } else {
         __booleanFlow.failureList(2)
     }
     ok__1"],

    ["x =~ y",
     "
     def sp__1 := x
     def [ok__2, &&y] := escape fail__3 {
         def y exit fail__3 := sp__1
         __makeList.run(true, &&y)
     } catch problem__4 {
         def via (__slotToBinding) &&b__5 := Ref.broken(problem__4)
         __makeList.run(false, &&b__5)
     }
     ok__2"],

    ["def x ? (e) := z",
     "def via (__suchThat) [x, via (__suchThat.run(e)) _] := z"],

    ["def x ? (f(x) =~ y) := z",
     "
     def via (__suchThat) [x, via (__suchThat.run({def sp__1 := f.run(x)
     def [ok__2, &&y] := escape fail__3 {
         def fail__3 exit fail__3 := sp__1
         __makeList.run(true, &&y)
     } catch problem__4 {
         def via (__slotToBinding) &&b__5 := Ref.broken(problem__4)
         __makeList.run(false, &&b__5)
     }
     ok__2
     })) _] := z"],

    [`def ["a" => b, "c" => d] := x`,
     `def via (__mapExtract.run("a")) [b, via (__mapExtract.run("c")) [d, _ :__mapEmpty]] := x`],

    ["def [(a) => b] | c := x",
     "def via (__mapExtract.run(a)) [b, c] := x"],

    ["def [=> b] := x",
     "def via (__mapExtract.run(\"b\")) [b, _: __mapEmpty] := x"],

    ["def [=> &b] := x",
     "def via (__mapExtract.run(\"&b\")) [__slotToBinding(&&b), _: __mapEmpty] := x"],

    [`["a" => b, "c" => d]`,
     `__makeMap.fromPairs(__makeList.run(__makeList.run("a", b), __makeList.run("c", d)))`],

    [`[=> a, => &b]`,
     `__makeMap.fromPairs(__makeList.run(__makeList.run("a", a), __makeList.run("&b", &&b.get())))`],

    ["for x in y:
          z",
     "
     escape __break:
         var validFlag__1 := true
         try:
             __loop.run(y, object _ {
                 \"For-loop body\"
                 method run (key__2, value__3) {
                     __validateFor.run(validFlag__1)
                     escape __continue {
                         def _ := key__2
                         def x := value__3
                         z
                         null
                     }
                 }
             })
         finally:
             validFlag__1 := false
         null"],
    ["[for x in (y) if (a) z]",
     "
     var validFlag__1 := true
     try:
         __accumulateList.run(y, object _ {
             \"For-loop body\"
             method run (key__2, value__3, skip__4) {
                 __validateFor.run(validFlag__1)
                 def _ := key__2
                 def x := value__3
                 if (a) {
                     z
                 } else {
                     skip__4.run()
                 }
             }
         })
     finally:
         validFlag__1 := false"],

    ["[for x in (y) if (a) k => v]",
     "
     var validFlag__1 := true
     try:
         __accumulateMap.run(y, object _ {
             \"For-loop body\"
             method run (key__2, value__3, skip__4) {
                 __validateFor.run(validFlag__1)
                 def _ := key__2
                 def x := value__3
                 if (a) {
                     __makeList.run(k, v)
                 } else {
                     skip__4.run()
                 }
             }
         })
     finally:
         validFlag__1 := false"],

    ["
     while (x):
         y",

     "
     escape __break:
         __loop.run(__iterWhile.run(object _ {
             method run() {
                 x
             }
         }),
         object _ {
             \"While loop body\"
             method run(_, _) :Bool {
                 escape __continue {
                     y
                 }
                 true
             }
         })"],
    ["
     object foo extends (baz.get()):
         pass",
     "
     def foo := {def super := baz.get()
     object foo {
         match pair__1 {
             M.callWithPair(super, pair__1)
         }
     }}
     "],
    ["
     object foo:
         to baz():
             x
     ",
     "
     object foo
         method baz():
             escape __return:
                 x
                 null
     "],
    ["
     def foo():
         x
     ",
     "
     object foo:
         method run():
             escape __return:
                 x
                 null
     "],
    ["
     switch (x):
         match [a, b]:
             c
         match x:
             y
     ",
     "
     {def specimen__1 := x
     escape ej__2:
         def [a, b] exit ej__2 := specimen__1
         c
     catch failure__3:
         escape ej__4:
             def ej__4 exit specimen__1 := y
         catch failure__5:
             __switchFailed.run(specimen__1, failure__3, failure__5)
     "],
    ["
     switch (x):
         match ==2:
             'a'
     ",
     "
     {def specimen__1 := x
     escape ej__2:
         def via (__matchSame.run(1)) exit ej__2 := specimen__1
         'a'
     catch failure__3:
         __switchFailed.run(specimen__1, failure__3)
     "],
     ["
      interface foo:
          pass
      ",
      "def foo := {__makeProtocolDesc.run(null, meta.context().getFQNPrefix().add(\"foo__T\"), __makeList.run(), __makeList.run(), __makeList.run())}"],
     [`
      interface foo extends x, y implements a, b:
          "yay"
          to baz(c :Int):
              "blee"
          to boz(d) :Double
      `,
      `def foo := {__makeProtocolDesc.run("yay", meta.context().getFQNPrefix().add("foo__T"), __makeList.run("x", "y"), __makeList.run("a", "b"), __makeList.run({__makeMessageDesc.run("blee", "baz", __makeList.run(__makeParamDesc.run("c", Int)), Void)}, {__makeMessageDesc.run(null, "boz", __makeList.run(__makeParamDesc.run("d", any)), Double)}))}`],
     ["
      try:
          x
      catch p:
          y
      catch q:
          z
      ",
      "
      try:
          try:
              x
          catch p:
              y
      catch q:
          z
      "],
     ["
      try:
          x
      catch p:
          y
      finally:
          z
      ",
      "
      try:
          try:
              x
          catch p:
              y
      finally:
          z
      "],
    ["
     when (x) ->
         y
     ",
     `
     {Ref.whenResolved(x, object _ {
         "when-catch 'done' function"
         method run(resolution__1) {
             if (Ref.isBroken(resolution__1)) {
                 Ref.broken(Ref.optProblem(resolution__1))
             } else {
                 y
             }
         }
      })}
      `],
    ["
     when (x) ->
         y
     catch p:
         z
     ",
     `
     {Ref.whenResolved(x, object _ {
         "when-catch 'done' function"
         method run(resolution__1) {
             try {
                 if (Ref.isBroken(resolution__1)) {
                     Ref.broken(Ref.optProblem(resolution__1))
                 } else {
                     y
                 }
             } catch p {
                 z
             }
         }
      })}
      `],
     ["`hello $x world`",
      `simple__quasiParser.valueMaker(__makeList.run("hello ", simple__quasiParser.valueHole(0), " world")).substitute(__makeList.run(x))`],
     ["def foo`(@x)` := 1",
      `def via (__quasiMatcher.run(foo__quasiParser.matchMaker(__makeList.run("(", foo__quasiParser.patternHole(0), ")")), __makeList.run())) [x] := 1`],
     ["def foo`(@x:$y)` := 1",
      `def via (__quasiMatcher.run(foo__quasiParser.matchMaker(__makeList.run("(", foo__quasiParser.patternHole(0), ":", foo__quasiParser.valueHole(0), ")")), __makeList.run(y))) [x] := 1`],
]

def trim(s):
    def lines := s.split("\n")
    var dent := 0
    for line in lines:
        if line == "":
            continue
        for i => c in line:
            if (c != ' '):
                dent := i
                break
        break
    def trimmedLines := [].diverge()
    for line in lines:
        if line != "":
            trimmedLines.push(line.slice(dent, line.size()))
    return "\n".join(trimmedLines)

for item in fixedPointSpecimens:
    tests.push(fn assert {
        })

for [specimen, result] in specimens:
    tests.push(fn assert {
        })
unittest(tests)
