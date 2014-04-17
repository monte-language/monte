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

        to _makeIterator():
            var i := 0
            var poz := bottom
            return object regionIterator:
                to next(ej):
                    if (poz <= top):
                        def result := [i, poz]
                        i += 1
                        poz := poz.next()
                        return result
                    else:
                        throw.eject(ej, "iteration done")

        to descending():
            var i := 0
            var pos := top
            return object descender:
                to _makeIterator():
                    return object regionIteratorDesc:
                        to next(ej):
                            if (pos >= bottom):
                                def result := [i, pos]
                                i += 1
                                pos := pos.previous()
                                return result
                            else:
                                throw.eject(ej, "iteration done")

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

def _id(k, i, _):
    return i

def asList(x):
    return __accumulateList(x, _id)

def testRegions(assert):
    def thru():
        assert.equal((0..3)(1), true)
        assert.equal((0..3)(-1), false)
        assert.equal((0..3)(4), false)

    def thruCoerce():
        def x :(0..!5) := 3
        assert.equal(x, 3)

    def thruCoerceFailure():
        assert.ejects(def _(ej, fail) {
            def x :(0..!5) exit ej := 42
            fail("Guard did not fail")
        })

    def thruIterate():
        assert.equal(asList(0..3), [0, 1, 2, 3])

    def tillIterate():
        assert.equal(asList(0..!3), [0, 1, 2])

    def thruDescending():
        assert.equal(asList((0..3).descending()), [3, 2, 1, 0])

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
        thruCoerceFailure,
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
