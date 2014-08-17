module makeTag, makeTerm, makeTermLexer, unittest
export (parseTerm, term__quasiParser)
def tokenStart := 'a'..'z' | 'A'..'Z' | '_'..'_' | '$'..'$' | '.'..'.'
def parseTerm(input):
    def tokens := __makeList.fromIterable(makeTermLexer(input))
    var position := -1

    def onError(e, msg):
        def syntaxError(_):
            e(msg)
        return syntaxError

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

    def accept(termName, fail):
        def t := advance(fail)
        if (t.getTag().getName() == termName):
            return t
        else:
            rewind()
            fail(`expected $termName, got $t`)

    def maybeAccept(termName):
        escape e:
            def t := advance(e)
            if (t.getTag().getName() == termName):
                return t
        rewind()
        return null

    def functor(fail):
        # XXX maybe tokens shouldn't be represented as terms? not sure
        def token := advance(fail)

        if (token.getData() != null):
            return token
        def name := token.getTag().getName()
        if (name.size() > 0 && tokenStart(name[0])):
            return token
        rewind()
        fail(null)

    def term

    def extraTerm(fail):
        # tuple
        # labelled bag
        # bag
        def rootTerm := functor(fail)

        def args := [].diverge()
        if (maybeAccept("(") != null):
            escape e:
                args.push(term(e))
            catch err:

                accept(")", fail)
                return rootTerm
            escape outOfArgs:
                while (true):
                    accept(",", outOfArgs)
                    args.push(term(outOfArgs))

            accept(")", fail)

        return makeTerm(rootTerm.getTag(), rootTerm.getData(), args.snapshot(), rootTerm.getSpan())

    bind term(fail):
        def k := extraTerm(fail)
        if (maybeAccept(':') != null):
            return makeTerm(makeTag(".attr.", null, any), null,
                            [k, extraTerm(onError(fail, "Expected term after ':'"))], null)
        else:
            return k
    term # deleting this line breaks tests. is there some compiler BS going on?
    return term(throw)

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

def test_simpleTerm(assert):
    def mk(name, args):
        return makeTerm(makeTag(null, name, any), null, args, null)
    assert.equal(parseTerm("x"), mk("x", []))
    assert.equal(parseTerm("x()"), mk("x", []))
    assert.equal(parseTerm("x(y)"), mk("x", [mk("y", [])]))


unittest([test_literal, test_simpleTerm])
