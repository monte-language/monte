from monte.runtime.base import throw
from monte.runtime.data import true
from monte.runtime.guards.base import Guard, anyGuard
from monte.runtime.tables import ConstList, ConstMap

class _ConstListGuard(Guard):
    _m_fqn = "ConstList"

    def _subCoerce(self, specimen, ej):
        if isinstance(specimen, ConstList):
            if self.elementGuard is anyGuard:
                return specimen
            else:
                for i, v in enumerate(specimen.l):
                    coerced = self.elementGuard.coerce(v, ej)
                    if coerced is v:
                        continue
                    else:
                        remainder = tuple([self.elementGuard.coerce(x, ej)
                                     for x in specimen.l[i:]])
                        return ConstList(specimen.l[:i] + remainder)
                return specimen
        else:
            throw.eject(ej, "is not a ConstList")

class ConstListGuard(_ConstListGuard):
    def __init__(self):
        self.elementGuard = anyGuard

    def supersetOf(self, guard):
        if isinstance(guard, ConstListGuard):
            return true

    def get(self, eg):
        return SpecializedConstListGuard(eg)

class SpecializedConstListGuard(_ConstListGuard):
    _m_fqn = "ConstList$SpecializedConstList"
    def __init__(self, elementGuard):
        self.elementGuard = elementGuard

listGuard = ConstListGuard()

class _ConstMapGuard(Guard):
    _m_fqn = "ConstMap"

    def _subCoerce(self, specimen, ej):
        if isinstance(specimen, ConstMap):
            if self.keyGuard is anyGuard and self.valueGuard is anyGuard:
                return specimen
            else:
                d = {}
                ks = []
                for i, k in enumerate(specimen._keys):
                    coercedK = self.keyGuard.coerce(k, ej)
                    coercedV = self.valueGuard.coerce(specimen.d[k], ej)
                    ks.append(coercedK)
                    d[coercedK] = coercedV
                return ConstMap(d, ks)
        else:
            throw.eject(ej, "is not a ConstMap")

class ConstMapGuard(_ConstMapGuard):
    def __init__(self):
        self.keyGuard = anyGuard
        self.valueGuard = anyGuard

    def supersetOf(self, guard):
        if isinstance(guard, ConstMapGuard):
            return true

    def get(self, kg, vg):
        return SpecializedConstMapGuard(kg, vg)

class SpecializedConstMapGuard(_ConstMapGuard):
    _m_fqn = "ConstMap$SpecializedConstMap"

    def __init__(self, keyGuard, valueGuard):
        self.keyGuard = keyGuard
        self.valueGuard = valueGuard


mapGuard = ConstMapGuard()
