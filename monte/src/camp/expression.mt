def makeCAMP := import("camp")

def makeParser(code):
    return object campCode:
        to getCode():
            return code

        to add(other):
            return makeParser(code + other.getCode())

        to complement():
            def len := code.size()
            def insts := [['H', len + 3]] + code + [['M', 1], 'F']
            return makeParser(insts)

def ex(item):
    return makeParser([['X', item]])

def testCampCode(assert):
    def testEx():
        def code := ex('x')
        assert.equal(makeCAMP(code.getCode(), "x").run(), true)
    def testComplement():
        def code := ~ex('x') + ex('y')
        assert.equal(makeCAMP(code.getCode(), "y").run(), true)
    return [
        testEx,
        testComplement,
    ]

def unittest := import("unittest")

unittest([testCampCode])
