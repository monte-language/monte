def [_any, _all] := import("anyAll")
def atoi := import("atoi")

def _glueReps([x, xs]):
    if (xs == null):
        return [x]
    return [x] + xs

# The core.

object empty:
    pass

object nullSet:
    pass

object term:
    pass

object exactly:
    pass

object anything:
    pass

object reduction:
    pass

object alternation:
    pass

object catenation:
    pass

object repeat:
    pass

# For QLs.

object value:
    pass

def _join(xs, glue):
    var out := ""
    if (xs.size() == 0):
        return out

    def l := xs.diverge()
    def end := l.pop()
    for x in l:
        out += x
        out += glue
    return out + end

def parserSize(l):
    switch (l):
        match ==empty:
            return 1
        match ==nullSet:
            return 1
        match ==anything:
            return 1
        match [==exactly, _]:
            return 1
        match [==value, _]:
            return 1

        match [==term, ts]:
            return 1 + parserSize(ts)
        match [==reduction, inner, f]:
            return 1 + parserSize(inner)
        match [==alternation, ls]:
            var sum := 1
            for l in ls:
                sum += parserSize(l)
            return sum
        match [==catenation, a, b]:
            return 1 + parserSize(a) + parserSize(b)
        match [==repeat, inner]:
            return 1 + parserSize(inner)

        match _:
            return 1

def showParser(l, out):
    switch (l):
        match ==empty:
            out.print("∅")
        match ==nullSet:
            out.print("ε")
        match ==anything:
            out.print("any")

        match [==term, ts]:
            out.print("term(")
            out.quote(ts)
            out.print(")")
        match [==exactly, t]:
            out.print("ex(")
            out.quote(t)
            out.print(")")
        match [==reduction, inner, f]:
            out.println("red(")
            def indent := out.indent(null)
            showParser(inner, indent)
            indent.println(",")
            indent.println(f)
            out.print(")")
        match [==alternation, ls]:
            out.println("alt([")
            def indent := out.indent(null)
            for option in ls:
                showParser(option, indent)
                indent.println(",")
            out.print("])")
        match [==catenation, a, b]:
            out.println("cat(")
            def indent := out.indent(null)
            showParser(a, indent)
            indent.println(",")
            showParser(b, indent)
            out.print(")")
        match [==repeat, inner]:
            out.print("rep(")
            showParser(inner, out)
            out.print(")")

        match [==value, inner]:
            out.print(`val($inner)`)

        match _:
            traceln(`I don't know how to print $l`)

def onlyNull(l) :boolean:
    switch (l):
        match ==nullSet:
            return true
        match [==term, _]:
            return true

        match [==reduction, inner, _]:
            return onlyNull(inner)
        match [==alternation, ls]:
            return _all([onlyNull(l) for l in ls])
        match [==catenation, a, b]:
            return onlyNull(a) & onlyNull(b)

        match _:
            return false

def nullable(l) :boolean:
    if (onlyNull(l)):
        return true

    switch (l):
        match [==reduction, inner, _]:
            return nullable(inner)
        match [==alternation, ls]:
            return _any([nullable(l) for l in ls])
        match [==catenation, a, b]:
            return nullable(a) & nullable(b)

        match [==repeat, _]:
            return true

        match _:
            return false

def isEmpty(l) :boolean:
    switch (l):
        match ==empty:
            return true
        match [==reduction, inner, _]:
            return isEmpty(inner)
        match [==alternation, ls]:
            return _all([isEmpty(l) for l in ls])
        match [==catenation, a, b]:
            return isEmpty(a) | isEmpty(b)
        match [==repeat, l]:
            return isEmpty(l)

        match _:
            return false

def trees(l):
    switch (l):
        match ==nullSet:
            return [null]
        match [==term, ts]:
            return ts
        match [==reduction, inner, f]:
            var rv := []
            def ts := trees(inner)
            for tree in ts:
                rv += f(tree)
            return rv
        match [==alternation, ls]:
            var ts := []
            for l in ls:
                ts += trees(l)
            return ts
        match [==catenation, a, b]:
            def ts := [].diverge()
            for x in trees(a):
                for y in trees(b):
                    ts.push([x, y])
            return ts.snapshot()
        match [==repeat, _]:
            return [null]

        match _:
            return []

def _leaders(l):
    switch (l):
        match ==nullSet:
            return [null]
        match [==term, _]:
            return [null]

        match ==anything:
            return [anything]
        match [==exactly, c]:
            return [c]

        match [==reduction, inner, _]:
            return _leaders(inner)

        match [==alternation, ls]:
            var rv := []
            for inner in ls:
                rv += _leaders(inner)
            return rv

        match [==catenation, a ? nullable(a), b]:
            if (onlyNull(a)):
                return _leaders(b)
            else:
                return _leaders(a) + _leaders(b)
        match [==catenation, a, b]:
            return _leaders(a)

        match [==repeat, l]:
            return [null] + _leaders(l)

        match _:
            return []

