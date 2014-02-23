from monte.runtime.base import MonteObject, throw
from monte.runtime.guards.base import Guard

class MonteBool(MonteObject):

    def __init__(self, value):
        self._b = value

    def __nonzero__(self):
        return self._b

    def __eq__(self, other):
        if not isinstance(other, MonteBool):
            return false
        return bwrap(self._b == other._b)

    def _m_and(self, other):
        if not isinstance(other, MonteBool):
            raise RuntimeError("Bools can't be compared with non-bools")
        return bwrap(self._b and other._b)

    def _m_or(self, other):
        if not isinstance(other, MonteBool):
            raise RuntimeError("Bools can't be compared with non-bools")
        return bwrap(self._b or other._b)

    def _m_not(self):
        return bwrap(not self._b)

    def xor(self, other):
        if not isinstance(other, MonteBool):
            raise RuntimeError("Bools can't be compared with non-bools")
        return bwrap(self._b != other._b)

    def __repr__(self):
        return ["false", "true"][self._b]


false = MonteBool(False)
true = MonteBool(True)

def bwrap(b):
    return true if b else false

class BooleanGuard(Guard):
    _m_fqn = "bool"
    def _subCoerce(self, specimen, ej):
        if specimen in [true, false]:
            return specimen
        elif specimen in [True, False]:
            return bwrap(specimen)
        else:
            throw.eject(ej, "%r is not a boolean" % (specimen,))

booleanGuard = BooleanGuard()
