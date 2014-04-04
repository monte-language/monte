def [_any, _all] := import("anyAll")
def atoi := import("atoi")

def _glueReps([x, xs]):
    if (xs == null):
        return [x]
    return [x] + xs

def concatMap(f):
    def concatMapper(xss):
        def rv := [].diverge()
        for xs in xss:
            for x in xs:
                rv.push(f(x))
        return rv.snapshot()
    return concatMapper

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
    def rv := [].diverge()
    for x in xs:
        if (x != empty):
            rv.push(x)
    return rv.snapshot()

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
                return concatMap(g)(f(x))
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
            traceln(`xs $xs`)
            def curry(y):
                def ts := [].diverge()
                traceln(`y $y`)
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
    # traceln(`replace $language $values`)
    switch (language):
        match [==value, index]:
            return [exactly, values[index]]
        match [tag] + inner:
            return [tag] + [replaceValues(l, values) for l in inner]
        match x:
            return x

def makeDerp(language):
    return object parser:
        to unwrap():
            return language

        to _printOn(out):
            return showParser(language, out)

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
            traceln("Compacted: " + M.toString(p))
            return p

        to feedMany(cs):
            var p := parser
            for c in cs:
                p feed= c
            return p

        to results():
            return trees(language)

        to substitute(values):
            traceln(`Substituting values: $values`)
            return makeDerp(replaceValues(language, values))

def testParse(parser, input):
    def derp := makeDerp(parser).feedMany(input)
    def rv := derp.results()
    traceln(`$rv`)
    return rv

def justFirst(x, y):
    return [reduction, [catenation, x, y], def _([x, y]) { return [x] }]

def justSecond(x, y):
    return [reduction, [catenation, x, y], def _([x, y]) { return [y] }]

def oneOrMore(l):
    return [catenation, l, [repeat, l]]

def repToList(l):
    var reps := l
    def rv := [].diverge()
    while (reps != null):
        rv.push(reps[0])
        reps := reps[1]
    return [rv.snapshot()]

def number := [reduction,
    oneOrMore([alternation, [[exactly, c] for c in "0123456789"]]),
    def toNumber(x) { return [atoi(i) for i in repToList(x)] }]

def testNumber(assert):
    def testNumberSimple():
        assert.equal(testParse(number, "42"), [42])
    return [
        testNumberSimple,
    ]

def bracket(bra, x, ket):
    return justSecond(bra, justFirst(x, ket))

def parseValue := [reduction,
     justSecond([exactly, '$'],
        bracket([exactly, '{'], number, [exactly, '}'])),
     def _(x) { return [[value, x]] }]

def testParseValue(assert):
    def testParseValueSimple():
        assert.equal(testParse(parseValue, "${10}"), [[value, 10]])
    return [
        testParseValueSimple,
    ]

def oneOf(xs):
    return [alternation, [[exactly, x] for x in xs]]

def catTree(ls):
    switch (ls):
        match [x, ==null]:
            return [x]
        match [x, y]:
            return [[catenation, x, catTree(y)]]
        match x:
            return [x]

def character := oneOf("xyz")

def charSet := bracket([exactly, '['],
    [reduction, [repeat, character], repToList],
    [exactly, ']'])

def anyChar := [reduction, [exactly, '.'], def _(_) { return [anything] }]

def singleItem := [alternation, [
    [reduction, character, def c(x) { return [[exactly, x]] }],
    [reduction, charSet, def _(x) { return [oneOf(x)] }],
    anyChar,
    parseValue]]

def itemMaybe := [reduction, justFirst(singleItem, [exactly, '?']),
    def interro(x) { return [[alternation, [x, nullSet]]] }]

def itemStar := [reduction, justFirst(singleItem, [exactly, '*']),
    def star(x) { return [[repeat, x]] }]

def item := [alternation, [itemStar, itemMaybe, singleItem]]

def regex := [reduction, [repeat, item], catTree]

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
