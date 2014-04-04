def fold := import("hands.fold")
def unittest := import("unittest")

def testFold(assert):
    def adder(x, y):
        return x + y

    def first(x, y):
        return x

    def second(x, y):
        return y

    def testFoldlSimple():
        assert.equal(fold.foldl(adder, 0, [1, 2, 3, 4, 5]), 15)

    def testFoldlOrdered():
        assert.equal(fold.foldl(second, 0, [1, 2, 3, 4, 5]), 5)

    def testFoldrSimple():
        assert.equal(fold.foldr(adder, 0, [1, 2, 3, 4, 5]), 15)

    def testFoldrOrdered():
        assert.equal(fold.foldr(first, 0, [1, 2, 3, 4, 5]), 1)

    return [
        testFoldlSimple,
        testFoldlOrdered,
        testFoldrSimple,
        testFoldrOrdered,
    ]

unittest([
    testFold,
])
