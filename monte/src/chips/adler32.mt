def fold := import("hands.fold")
def ["Mod" => Mod] | _ := import("word")

def adlerPrime :int := 65521

def _adler([a, b], d):
    def t := a + d
    return [t, b + t]

def adler32(bytes) :int:
    def [a :Mod[adlerPrime], b :Mod[adlerPrime]] := fold(_adler, [1, 0], bytes)
    return b << 16 | a

def testAdler32(assert):
    def testWPVector():
        assert.equal(adler32([c.asInteger() for c in "Wikipedia"]),
                     0x11e60398)
    return [
        testWPVector,
    ]

def unittest := import("unittest")
unittest([testAdler32])

adler32
