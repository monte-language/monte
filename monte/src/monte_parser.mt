module unittest, makeMonteLexer, astBuilder
export (parseModule, parseExpression, parsePattern)
def spanCover(left, right):
    if (left == null || right == null):
        return null
    return left.combine(right)

# # XXX dupe from term parser module
# def makeQuasiTokenChain(makeLexer, template):
#     var i := -1
#     var current := makeLexer("", qBuilder)
#     var lex := current
#     def [VALUE_HOLE, PATTERN_HOLE] := makeLexer.holes()
#     var j := 0
#     return object chainer:
#         to _makeIterator():
#             return chainer

#         to valueHole():
#            return VALUE_HOLE

#         to patternHole():
#            return PATTERN_HOLE

#         to next(ej):
#             if (i >= template.size()):
#                 throw.eject(ej, null)
#             j += 1
#             if (current == null):
#                 if (template[i] == VALUE_HOLE || template[i] == PATTERN_HOLE):
#                     def hol := template[i]
#                     i += 1
#                     return [j, hol]
#                 else:
#                     current := lex.lexerForNextChunk(template[i])._makeIterator()
#                     lex := current
#             escape e:
#                 def t := current.next(e)[1]
#                 return [j, t]
#             catch z:
#                 i += 1
#                 current := null
#                 return chainer.next(ej)

