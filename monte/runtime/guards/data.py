from operator import gt, lt, ge, le, ne
from functools import partial

from monte.runtime.base import throw
from monte.runtime.data import (bwrap, null, true, false, Bytestring, Character,
                                Float, Integer, String, Twine)
from monte.runtime.guards.base import (PythonTypeGuard, Guard, PrintFQN,
                                       deepFrozenGuard)


class VoidGuard(PrintFQN, Guard):
    _m_fqn = "void"
    _m_auditorStamps = (deepFrozenGuard,)
    def _subCoerce(self, specimen, ej):
        if specimen in [None, null]:
            return specimen
        throw.eject(ej, "%r is not null" % (specimen,))

voidGuard = VoidGuard()


class BooleanGuard(PrintFQN, Guard):
    _m_fqn = "boolean"
    _m_auditorStamps = (deepFrozenGuard,)
    def _subCoerce(self, specimen, ej):
        if specimen is true or specimen is false:
            return specimen
        elif specimen in [True, False]:
            import pdb; pdb.set_trace()
            raise ValueError("yer doin it wrong")
        else:
            throw.eject(ej, "%r is not a boolean" % (specimen,))

booleanGuard = BooleanGuard()


class IntegerGuard(PrintFQN, Guard):
    _m_fqn = "int"
    _m_auditorStamps = (deepFrozenGuard,)

    def _subCoerce(self, specimen, ej):
        if isinstance(specimen, Integer):
            return specimen
        else:
            throw.eject(ej, "%r is not a number" % (specimen,))

intGuard = IntegerGuard()


class FloatGuard(PrintFQN, Guard):
    _m_fqn = "float"
    _m_auditorStamps = (deepFrozenGuard,)

    def _subCoerce(self, specimen, ej):
        if isinstance(specimen, Integer):
            return Float(specimen.n)
        elif isinstance(specimen, Float):
            return specimen
        else:
            throw.eject(ej, "%r is not a number" % (specimen,))


floatGuard = FloatGuard()

charGuard = PythonTypeGuard(Character, "char")
stringGuard = PythonTypeGuard(Twine, "Str")
twineGuard = PythonTypeGuard(Twine, "Str")
bytesGuard = PythonTypeGuard(Bytestring, "Bytes")
