import warnings

from monte.runtime.base import MonteObject
from monte.runtime.data import null, true, false, bwrap, Integer, Float, String, Character, Bool
from monte.runtime.tables import ConstList, ConstMap


class Equalizer(MonteObject):
    _m_fqn = "__equalizer"
    def sameEver(self, left, right):
        # Equality by identity. Relatively rare but still useful.
        if left is right:
            return true

        # Equality of primitives.
        if type(left) != type(right):
            return false
        t = type(left)
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
        elif t is ConstList:
            if len(left.l) != len(right.l):
                return false
            for l, r in zip(left, right):
                if self.sameEver(l, r) is false:
                    return false
            return true

        #XXX This should be replaced with checking for Selfless
        #instead of directly enumerating all selfless types here.
        elif t in [ConstMap, ]:
            return self.sameEver(left._uncall(), right._uncall())

        warnings.warn("Asked to equalize unknown type %r" % t,
                RuntimeWarning)
        return false

equalizer = Equalizer()