def parseMonte(lex, builder, mode, err):
    def [VALUE_HOLE, PATTERN_HOLE] := [lex.valueHole(), lex.patternHole()]
    def tokens := __makeList.fromIterable(lex)
    var dollarHoleValueIndex := -1
    var atHoleValueIndex := -1
    var position := -1

    def advance(ej):
        position += 1
        if (position >= tokens.size()):
            ej("hit EOF")
        return tokens[position]

    def advanceTag(ej):
        def t := advance(ej)
        def isHole := t == VALUE_HOLE || t == PATTERN_HOLE
        if (isHole):
            return t
        else:
            return t.getTag().getName()

    def accept(tagname, fail):
        def t := advance(fail)
        def specname := t.getTag().getName()
        if (specname != tagname):
            position -= 1
            fail(specname)
        return t

    def acceptEOLs():
        while (true):
            position += 1
            if (position >= tokens.size()):
                return
            def t := tokens[position]
            def isHole := t == VALUE_HOLE || t == PATTERN_HOLE
            if (isHole || t.getTag().getName() != "EOL"):
                return

    def peek():
        if (position + 1 >= tokens.size()):
            return null
        return tokens[position + 1]

    def acceptKw(tagname, fail):
        return accept(tagname, fn t {fail(`expected keyword ${M.toQuote(tagname)}, got ${M.toQuote(t)}`)})

    def acceptTag(tagname, fail):
        return accept(tagname, fn t {fail(`expected $tagname, got $t`)})

    def opt(rule, ej):
        escape e:
            return rule(e)
        catch _:
            return null

    def spanHere():
        if (position + 1 >= tokens.size()):
            return null
        return tokens[position.max(0)].getSpan()

    def spanFrom(start):
        return spanCover(start, spanHere())

    def peekTag():
        if (position + 1 >= tokens.size()):
            return null
        return tokens[position + 1].getTag().getName()

    def acceptList(rule):
        def items := [].diverge()
        escape e:
            items.push(rule(e))
            while (true):
                acceptTag(",", __break)
                items.push(rule(__break))
        return items.snapshot()

    def acceptListOrMap(ruleList, ruleMap):
        var isMap := false
        def items := [].diverge()
        def startpos := position
        escape em:
            items.push(ruleMap(em))
            isMap := true
        catch _:
            escape e:
                position := startpos
                items.push(ruleList(e))
                isMap := false
            catch _:
                return [[], false]
        while (true):
            acceptTag(",", __break)
            if (isMap):
                items.push(ruleMap(__break))
            else:
                items.push(ruleList(__break))
        return [items.snapshot(), isMap]

    def expr
    def order
    #def block
    def prim
    def pattern
    def quasiliteral(id, isPattern, ej):
        def spanStart := if (id == null) {spanHere()} else {id.getSpan()}
        def name := if (id == null) {null} else {id.getData()}
        def parts := [].diverge()
        while (true):
            def t := advance(ej)
            def tname := t.getTag().getName()
            if (tname == "QUASI_OPEN" && t.getData() != ""):
                parts.push(builder.QuasiText(t.getData(), t.getSpan()))
            else if (tname == "QUASI_CLOSE"):
                parts.push(builder.QuasiText(t.getData(), t.getSpan()))
                break
            else if (tname == "DOLLAR_IDENT"):
                parts.push(builder.QuasiExprHole(
                               builder.NounExpr(t.getData(), t.getSpan()),
                               t.getSpan()))
            else if (tname == "${"):
                def subexpr := expr(ej)
                parts.push(builder.QuasiExprHole(subexpr, subexpr.getSpan()))
            else if (tname == "AT_IDENT"):
                parts.push(builder.QuasiPatternHole(
                               builder.FinalPattern(
                                   builder.NounExpr(t.getData(), t.getSpan()),
                                   null, t.getSpan()),
                               t.getSpan()))
            else if (tname == "@{"):
                def subpatt := pattern(ej)
                parts.push(builder.QuasiPatternHole(subpatt, subpatt.getSpan()))
        if (isPattern):
            return builder.QuasiParserPattern(name, parts, spanFrom(spanStart))
        else:
            return builder.QuasiParserExpr(name, parts, spanFrom(spanStart))

    def guard(ej):
       if (peekTag() == "IDENTIFIER"):
            def t := advance(ej)
            return builder.NounExpr(t.getData(), t.getSpan())
       acceptTag("(", ej)
       def e := expr(ej)
       acceptTag(")", ej)
       return e

    def namePattern(ej, tryQuasi):
        def spanStart := spanHere()
        def nex := peekTag()
        if (nex == "IDENTIFIER"):
            def t := advance(ej)
            def nex2 := peekTag()
            if (nex2 == "QUASI_OPEN" || nex2 == "QUASI_CLOSE"):
                if (tryQuasi):
                    return quasiliteral(t, true, ej)
                else:
                    ej(nex2)
            else:
                def g := if (nex2 == ":") {advance(ej); guard(ej)} else {null}
                return builder.FinalPattern(builder.NounExpr(t.getData(), t.getSpan()), g, spanFrom(spanStart))
        else if (nex == "::"):
            advance(ej)
            def spanStart := spanHere()
            def t := accept(".String.", ej)
            def g := if (peekTag() == ":") {advance(ej); guard(ej)} else {null}
            return builder.FinalPattern(builder.NounExpr(t.getData(), t.getSpan()), g, spanFrom(spanStart))
        else if (nex == "var"):
            advance(ej)
            def spanStart := spanHere()
            def t := advance(ej)
            def tn := t.getTag().getName()
            if (tn == "IDENTIFIER"):
                def g := if (peekTag() == ":") {advance(ej); guard(ej)} else {null}
                return builder.VarPattern(builder.NounExpr(t.getData(), t.getSpan()), g, spanFrom(spanStart))
            else if (tn == "::"):
                def t := accept(".String.", ej)
                def g := if (peekTag() == ":") {advance(ej); guard(ej)} else {null}
                return builder.VarPattern(builder.NounExpr(t.getData(), t.getSpan()), g, spanFrom(spanStart))
        else if (nex == "&"):
            advance(ej)
            def spanStart := spanHere()
            def t := advance(ej)
            def tn := t.getTag().getName()
            if (tn == "IDENTIFIER"):
                def g := if (peekTag() == ":") {advance(ej); guard(ej)} else {null}
                return builder.SlotPattern(builder.NounExpr(t.getData(), t.getSpan()), g, spanFrom(spanStart))
            else if (tn == "::"):
                def t := accept(".String.", ej)
                def g := if (peekTag() == ":") {advance(ej); guard(ej)} else {null}
                return builder.SlotPattern(builder.NounExpr(t.getData(), t.getSpan()), g, spanFrom(spanStart))
        else if (nex == "&&"):
            advance(ej)
            def spanStart := spanHere()
            def t := advance(ej)
            def tn := t.getTag().getName()
            if (tn == "IDENTIFIER"):
                return builder.BindingPattern(builder.NounExpr(t.getData(), t.getSpan()), spanCover(t.getSpan(), spanFrom(spanStart)))
            else if (tn == "::"):
                def t := accept(".String.", ej)
                return builder.BindingPattern(builder.NounExpr(t.getData(), t.getSpan()), spanCover(t.getSpan(), spanFrom(spanStart)))
        else if (nex == "bind"):
            advance(ej)
            def spanStart := spanHere()
            def t := advance(ej)
            def tn := t.getTag().getName()
            if (tn == "IDENTIFIER"):
                return builder.BindPattern(builder.NounExpr(t.getData(), t.getSpan()), spanFrom(spanStart))
            else if (tn == "::"):
                def t := accept(".String.", ej)
                return builder.BindPattern(builder.NounExpr(t.getData(), t.getSpan()), spanFrom(spanStart))
        ej(nex)

    def mapPatternItemInner(ej):
        def spanStart := spanHere()
        if (peekTag() == "=>"):
            advance(ej)
            def p := namePattern(ej, false)
            return builder.MapPatternImport(p, spanFrom(spanStart))
        def k := if (peekTag() == "(") {
            advance(ej)
            def e := expr(ej)
            acceptTag(")", ej)
            e
        } else {
            if ([".String.", ".int.", ".float64.", ".char."].contains(peekTag())) {
                def t := advance(ej)
                builder.LiteralExpr(t, t.getSpan())
            } else {
                ej(peekTag())
            }
        }
        accept("=>", ej)
        return builder.MapPatternAssoc(k, pattern(ej), spanFrom(spanStart))

    def mapPatternItem(ej):
        def spanStart := spanHere()
        def p := mapPatternItemInner(ej)
        if (peekTag() == ":="):
            advance(ej)
            return builder.MapPatternDefault(p, order(ej), spanFrom(spanStart))
        else:
            return builder.MapPatternRequired(p, spanFrom(spanStart))

    def _pattern(ej):
        escape e:
            return namePattern(e, true)
        # ... if namePattern fails, keep going
        def spanStart := spanHere()
        def nex := peekTag()
        if (nex == "QUASI_OPEN" || nex == "QUASI_CLOSE"):
            return quasiliteral(null, true, ej)
        else if (nex == "=="):
            def spanStart := spanHere()
            advance(ej)
            return builder.SamePattern(prim(ej), true, spanFrom(spanStart))
        else if (nex == "!="):
            def spanStart := spanHere()
            advance(ej)
            return builder.SamePattern(prim(ej), false, spanFrom(spanStart))
        else if (nex == "_"):
            advance(ej)
            def spanStart := spanHere()
            def g := if (peekTag() == ":") {advance(ej); guard(ej)} else {null}
            return builder.IgnorePattern(g, spanFrom(spanStart))
        else if (nex == "via"):
            advance(ej)
            def spanStart := spanHere()
            acceptTag("(", ej)
            def e := expr(ej)
            acceptTag(")", ej)
            return builder.ViaPattern(e, pattern(ej), spanFrom(spanStart))
        else if (nex == "["):
            def spanStart := spanHere()
            advance(ej)
            def [items, isMap] := acceptListOrMap(pattern, mapPatternItem)
            acceptTag("]", ej)
            if (isMap):
                def tail := if (peekTag() == "|") {advance(ej); _pattern(ej)}
                return builder.MapPattern(items, tail, spanFrom(spanStart))
            else:
                def tail := if (peekTag() == "+") {advance(ej); _pattern(ej)}
                return builder.ListPattern(items, tail, spanFrom(spanStart))
        ej(nex)

    bind pattern(ej):
        def spanStart := spanHere()
        def p := _pattern(ej)
        if (peekTag() == "?"):
            advance(ej)
            acceptTag("(", ej)
            def e := expr(ej)
            acceptTag(")", ej)
            return builder.SuchThatPattern(p, e, spanFrom(spanStart))
        else:
            return p
    "XXX buggy expander eats this line"
    def mapItem(ej):
        def spanStart := spanHere()
        if (peekTag() == "=>"):
            advance(ej)
            return builder.MapExprExport(prim(ej), spanFrom(spanStart))
        def k := prim(ej)
        accept("=>", ej)
        def v := prim(ej)
        return builder.MapExprAssoc(k, v, spanFrom(spanStart))

    bind prim(ej):
        def tag := peekTag()
        if ([".String.", ".int.", ".float64.", ".char."].contains(tag)):
            def t := advance(ej)
            return builder.LiteralExpr(t, t.getSpan())
        if (tag == "IDENTIFIER"):
            def t := advance(ej)
            def nex := peekTag()
            if (nex == "QUASI_OPEN" || nex == "QUASI_CLOSE"):
                return quasiliteral(t, false, ej)
            else:
                return builder.NounExpr(t.getData(), t.getSpan())
        if (tag == "::"):
            def spanStart := spanHere()
            advance(ej)
            def t := accept(".String.", ej)
            return builder.NounExpr(t.getData(), t.getSpan())
        if (tag == "QUASI_OPEN" || tag == "QUASI_CLOSE"):
            return quasiliteral(null, false, ej)
        # paren expr
        if (tag == "("):
            advance(ej)
            def e := expr(ej)
            accept(")", ej)
            return e
        # hideexpr
        if (tag == "{"):
            def spanStart := spanHere()
            advance(ej)
            if (peekTag() == "}"):
                advance(ej)
                return builder.HideExpr(builder.SeqExpr([], null), spanFrom(spanStart))
            def e := expr(ej)
            accept("}", ej)
            return builder.HideExpr(e, spanFrom(spanStart))
        # list/map
        if (tag == "["):
            def spanStart := spanHere()
            advance(ej)
            if (peekTag() == "for"):
                advance(ej)
                # XXX
            def [items, isMap] := acceptListOrMap(expr, mapItem)
            accept("]", ej)
            if (isMap):
                return builder.MapExpr(items, spanFrom(spanStart))
            else:
                return builder.ListExpr(items, spanFrom(spanStart))
        throw.eject(ej, `don't recognize $tag`)
    "XXX buggy expander eats this line"
    # let's pretend
    bind order := prim
    bind expr := prim
    def blockExpr := prim
    def seqSep(ej):
        var next := advanceTag(ej)
        if (next != ";" && next != "EOL"):
            ej(null)
        while (true):
            next := advanceTag(ej)
            if (next != ";" && next != "EOL"):
                break
        return next

    def seq(ej):
        def start := spanHere()
        def exprs := [blockExpr(ej)].diverge()
        while (true):
            seqSep(__break)
            exprs.push(blockExpr(__break))
        opt(seqSep, ej)
        return builder.SeqExpr(exprs.snapshot(), spanFrom(start))

    def block(ej):
        acceptTag("{", ej)
        def contents := escape e {
            seq(ej)
        } catch _ {
            builder.SeqExpr([], null)
        }
        acceptTag("}", ej)
        return contents

    # would be different if we have toplevel-only syntax like pragmas
    def topSeq := seq

    def noun(ej):
        if (peekTag() == "IDENTIFIER"):
            def t := advance(ej)
            return builder.NounExpr(t.getData(), t.getSpan())
        else:
            acceptTag("::", ej)
            def spanStart := spanHere()
            advance(ej)
            def t := accept(".String.", ej)
            return builder.NounExpr(t.getData(), spanFrom(spanStart))

    def module_(ej):
        def start := spanHere()
        def modKw := acceptKw("module", ej)
        def imports := acceptList(pattern)
        acceptEOLs()
        acceptKw("export", ej)
        def exports := acceptList(noun)
        def body := topSeq(ej)
        return builder."Module"(imports, exports, body, spanFrom(start))

    def start(ej):
        if (peekTag() == "module"):
            return module_(ej)
        else:
            return topSeq(ej)
    if (mode == "module"):
        return start(err)
    else if (mode == "expression"):
        return expr(err)
    else if (mode == "pattern"):
        return pattern(err)
    return "broke"

