module makeTag, makeTerm, makeTermLexer, convertToTerm, unittest
export (parseTerm, term__quasiParser)
def tokenStart := 'a'..'z' | 'A'..'Z' | '_'..'_' | '$'..'$' | '.'..'.'

def _parseTerm(lex, holeValues, err):
    def [VALUE_HOLE, PATTERN_HOLE] := [lex.valueHole(), lex.patternHole()]
    def tokens := __makeList.fromIterable(lex)
    var holeValueIndex := 0
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
        def isHole := t == VALUE_HOLE || t == PATTERN_HOLE
        if (!isHole && t.getTag().getName() == termName):
            return t
        else:
            rewind()
            fail(`expected $termName, got $t`)

    def maybeAccept(termName):
        escape e:
            def t := advance(e)
            def isHole := t == VALUE_HOLE || t == PATTERN_HOLE
            if (!isHole && t.getTag().getName() == termName):
                return t
        rewind()
        return null

    def functor(fail):
        # XXX maybe tokens shouldn't be represented as terms? not sure
        def token := advance(fail)
        if (token == VALUE_HOLE):
            def f := convertToTerm(holeValues[holeValueIndex], fail)
            holeValueIndex += 1
            return [f, true]
        if (token.getData() != null):
            return [token, false]
        def name := token.getTag().getName()
        if (name.size() > 0 && tokenStart(name[0])):
            return [token, false]
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
        if (maybeAccept("[") != null):
            return makeTerm(makeTag(null, ".tuple.", any), null, arglist("]", fail), null)
        else if (maybeAccept("{") != null):
            return makeTerm(makeTag(null, ".bag.", any), null, arglist("}", fail), null)
        def [rootTerm, filledHole] := functor(fail)
        var args := []
        if (filledHole):
            args := rootTerm.getArgs()
        if (maybeAccept("{") != null):
            if (filledHole && args != []):
                fail(`Can't fill a functor hole with term $rootTerm`)
            return makeTerm(rootTerm.getTag(), rootTerm.getData(), [makeTerm(makeTag(null, ".bag.", any), null, arglist("}", fail), null)], rootTerm.getSpan())
        if (maybeAccept("(") != null):
            if (filledHole && args != []):
                fail(`Can't fill a functor hole with term $rootTerm`)
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
    return term(err)

def parseTerm(input):
    def lex := makeTermLexer(input)
    return _parseTerm(lex, [], throw)

def makeQuasiTokenChain(makeLexer, template):
    var i := -1
    var current := makeLexer("")
    var lex := current
    def [VALUE_HOLE, PATTERN_HOLE] := makeLexer.holes()
    var j := 0
    return object chainer:
        to _makeIterator():
            return chainer

        to valueHole():
           return VALUE_HOLE

        to patternHole():
           return PATTERN_HOLE

        to next(ej):
            if (i >= template.size()):
                throw.eject(ej, null)
            j += 1
            if (current == null):
                if (template[i] == VALUE_HOLE || template[i] == PATTERN_HOLE):
                    def hol := template[i]
                    i += 1
                    return [j, hol]
                else:
                    current := lex.lexerForNextChunk(template[i])._makeIterator()
                    lex := current
            escape e:
                def t := current.next(e)[1]
                return [j, t]
            catch z:
                i += 1
                current := null
                return chainer.next(ej)


def [VALUE_HOLE, PATTERN_HOLE] := makeTermLexer.holes()

object quasitermParser:
    to valueHole(n):
        return VALUE_HOLE
    to patternHole(n):
        return PATTERN_HOLE
    to valueMaker(template):
        return object valueQTerm:
            to substitute(values):
                def chain := makeQuasiTokenChain(makeTermLexer, template)
                return _parseTerm(chain, values, throw)

    to matchMaker(template):
        return object patternQTerm:
            to matchBind(values, specimen, ej):
                def chain := makeQuasiTokenChain(makeTermLexer, template)
                def qpatt := _parseTerm(chain, values, ej)

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

def test_qtermSubstitute(assert):
    def qt__quasiParser := quasitermParser
    {
         def x := 1
         def y := parseTerm("baz")
         assert.equal(qt`foo($x, $y)`, parseTerm("foo(1, baz)"))

    }
    {
        def x := parseTerm("foo")
        assert.equal(qt`$x(3)`, parseTerm("foo(3)"))
        def y := parseTerm("baz(3)")
        assert.equal(qt`foo($y)`._uncall(), parseTerm("foo(baz(3))")._uncall())
    }
    {
        def x := parseTerm("foo(3)")
        assert.raises(fn { qt`$x(3)` })
    }
    {
        def args := [qt`foo`, qt`bar(3)`]
        assert.equal(qt`zip($args*)`, qt`zip(foo, bar(3))`)
        assert.equal(qt`zip($args+)`, qt`zip(foo, bar(3))`)
        assert.equal(qt`zip(${[]})*`, qt`zip`)
        assert.raises(fn {qt`zip($args?)`})
        assert.raises(fn {qt`zip(${[]}+)`})
    }


def test_qtermMatch(assert):
    def qt__quasiParser := quasitermParser
    {
        def qt`@foo` := "hello"
        assert.equal(foo, "hello")
    }
    {
        def qt`@bar()` := "hello"
        assert.equal(bar, "hello")
    }
    {
        assert.raises(fn {def qt`hello@foo` := "hello"})
    }
    {
        def qt`hello@foo` := qt`hello(3, 4)`
        assert.equal(foo, qt`hello(3, 4)`)
    }
    {
        def qt`.String.@foo` := "hello"
        assert.equal(foo, qt`"hello"`)
    }
    {
        # XXX WTF does this mean?
        def qt`hello@bar()` := "hello"
        assert.equal(bar, term`hello`)
    }
    {
        assert.raises(fn {
            def qt`hello@bar()` := "hello world"
        })
    }
    {
        def qt`${qt`foo`}(@args*)` := term`foo(2, 3)`
        assert.equal(args, [qt`2`, qt`3`])
    }
    {
        def t := qt`foo(bar, bar(3), zip(zap)`
        def qt`foo(bar@bars*, zip@z)` := t
        assert.equal(bars, [qt`bar`, qt`bar(3)`])
        assert.equal(z, qt`zip(zap)`)
    }
    {
        def qt`[@x*, @y, @z]` := qt`[4, 5, 6, 7, 8]`
        assert.equal([x, y, z], [[qt`4`, qt`5`, qt`6`], qt`7`, qt`8`])
    }
    {
        def qt`[@x*, @y?, @z]` := qt`[4, 5, 6, 7, 8]`
        assert.equal([x, y, z], [[qt`4`, qt`5`, qt`6`, qt`7`], [], qt`8`])
    }
    {
        def qt`[@x*, @y+, @z]` := qt`[4, 5, 6, 7, 8]`
        assert.equal([x, y, z], [[qt`4`, qt`5`, qt`6`], [qt`7`], qt`8`])
    }
    {
        def qt`[@x*, (@y, @z)+]` := qt`[4, 5, 6, 7, 8]`
        assert.equal([x, y, z], [[qt`4`, qt`5`, qt`6`], [qt`7`], [qt`8`]])
    }
unittest([test_literal, test_simpleTerm, test_fullTerm, test_qtermSubstitute])
