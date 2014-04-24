# The 33rd-order polynomial used in CRC32.
# Bit-reversed in order to be able to do right-hand shifts.
# http://reveng.sourceforge.net/crc-catalogue/17plus.htm#crc.cat.crc-32
def poly32 := 0xedb88320

# Perform a polynomial multiplication over a single byte, returning the new
# checksum state.
def _CRCByte(poly :int, var c :int) :int:
    for bit in [null] * 8:
        if ((c & 1) == 1):
            c := poly ^ (c >> 1)
        else:
            c >>= 1
    return c

# Construct a map of all 256 bytes to their CRC32 states.
def _makeCRCMap() :Map[int, int]:
    var rv := [].asMap()
    var i := 0
    while (i < 256):
        rv |= [i => _CRCByte(poly32, i)]
        i += 1
    return rv

def _map :DeepFrozen := _makeCRCMap()

def CRC32(bytes) implements DeepFrozen:
    var state := 0xffffffff
    for byte in bytes:
        def next := state ^ byte
        state := _map[next & 0xff] ^ (state >> 8)
    return state ^ 0xffffffff

def unittest := import("unittest")

def testCRC32Vectors(assert):
    def testEmpty():
        assert.equal(CRC32([]), 0x00000000)
    def testCRCCalculator():
        assert.equal(CRC32([c.asInteger() for c in "123456789"]), 0xcbf43926)
    def testCRCCatalog():
        assert.equal(CRC32([0x00] * 40), 0xe9ec3db1)
        assert.equal(CRC32([0xff] * 40), 0x8cd04c73)
    return [
        testEmpty,
        testCRCCalculator,
        testCRCCatalog,
    ]

unittest([testCRC32Vectors])

CRC32