def parseExpression(lex, builder, err):
    return parseMonte(lex, builder, "expression", err)

def parseModule(lex, builder, err):
    return parseMonte(lex, builder, "module", err)

def parsePattern(lex, builder, err):
    return parseMonte(lex, builder, "pattern", err)

# object quasiMonteParser:
#     to valueHole(n):
#         return VALUE_HOLE
#     to patternHole(n):
#         return PATTERN_HOLE

#     to valueMaker(template):
#         def chain := makeQuasiTokenChain(makeMonteLexer, template)
#         def q := makeMonteParser(chain, astBuilder)
#         return object qast extends q:
#            to substitute(values):
#                return q.transform(holeFiller)

#     to matchMaker(template):
#         def chain := makeQuasiTokenChain(makeMonteLexer, template)
#         def q := makeMonteParser(chain, astBuilder)
#         return object qast extends q:
#             to matchBind(values, specimen, ej):
#                 escape ej:
#                     def holeMatcher := makeHoleMatcher(ej)
#                     q.transform(holeMatcher)
#                     return holeMatcher.getBindings()
#                 catch blee:
#                     ej(`$q doesn't match $specimen: $blee`)

# Tests.

def expr(s):
 return parseExpression(makeMonteLexer(s), astBuilder, throw).asTerm()

