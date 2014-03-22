def atoi(cs) :int:
    def ns := [c.asInteger() - 48 for c in cs]
    var rv := 0
    for n in ns:
        rv := rv * 10 + n
    return rv

def testAToI(assert):
    def testLUE():
        assert.equal(atoi("42"), 42)
    return [
        testLUE,
    ]

def unittest := import("unittest")

unittest([
    testAToI,
])

atoi
