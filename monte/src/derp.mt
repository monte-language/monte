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
    object o:
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
    return o

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
    object exInner:
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
    return exInner

def testExactly(assert):
    def testExactlyDerive():
        assert.equal(ex('x').derive('x').trees(), ['x'])
    return [
        testExactlyDerive,
    ]

def red(l, f):
    object redInner:
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
    return redInner

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
    object altInner:
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
    return altInner

def cat(a, b):
    object catInner:
        to derive(c):
            if (a.isEmpty()):
                return empty
            if (b == empty):
                return empty
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
                    l.append([x, y])
            return l
    return catInner

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

def parse(language, cs):
    var l := language
    for c in cs:
        traceln(`Character: $c`)
        l := l.derive(c)
        if (l.isEmpty()):
            traceln("Language is empty!")
    return l.trees()

# throw("abort")
traceln("~~~")
traceln(parse(ex('x'), "x"))
traceln("~~~")
traceln(parse(alt(ex('x'), ex('y')), "x"))
traceln("~~~")
traceln(parse(alt(ex('x'), ex('y')), "y"))
traceln("~~~")
traceln(parse(cat(ex('x'), ex('y')), "xy"))
traceln("~~~")
traceln(parse(rep(ex('x')), "xxx"))


object unitTestAssertions:
    to equal(left, right):
        if (left != right):
            throw(`assertion failure: $left != $right`)
    to inequal(left, right):
        if (left == right):
            throw(`assertion failure: $left == $right`)

def runTests(suites):
    for s in suites:
        traceln(`testing suite $s`)
        def tests := s(unitTestAssertions)
        for t in tests:
            traceln(`$t`)
            t()

runTests([
    testEmpty,
    testExactly,
    testReduce,
])