def pattern(s):
 return parsePattern(makeMonteLexer(s), astBuilder, throw).asTerm()

def testLiteral(assert):
    assert.equal(expr("\"foo bar\""), term`LiteralExpr("foo bar")`)
    assert.equal(expr("'z'"), term`LiteralExpr('z')`)
    assert.equal(expr("7"), term`LiteralExpr(7)`)
    assert.equal(expr("(7)"), term`LiteralExpr(7)`)
    assert.equal(expr("0.5"), term`LiteralExpr(0.5)`)

def testNoun(assert):
    assert.equal(expr("foo"), term`NounExpr("foo")`)
    assert.equal(expr("::\"object\""), term`NounExpr("object")`)

def testQuasiliteralExpr(assert):
    assert.equal(expr("`foo`"), term`QuasiParserExpr(null, [QuasiText("foo")])`)
    assert.equal(expr("bob`foo`"), term`QuasiParserExpr("bob", [QuasiText("foo")])`)
    assert.equal(expr("bob`foo`` $x baz`"), term`QuasiParserExpr("bob", [QuasiText("foo`` "), QuasiExprHole(NounExpr("x")), QuasiText(" baz")])`)
    assert.equal(expr("`($x)`"), term`QuasiParserExpr(null, [QuasiText("("), QuasiExprHole(NounExpr("x")), QuasiText(")")])`)

