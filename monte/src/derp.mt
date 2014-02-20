object bool:
    to coerce(x, ejector) :any:
        if (x == true | x == false):
            return x
        else:
            throw.eject(ejector, "Must be an integer")
    to MakeSlot(x :bool) :any:
        var v := x
        object slot:
            to getValue():
                return v
            to setValue(x :bool):
                return v := x
        return slot

object empty:
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
        to derive(c):
            if (c == t):
                return term([c])
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

def red(l, f):
    return object redInner:
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

def alt(a, b):
    if (a == empty):
        return b
    if (b == empty):
        return a
    return object altInner:
        to derive(c):
            return alt(a.derive(c), b.derive(c))
        to isEmpty() :bool:
            return a.isEmpty() & b.isEmpty()
        to nullable() :bool:
            return a.nullable() | b.nullable()
        to onlyNull() :bool:
            return a.onlyNull() & b.onlyNull()
        to trees():
            return a.trees() + b.trees()

def testAlternation(assert):
    def testAlternationDerive():
        def l := alt(ex('x'), ex('y'))
        # assert.equal(l.derive('x').trees(), ['x'])
        # assert.equal(l.derive('y').trees(), ['y'])
    return [
        testAlternationDerive,
    ]

def cat(a, b):
    if (a.isEmpty()):
        return empty
    if (b == empty):
        return empty
    return object catInner:
        to derive(c):
            def da := a.derive(c)
            def l := cat(da, b)
            if (a.nullable()):
                def db := b.derive(c)
                return alt(l, cat(term(a.trees()), db))
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
        # assert.equal(l.derive('x').derive('y').trees(), ['x', 'y'])
    return [
        testCatenationDerive,
    ]

def rep(l):
    if (l == empty):
        return empty
    object repInner:
        to derive(c):
            return cat(l.derive(c), rep(l))
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
        assert.equal(l.derive('x').trees(), ['x'])
        # assert.equal(l.derive('x').derive('x').trees(), ['x', 'x'])
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


object unitTestAssertions:
    to equal(left, right):
        if (left != right):
            throw(`assertion failure: $left != $right`)
    to inequal(left, right):
        if (left == right):
            throw(`assertion failure: $left == $right`)

def runTests(suites):
    for s in suites:
        traceln(`Testing suite $s`)
        def tests := s(unitTestAssertions)
        for t in tests:
            traceln(`$t`)
            t()
            traceln("Passed!")

runTests([
    testEmpty,
    testExactly,
    testReduce,
    testAlternation,
    testCatenation,
    testRepeat,
])
