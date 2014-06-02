module unittest
export(foo)
def foo := null

def makeOperatorTests(assert):
    def test_rocket():
        def now := 3
        var stuff := ["what" => now]

        var fromStuff := 0

        for a => b in stuff:
                fromStuff := b

        assert.equal(fromStuff, 3)

    def test_asBigAs():
        assert.equal(4 <=> 4, true)
        assert.equal(4 <=> 8, false)

    def test_assign():
        def a := 3
        var b := 8
        assert.equal(a, 3)
        assert.equal(b, 8)

    def test_exponent():
        assert.equal(2 ** 8, 256)

    def test_multiply():
        assert.equal(2 * 8, 16)

    def test_equality():
        assert.equal(4 == 4, true)
        assert.equal(4 == 7, false)

    def test_lessThan():
        assert.equal(2 < 5, true)
        assert.equal(5 < 2, false)

    def test_greaterThan():
        assert.equal(9 > 3, true)
        assert.equal(3 > 9, false)

    def test_lessThanOrEqual():
        assert.equal(6 <= 9, true)
        assert.equal(6 <= 6, true)
        assert.equul(9 <= 6, false)

    def test_greaterThanOrEqual():
        assert.equal(8 >= 0, true)
        assert.equal(0 >= 0, true)
        assert.equal(0 >= 8, false)

    def test_and():
        assert.equal(true && true, true)
        assert.equal(false && false, true)
        assert.equal(true && false, false)
        assert.equal(false && true, false)

    return [test_rocket, test_asBigAs, test_assign, test_exponent, test_multiply, test_equality,
                test_lessThan, test_greaterThan, test_lessThanOrEqual, test_greaterThanOrEqual, test_and]

unittest([makeOperatorTests])