def testHide(assert):
    assert.equal(expr("{}"), term`HideExpr(SeqExpr([]))`)
    assert.equal(expr("{1}"), term`HideExpr(LiteralExpr(1))`)

def testList(assert):
    assert.equal(expr("[]"), term`ListExpr([])`)
    assert.equal(expr("[a, b]"), term`ListExpr([NounExpr("a"), NounExpr("b")])`)

def testMap(assert):
    assert.equal(expr("[k => v, => a]"),
         term`MapExpr([MapExprAssoc(NounExpr("k"), NounExpr("v")),
                       MapExprExport(NounExpr("a"))])`)
    assert.equal(expr("[=> b, k => v]"),
         term`MapExpr([MapExprExport(NounExpr("b")),
                       MapExprAssoc(NounExpr("k"), NounExpr("v"))])`)

def testIgnorePattern(assert):
    assert.equal(pattern("_"), term`IgnorePattern(null)`)
    assert.equal(pattern("_ :Int"), term`IgnorePattern(NounExpr("Int"))`)
    assert.equal(pattern("_ :(1)"), term`IgnorePattern(LiteralExpr(1))`)

def testFinalPattern(assert):
    assert.equal(pattern("foo"), term`FinalPattern(NounExpr("foo"), null)`)
    assert.equal(pattern("foo :Int"), term`FinalPattern(NounExpr("foo"), NounExpr("Int"))`)
    assert.equal(pattern("foo :(1)"), term`FinalPattern(NounExpr("foo"), LiteralExpr(1))`)
    assert.equal(pattern("::\"foo baz\""), term`FinalPattern(NounExpr("foo baz"), null)`)
    assert.equal(pattern("::\"foo baz\" :Int"), term`FinalPattern(NounExpr("foo baz"), NounExpr("Int"))`)
    assert.equal(pattern("::\"foo baz\" :(1)"), term`FinalPattern(NounExpr("foo baz"), LiteralExpr(1))`)

