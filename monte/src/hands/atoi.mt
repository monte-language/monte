def atoi(var cs) :int implements DeepFrozen:
    def neg := cs[0] == '-'
    if (neg):
        cs := cs.slice(1)

    def ns := [c.asInteger() - 48 for c in cs]
    var rv := 0
    for n in ns:
        rv := rv * 10 + n
    if (neg):
        rv *= -1
    return rv

def testAToI(assert):
    def testLUE():
        assert.equal(atoi("42"), 42)

    def testNegative():
        assert.equal(atoi("-42"), -42)

    return [
        testLUE,
        testNegative,
    ]

def unittest := import("unittest")

unittest([
    testAToI,
])

atoi
