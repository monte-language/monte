from monte.runtime.base import MonteObject
from monte.runtime.data import Integer, bwrap, null, true, false
from monte.runtime.flow import MonteIterator


class EListMixin(object):

    def _printOn(self, out):
        # XXX consider some sort of pretty-printer interface that can
        # distinguish writing subelements from delimiter characters
        out.raw_print(u'[')
        if self.l:
            it = iter(self.l)
            item = next(it)
            out.quote(item)
            for item in it:
                out.raw_print(u', ')
                out.quote(item)
        out.raw_print(u']')

    def _makeIterator(self):
        return MonteIterator((Integer(i), o) for (i, o)
                             in zip(range(len(self.l)), self.l))

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
        if not 0 <= idx.n < len(self.l):
            raise IndexError(idx.n)
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
    _m_fqn = "__makeList$ConstList"
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
    _m_fqn = "__makeList$FlexList"
    def __init__(self, l):
        self.l = l

    def _printOn(self, out):
        EListMixin._printOn(self, out)
        out.raw_print(u'.diverge()')

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

    def get(self, index):
        if not isinstance(index, Integer):
            raise RuntimeError("Expected Integer, got %r" % index)
        return self.l[index.n]

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

_absent = object()

class EMapMixin(object):
    def __init__(self, d, keys=None):
        self.d = d
        if keys is None:
            self._keys = self.d.keys()
        else:
            assert len(keys) == len(self.d)
            self._keys = keys

    def _printOn(self, out):
        if len(self._keys) == 0:
            out.raw_print(u'[].asMap()')
            return
        out.raw_print(u'[')
        it = iter(self._keys)
        k = next(it)
        out.quote(k)
        out.raw_print(u' => ')
        out.quote(self.d[k])
        for k in it:
            out.raw_print(u', ')
            out.quote(k)
            out.raw_print(u' => ')
            out.quote(self.d[k])
        out.raw_print(u']')

    def diverge(self):
        return FlexMap(self.d.copy(), self._keys[:])

    def get(self, key):
        result = self.d.get(key, _absent)
        if result is _absent:
            raise RuntimeError("%r not found" % (key,))
        return result

    def fetch(self, key, instead):
        result = self.d.get(key, _absent)
        if result is _absent:
            return instead()
        return result

    def contains(self, candidate):
        return bwrap(candidate in self.d.values())

    def intersects(self, other):
        for k in self._keys:
            if other.maps(k):
                return true
        return false

    def size(self):
        return Integer(len(self.d))

    def _makeIterator(self):
        return MonteIterator((k, self.d[k]) for k in self._keys)

    def _m_or(self, behind):
        if not isinstance(behind, (ConstMap, FlexMap)):
            raise RuntimeError("%r is not a map" % (behind,))
        if len(self.d) == 0:
            return behind.snapshot()
        elif len(behind.d) == 0:
            return self.snapshot()
        flex = behind.diverge()
        flex.putAll(self)
        return flex.snapshot()

    def _m_and(self, mask):
        if not isinstance(mask, (ConstMap, FlexMap)):
            raise RuntimeError("%r is not a map" % (mask,))
        if len(self.d) > len(mask.d):
            bigger = self
            smaller = mask
        else:
            bigger = mask
            smaller = self

        if len(smaller.d) == 0:
            return ConstMap({})
        flex = FlexMap({})
        for k in smaller._keys:
            if k in bigger._keys:
                flex.put(key, self.d[key])
        return flex.snapshot()

    def butNot(self, mask):
        if not isinstance(mask, (ConstMap, FlexMap)):
            raise RuntimeError("%r is not a map" % (mask,))
        if len(self.d) == 0:
            return ConstMap({})
        elif len(mask.d) == 0:
            return self.snapshot()
        flex = self.diverge()
        flex.removeKeys(mask)
        return flex.snapshot()

    def maps(self, k):
        return bwrap(k in self.d)

    def _m_with(self, key, val):
        flex = self.diverge()
        flex.put(key, val)
        return flex.snapshot()

    def without(self, key):
        flex = self.diverge()
        flex.removeKey(key)
        return flex.snapshot()

    def getKeys(self):
        return ConstList(self._keys)

    def sortKeys(self, keyFunc=None):
        keys = sorted(self._keys, key=keyFunc)
        return ConstMap(self.d, keys)

    def getValues(self):
        return ConstList(self.d[k] for k in self._keys)

    def getPair(self):
        return ConstList([self.getKeys(), self.getValues()])

    #snapshot
    #readOnly
    #domain
    #removeKey
    #putAll
    #put


class ConstMap(EMapMixin, MonteObject):
    _m_fqn = "__makeMap$ConstMap"

    def snapshot(self):
        return self

    def readOnly(self):
        return self

    def domain(self):
        raise NotImplementedError()

    def _uncall(self):
        return ConstList([mapMaker, "fromColumns",
                          ConstList([
                              ConstList(self._keys),
                              ConstList(self.d[k] for k in self._keys)])])


class FlexMap(EMapMixin, MonteObject):
    _m_fqn = "__makeMap$FlexMap"

    def _printOn(self, out):
        EMapMixin._printOn(self, out)
        out.raw_print(u'.diverge()')

    def snapshot(self):
        return ConstMap(self.d.copy(), self._keys[:])

    def readOnly(self):
        raise NotImplementedError()

    def domain(self):
        raise NotImplementedError()

    def removeKey(self, k):
        try:
            i = self._keys.index(k)
        except ValueError:
            return null
        del self.d[k]
        if i + 1 < len(self._keys):
            lastk = self._keys.pop()
            self._keys[i] = lastk
        else:
            del self._keys[i]

    def put(self, k, v):
        self.d[k] = v
        if k not in self._keys:
            self._keys.append(k)

    def putAll(self, other):
        if not isinstance(other, (ConstMap, FlexMap)):
            raise RuntimeError("%r is not a map" % (other,))
        for (k, v) in other.d.iteritems():
            self.put(k, v)

    def _uncall(self):
        return ConstList([self.snapshot(), "diverge", ConstList([])])


class mapMaker(object):
    _m_fqn = "__makeMap"
    @staticmethod
    def fromPairs(pairs):
        return ConstMap(dict(p for (i, p) in pairs._makeIterator()), [p.get(Integer(0)) for p in pairs])

    @staticmethod
    def fromColumns(keys, vals):
        if not isinstance(keys, (ConstList, FlexList)):
            raise RuntimeError("%r is not a list" % (keys,))
        if not isinstance(vals, (ConstList, FlexList)):
            raise RuntimeError("%r is not a list" % (vals,))
        return ConstMap(dict(zip(keys.l, vals.l)), keys)


