module OrderedSpaceMaker
export (charSpace, intSpace, floatSpace, __makeOrderedSpace)

def charSpace := OrderedSpaceMaker(Char, "Char")
def intSpace := OrderedSpaceMaker(Int, "Int")
def floatSpace := OrderedSpaceMaker(Double, "Double")

object __makeOrderedSpace extends OrderedSpaceMaker:
    /**
     * Given a value of a type whose reflexive (x <=> x) instances are
     * fully ordered, this returns the corresponding OrderedSpace
     */
    to spaceOfValue(value):
        if (value =~ i :Int):
            return intSpace
        else if (value =~ f :Double):
            return floatSpace
        else if (value =~ c :Char):
            return charSpace
        else:
            def type := value._getAllegedType()
            return OrderedSpaceMaker(type, M.toQuote(type))

    /**
     * start..!bound is equivalent to
     * (space >= start) & (space < bound)
     */
    to op__till(start, bound):
        def space := __makeOrderedSpace.spaceOfValue(start)
        return (space >= start) & (space < bound)

    /**
     * start..stop is equivalent to
     * (space >= start) & (space <= stop)
     */
    to op__thru(start, stop):
        def space := __makeOrderedSpace.spaceOfValue(start)
        return (space >= start) & (space <= stop)
