def rng := import("javaRandom")
def unittest := import("unittest")

def [Heap, makeHeap] := import("heap")


def testHeap(assert):
    # Tests push, pop, and size.
    def testBasicUsage():
        def h := makeHeap([])
        assert.equal(h.size(), 0)
        h.push(2)
        assert.equal(h.size(), 1)
        h.push(1)
        assert.equal(h.size(), 2)

        assert.equal(h.pop(), 1)
        assert.equal(h.size(), 1)
        assert.equal(h.pop(), 2)
        assert.equal(h.size(), 0)

    # Test that peek returns the same thing as pop, and that they are right.
    def testPeekPop():
        def l := [1, 2, 3, 4, 5, 6]
        def h := makeHeap(l)
        for v in l:
            assert.equal(v, h.peek())
            assert.equal(v, h.pop())

    # Test that snapshop returns a separate heap.
    def testSnapshot():
        def h1 := makeHeap([1, 2, 3, 4, 5, 6])
        def h2 := h1.snapshot()
        h2.pop()
        assert.equal(6, h1.size())
        assert.equal(5, h2.size())

    def testSorted():
        def h := makeHeap([6, 5, 4, 3, 2, 1])
        def l := h.sorted()
        assert.equal(l, [1, 2, 3, 4, 5, 6])

    return [
        testBasicUsage,
        testPeekPop,
        testSnapshot,
        testSorted,
    ]

unittest([testHeap])
