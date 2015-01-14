from monte.runtime.base import MonteObject, ejector, typecheck
from monte.runtime.data import String, Integer, bwrap, null, true, false
from monte.runtime.flow import MonteIterator
from monte.runtime.guards.base import (deepFrozenFunc, deepFrozenGuard,
                                       selflessGuard, transparentStamp)


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
        return MonteIterator(ConstList((Integer(i), o)) for (i, o)
                             in zip(range(len(self.l)), self.l))

    def size(self):
        return Integer(len(self.l))

    def contains(self, item):
        return bwrap(item in self.l)

    def add(self, other):
        other = typecheck(other, EListMixin)
        return ConstList(tuple(self.l) + tuple(other.l))

    def diverge(self, guard=None):
        return FlexList(self.l[:], guard)

    def sort(self, keyFunc=None):
        return ConstList(sorted(self.l, key=keyFunc))

    def fetch(self, idx, insteadThunk):
        if 0 <= idx.n < len(self.l):
            return self.get(idx)
        else:
            return insteadThunk()

    def last(self):
        return self.l[-1]

    def get(self, idx):
        idx = typecheck(idx, Integer)
        if not 0 <= idx.n < len(self.l):
            raise IndexError(idx.n)
        return self.l[idx.n]

    def slice(self, start, stop=None):
        start = typecheck(start, Integer).n
        if stop is not None:
            stop = typecheck(stop, Integer).n
        return ConstList(self.l[start:stop])

    def _m_with(self, *a):
        if len(a) == 1:
            return ConstList(tuple(self.l) + (a[0],))
        elif len(a) == 2:
            i = typecheck(a[0], Integer).n
            return ConstList(tuple(self.l[:i]) + (a[1],) + tuple(self.l[i:]))
        else:
            raise RuntimeError("with() takes 1 or 2 arguments")

    def multiply(self, n):
        n = typecheck(n, Integer)
        return ConstList(self.l * n.n)

    def asMap(self):
        items = [(Integer(i), v) for i, v in enumerate(self.l)]
        d = dict(items)
        keys = [x[0] for x in items]
        return ConstMap(d, keys)

    def asKeys(self):
        return ConstMap(dict.fromkeys(self.l, null), keys=self.l)

    def asSet(self):
        raise NotImplementedError()


class ConstList(EListMixin, MonteObject):
    _m_fqn = "__makeList$ConstList"
    _m_auditorStamps = (selflessGuard, transparentStamp)

    def __init__(self, l):
        self.l = tuple(l)

    def op__cmp(self, other):
        other = typecheck(other, ConstList)
        return Integer(cmp(self.l, other.l))

    def snapshot(self):
        return self

    def readOnly(self):
        return self

    def _uncall(self):
        return ConstList([makeMonteList, String(u"run"), self])

    #E list methods left out, due to indolence: includes, startOf, lastStartOf


class FlexList(EListMixin, MonteObject):
    _m_fqn = "__makeList$FlexList"
    def __init__(self, l, valueGuard=None):
        self.valueGuard = valueGuard
        if valueGuard is None:
            self.l = list(l)
        else:
            self.l = [valueGuard.coerce(x, null) for x in l]

    def _printOn(self, out):
        EListMixin._printOn(self, out)
        out.raw_print(u'.diverge()')

    def readOnly(self):
        return ROList(self.l)

    def put(self, idx, value):
        idx = typecheck(idx, Integer)
        if not 0 <= idx.n < len(self.l):
            raise IndexError(idx)
        if self.valueGuard is not None:
            value = self.valueGuard.coerce(value, null)
        self.l[idx.n] = value
        return null

    def sortInPlace(self, keyFunc=None):
        self.l.sort(key=keyFunc)
        return null

    def push(self, value):
        if self.valueGuard is not None:
            value = self.valueGuard.coerce(value, null)
        self.l.append(value)
        return null

    def extend(self, other):
        contents = typecheck(other, (ConstList, FlexList)).l
        contents = other.l
        if self.valueGuard is not None:
            contents = [self.valueGuard.coerce(x, null) for x in contents]
        self.l.extend(contents)
        return null

    def pop(self):
        return self.l.pop()

    def get(self, index):
        index = typecheck(index, Integer)
        return self.l[index.n]

    def setSlice(self, start, bound, other):
        other = typecheck(other, (ConstList, FlexList))
        start = typecheck(start, Integer)
        bound = typecheck(bound, Integer)
        if not 0 <= start.n < len(self.l):
            raise IndexError(start)
        if not 0 <= bound.n <= len(self.l):
            raise IndexError(bound)
        contents = other.l
        if self.valueGuard is not None:
            contents = [self.valueGuard.coerce(x, null) for x in contents]
        self.l[start.n:bound.n] = contents
        return null

    def insert(self, idx, value):
        idx = typecheck(idx, Integer)
        if not 0 <= idx.n <= len(self.l):
            raise IndexError(idx)
        if self.valueGuard is not None:
            value = self.valueGuard.coerce(value, null)
        self.l.insert(idx, value)
        return null

    def removeSlice(self, start, bound):
        start = typecheck(start, Integer)
        bound = typecheck(bound, Integer)
        if not 0 <= start.n < len(self.l):
            raise IndexError(start)
        if not 0 <= bound.n <= len(self.l):
            raise IndexError(bound)
        del self.l[start.n:bound.n]
        return null

    def snapshot(self):
        return ConstList(self.l[:])

    def _uncall(self):
        return ConstList([ConstList([self.l]), String(u"diverge"), ConstList([])])

    def _makeIterator(self):
        return MonteIterator(ConstList((Integer(i), o)) for (i, o) in zip(range(len(self.l)), self.l))

