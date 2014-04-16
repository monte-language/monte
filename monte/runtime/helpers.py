"""
Objects used by Monte syntax expansions.
"""
from monte.runtime.base import MonteObject, ejector, throw
from monte.runtime.data import true, false, null, String, Integer, bwrap
from monte.runtime.equalizer import equalizer
from monte.runtime.flow import MonteIterator
from monte.runtime.ref import UnconnectedRef
from monte.runtime.tables import ConstList, FlexList, ConstMap, FlexMap, mapMaker


def validateFor(flag):
    if not flag:
        raise RuntimeError("For-loop body isn't valid after for-loop exits.")


def accumulateList(coll, obj):
    it = coll._makeIterator()
    skip = ejector("listcomp_skip")
    ej = ejector("iteration")
    acc = []
    try:
        while True:
            try:
                key, item = it.next(ej)
                acc.append(obj.run(key, item, skip))
            except skip._m_type:
                continue
    except ej._m_type:
        pass
    finally:
        ej.disable()

    return ConstList(acc)


def accumulateMap(coll, obj):
    return mapMaker.fromPairs(accumulateList(coll, obj))


def iterWhile(f):
    return MonteIterator((null, v) for v in iter(f, false))


class Comparer(MonteObject):
    def _check(self, left, right, first, second):
        try:
            return getattr(left.op__cmp(right), first)()
        except RuntimeError:
            try:
                return getattr(right.op__cmp(left), second)()
            except RuntimeError:
                pass
            raise  # re-raise from the first except clause.

    def greaterThan(self, left, right):
        return self._check(left, right, 'aboveZero', 'atMostZero')

    def geq(self, left, right):
        return self._check(left, right, 'atLeastZero', 'belowZero')

    def lessThan(self, left, right):
        return self._check(left, right, 'belowZero', 'atLeastZero')

    def leq(self, left, right):
        return self._check(left, right, 'atMostZero', 'aboveZero')

    def asBigAs(self, left, right):
        return self._check(left, right, 'isZero', 'isZero')

comparer = Comparer()


class MakeVerbFacet(MonteObject):
    _m_fqn = "__makeVerbFacet$verbFacet"
    def curryCall(self, obj, verb):
        if not isinstance(verb, String):
            raise RuntimeError("%r is not a string" % (verb,))
        def facet(*a):
            return getattr(obj, verb.s)(*a)
        return facet

makeVerbFacet = MakeVerbFacet()


def matchSame(expected):
    def sameMatcher(specimen, ej):
        if equalizer.sameEver(specimen, expected) is true:
            return expected
        else:
            ej("%r is not %r" % (specimen, expected))
    return sameMatcher


def switchFailed(specimen, *failures):
    raise RuntimeError("%s did not match any option: [%s]" % (
        specimen,
        " ".join(str(f) for f in failures)))


_absent = object()
def suchThat(x, y=_absent):
    if y is _absent:
        # 1-arg invocation.
        def suchThatMatcher(specimen, ejector):
            if not x:
                ejector("such-that expression was false")
        return suchThatMatcher
    else:
        return ConstList([x, None])


def extract(x, instead=_absent):
    if instead is _absent:
        # 1-arg invocation.
        def extractor(specimen, ejector):
            return [specimen.fetch(x, lambda: ejector), specimen.without(x)]
        return extractor
    else:
        def extractor(specimen, ejector):
            if not isinstance(specimen, (ConstMap, FlexMap)):
                raise RuntimeError("%r is not a map" % (specimen,))
            value = specimen.d.get(x, _absent)
            if value is _absent:
                value = ConstList([instead(), specimen])
            return [value, specimen.without(x)]
        return extractor


class Empty:
    def coerce(self, specimen, ej):
        if specimen.size() == Integer(0):
            return specimen
        else:
            throw.eject(ej, "Not empty: %s" % specimen)


def splitList(cut):
    if not isinstance(cut, Integer):
        raise RuntimeError("%r is not an integer" % (cut,))
    cut = cut.n
    def listSplitter(specimen, ej):
        if not isinstance(specimen, (ConstList, FlexList)):
            throw.eject(
                ej, "Can't split non-list")
        if len(specimen.l) < cut:
            throw.eject(
                ej, "A %s size list doesn't match a >= %s size list pattern"
                    % (len(specimen), cut))
        vals = list(specimen.l[:cut])
        vals.append(ConstList(specimen.l[cut:]))
        return ConstList(vals)
    return listSplitter


class BooleanFlow(MonteObject):
    _m_fqn = "__booleanFlow"
    def __init__(self, vat):
        self.vat = vat

    def broken(self):
        return UnconnectedRef("boolean flow expression failed", self.vat)

    def failureList(self, size):
        if not isinstance(size, Integer):
            raise RuntimeError("%r is not an integer" % (size,))
        return ConstList([false] + [self.broken()] * size.n)


def makeViaBinder(resolver, guard):
    def bindit(specimen, ej):
        if guard is null:
            resolver.resolve(specimen)
        else:
            resolver.resolve(guard.coerce(specimen, ej))
    return bindit
