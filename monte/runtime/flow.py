from monte.runtime.base import MonteObject, ejector

class MonteIterator(MonteObject):
    def __init__(self, it):
        self.it = it

    def __iter__(self):
        return self.it

    def _makeIterator(self):
        return self

    def next(self, ej):
        try:
            return self.it.next()
        except StopIteration:
            ej()


#deepFrozenFunc
def monteLooper(coll, obj):
    it = coll._makeIterator()
    ej = ejector("iteration")
    try:
        while True:
            key, item = it.next(ej)
            obj.run(key, item)
    except ej._m_type:
        pass
    finally:
        ej.disable()
