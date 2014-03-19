from monte.runtime.base import throw
from monte.runtime.data import bwrap, true, false, Character, Float, Integer, String
from monte.runtime.guards.base import PythonTypeGuard, Guard, PrintFQN

class VoidGuard(PrintFQN, Guard):
    _m_fqn = "void"

    def _subCoerce(self, specimen, ej):
        if specimen is not None:
            throw.eject(ej, "%r is not null" % (specimen,))

voidGuard = VoidGuard()


class BooleanGuard(PrintFQN, Guard):
    _m_fqn = "bool"
    def _subCoerce(self, specimen, ej):
        if specimen in [true, false]:
            return specimen
        elif specimen in [True, False]:
            return bwrap(specimen)
        else:
            throw.eject(ej, "%r is not a boolean" % (specimen,))

booleanGuard = BooleanGuard()


class IntegerGuard(PrintFQN, Guard):
    _m_fqn = "int"
    def _subCoerce(self, specimen, ej):
        if isinstance(specimen, Integer):
            return specimen
        elif isinstance(specimen, Float):
            return Integer(specimen.n)
        else:
            throw.eject(ej, "%r is not a number")

intGuard = IntegerGuard()


class FloatGuard(PrintFQN, Guard):
    _m_fqn = "float"
    def _subCoerce(self, specimen, ej):
        if isinstance(specimen, Integer):
            return Float(specimen.n)
        elif isinstance(specimen, Float):
            return specimen
        else:
            throw.eject(ej, "%r is not a number")

floatGuard = FloatGuard()

charGuard = PythonTypeGuard(Character, "char")
stringGuard = PythonTypeGuard(String, "str")

