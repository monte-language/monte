module unittest
export (OrderedRegionMaker, OrderedSpaceMaker)
def primInt :DeepFrozen := int

/**
 * A min where null represents positive infinity
 */
def min(a, b) as DeepFrozen:
    if (a == null):
        return b
    else if (b == null):
        return a
    else:
        return a.min(b)


/**
 * A max where null represents negative infinity
 */
def max(a, b) as DeepFrozen:
    if (a == null):
        return b
    else if (b == null):
        return a
    else:
        return a.max(b)

/**
 * A get that returns null if index is out of bounds
 */
def get(list, index) as DeepFrozen:
    if (index < 0 || index >= list.size()):
        return null
    else:
        return list[index]

/**
 * Makes inequality-based regions for fully ordered positions like
 * integers, float64s, and chars, where, for every position, there is a
 * 'next()' and 'previous()' operation.

 * If you want similar regions over, for example, Strings or rational numbers,
 * you'd have to do something else.

 * The in edges are members of the region, as are the non-edges
 * immediately following them. The out edges are not in the region, as
 * are the non-edges immediately following them. Therefore, the empty
 * region has args (true, []) while the full region has args
 * (false, [])
 *
 * @param myBoundedLeft If true, then the even egdes are in-edges and the odd
 *                      edges are out-edges. Otherwise, vice verse.
 * @param myEdges is an ascending list of one-dimensional fully ordered
 *                positions.
 * @author Mark S. Miller
 */
