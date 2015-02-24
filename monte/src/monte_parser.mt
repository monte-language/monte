module unittest, makeMonteLexer, astBuilder
export (parseMonte)
def spanCover(left, right):
    if (left == null || right == null):
        return null
    return left.combine(right)

def parseMonte(lex, builder, err):
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
        if (advanceTag(fail) != tagname):
            position -= 1
            fail(tagname)

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

    #def expr
    #def block

    def prim(ej):
        if ([".String.", ".int.", ".float64.", ".char."].contains(peek().getTag().getName())):
            def t := advance(ej)
            return builder.LiteralExpr(t, t.getSpan())
        # basic
        # quasi
        # noun
        # paren expr
        # hideexpr
        # list/map

    # let's pretend
    def expr := prim
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
    def pattern(ej):
        pass

    def noun(ej):
        pass

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
    return start(err)
# Tests.


def expr(s):
    def term`SeqExpr([@result])` := parseMonte(makeMonteLexer(s), astBuilder, throw).asTerm()
    return result

def testLiteral(assert):
    assert.equal(expr("\"foo bar\""), term`LiteralExpr("foo bar")`)
    assert.equal(expr("'z'"), term`LiteralExpr('z')`)
    assert.equal(expr("7"), term`LiteralExpr(7)`)
    assert.equal(expr("0.5"), term`LiteralExpr(0.5)`)

unittest([testLiteral])
