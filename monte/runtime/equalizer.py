from monte.runtime.base import MonteObject
from monte.runtime.data import null, true, false, bwrap, Integer, Float, String, Character, Bool
class Equalizer(MonteObject):
    _m_fqn = "__equalizer"
    def sameEver(self, left, right):
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

equalizer = Equalizer()

