object OrderedRegionMaker as DeepFrozen:
    to run(myType :DeepFrozen, myName :str, var initBoundedLeft :boolean, var initEdges):

        /**
         * Notational convenience
         */
        def region(boundedLeft :boolean, edges) as DeepFrozen:
            return OrderedRegionMaker(myType, myName, boundedLeft, edges)


        if (initEdges.size() >= 1 && initEdges[0].previous() <=> initEdges[0]):
            # if the first edge is the least element, get rid of it and
            # flip parity
            initEdges := initEdges(1, initEdges.size())
            initBoundedLeft := !initBoundedLeft

        initEdges := initEdges.snapshot()
        def myInParity :primInt := if (initBoundedLeft) {0} else {1}
        def myLen :primInt := initEdges.size()
        def myTypeR :Same[myType] := myType # for SubrangeGuard audit

        def myBoundedLeft :boolean := initBoundedLeft
        def myEdges :DeepFrozen := initEdges

        /**
         * As guards, regions only accept positions in the region.
         */
        # XXX needs "implements Guard", when that makes sense
        object self implements DeepFrozen, SubrangeGuard[myType], SubrangeGuard[DeepFrozen]:

            /**
             * Returns a ConstList of edge positions in ascending order
             */
            to getEdges():
                return myEdges

            /**
             * mostly prints in Monte sugared expression syntax
             */
            to _printOn(out):
                def printEdge(boundedLeft, edge :myType):
                    out.print("(")
                    out.print(myName)
                    out.print(if (boundedLeft) {" >= "} else {" < "})
                    out.print(edge)
                    out.print(")")

                def printInterval(left :myType, right :myType):
                    out.print(left)
                    out.print("..!")
                    out.print(right)

                if (myLen == 0):
                    if (myBoundedLeft):
                        out.print("<empty ")
                        out.print(myName)
                        out.print(" region>")
                    else:
                        out.print("<full ")
                        out.print(myName)
                        out.print(" region>")

                else if (myLen == 1):
                    printEdge(myBoundedLeft, myEdges[0])
                else:
                    var i := if (myBoundedLeft) {
                        printInterval(myEdges[0], myEdges[1])
                        2
                    } else {
                        printEdge(false, myEdges[0])
                        1
                    }
                    while (i + 1 < myLen):
                        out.print(" | ")
                        printInterval(myEdges[i], myEdges[i+1])
                        i += 2
                    if (i < myLen):
                        out.print(" | ")
                        printEdge(true, myEdges[i])

            /**
             * Is pos in the region?

             * If it's in the type but not in the region, the answer is false.
             * If it's not in the type, a problem is thrown.
             */
            to run(pos :myType) :boolean:
                # XXX linear time algorithm. For long myEdges lists,
                # it should do a binary search.
                for i => edge in myEdges:
                    if (edge > pos):
                        # it's on or above an in edge if it's below
                        # an out edge
                        return i % 2 != myInParity
                # or if it's past the last edge, and we aren't
                # bounded right
                return myLen % 2 != myInParity

            /**
             * All Regions are also Guards, either coercing a
             * specimen to a position in the region, or rejecting it.
             */
            to coerce(var specimen, optEjector) :myTypeR:
                specimen := myType.coerce(specimen, optEjector)
                if (self(specimen)):
                    return specimen
                else:
                    throw.eject(optEjector,
                                `${M.toQuote(specimen)} is not in the region ${M.toQuote(self)}`)

            /**
             * Return the type's trivial value if it is in the region,
             * otherwise fail.
             */
            to getTheTrivialValue():
                return self.coerce(
                    def t := myType.getTheTrivialValue(),
                    def cantTrivialize(_) {
                        throw(`trivial value $t is not available in region $self`)})
            /**
             * Note that the empty region is bounded left, but it doesn't
             * have a start
             */
            to isBoundedLeft() :boolean:
                return myBoundedLeft

            /**
             * Note that the empty region is bounded left, but it doesn't
             * have a start.

             * Returns the start or null. The start is the least element
             * which is *in* the region.
             */
            to getOptStart() :nullOk[myType]:
                if (myBoundedLeft && myLen >= 1):
                    return myEdges[0]
                else:
                    return null

            /**
             * Note that the empty region is bounded right, but it doesn't
             * have a bound
             */
            to isBoundedRight() :boolean:
                return myLen % 2 == myInParity

            /**
             * Note that the empty region is bounded right, but it doesn't
             * have a bound.

             * Returns the bound or null. The right bound is the least
             * element greater than all elements in the region. Unlike the
             * left bound, it is *not* in the region.
             */
            to getOptBound() :nullOk[myType]:
                if (myLen >= 1 && myLen % 2 == myInParity):
                    return myEdges[myLen -1]
                else:
                    return null

            /**
             * Does this region contain no positions?

             * An empty region can always be constructed by the intersection
             * of a distinction and its complement, and is therefore an
             * interval, but not a distinction.
             */
            to isEmpty() :boolean:
                return myLen == 0 && myBoundedLeft

            /**
             * Does this region contain all positions?

             * The full region is the intersection (and) of no regions, and
             * is therefore a interval but not a distinction.
             */
            to isFull() :boolean:
                return myLen == 0 && !myBoundedLeft

            /**
             * All regions of a coordinate space can be made by and/or/nots
             * of distinctions.

             * The not of a distinction must be a distinction. For this space,
             * the distinctions are (myType < y) and (myType >= y).
             */
            to isDistinction() :boolean:
                return myLen == 1

            /**
             * The intersection of distinctions must be an interval (it may
             * or may not also be a distinction).

             * Therefore, the
             * intersection of intervals is also an interval. The
             * intersection of no regions is the full region, which is a
             * interval. The intersection of a distinction and its
             * complement is the empty region, which is an interval. All
             * distinctions are intervals. The complement of an interval
             * need not be an interval. A non-interval is a complex
             * region.
             */
            to isSimpleRegion() :boolean:
                if (myLen <= 1):
                    # distinctions, empty, and full are all intervals
                    return true
                else if (myLen == 2):
                    # x..!y is an interval
                    return myBoundedLeft
                else:
                    # nothing else is an interval
                    return false

            /**
             * A region can be asked to decompose itself into intervals.

             * The original region is the union (or) of these intervals.
             * In the case of an OrderedRegion, the intervals returned are
             * disjoint and ascending.

             * If the region is full, this returns a singleton list
             * containing the full interval. If this region is empty, then
             * this return an empty list, since the empty region is the
             * union of no regions.
             */
            to getSimpleRegions():
                def flex := [].diverge()
                if (! myBoundedLeft):
                    if (myLen == 0):
                        flex.push(region(false, []))
                    else:
                        flex.push(region(false, [myEdges[0]]))
                var i := myInParity
                while (i < myLen):
                    flex.push(region(true, myEdges(i, myLen.min(i+2))))
                    i += 2
                return flex.snapshot()

            /**
             * An interval can be asked to decompose itself into distinctions.

             * The original interval is the intersection (and) of these
             * distinctions.

             * The full interval returns a list of no distinctions. The
             * empty interval return the list [(myType < 0), (myType >= 0)],
             * ie, 0..!0.
             */
            to getDistinctions():
                if (myLen == 1):
                    # a distinctions is one inequality
                    return [self]
                else if (myLen == 2 && myBoundedLeft):
                    # an interval is the intersection of two inequalities
                    return [region(true, [myEdges[0]]),
                           region(false, [myEdges[1]])]
                else if (myLen == 0):
                    if (myBoundedLeft):
                        # the empty region is the intersection of two
                        # disjoint distinctions, for example, a
                        # distinction and its complement, for example,
                        # (myType < 0) and (myType >= 0)
                        [region(false, [0]),
                         region(true, [0])]
                    else:
                        # the full region is the intersection of no
                        # distinctions
                        return []
                else:
                    throw("can only get distinctions from an interval")

            /**
             * the region you get if you displace all my positions by
             * offset.

             * Note that offset may not be of myType. For example,
             * "(char > 'a') + 3" is fine.
             */
            to add(offset):
                def flex := [].diverge()
                for edge in myEdges:
                    flex.push(edge + offset)
                return region(myBoundedLeft, flex)

            /**
             * the region you get if you displace all my positions by -offset
             */
            to subtract(offset):
                return self + -offset


            /**
             * A region whose membership is the opposite of this one.
             */
            to not():
                return region(!myBoundedLeft, myEdges)

            /**
             * only those positions in both regions
             */
            to and(other):
                def otherEdges := other.getEdges()
                def otherLen := otherEdges.size()
                def flex := [].diverge()
                var i := -myInParity
                var j := if (other.isBoundedLeft()) {0} else {-1}
                var newBoundedLeft := true
                while (i < myLen && j < otherLen):
                    def in1 := get(myEdges, i)
                    def in2 := get(otherEdges, j)
                    def out1 := get(myEdges, i + 1)
                    def out2 := get(otherEdges, j + 1)
                    def maxin := max(in1, in2)
                    def minout := min(out1, out2)
                    #XXX compiler bug workaround
                    def bleh := maxin == null || minout == null
                    if (bleh || maxin < minout):
                        if (maxin == null):
                            newBoundedLeft := false
                        else:
                            flex.push(maxin)
                        if (minout != null):
                            flex.push(minout)
                    # XXX compiler bug workaround
                    def bluh := (out1 != null && out1 < out2)
                    if (out2 == null || bluh):
                        i += 2
                    else:
                        j += 2
                return region(newBoundedLeft, flex)

            /**
             * all positions in either region
             */
            to or(other):
                return !(!self & !other)

            /**
             * all position in me but not in other.
             */
            to butNot(other):
                return self & !other

            /**
             * enumerates positions in ascending order.

             * This doesn't necessarily terminate.
             */
            to _makeIterator():
                if (! myBoundedLeft):
                    throw("No least position")
                if (myLen == 0):
                    return []._makeIterator()

                # Iteration covers each position between start and end edges.
                # i - iteration counter, produced as key
                # index - index of current start edge.
                # pos - next value to be produced by iterator.
                # lim - value at current end edge.
                var i := 0
                var index := 0
                var pos := myEdges[0]
                var lim := null
                if (myLen > 1):
                    lim := myEdges[1]
                var endReached := false
                return object iterator:
                    to next(done):
                        if (endReached):
                            throw.eject(done, "iteration done")
                        if (index + 1 < myLen):
                            def val := [i, pos]
                            i += 1
                            pos := pos.next()
                            if (!(pos < lim)):
                                index += 2
                                if (index >= myLen):
                                    endReached := true
                                else:
                                    pos := myEdges[index]
                                    lim := myEdges[index + 1]
                            return val
                        else if (index < myLen):
                            def val := [i, pos]
                            def nextPos := pos.next()
                            i += 1
                            if (pos <=> nextPos):
                                endReached := true
                            else:
                                pos := nextPos
                            return val

            /**
             * returned object will enumerate positions in descending order
             */
            to descending():
                if (myLen == 0):
                    return []._makeIterator()
                var i := 0
                var index := myLen - 1
                var pos := myEdges[index].previous()
                var lim := myEdges[index - 1]
                var endReached := false
                return object descender:
                    to _makeIterator():
                        if (!(self.isBoundedRight())):
                            throw("No greatest position")
                        return descender
                    to next(done):
                        if (endReached):
                            throw.eject(done, "Iteration done")
                        if (index >= 1):
                            def val := [i, pos]
                            i += 1
                            pos := pos.previous()
                            if (!(pos >= lim)):
                                index -= 2
                                if (index < 0):
                                    endReached := true
                                else:
                                    pos := myEdges[index].previous()
                                    if (index > 0):
                                        lim := myEdges[index - 1]
                            return val
                        else if (index == 0):
                            def val := [i, pos]
                            def prevPos := pos.previous()
                            i += 1
                            if (!(pos < prevPos)):
                                endReached := true
                            else:
                                pos := prevPos
                            return val

            /**
             * As a region, my comparison is a subset test.
             */
            to op__cmp(other) :float:
                def selfExtra := !(self & !other).isEmpty()
                def otherExtra := !(other & !self).isEmpty()
                if (selfExtra):
                    if (otherExtra):
                        # Both have left-overs, so they're incomparable.
                        return NaN
                    else:
                        # Only self has left-overs, so we're a strict
                        # superset of other
                        return 1.0
                else:
                    if (otherExtra):
                        # Only other has left-overs, so we're a strict
                        # subset of other
                        return -1.0
                    else:
                        # No left-overs, so we're as-big-as each other
                        return 0.0
        return self

