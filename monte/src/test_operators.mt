module unittest

def makeOperatorTests(assert):
    def test_op_rocket():
        def ar := [1,3]
        var change_me := 0

        for a => b in ar:
            change_me := b

        assert.equal(change_me, 3)

    def test_op_asBigAs():
        assert.equal(4 <=> 4, true)
        assert.equal(4 <=> 8, false)

    def test_op_assign():
        def a := 3
        var b := 8
        assert.equal(a, 3)
        assert.equal(b, 8)

    def test_op_exponent():
        assert.equal(2 ** 8, 256)

    def test_op_multiply():
        assert.equal(2 * 8, 16)

    def test_op_equality():
        assert.equal(4 == 4, true)
        assert.equal(4 == 7, false)

    def test_op_lessThan():
        assert.equal(2 < 5, true)
        assert.equal(5 < 2, false)

    def test_op_greaterThan():
        assert.equal(9 > 3, true)
        assert.equal(3 > 9, false)

    def test_op_lessThanOrEqual():
        assert.equal(6 <= 9, true)
        assert.equal(6 <= 6, true)
        assert.equul(9 <= 6, false)

    def test_op_greaterThanOrEqual():
        assert.equal(8 >= 0, true)
        assert.equal(0 >= 0, true)
        assert.equal(0 >= 8, false)

    def test_op_and():
        assert.equal(true && true, true)
        assert.equal(false && false, true)
        assert.equal(true && false, false)
        assert.equal(false && true, false)

    return [test_op_rocket, test_op_asBigAs, test_op_assign, test_op_exponent, test_op_multiply, test_op_equality,
                test_op_lessThan, test_op_greaterThan, test_op_lessThanOrEqual, test_op_greaterThanOrEqual, test_op_and]

unittest([makeOperatorTests])