def _filterEmpty(xs):
    return [x for x in xs if x != empty]

def derive(l, c):
    switch (l):
        match x ? isEmpty(x):
            return empty

        match ==nullSet:
            return empty
        match [==term, _]:
            return empty

        match ==anything:
            return [term, [c]]
        match [==exactly, ==c]:
            return [term, [c]]
        match [==exactly, _]:
            return empty

        match [==reduction, inner, f]:
            return [reduction, derive(inner, c), f]
        match [==alternation, ls]:
            return [alternation, _filterEmpty([derive(l, c) for l in ls])]

        match [==catenation, a ? nullable(a), b]:
            def da := derive(a, c)
            def db := derive(b, c)
            return [alternation,
                [[catenation, da, b],
                 [catenation, [term, trees(a)], db]]]
        match [==catenation, a, b]:
            return [catenation, derive(a, c), b]

        match [==repeat, l]:
            return [catenation, derive(l, c), [repeat, l]]

        match _:
            return empty

def doCompact(l, i):
    if (i <= 0):
        return l

    def j := i - 1

    switch (l):
        match [==reduction, x ? isEmpty(x), _]:
            return empty
        match [==reduction, inner ? onlyNull(inner), f]:
            var reduced := []
            for tree in trees(inner):
                reduced += f(tree)
            return [term, reduced]

        match [==reduction, [==reduction, inner, f], g]:
            def compose(x):
                var rv := []
                for item in f(x):
                    rv += g(item)
                return rv
            return [reduction, doCompact(inner, j), compose]

        match [==reduction, inner, f]:
            return [reduction, doCompact(inner, j), f]

        match [==alternation, ls]:
            def compacted := _filterEmpty([doCompact(l, j) for l in ls])
            switch (compacted):
                match []:
                    return empty
                match [inner]:
                    return inner
                match x:
                    return [alternation, x]

        match [==catenation, a ? onlyNull(a), b]:
            def xs := trees(a)
            def curry(y):
                def ts := [].diverge()
                for x in xs:
                    ts.push([x, y])
                return ts.snapshot()
            return [reduction, doCompact(b, j), curry]

        match [==catenation, a, b]:
            if (isEmpty(a) | isEmpty(b)):
                return empty
            return [catenation, doCompact(a, j), doCompact(b, j)]

        match [==repeat, x ? isEmpty(x)]:
            return [term, [null]]

        match [==repeat, inner]:
            return [repeat, doCompact(inner, j)]

        match _:
            return l

def compact(l):
    return doCompact(l, 30)

def testEmpty(assert):
    def testEmptyDerive():
        assert.equal(derive(empty, 'x'), empty)
    return [
        testEmptyDerive,
    ]

def testExactly(assert):
    def testExactlyDerive():
        assert.equal(trees(derive([exactly, 'x'], 'x')), ['x'])
    return [
        testExactlyDerive,
    ]

def testReduce(assert):
    def plusOne(x):
        return [x + 1]
    def testReduceDerive():
        assert.equal(trees(derive([reduction, [exactly, 'x'], plusOne], 'x')), ['y'])
    return [
        testReduceDerive,
    ]

def testAlternation(assert):
    def testAlternationOptimization():
        def l := [alternation, [empty]]
        assert.equal(compact(l), empty)
    def testAlternationPair():
        def l := [alternation, [[exactly, 'x'], [exactly, 'y']]]
        assert.equal(trees(derive(l, 'x')), ['x'])
        assert.equal(trees(derive(l, 'y')), ['y'])
    def testAlternationMany():
        def l := [alternation, [[exactly, 'x'], [exactly, 'y'], [exactly, 'z']]]
        assert.equal(trees(derive(l, 'x')), ['x'])
        assert.equal(trees(derive(l, 'y')), ['y'])
        assert.equal(trees(derive(l, 'z')), ['z'])
        assert.equal(trees(derive(l, 'w')), [])
    return [
        testAlternationOptimization,
        testAlternationPair,
        testAlternationMany,
    ]

def testCatenation(assert):
    def testCatenationCompactEmpty():
        def l := [catenation, empty, [exactly, 'x']]
        assert.equal(compact(l), empty)
    def testCatenationCompactNull():
        def l := [catenation, [term, ['x']], [term, ['y']]]
        assert.equal(trees(compact(l)), [['x', 'y']])
    def testCatenationDerive():
        def l := [catenation, [exactly, 'x'], [exactly, 'y']]
        assert.equal(trees(derive(derive(l, 'x'), 'y')), [['x', 'y']])
    return [
        testCatenationCompactEmpty,
        testCatenationCompactNull,
        testCatenationDerive,
    ]

def testRepeat(assert):
    def testRepeatNull():
        def l := [repeat, [exactly, 'x']]
        assert.equal(true, nullable(l))
        assert.equal(false, onlyNull(l))
    def testRepeatDerive():
        def l := [repeat, [exactly, 'x']]
        assert.equal(trees(derive(l, 'x')), [['x', null]])
        assert.equal(trees(derive(derive(l, 'x'), 'x')), [['x', ['x', null]]])
    return [
        testRepeatDerive,
    ]