object OrderedSpaceMaker as DeepFrozen:

    /**
     * Given a value of a type whose reflexive (x <=> x) instances are
     * fully ordered, this returns the corresponding OrderedSpace
     */
    to spaceOfValue(value):
        if (value =~ i :int):
            return int
        else if (value =~ f :float):
            return float
        else if (value =~ c :char):
            return char
        else:
            def type := value._getAllegedType()
            return OrderedSpaceMaker(type, M.toQuote(type))

    /**
     * start..!bound is equivalent to
     * (space >= start) & (space < bound)
     */
    to op__till(start, bound):
        def space := OrderedSpaceMaker.spaceOfValue(start)
        return (space >= start) & (space < bound)

    /**
     * start..stop is equivalent to
     * (space >= start) & (space <= stop)
     */
    to op__thru(start, stop):
        def space := OrderedSpaceMaker.spaceOfValue(start)
        return (space >= start) & (space <= stop)

    /**
     * Given a type whose reflexive (x <=> x) instances are fully
     * ordered, this makes an OrderedSpace for making Regions and
     * Twisters for those instances using operator notation.
     */
    to run(myType :DeepFrozen, myName :str):

        /**
         * Notational convenience
         */
        def region(boundedLeft :boolean, edges) as DeepFrozen:
            return OrderedRegionMaker(myType, myName, boundedLeft, edges)


        /**
         * The OrderedSpace delegates to the myType.
         * <p>
         * Of all normal guard messages, the only one it implements itself
         * rather than delegating is _printOn/1.
         */
        object OrderedSpace extends myType as DeepFrozen:

            /**
             * Just uses the name used to construct this OrderedSpace
             */
            to _printOn(out):
                out.print(myName)


            /**
             * One step in executing the expansion of the relational
             * operators
             */
            to op__cmp(myY :myType):
                return object regionMaker:

                    /**
                     * (myType < myY)
                     */
                    to belowZero():
                        return region(false, [myY])

                    /**
                     * (myType <= myY)
                     */
                    to atMostZero():
                        def nextY := myY.next()
                        if (myY <=> nextY):
                            # all positions <= the last position means
                            # all positions period.
                            return region(false, [])
                        else:
                            return region(false, [nextY])

                    /**
                     * (myType <=> myY)
                     */
                    to isZero():
                        def nextY := myY.next()
                        if (myY <=> nextY):
                            # If myY is the last position, then myY..myY is
                            # equivalent to myType >= myY
                            return region(true, [myY])
                        else:
                            return region(true, [myY, nextY])

                    /**
                     * (myType >= myY)
                     */
                    to atLeastZero():
                        return region(true, [myY])

                    /**
                     * (myType > myY)
                     */
                    to aboveZero():
                        def nextY := myY.next()
                        if (myY <=> nextY):
                            # If myY is the last position, then all positions
                            # after it are no positions at all.
                            return region(true, [])
                        else:
                            return region(true, [nextY])

            /**
             * (myType + myOffset).
             * <p>
             * Note that myOffset doesn't have to be a member of myType. For
             * example, "char + 3" is legal.
             */
            to add(myOffset):
                object twister:
                    to _printOn(out):
                        out.print(`($myName + $myOffset)`)

                    to run(addend :myType):
                        return addend + myOffset

                    to getOffset():
                        return myOffset

                    to add(moreOffset):
                        return OrderedSpace + (myOffset + moreOffset)

                    to subtract(moreOffset):
                        return twister + -moreOffset

            /**
             * (myType - offset)
             */
            to subtract(offset):
                return OrderedSpace + -offset
        return OrderedSpace


def testIterable(assert):
    def intspace := OrderedSpaceMaker(int, "int")
    def reg := (intspace >= 0) & (intspace < 5)
    assert.equal([x for x in reg], [0, 1, 2, 3, 4])

def testContainment(assert):
    def intspace := OrderedSpaceMaker(int, "int")
    def reg := (intspace >= 0) & (intspace < 5)
    assert.equal(reg(3), true)
    assert.equal(reg(5), false)
    assert.raises(fn fail {reg(1.0)})

def testGuard(assert):
    def intspace := OrderedSpaceMaker(int, "int")
    def reg := (intspace >= 0) & (intspace < 5)
    assert.equal(def x :reg := 3, 3)
    assert.ejects(fn ej, fail {def x :reg exit ej := 7})

def testDeepFrozen(assert):
    def intspace := OrderedSpaceMaker(int, "int")
    def reg := (intspace >= 0) & (intspace < 5)
    def x :reg := 2
    #traceln("welp")
    object y implements DeepFrozen:
        to add(a):
            return a + x
    assert.equal(y =~ _ :DeepFrozen, true)

unittest([testIterable, testContainment, testGuard, testDeepFrozen])
