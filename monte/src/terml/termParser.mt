module makeTag, makeTerm, makeTermLexer, unittest
export (parseTerm, term__quasiParser)

def parseTerm(input):
    def tokens := __makeList.fromIterable(makeTermLexer(input))
    var position := -1
    escape done:
        def advance(ej):
            position += 1
            if (position >= tokens.size()):
                ej("hit EOF")
            return tokens[position]

        def rewind():
            position -= 1

        def peek():
            if (position + 1 >= tokens.size()):
                return null
            return tokens[position + 1]

        def accept(termName):
            def t := advance(done)
            if (t.getTag().getName() == termName):
                return t
            else:
                done(`expected $termName, got $t`)

        def maybeAccept(termName):
            escape e:
                def t := advance(e)
                if (t.getTag().getName() == termName):
                    return t
            rewind()
            return null

        def functor():
            return "you win"

        def extraTerm():
            # tuple
            # labelled bag
            # bag
            def token := advance(done)
            if (token.getData() != null):
                return token
            def name := functor()
            # args
            return name

        def term():
            def k := extraTerm()
            if (maybeAccept(':') != null):
                return makeTerm(makeTag(".attr.", null, any), null,
                                [k, extraTerm()], null)
            else:
                return k

        return term()

def term__quasiParser := null

def test_literal(assert):
    def mk(tag, val):
        return makeTerm(makeTag(null, tag, any), val, [], null)
    assert.equal(parseTerm("0xDECAFC0FFEEBAD"), mk(".int.", 0xDECAFC0FFEEBAD))
    assert.equal(parseTerm("3.14159E17"), mk(".float64.", 3.14159E17))
    assert.equal(parseTerm("1e9"), mk(".float64.", 1e9))
    assert.equal(parseTerm("0"), mk(".int.", 0))
    assert.equal(parseTerm("7"), mk(".int.", 7))
    assert.equal(parseTerm("-1"), mk(".int.", -1))
    assert.equal(parseTerm("-3.14"), mk(".float64.", -3.14))
    assert.equal(parseTerm("3_000"), mk(".int.", 3000))
    assert.equal(parseTerm("0.91"), mk(".float64.", 0.91))
    assert.equal(parseTerm("3e-2"), mk(".float64.", 3e-2))
    assert.equal(parseTerm("\"foo\\nbar\""), mk(".String.", "foo\nbar"))
    assert.equal(parseTerm("\"foo\\\nbar\""), mk(".String.", "foobar"))
    assert.equal(parseTerm("\"z\\x61p\""), mk(".String.", "zap"))
    assert.equal(parseTerm("'x'"), mk(".char.", 'x'))
    assert.equal(parseTerm("'\\n'"), mk(".char.", '\n'))
    assert.equal(parseTerm("'\\u0061'"), mk(".char.", 'a'))


unittest([test_literal])
