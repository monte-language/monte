def makeRegion(bottom, top):
    return object region:
        to run(item) :boolean:
            if (item >= bottom & item <= top):
                return true
            return false

        to iterate():
            def rv := [].diverge()
            var b := bottom
            while (b <= top):
                rv.push(b)
                b := b.next()
            return rv.snapshot()

object __makeOrderedSpace:
    to op__thru(left, right):
        return makeRegion(left, right)
    to op__till(left, right):
        return makeRegion(left, right.previous())

def testRegions(assert):
    def thru():
        assert.equal((0..3)(1), true)
        assert.equal((0..3)(-1), false)
        assert.equal((0..3)(4), false)
    def thruIterate():
        assert.equal((0..3).iterate(), [0, 1, 2, 3])
    def tillIterate():
        assert.equal((0..!3).iterate(), [0, 1, 2])
    return [
        thru,
        thruIterate,
        tillIterate,
    ]

def unittest := import("unittest")
unittest([
    testRegions,
])
