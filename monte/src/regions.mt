def makeRegion(bottom, top):
    return object region:
        to run(item) :boolean:
            if (item >= bottom && item <= top):
                return true
            return false

        to coerce(specimen, ej):
            if (region(specimen)):
                return specimen
            else:
                throw.eject(ej, `Not in region: $specimen`)

        to iterate():
            def rv := [].diverge()
            var b := bottom
            while (b <= top):
                rv.push(b)
                b := b.next()
            return rv.snapshot()

        to descending():
            def rv := [].diverge()
            var t := top
            while (t >= bottom):
                rv.push(t)
                t := t.previous()
            return rv.snapshot()

        to add(var amount):
            var b := bottom
            var t := top
            while ((amount -= 1) >= 0):
                b := b.next()
                t := t.next()
            return makeRegion(b, t)

        to subtract(var amount):
            var b := bottom
            var t := top
            while ((amount -= 1) >= 0):
                b := b.previous()
                t := t.previous()
            return makeRegion(b, t)


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

    def thruCoerce():
        def x :(0..!5) := 3
        assert.equal(x, 3)

    def thruIterate():
        assert.equal((0..3).iterate(), [0, 1, 2, 3])

    def tillIterate():
        assert.equal((0..!3).iterate(), [0, 1, 2])

    def thruDescending():
        assert.equal((0..3).descending(), [3, 2, 1, 0])

    def thruAdd():
        def region := (0..3) + 3
        assert.equal(region(4), true)
        assert.equal(region(0), false)

    def thruSubtract():
        def region := (0..3) - 3
        assert.equal(region(-1), true)
        assert.equal(region(2), false)

    return [
        thru,
        thruCoerce,
        thruIterate,
        tillIterate,
        thruDescending,
        thruAdd,
        thruSubtract,
    ]

def unittest := import("unittest")
unittest([
    testRegions,
])

__makeOrderedSpace
