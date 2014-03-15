import warnings

from monte.runtime.base import MonteObject, toQuote
from monte.runtime.data import null, true, false, bwrap, Integer, Float, String, Character, Bool
from monte.runtime.tables import ConstList, ConstMap


def _findSofar(left, right, sofar):
    lid, rid = id(left), id(right)
    if rid < lid:
        lid, rid = rid, lid
    return bwrap((lid, rid) in sofar)

def _pushSofar(left, right, sofar):
    lid, rid = id(left), id(right)
    if rid < lid:
        lid, rid = rid, lid
    sofar.append((lid, rid))


def _same(left, right, sofar):
    from monte.runtime.ref import _resolution
    left = _resolution(left)
    right = _resolution(right)

    # Equality by identity. Relatively rare but still useful.
    if left is right:
        return true

    if sofar and _findSofar(left, right, sofar):
        return true

    t = type(left)
    if t is ConstList:
        if type(right) is not ConstList:
            return false
        if len(left.l) != len(right.l):
            return false
        _pushSofar(left, right, sofar)
        for l, r in zip(left, right):
            result = _same(l, r, sofar)
            if result is null:
                return null
            if result is false:
                return false
        return true

    #XXX This should be replaced with checking for Selfless
    #instead of directly enumerating all selfless types here.
    if t in [ConstMap, ] and type(right) is t:
        return _same(left._uncall(), right._uncall(), sofar)

    # Equality of primitives.
    if type(left) != type(right):
        return false
    if left in (null, true, false):
        return bwrap(left is right)
    if t in (Integer, Float):
        return bwrap(left.n == right.n)
    elif t is Bool:
        return bwrap(left._b == right._b)
    elif t is String:
        return bwrap(left.s == right.s)
    elif t is Character:
        return bwrap(left._c == right._c)

    warnings.warn("Asked to equalize unknown type %r" % t,
            RuntimeWarning)
    return false


class Equalizer(MonteObject):
    _m_fqn = "__equalizer"
    def sameEver(self, left, right):
        result = _same(left, right, [])
        if result is null:
            raise RuntimeError("Not sufficiently settled: %s == %s" % (
                toQuote(left), toQuote(right)))
        return result

equalizer = Equalizer()



















