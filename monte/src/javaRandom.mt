def __makeOrderedSpace := import("regions")

def GEN := 0x5deece66d
def MASK48 := (1 << 48) - 1

def makeJavaRandom(seed):
    var state := GEN ^ seed & MASK48
    return object javaRandom:
        to next(width :(1..48)):
            state *= GEN
            state += 0xb
            state &= MASK48

            return state >> (48 - width)


def unittest := import("unittest")

def testKnowns(assert):
    def testKnownValues():
        def r := makeJavaRandom(0)
        # These values came from java-random from pypi, using a width of 8 bits.
        def values := [187, 212, 61, 155, 163, 79, 140, 29, 152, 200, 85, 64, 98]
        for expected in values:
            assert.equal(expected, r.next(8))

    return [testKnownValues]

def testWidths(assert):
    def r := makeJavaRandom(0)

    def testValid():
        for w in 1..48:
            r.next(w)

    return [testValid]

unittest([testKnowns, testWidths])


def r := makeJavaRandom(0)
