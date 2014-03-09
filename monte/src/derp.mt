object bool:
    to coerce(x, ejector) :any:
        if (x == true | x == false):
            return x
        else:
            throw.eject(ejector, "Must be a bool")
    to MakeSlot(x :bool) :any:
        var v := x
        object slot:
            to getValue():
                return v
            to setValue(x :bool):
                return v := x
        return slot

def _all(l):
    var rv :bool := true
    for x in l:
        rv &= x
    return rv

def _any(l):
    var rv :bool := false
    for x in l:
        rv |= x
    return rv

def _glueReps([x, xs]):
    if (xs == null):
        return [x]
    return [x] + xs

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

def _join(xs, glue):
    def l := xs.diverge()
    def end := l.pop()
    var out := ""
    for x in l:
        out += x
        out += glue
    return out + end

def showParser(l):
    switch (l):
        match ==empty:
            return "empty"
        match ==nullSet:
            return "null"
        match ==anything:
            return "any"

        match [==term, ts]:
            return `term($ts)`
        match [==exactly, t]:
            return `ex($t)`
        match [==reduction, inner, f]:
            return "red(" + showParser(inner) + `, $f)`
        match [==alternation, ls]:
            return "alt([" + _join([showParser(l) for l in ls], ", ") + "])"
        match [==catenation, a, b]:
            return "cat(" + showParser(a) + ", " + showParser(b) + ")"
        match [==repeat, l]:
            return "rep(" + showParser(l) + ")"

        match _:
            return `$l`

def onlyNull(l) :bool:
    switch (l):
        match ==nullSet:
            return true
        match [==term, _]:
            return true

        match [==reduction, inner]:
            return onlyNull(inner)
        match [==alternation, ls]:
            return _all([onlyNull(l) for l in ls])
        match [==catenation, a, b]:
            return onlyNull(a) & onlyNull(b)

        match _:
            return false

def nullable(l) :bool:
    if (onlyNull(l)):
        return true

    switch (l):
        match [==reduction, inner]:
            return nullable(inner)
        match [==alternation, ls]:
            return _any([nullable(l) for l in ls])
        match [==catenation, a, b]:
            return nullable(a) & nullable(b)

        match [==repeat, _]:
            return true

        match _:
            return false

def isEmpty(l) :bool:
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
            return [f(t) for t in trees(inner)]
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

def derive(l, c):
    switch (l):
        match ==empty:
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
            return [alternation, [derive(l, c) for l in ls]]

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
        match [==reduction, ==empty, _]:
            return empty
        match [==reduction, inner ? onlyNull(inner), f]:
            return [term, [f(t) for t in trees(inner)]]

        match [==alternation, []]:
            return empty
        match [==alternation, [inner]]:
            return inner
        match [==alternation, ls]:
            return doCompact([alternation,
                [doCompact(l, j) for l in ls if l != empty]], j)

        match [==catenation, l ? isEmpty(l), _]:
            return empty
        match [==catenation, _, ==empty]:
            return empty

        match [==catenation, a, b]:
            return doCompact([catenation, doCompact(a, j), doCompact(b, j)], j)

        match [==repeat, ==empty]:
            return empty

        match _:
            return l

def compact(l):
    return doCompact(l, 7)

traceln("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

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
        return x + 1
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
    def testCatenationDerive():
        def l := [catenation, [exactly, 'x'], [exactly, 'y']]
        assert.equal(trees(derive(derive(l, 'x'), 'y')), [['x', 'y']])
    return [
        testCatenationDerive,
    ]

def testRepeat(assert):
    def testRepeatDerive():
        def l := [repeat, [exactly, 'x']]
        assert.equal(trees(derive(l, 'x')), [['x', null]])
        assert.equal(trees(derive(derive(l, 'x'), 'x')), [['x', ['x', null]]])
    return [
        testRepeatDerive,
    ]

def makeDerp(language):
    var l := language

    traceln("Making parser: " + showParser(l))

    return object parser:
        to show():
            return showParser(l)

        to feed(c):
            traceln(`Character: $c`)
            l := derive(l, c)
            traceln("Now have: " + showParser(l))
            l := compact(l)
            traceln("Compacted: " + showParser(l))
            if (isEmpty(l)):
                traceln("Language is empty!")

        to feedMany(cs):
            for c in cs:
                parser.feed(c)

        to results():
            return trees(l)

def justFirst(x, y):
    return [reduction, [catenation, x, y], def _([x, y]) { return x }]

def justSecond(x, y):
    return [reduction, [catenation, x, y], def _([x, y]) { return y }]

def unittest := import("unittest")

unittest([
    testEmpty,
    testExactly,
    testReduce,
    testAlternation,
    testCatenation,
    testRepeat,
])

def xsys := makeDerp([repeat,
    [alternation, [[exactly, 'x'], [exactly, 'y']]]])

traceln(xsys.show())

xsys.feedMany("xxyyxy")

traceln(`${xsys.results()}`)

# def catTree(ls):
#     switch (ls):
#         match [x, ==null]:
#             return x
#         match [x, y]:
#             return cat(x, catTree(y))
#         match x:
#             return x
#
# def repToList(list):
#     var reps := list
#     def rv := [].diverge()
#     while (reps != null):
#         rv.push(reps.get(0))
#         reps := reps.get(1)
#     return rv.snapshot()
#
# def oneOf := null
#
# def number := rep(oneOf("0123456789"))
# def character := oneOf("xyz")
#
# def charSet := justSecond(ex('['),
#                           justFirst(red(rep(character), repToList), ex(']')))
# def anyChar := red(ex('.'), def _(_) { return anything })
#
# def item := alt([red(character, ex),
#                  red(charSet, oneOf),
#                  anyChar])
# def itemStar := red(justFirst(item, ex('*')), rep)
# def regex := red(rep(itemStar), catTree)
#
# traceln("~~~~~")
# def xyzzy := parse(regex, "x*y*z*y*")
# traceln("~~~~~")
# traceln(parse(xyzzy, "xyzzy"))
#
# traceln("~~~~~")
# def xyzzy2 := parse(regex, "[xyz]*")
# traceln("~~~~~")
# traceln(parse(xyzzy2, "xyzzy"))
#
# traceln("~~~~~")
# def xyzzy3 := parse(regex, "x.z..")
# traceln("~~~~~")
# traceln(parse(xyzzy3, "xyzzy"))
