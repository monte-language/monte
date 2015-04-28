module unittest
export (makeMaths)
def makeMaths(a :Int, b :Int):
    return object Maths:
        to add() :Int:
            return a + b
        to subtract() :Int:
            return a - b

def mathTests(assert):
    def testAddPositive():
        def mth := makeMaths(1, 2)
        assert.equal(mth.add(), 3)
    def testAddNegative():
        def mth := makeMaths(-1, -1)
        assert.equal(mth.add(), -2)
    def testSubtract():
        def mth := makeMaths(3, 2)
        assert.equal(mth.subtract(), 1)
    def testSubtractNegative():
        def mth := makeMaths(3, -2)
        assert.equal(mth.subtract(), 5)
    return [testAddPositive, testAddNegative, testSubtract,
            testSubtractNegative]

unittest([mathTests])
