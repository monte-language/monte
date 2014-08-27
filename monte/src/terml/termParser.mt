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
    def arglist(closer, fail):
        def args := [].diverge()
        escape e:
            args.push(term(e))
        catch err:
            accept(closer, fail)
            return []
        escape outOfArgs:
            while (true):
                accept(",", outOfArgs)
                args.push(term(outOfArgs))
        accept(closer, fail)
        return args.snapshot()

    def extraTerm(fail):
        # tuple
        # labelled bag
        # bag
        if (maybeAccept("[") != null):
            return makeTerm(makeTag(null, ".tuple.", any), null, arglist("]", fail), null)
        else if (maybeAccept("{") != null):
            return makeTerm(makeTag(null, ".bag.", any), null, arglist("}", fail), null)
        def rootTerm := functor(fail)
        if (maybeAccept("{") != null):
            return makeTerm(rootTerm.getTag(), rootTerm.getData(), [makeTerm(makeTag(null, ".bag.", any), null, arglist("}", fail), null)], rootTerm.getSpan())
        var args := []
        if (maybeAccept("(") != null):
            args := arglist(")", fail)
        return makeTerm(rootTerm.getTag(), rootTerm.getData(), args, rootTerm.getSpan())

    bind term(fail):
        def k := extraTerm(fail)
        if (maybeAccept(":") != null):
            def v := extraTerm(onError(fail, "Expected term after ':'"))
            return makeTerm(makeTag(null, ".attr.", any), null,
                            [k, v], null)
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
    assert.equal(parseTerm("x(y, z)"), mk("x", [mk("y", []), mk("z", [])]))
    assert.equal(parseTerm("x(y, z,)"), mk("x", [mk("y", []), mk("z", [])]))

def test_fullTerm(assert):
    assert.equal(parseTerm("[x, y, 1]"), parseTerm(".tuple.(x, y, 1)"))
    assert.equal(parseTerm("{x, y, 1}"), parseTerm(".bag.(x, y, 1)"))
    assert.equal(parseTerm("f {x, y, 1}"), parseTerm("f(.bag.(x, y, 1))"))
    assert.equal(parseTerm("a: b"), parseTerm(".attr.(a, b)"))


unittest([test_literal, test_simpleTerm, test_fullTerm])