def testSlotPattern(assert):
    assert.equal(pattern("&foo"), term`SlotPattern(NounExpr("foo"), null)`)
    assert.equal(pattern("&foo :Int"), term`SlotPattern(NounExpr("foo"), NounExpr("Int"))`)
    assert.equal(pattern("&foo :(1)"), term`SlotPattern(NounExpr("foo"), LiteralExpr(1))`)
    assert.equal(pattern("&::\"foo baz\""), term`SlotPattern(NounExpr("foo baz"), null)`)
    assert.equal(pattern("&::\"foo baz\" :Int"), term`SlotPattern(NounExpr("foo baz"), NounExpr("Int"))`)
    assert.equal(pattern("&::\"foo baz\" :(1)"), term`SlotPattern(NounExpr("foo baz"), LiteralExpr(1))`)


def testVarPattern(assert):
    assert.equal(pattern("var foo"), term`VarPattern(NounExpr("foo"), null)`)
    assert.equal(pattern("var foo :Int"), term`VarPattern(NounExpr("foo"), NounExpr("Int"))`)
    assert.equal(pattern("var foo :(1)"), term`VarPattern(NounExpr("foo"), LiteralExpr(1))`)
    assert.equal(pattern("var ::\"foo baz\""), term`VarPattern(NounExpr("foo baz"), null)`)
    assert.equal(pattern("var ::\"foo baz\" :Int"), term`VarPattern(NounExpr("foo baz"), NounExpr("Int"))`)
    assert.equal(pattern("var ::\"foo baz\" :(1)"), term`VarPattern(NounExpr("foo baz"), LiteralExpr(1))`)

def testBindPattern(assert):
    assert.equal(pattern("bind foo"), term`BindPattern(NounExpr("foo"))`)
    assert.equal(pattern("bind ::\"foo baz\""), term`BindPattern(NounExpr("foo baz"))`)

def testBindingPattern(assert):
    assert.equal(pattern("&&foo"), term`BindingPattern(NounExpr("foo"))`)
    assert.equal(pattern("&&::\"foo baz\""), term`BindingPattern(NounExpr("foo baz"))`)

def testSamePattern(assert):
    assert.equal(pattern("==1"), term`SamePattern(LiteralExpr(1), true)`)
    assert.equal(pattern("==(x)"), term`SamePattern(NounExpr("x"), true)`)

def testNotSamePattern(assert):
    assert.equal(pattern("!=1"), term`SamePattern(LiteralExpr(1), false)`)
    assert.equal(pattern("!=(x)"), term`SamePattern(NounExpr("x"), false)`)

