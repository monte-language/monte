def ["Word" => Word] | _ := import("word")
def unittest := import("unittest")

# Secret creator of filters with a preset filter filled in. For building
# unions and intersections.
def _makeBloom(width, hashes, var filter :Word[width]):
    return object bloom:
        # A Bloom filter of bit width ``width`` and using hash functions
        # ``hashes``.

        to add(item) :void:
            for hash in hashes:
                var offset := hash(item) % width
                filter |= 1 << offset

        # to and
        # to or

        to contains(item) :boolean:
            for hash in hashes:
                var offset := hash(item) % width
                if ((filter & (1 << offset)) == 0):
                    # Negative; not present.
                    return false
            # Positive; item might be present.
            return true

        to size() :float:
            # Estimate the number of items in the filter.
            # First, we need the number of bits in the filter. There's no
            # builtin pop count, so we'll open-code it.
            var popCount := 0
            var i := filter
            while (i > 0):
                if ((i & 1) == 1):
                    popCount += 1
                i >>= 1

            def top := (1 - popCount.asFloat() / width).log()
            return -top * width / hashes.size()

def makeBloom(width, hashes):
    return _makeBloom(width, hashes, 0)

def testBloom(assert):
    def id(x):
        return x

    def negative():
        def bloom := makeBloom(32, [id])
        assert.equal(bloom.contains(42), false)
    def positive():
        def bloom := makeBloom(32, [id])
        bloom.add(42)
        assert.equal(bloom.contains(42), true)
    def overlap():
        def bloom := makeBloom(32, [id])
        bloom.add(42)
        assert.equal(bloom.contains(10), true)

    return [
        negative,
        positive,
        overlap,
    ]

unittest([
    testBloom,
])

makeBloom
