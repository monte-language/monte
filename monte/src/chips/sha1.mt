def __makeOrderedSpace := import("regions")
def ["Word" => Word] | _ := import("word")

def h0 :Word[32] := 0x64752301
def h1 :Word[32] := 0xefcdab89
def h2 :Word[32] := 0x98badcfe
def h3 :Word[32] := 0x10325476
def h4 :Word[32] := 0xc3d2e1f0

# XXX Wow, the lack of actual Unicode handling here is crap.

def thatThing(var i):
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
    # Pad out to the next 64 bytes, including the length of the message.
    def zeroes := [0x00] * ((55 - message.size()) % 64)
    message += [0x80] + zeroes + thatThing(ml)

    return message

def make32([a, b, c, d]) :Word[32]:
    return (a << 24) | (b << 16) | (c << 8) | d

def leftRotate(var x :Word[32], var i):
    while (i > 0):
        i -= 1
        if ((x & 0x80000000) != 0):
            x := (x << 1) | 0x1
        else:
            x <<= 1
    return x

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

unittest([
    testChunksOf,
    testLeftRotate,
])

def SHA1(message):
    var h :List[Word[32]] := [h0, h1, h2, h3, h4]

    traceln(chunksOf(64, message))

    for chunk in chunksOf(64, message):
        def words := [make32(c) for c in chunksOf(4, chunk)].diverge()
        for i in 16..!80:
            words.push(leftRotate(words[i - 3] ^
                                  words[i - 8] ^
                                  words[i - 14] ^
                                  words[i - 16], 1))

        var a := h[0]
        var b := h[1]
        var c := h[2]
        var d := h[3]
        var e := h[4]

        for i in 0..!80:
            # XXX I'd really like to do this with `def [f, k] := if ...` but
            # the parser can't currently grok that.
            var f := null
            var k := null
            if (i < 20):
                # XXX have to use this to get ~b since Words don't actually
                # wrap ints. Revisit when Words suck less.
                f := (b & c) | ((b ^ 0xffffffff) & d)
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

            traceln(`f $f e $e k $k w[i] ${words[i]}`)
            def temp :Word[32] := leftRotate(h[0], 5) + f + e + k + words[i]
            e := d
            d := c
            c := leftRotate(b, 30)
            b := a
            a := temp

        traceln(`a $a b $b c $c d $d e $e`)

        h := [h[0] + a, h[1] + b, h[2] + c, h[3] + d, h[4] + e]

        traceln(`Post h $h`)

    traceln(`Yay $h`)
    return (h[0] << 128) | (h[1] << 96) | (h[2] << 64) | (h[3] << 32) | h[4]

traceln(SHA1(_pad([])))