def testViaPattern(assert):
    assert.equal(pattern("via (b) a"), term`ViaPattern(NounExpr("b"), FinalPattern(NounExpr("a"), null))`)

def testListPattern(assert):
    assert.equal(pattern("[]"), term`ListPattern([], null)`)
    assert.equal(pattern("[a, b]"), term`ListPattern([FinalPattern(NounExpr("a"), null), FinalPattern(NounExpr("b"), null)], null)`)
    assert.equal(pattern("[a, b] + c"), term`ListPattern([FinalPattern(NounExpr("a"), null), FinalPattern(NounExpr("b"), null)], FinalPattern(NounExpr("c"), null))`)

def testMapPattern(assert):
     assert.equal(pattern("[\"k\" => v, (a) => b, => c]"), term`MapPattern([MapPatternRequired(MapPatternAssoc(LiteralExpr("k"), FinalPattern(NounExpr("v"), null))), MapPatternRequired(MapPatternAssoc(NounExpr("a"), FinalPattern(NounExpr("b"), null))), MapPatternRequired(MapPatternImport(FinalPattern(NounExpr("c", null))))], null)`)
     assert.equal(pattern("[\"a\" => b := 1] | c"), term`MapPattern([MapPatternDefault(MapPatternAssoc(LiteralExpr("a"), FinalPattern(NounExpr("b"), null)), LiteralExpr(1))], FinalPattern(NounExpr("c"), null))`)
     assert.equal(pattern("[\"k\" => &v, => &&b, => ::\"if\"]"), term`MapPattern([MapPatternRequired(MapPatternAssoc(LiteralExpr("k"), SlotPattern(NounExpr("v"), null))), MapPatternRequired(MapPatternImport(BindingPattern(NounExpr("b")))), MapPatternRequired(MapPatternImport(FinalPattern(NounExpr("if"), null)))], null)`)

def testQuasiliteralPattern(assert):
    assert.equal(pattern("`foo`"), term`QuasiParserPattern(null, [QuasiText("foo")])`)
    assert.equal(pattern("bob`foo`"), term`QuasiParserPattern("bob", [QuasiText("foo")])`)
    assert.equal(pattern("bob`foo`` $x baz`"), term`QuasiParserPattern("bob", [QuasiText("foo`` "), QuasiExprHole(NounExpr("x")), QuasiText(" baz")])`)
    assert.equal(pattern("`($x)`"), term`QuasiParserPattern(null, [QuasiText("("), QuasiExprHole(NounExpr("x")), QuasiText(")")])`)
    assert.equal(pattern("`foo @{w}@x $y${z} baz`"), term`QuasiParserPattern(null, [QuasiText("foo "), QuasiPatternHole(FinalPattern(NounExpr("w"), null)), QuasiPatternHole(FinalPattern(NounExpr("x"), null)), QuasiText(" "), QuasiExprHole(NounExpr("y")), QuasiExprHole(NounExpr("z")), QuasiText(" baz")])`)

def testSuchThatPattern(assert):
    assert.equal(pattern("x :y ? (1)"), term`SuchThatPattern(FinalPattern(NounExpr("x"), NounExpr("y")), LiteralExpr(1))`)


# def test_holes(assert):
#     assert.equal(quasiMonteParser.valueMaker(["foo(", quasiMonteParser.valueHole(0), ")"]), term`ValueHoleExpr(0)`)
#     assert.equal(expr("@{2}"), term`PatternHoleExpr(2)`)
#     assert.equal(pattern("${2}"), term`ValueHoleExpr(0)`)
#     assert.equal(pattern("@{2}"), term`PatternHoleExpr(0)`)
unittest([testLiteral, testNoun, testQuasiliteralExpr, testHide, testList, testMap, testIgnorePattern, testFinalPattern, testVarPattern, testBindPattern, testSamePattern, testNotSamePattern, testSlotPattern, testBindingPattern, testViaPattern, testListPattern, testMapPattern, testQuasiliteralPattern, testSuchThatPattern])
