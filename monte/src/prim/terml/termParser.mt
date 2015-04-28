module __makeOrderedSpace, makeTag, optMakeTagFromData, makeTerm, makeTermLexer, convertToTerm, makeQFunctor, makeQTerm, makeQSome, makeQDollarHole, makeQAtHole, qEmptySeq, makeQPairSeq, termBuilder, unittest
export (parseTerm, quasitermParser)
def tokenStart := 'a'..'z' | 'A'..'Z' | '_'..'_' | '$'..'$' | '.'..'.'


def mkq(name, data):
    return makeQFunctor(makeTag(null, name, Any), data, null)

object qBuilder:
    to leafInternal(tag, data, span):
        return makeQFunctor(tag, data, span)

    to leafData(data, span):
        return makeQFunctor(optMakeTagFromData(data, mkq), data, span)

    to composite(tag, data, span):
        return qBuilder.term(qBuilder.leafInternal(tag, null, span), qBuilder.leafData(data, span))

    to term(functor, args):
        if (functor.isHole() && !functor.getIsFunctorHole()):
            return functor
        return makeQTerm(functor, args)

    to some(sub, quant):
        return makeQSome(sub, quant, if (sub == null) {null} else {sub.getSpan()})

    to empty():
        return qEmptySeq

    to addArg(arglist, arg):
        return makeQPairSeq(arglist, arg)


def _parseTerm(lex, builder, err):
    def [VALUE_HOLE, PATTERN_HOLE] := [lex.valueHole(), lex.patternHole()]
    def tokens := __makeList.fromIterable(lex)
    var dollarHoleValueIndex := -1
    var atHoleValueIndex := -1
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
        def token := advance(fail)
        if (token == VALUE_HOLE):
            return makeQDollarHole(null, dollarHoleValueIndex += 1, false)
        if (token == PATTERN_HOLE):
            return makeQAtHole(null, atHoleValueIndex += 1, false)
        if (token.getData() != null):
            return token
        def name := token.getTag().getName()
        if (name.size() > 0 && tokenStart(name[0])):
            if (peek() == VALUE_HOLE):
                advance(fail)
                return makeQDollarHole(token, dollarHoleValueIndex += 1, false)
            if (peek() == PATTERN_HOLE):
                advance(fail)
                return makeQAtHole(token.getTag(), atHoleValueIndex += 1, false)
            return token
        rewind()
        fail(null)

    def term
    def arglist(closer, fail):
        var args := builder.empty()
        escape e:
            args := builder.addArg(args, term(e))
        catch err:
            accept(closer, fail)
            return args
        escape outOfArgs:
            while (true):
                accept(",", outOfArgs)
                args := builder.addArg(args, term(outOfArgs))
        accept(closer, fail)
        return args
    def namedTerm(name, args):
        return builder.term(builder.leafInternal(makeTag(null, name, Any), null, null), args)
    def extraTerm(fail):
        if (maybeAccept("[") != null):
            return namedTerm(".tuple.", arglist("]", fail))
        else if (maybeAccept("{") != null):
            return namedTerm(".bag.", arglist("}", fail))
        def rootTerm := functor(fail)
        if (maybeAccept("{") != null):
            def f := rootTerm.asFunctor()
            return builder.term(f, builder.addArg(builder.empty(), namedTerm(".bag.", arglist("}", fail))))
        if (maybeAccept("(") != null):
            def f := rootTerm.asFunctor()
            return builder.term(f, arglist(")", fail))
        return builder.term(rootTerm, builder.empty())

    def prim(fail):
        def k := extraTerm(fail)
        if (maybeAccept(":") != null):
            def v := extraTerm(onError(fail, "Expected term after ':'"))
            return namedTerm(".attr.", builder.addArg(builder.addArg(builder.empty(), k), v))
        else:
            return k

    def some(t):
        if (maybeAccept("*") != null):
            return builder.some(t, "*")
        if (maybeAccept("+") != null):
            return builder.some(t, "+")
        if (maybeAccept("?") != null):
            return builder.some(t, "?")
        return t

    bind term(fail):
        if (maybeAccept("(") != null):
            return some(arglist(")", fail))
        return some(prim(fail))

    term # deleting this line breaks tests. is there some compiler BS going on?
    return prim(err)

def parseTerm(input):
    def lex := makeTermLexer(input, termBuilder)
    return _parseTerm(lex, termBuilder, throw)

def makeQuasiTokenChain(makeLexer, template):
    var i := -1
    var current := makeLexer("", qBuilder)
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
        def chain := makeQuasiTokenChain(makeTermLexer, template)
        def q := _parseTerm(chain, qBuilder, throw)
        return object qterm extends q:
           to substitute(values):
               def vals := q.substSlice(values, [].diverge())
               if (vals.size() != 1):
                  throw(`Must be a single match: ${vals}`)
               return vals[0]

    to matchMaker(template):
        def chain := makeQuasiTokenChain(makeTermLexer, template)
        def q := _parseTerm(chain, qBuilder, throw)
        return object qterm extends q:
            to matchBind(values, specimen, ej):
                def bindings := [].diverge()
                def blee := q.matchBindSlice(values, [specimen], bindings, [], 1)
                if (blee == 1):
                    return bindings
                else:
                    ej(`$q doesn't match $specimen: $blee`)

    to makeTag(code, name, guard):
        return makeTag(code, name, guard)

    to makeTerm(tag, data, arglist, span):
        return makeTerm(tag, data, arglist, span)



def test_literal(assert):
    def mk(tag, val):
        return makeTerm(makeTag(null, tag, Any), val, [], null)
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
        return makeTerm(makeTag(null, name, Any), null, args, null)
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
        assert.equal(qt`zip(${[]}*)`, qt`zip`)
        assert.raises(fn {qt`zip($args?)`})
        assert.raises(fn {qt`zip(${[]}+)`})
    }


def test_qtermMatch(assert):
    def qt__quasiParser := quasitermParser
    {
        def qt`@foo` := "hello"
        assert.equal(foo, parseTerm("\"hello\""))
    }
    {
        def qt`@bar()` := "hello"
        assert.equal(bar, parseTerm("hello"))
    }
    {
        assert.raises(fn {def qt`hello@foo` := "hello"})
    }
    {
        def qt`hello@foo` := parseTerm("hello(3, 4)")
        assert.equal(foo, parseTerm("hello(3, 4)"))
    }
    {
        def qt`.String.@foo` := "hello"
        assert.equal(foo, qt`"hello"`)
    }
    {
        # XXX WTF does this mean?
        def qt`hello@bar()` := "hello"
        assert.equal(bar, parseTerm("hello"))
    }
    {
        assert.raises(fn {
            def qt`hello@bar()` := "hello world"
        })
    }
    {
        def qt`${qt`foo`}(@args*)` := parseTerm("foo(2, 3)")
        assert.equal(args, [qt`2`, qt`3`])
    }
    {
        def t := qt`foo(bar, bar(3), zip(zap))`
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
unittest([test_literal, test_simpleTerm, test_fullTerm, test_qtermSubstitute,
          test_qtermMatch])