def replaceValues(language, values):
    switch (language):
        match [==value, index]:
            return [exactly, values[index]]
        match [tag] + inner:
            return [tag] + [replaceValues(l, values) for l in inner]
        match x:
            return x

def _pureToList(f):
    def listWrapper(x):
        return [f(x)]
    return listWrapper

def makeDerp(language):
    return object parser:
        to unwrap():
            return language

        # Monte core methods.

        to _printOn(out):
            out.print(`Parser (${parserSize(language)}): `)
            return showParser(language, out)

        # EDSL wrapper methods.

        to add(other):
            # Addition is catenation.
            return makeDerp([catenation, language, other.unwrap()])

        to or(other):
            # Alternation.
            return makeDerp([alternation, [language, other.unwrap()]])

        to remainder(other):
            # Inspired by lens, which uses `%` for its modification/map API.
            # Their mnemonic is *mod*ification, for *mod*ulus. However, Monte
            # uses `%%` for modulus and `%` for remainder. We choose the
            # latter in order to avoid any accidental expMod() conversions and
            # also to improve readability.
            return makeDerp([reduction, language, _pureToList(other)])

        to modulus(other):
            # Okay, I lied. This is a way to craft a reduction that does raw
            # things and directly returns however many items it desires.
            return makeDerp([reduction, language, other])

        to repeated():
            # Repeat!
            return makeDerp([repeat, language])

        # Parser API.

        to leaders():
            # return _leaders(language).asSet()
            return _leaders(language)

        to feed(c):
            traceln(`Leaders: ${parser.leaders()}`)
            traceln(`Character: $c`)
            def l := compact(derive(language, c))
            def p := makeDerp(l)
            if (isEmpty(l)):
                traceln("Language is empty!")
            # traceln("Compacted: " + M.toString(p))
            return p

        to feedMany(cs):
            var p := parser
            for c in cs:
                p feed= c
            return p

        to results():
            return trees(language)

        # QL value support.

        to substitute(values):
            return makeDerp(replaceValues(language, values))

def ex(x):
    return makeDerp([exactly, x])

def testParse(parser, input):
    def derp := parser.feedMany(input)
    def rv := derp.results()
    traceln(`$rv`)
    return rv

def [
    "oneOrMore" => oneOrMore,
    "justFirst" => justFirst,
    "justSecond" => justSecond,
    "bracket" => bracket
] | _ := import("derp.combiners")

def repToList(l):
    var reps := l
    def rv := [].diverge()
    while (reps != null):
        rv.push(reps[0])
        reps := reps[1]
    return rv.snapshot()

def number := oneOrMore(makeDerp([alternation, [[exactly, c] for c in "0123456789"]])) % def toNumber(x) { return atoi(repToList(x)) }

def testNumber(assert):
    def testNumberSimple():
        assert.equal(testParse(number, "42"), [42])
    return [
        testNumberSimple,
    ]

def parseValue := justSecond(ex('$'), bracket(ex('{'), number, ex('}'))) % def _(x) { return [value, x] }

def testParseValue(assert):
    def testParseValueSimple():
        assert.equal(testParse(parseValue, "${10}"), [[value, 10]])
    return [
        testParseValueSimple,
    ]

def oneOf(xs):
    return makeDerp([alternation, [[exactly, x] for x in xs]])

def catTree(ls):
    switch (ls):
        match [x, ==null]:
            return x
        match [x, y]:
            return x + catTree(y)
        match x:
            return x

def character := oneOf("xyz")

def charSet := bracket(ex('['), character.repeated() % repToList, ex(']'))

def anyChar := ex('.') % def _(_) { return makeDerp(anything) }

def singleItem := character % ex | charSet % oneOf | anyChar | parseValue % makeDerp

def itemMaybe := justFirst(singleItem, ex('?')) % def interro(x) { return x | makeDerp(nullSet) }

def itemStar := justFirst(singleItem, ex('*')) % def star(x) { return x.repeated() }

def item := itemStar | itemMaybe | singleItem

def regex := item.repeated() % catTree

object derp__quasiParser:
    to valueMaker(template):
        def p := testParse(regex, template)[0]
        return makeDerp(p)

def unittest := import("unittest")

unittest([
    testEmpty,
    testExactly,
    testReduce,
    testAlternation,
    testCatenation,
    testRepeat,
    testNumber,
    testParseValue,
])

def w := 'w'
def z := 'z'

def p := derp`${w}x${z}y${w}`.feedMany("wxzyw")
traceln(`${p.results()}`)

var xyzzy := null

for expr in ["x*y*z*y*", "[xyz]*", "x.z..", "xyzzy?"]:
    traceln("~~~~~")
    xyzzy := testParse(regex, expr)[0]
    traceln("~~~~~")
    testParse(xyzzy, "xyzzy")
