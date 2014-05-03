def __makeOrderedSpace := import("regions")
def ["Word" => Word] | _ := import("word")
def ["ubint32" => ubint32, "ubint64" => ubint64] | _ := import("struct")

def longToBytes(var i):
    var rv := []
    for _ in 0..!8:
        rv := [i & 0xff] + rv
        i >>= 8
    return rv

def chunksOf(i, l):
    var offset := 0
    def rv := [].diverge()
    while (offset < l.size()):
        rv.push(l.slice(offset, offset + i))
        offset += i
    return rv.snapshot()

def testChunksOf(assert):
    def empty():
        assert.equal(chunksOf(3, []), [])
    def perfectFit():
        assert.equal(chunksOf(3, [0, 1, 2, 3, 4, 5]), [[0, 1, 2], [3, 4, 5]])
    def ragged():
        assert.equal(chunksOf(3, [0, 1, 2, 3, 4]), [[0, 1, 2], [3, 4]])
    return [
        empty,
        perfectFit,
        ragged,
    ]

def _pad(var message):
    def ml :Word[64] := message.size() * 8

    # Establish some padding.
    # Pad out to the next 64 bytes, including the length of the message and
    # the 0x80 pad.
    def zeroes := [0x00] * ((-1 - ubint64.size() - message.size()) % 64)
    message += [0x80] + zeroes + ubint64.pack(ml)

    return message

def leftRotate(x, i) :Word[32]:
    return (x << i) | (x >> (32 - i))

def unittest := import("unittest")

def testLeftRotate(assert):
    def noop():
        assert.equal(leftRotate(42, 0), 42)
    def noOverflow():
        assert.equal(leftRotate(21, 1), 42)
    def overflow():
        assert.equal(leftRotate(0x80000000 | 10, 2), 42)
    return [
        noop,
        noOverflow,
        overflow,
    ]

def h :List[Word[32]] := [
    0x64752301,
    0xefcdab89,
    0x98badcfe,
    0x10325476,
    0xc3d2e1f0,
]

def SHA1(message):
    var h0 :Word[32] := h[0]
    var h1 :Word[32] := h[1]
    var h2 :Word[32] := h[2]
    var h3 :Word[32] := h[3]
    var h4 :Word[32] := h[4]

    for chunk in chunksOf(64, message):
        def words := [ubint32.unpack(c) for c in chunksOf(4, chunk)].diverge()
        for i in 16..!80:
            words.push(leftRotate(words[i - 3] ^
                                  words[i - 8] ^
                                  words[i - 14] ^
                                  words[i - 16], 1))

        var a :Word[32] := h0
        var b :Word[32] := h1
        var c :Word[32] := h2
        var d :Word[32] := h3
        var e :Word[32] := h4

        for i in 0..!80:
            # XXX I'd really like to do this with `def [f, k] := if ...` but
            # the parser can't currently grok that.
            var f := null
            var k := null
            if (i < 20):
                # (b & c) | (~b & d)
                f := d ^ (b & (c ^ d))
                k := 0x5a827999
            else if (i < 40):
                f := b ^ c ^ d
                k := 0x6ed9eba1
            else if (i < 60):
                f := (b & c) | (b & d) | (c & d)
                k := 0x8f1bbcdc
            else:
                f := b ^ c ^ d
                k := 0xca62c1d6

            def temp :Word[32] := leftRotate(h[0], 5) + f + e + k + words[i]
            e := d
            d := c
            c := leftRotate(b, 30)
            b := a
            a := temp

        h0 += a
        h1 += b
        h2 += c
        h3 += d
        h4 += e

    return (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4

def SHA1String(s):
    return SHA1(_pad([c.asInteger() for c in s]))

def testSHA1(assert):
    def empty():
        assert.equal(SHA1String(""),
                     0xda39a3ee5e6b4b0d3255bfef95601890afd80709)
    def fox():
        assert.equal(SHA1String("The quick brown fox jumps over the lazy dog"),
                     0x2fd4e1c67a2d28fced849ee1bb76e7391b93eb12)
    def cog():
        assert.equal(SHA1String("The quick brown fox jumps over the lazy cog"),
                     0xde9f2c7fd25e1b3afad3e85a0bd17d9b100db4b3)
    return [
        empty,
        fox,
        cog,
    ]

unittest([
    testChunksOf,
    testLeftRotate,
    testSHA1,
])
