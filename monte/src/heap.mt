module enumerate, rng, unittest
export (Heap, makeHeap)


interface Heap:
    pass


# A min-heap
def makeHeap(contents) :Heap:
    var storage := contents.diverge()

    object heap implements Heap:
        to size():
            return storage.size()

        to push(val):
            var index := storage.size()
            var parentIndex := ((index - 1) / 2).floor().round()
            storage.push(val)
            while (storage[index] < storage[parentIndex]):
                heap._swapIndex(index, parentIndex)
                index := parentIndex
                parentIndex := ((index - 1) / 2).floor().round()
                if (parentIndex < 0):
                    break

        to peek():
            if (storage.size() == 0):
                throw("Cannot peek from empty heap.")
            return storage[0]

        to pop():
            if (storage.size() == 0):
                throw("Cannot pop from empty heap.")

            var ret := storage[0]
            def val := storage.pop()
            if (storage.size() == 0):
                return ret
            else:
                storage[0] := val
            heap._heapifyDown(0)
            return ret

        to snapshot() :Heap:
            return makeHeap(storage.slice(0, storage.size()))

        to sorted() :List:
            def newHeap := heap.snapshot()
            def ret := [].diverge()
            while (heap.size() > 0):
                ret.push(heap.pop())
            return ret.snapshot()

        to visualize() :str:
            var out := ""
            for v in storage:
                out += `$v `
            return out

        to checkInvariant() :boolean:
            var errors := 0
            for [i, v] in enumerate(storage):
                def c1i := 2 * i + 1
                def c2i := 2 * i + 2

                if (c1i < storage.size()):
                    if (storage[c1i] < v):
                        errors += 1
                if (c2i < storage.size()):
                    if (storage[c2i] < v):
                        errors += 1
            return errors == 0

        to _swapIndex(i1, i2):
            def temp := storage[i1]
            storage[i1] := storage[i2]
            storage[i2] := temp

        to _heapifyDown(i):
            var index := i
            while (index < storage.size()):
                var c1 := index * 2 + 1
                var c2 := index * 2 + 2

                if (c1 >= storage.size()):
                    break

                else if (c2 >= storage.size()):
                    if (storage[index] > storage[c1]):
                        heap._swapIndex(index, c1)
                        index := c1
                    else:
                        break

                else if (storage[c1] < storage[c2]):
                    if (storage[index] > storage[c1]):
                        heap._swapIndex(index, c1)
                        index := c1
                    else:
                        break

                else:
                    if (storage[index] > storage[c2]):
                        heap._swapIndex(index, c2)
                        index := c2
                    else:
                        break

    var i := contents.size() - 1
    while (i >= 0):
        heap._heapifyDown(i)
        i -= 1

    return heap


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


[Heap, makeHeap]
