from monte.runtime.base import MonteObject
from monte.runtime.data import Integer, bwrap, null
from monte.runtime.flow import MonteIterator


class EListMixin(object):

    def __repr__(self):
        # XXX guaranteed to break in presence of cycles
        return '<m: [' + ', '.join(repr(x) for x in self.l) + ']>'

    def _makeIterator(self):
        return MonteIterator((Integer(i), o) for (i, o) in zip(range(len(self.l)), self.l))

    def size(self):
        return Integer(len(self.l))

    def contains(self, item):
        return bwrap(item in self.l)

    def add(self, other):
        return ConstList(tuple(self) + tuple(other))

    def diverge(self, guard=None):
        if guard is None:
            return FlexList(self.l[:])
        l = FlexList.fromType(guard)
        l.extend(list(self.l))
        return l

    def sort(self, keyFunc=None):
        return ConstList(sorted(self.l, key=keyFunc))

    def fetch(self, idx, insteadThunk):
        if 0 <= idx < len(self.l):
            return self.get(index)
        else:
            return insteadThunk()

    def last(self, idx):
        return self.l[-1]

    def get(self, idx):
        if not isinstance(idx, Integer):
            raise RuntimeError("%r is not a integer" % (idx,))
        if not 0 <= idx < len(self.l):
            raise IndexError(idx)
        return self.l[idx.n]

    def _m_with(self, *a):
        if len(a) == 1:
            return ConstList(self.l + [val])
        elif len(a) == 2:
            new = self.l[:]
            new.insert(a[0], a[1])
            return ConstList(new)
        else:
            raise RuntimeError("with() takes 1 or 2 arguments")

    def multiply(self, n):
        if not isinstance(n, Integer):
            raise RuntimeError("%r is not a integer" % (n,))
        return ConstList(self.l * n.n)

    def asMap(self):
        return Map([(Integer(i), v) for i, v in dict(enumerate(self.l))])

    def asKeys(self):
        return Map(dict.fromkeys(self.l, null))

    def asSet(self):
        raise NotImplementedError()


class ConstList(EListMixin, MonteObject):
    def __init__(self, l):
        self.l = tuple(l)

    def op__cmp(self, other):
        if not isinstance(other, ConstList):
            raise RuntimeError("%r is not a ConstList" % (other,))
        return Integer(cmp(self.l, other.l))

    def snapshot(self):
        return self

    def readOnly(self):
        return self

    def _uncall(self):
        return ConstList([makeMonteList, "run", self])

    #E list methods left out, due to indolence: includes, startOf, lastStartOf


class FlexList(EListMixin, MonteObject):

    def __init__(self, l):
        self.l = l

    def readOnly(self):
        return ROList(self.l)

    def put(self, idx, value):
        if not isinstance(idx, Integer):
            raise RuntimeError("%r is not a integer" % (idx,))
        if not 0 <= idx < len(self.l):
            raise IndexError(idx)
        self.l[idx] = value
        return null

    def sortInPlace(self, keyFunc=None):
        self.l.sort(key=keyFunc)
        return null

    def push(self, value):
        self.l.append(value)
        return null

    def extend(self, other):
        if not isinstance(other, (ConstList, FlexList)):
            raise RuntimeError("%r is not a list" % (other,))
        self.l.extend(other.l)
        return null

    def pop(self):
        return self.l.pop()

    def setSlice(self, start, bound, other):
        if not isinstance(other, (ConstList, FlexList)):
            raise RuntimeError("%r is not a list" % (other,))
        if not isinstance(start, Integer):
            raise RuntimeError("%r is not a integer" % (start,))
        if not isinstance(bound, Integer):
            raise RuntimeError("%r is not a integer" % (bound,))
        if not 0 <= start < len(self.l):
            raise IndexError(start)
        if not 0 <= bound <= len(self.l):
            raise IndexError(bound)
        self.l[start:bound] = other
        return null

    def insert(self, idx, value):
        if not isinstance(idx, Integer):
            raise RuntimeError("%r is not a integer" % (idx,))
        if not 0 <= idx < len(self.l):
            raise IndexError(idx)
        self.l.insert(idx, value)
        return null

    def removeSlice(self, start, bound):
        if not isinstance(start, Integer):
            raise RuntimeError("%r is not a integer" % (start,))
        if not isinstance(bound, Integer):
            raise RuntimeError("%r is not a integer" % (bound,))
        if not 0 <= start < len(self.l):
            raise IndexError(start)
        if not 0 <= bound <= len(self.l):
            raise IndexError(bound)
        del self.l[start:bound]
        return null

    def diverge(self):
        return FlexList(self.l[:])

    def snapshot(self):
        return ConstList(self.l[:])

    def _uncall(self):
        return ConstList([ConstList([self.l]), "diverge", ConstList([])])

    def _makeIterator(self):
        return MonteIterator((Integer(i), o) for (i, o) in zip(range(len(self.l), self.l)))


def makeMonteList(*items):
    return ConstList(items)

class Map(dict):
    _m_fqn = "Dict"
    __setitem__ = None
    get = dict.__getitem__


class mapMaker(object):
    _m_fqn = "__makeMap"
    @staticmethod
    def fromPairs(pairs):
        return Map(pairs)