class ListMaker(MonteObject):
    _m_fqn = "__makeList"
    _m_auditorStamps = (deepFrozenGuard,)

    def run(self, *items):
        return ConstList(items)

    def fromIterable(self, coll):
        items = []
        it = coll._makeIterator()
        ej = ejector("iteration")
        try:
            while True:
                key, item = it.next(ej)
                items.append(item)
        except ej._m_type:
            pass
        finally:
            ej.disable()
        return ConstList(items)

makeMonteList = ListMaker()

_absent = object()

class EMapMixin(object):
    def __init__(self, d, keys=None):
        self.d = d
        if keys is None:
            self._keys = self.d.keys()
        else:
            if len(keys) != len(self.d):
                raise RuntimeError("Keys don't match internal dict for FlexMap")
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

    def diverge(self, keyGuard=None, valueGuard=None):
        return FlexMap(self.d.copy(), self._keys[:], keyGuard, valueGuard)

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
        return MonteIterator(ConstList((k, self.d[k])) for k in self._keys)

    def _m_or(self, behind):
        behind = typecheck(behind, (ConstMap, FlexMap))
        if len(self.d) == 0:
            return behind.snapshot()
        elif len(behind.d) == 0:
            return self.snapshot()
        flex = behind.diverge()
        flex.putAll(self)
        return flex.snapshot()

    def _m_and(self, mask):
        mask = typecheck(mask, (ConstMap, FlexMap))
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
                flex.put(k, self.d[k])
        return flex.snapshot()

    def butNot(self, mask):
        mask = typecheck(mask, (ConstMap, FlexMap))
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
    _m_auditorStamps = (selflessGuard, transparentStamp)

    def snapshot(self):
        return self

    def readOnly(self):
        return self

    def domain(self):
        raise NotImplementedError()

    def _uncall(self):
        return ConstList([mapMaker, String(u"fromColumns"),
                          ConstList([
                              ConstList(self._keys),
                              ConstList(self.d[k] for k in self._keys)])])


class FlexMap(EMapMixin, MonteObject):
    _m_fqn = "__makeMap$FlexMap"

    def __init__(self, d, keys=None, keyGuard=None, valueGuard=None):
        self.keyGuard = keyGuard
        self.valueGuard = valueGuard
        origKeys = keys
        if keys is None:
            keys = d.keys()
        if keyGuard is not None:
            keys = [keyGuard.coerce(k, null) for k in keys]
        if valueGuard is not None:
            d = dict((k, valueGuard.coerce(d[origK], null)) for k, origK in zip(keys, origKeys))
        EMapMixin.__init__(self, d, keys)


    def _printOn(self, out):
        EMapMixin._printOn(self, out)
        out.raw_print(u'.diverge()')

    def snapshot(self):
        return ConstMap(self.d.copy(), self._keys[:])

    def readOnly(self):
        raise NotImplementedError()

    def domain(self):
        raise NotImplementedError()

    def removeKeys(self, mask):
        mask = typecheck(mask, (ConstMap, FlexMap))
        for k in mask._keys:
            self.removeKey(k)

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
        if self.keyGuard is not None:
            k = self.keyGuard.coerce(k, null)
        if self.valueGuard is not None:
            v = self.valueGuard.coerce(v, null)
        self.d[k] = v
        if k not in self._keys:
            self._keys.append(k)

    def putAll(self, other):
        other = typecheck(other, (ConstMap, FlexMap))
        for k in other._keys:
            self.put(k, other.d[k])

    def _uncall(self):
        return ConstList([self.snapshot(), String(u"diverge"), ConstList([])])


class mapMaker(object):
    _m_fqn = "__makeMap"
    _m_auditorStamps = (deepFrozenGuard,)
    @staticmethod
    def fromPairs(pairs):
        from monte.runtime.guards.tables import listGuard
        return ConstMap(dict(listGuard.coerce(p.get(Integer(1)), null).l
                             for p in pairs._makeIterator()),
                        [p.get(Integer(1)).get(Integer(0)) for p in pairs._makeIterator()])

    @staticmethod
    def fromColumns(keys, vals):
        keys = typecheck(keys, (ConstList, FlexList))
        vals = typecheck(vals, (ConstList, FlexList))
        return ConstMap(dict(zip(keys.l, vals.l)), keys)
