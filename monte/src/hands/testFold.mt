def fold := import("hands.fold")
def unittest := import("unittest")

def testFold(assert):

    def testFoldl():
        def adder(x, y):
            return x + y

        assert.equal(fold.foldl(adder, 0, [1, 2, 3, 4, 5]), 15)

    return [
        testFoldl,
    ]

unittest([
    testFold,
])
