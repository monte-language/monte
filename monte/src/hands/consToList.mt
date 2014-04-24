def consToList(var cons) implements DeepFrozen:
    var rv := []
    while (cons != null):
        rv with= cons[0]
        cons := cons[1]
    return rv.snapshot()

def testConsToList(assert):
    def test():
        assert.equal(consToList([1, [2, [3, null]]]), [1, 2, 3])
    return [test]

def unittest := import("unittest")

unittest([
    testConsToList,
])

consToList
