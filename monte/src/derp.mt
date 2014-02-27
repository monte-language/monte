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

object empty:
    to _uncall():
        return "empty"
    to derive(c):
        return empty
    to isEmpty() :bool:
        return true
    to nullable() :bool:
        return false
    to onlyNull() :bool:
        return false
    to trees():
        return []

def testEmpty(assert):
    def testEmptyDerive():
        assert.equal(empty.derive('x'), empty)
    return [
        testEmptyDerive,
    ]

object nullSet:
    to _uncall():
        return "nullSet"
    to derive(c):
        return empty
    to isEmpty() :bool:
        return false
    to nullable() :bool:
        return true
    to onlyNull() :bool:
        return true
    to trees():
        return [null]

def term(ts):
    return object o:
        to _uncall():
            return `term($ts)`
        to derive(c):
            return empty
        to isEmpty() :bool:
            return false
        to nullable() :bool:
            return true
        to onlyNull() :bool:
            return true
        to trees():
            return ts

object anything:
    to _uncall():
        return "anything"
    to derive(c):
        return term([c])
    to isEmpty() :bool:
        return false
    to nullable() :bool:
        return false
    to onlyNull() :bool:
        return false
    to trees():
        return []

def ex(t):
    return object exInner:
        to _uncall():
            return `ex($t)`
        to derive(c):
            if (t == c):
                return term([t])
            else:
                return empty
        to isEmpty() :bool:
            return false
        to nullable() :bool:
            return false
        to onlyNull() :bool:
            return false
        to trees():
            return []

def testExactly(assert):
    def testExactlyDerive():
        assert.equal(ex('x').derive('x').trees(), ['x'])
    return [
        testExactlyDerive,
    ]

def oneOf(ts):
    return object oneOfInner:
        to _uncall():
            return `oneOf($ts)`
        to derive(c):
            return term([t for t in ts if t == c])
        to isEmpty() :bool:
            return false
        to nullable() :bool:
            return false
        to onlyNull() :bool:
            return false
        to trees():
            return []

def testOneOf(assert):
    def testOneOfDerive():
        def l := oneOf(['x', 'y'])
        assert.equal(l.derive('x').trees(), ['x'])
        assert.equal(l.derive('y').trees(), ['y'])
    def testOneOfPolymorphic():
        def l := oneOf("xy")
        assert.equal(l.derive('x').trees(), ['x'])
        assert.equal(l.derive('y').trees(), ['y'])
    return [
        testOneOfDerive,
        testOneOfPolymorphic,
    ]

def red(l, f):
    return object redInner:
        to _uncall():
            return "red(" + l._uncall() + `, $f)`
        to derive(c):
            def d := l.derive(c)
            if (d.isEmpty()):
                return empty
            if (d.onlyNull()):
                return term([f(t) for t in d.trees()])
            return red(d, f)
        to isEmpty() :bool:
            return l.isEmpty()
        to nullable() :bool:
            return l.nullable()
        to onlyNull() :bool:
            return l.onlyNull()
        to trees():
            return [f(t) for t in l.trees()]

def testReduce(assert):
    def plusOne(x):
        return x + 1
    def testReduceDerive():
        assert.equal(red(ex('x'), plusOne).derive('x').trees(), ['y'])
    return [
        testReduceDerive,
    ]

def _all(l):
    var rv := true
    for x in l:
        rv &= x
    return rv

def _any(l):
    var rv := false
    for x in l:
        rv |= x
    return rv

def alt(languages):
    def ls := [l for l in languages if l != empty]
    if (ls.size() == 0):
        return empty
    if (ls.size() == 1):
        return ls.get(0)
    return object altInner:
        to _uncall():
            var buf := "alt("
            for l in ls:
                buf += l._uncall()
                buf += ", "
            return buf + ")"
        to derive(c):
            return alt([l.derive(c) for l in ls])
        to isEmpty() :bool:
            return _all([l.isEmpty() for l in ls])
        to nullable() :bool:
            return _any([l.nullable() for l in ls])
        to onlyNull() :bool:
            return _all([l.onlyNull() for l in ls])
        to trees():
            var ts := []
            for l in ls:
                ts += l.trees()
            return ts

def testAlternation(assert):
    def testAlternationOptimization():
        var l := alt([empty])
        assert.equal(l, empty)
    def testAlternationPair():
        def l := alt([ex('x'), ex('y')])
        assert.equal(l.derive('x').trees(), ['x'])
        assert.equal(l.derive('y').trees(), ['y'])
    def testAlternationMany():
        def l := alt([ex('x'), ex('y'), ex('z')])
        assert.equal(l.derive('x').trees(), ['x'])
        assert.equal(l.derive('y').trees(), ['y'])
        assert.equal(l.derive('z').trees(), ['z'])
        assert.equal(l.derive('w').trees(), [])
    return [
        testAlternationOptimization,
        testAlternationPair,
        testAlternationMany,
    ]

def cat(a, b):
    if (a.isEmpty()):
        return empty
    if (b == empty):
        return empty
    return object catInner:
        to _uncall():
            return "cat(" + a._uncall() + ", " + b._uncall() + ")"
        to derive(c):
            def da := a.derive(c)
            def l := cat(da, b)
            if (a.nullable()):
                def db := b.derive(c)
                return alt([l, cat(term(a.trees()), db)])
            return l
        to isEmpty() :bool:
            return a.isEmpty() | b.isEmpty()
        to nullable() :bool:
            return a.nullable() & b.nullable()
        to onlyNull() :bool:
            return a.onlyNull() & b.onlyNull()
        to trees():
            def l := [].diverge()
            for x in a.trees():
                for y in b.trees():
                    l.push([x, y])
            return l.readOnly()

def testCatenation(assert):
    def testCatenationDerive():
        def l := cat(ex('x'), ex('y'))
        assert.equal(l.derive('x').derive('y').trees(), [['x', 'y']])
    return [
        testCatenationDerive,
    ]

def _glueReps([x, xs]):
    if (xs == null):
        return [x]
    return [x] + xs

def rep(l):
    if (l == empty):
        return empty
    object repInner:
        to _uncall():
            return "rep(" + l._uncall() + ")"
        to derive(c):
            return red(cat(l.derive(c), rep(l)), _glueReps)
        to isEmpty() :bool:
            return l.isEmpty()
        to nullable() :bool:
            return true
        to onlyNull() :bool:
            return false
        to trees():
            return [null]
    return repInner

def testRepeat(assert):
    def testRepeatDerive():
        def l := rep(ex('x'))
        assert.equal(l.derive('x').trees(), [['x']])
        assert.equal(l.derive('x').derive('x').trees(), [['x', 'x']])
    return [
        testRepeatDerive,
    ]

def parse(language, cs):
    var l := language
    for c in cs:
        traceln(`Character: $c`)
        l := l.derive(c)
        if (l.isEmpty()):
            traceln("Language is empty!")
    return l.trees()

def dump(language):
    traceln(language._uncall())

def unittest := import("unittest")

unittest([
    testEmpty,
    testExactly,
    testOneOf,
    testReduce,
    testAlternation,
    testCatenation,
    testRepeat,
])

dump(rep(alt([ex('x'), ex('y')])))

traceln(parse(rep(alt([ex('x'), ex('y')])), "xxyyxy"))
