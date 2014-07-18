from operator import gt, lt, ge, le, ne
from functools import partial

from monte.runtime.base import throw
from monte.runtime.data import (bwrap, null, true, false, Character, Float,
                                Integer, Twine)
from monte.runtime.guards.base import PythonTypeGuard, Guard, PrintFQN, deepFrozenGuard


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
        if specimen in [true, false]:
            return specimen
        elif specimen in [True, False]:
            return bwrap(specimen)
        else:
            throw.eject(ej, "%r is not a boolean" % (specimen,))

booleanGuard = BooleanGuard()


class IntegerGuard(PrintFQN, Guard):
    _m_fqn = "int"
    _m_auditorStamps = (deepFrozenGuard,)

    def __init__(self, constraint=None, constraintMessage=''):
        super(IntegerGuard, self).__init__()
        self.constraint = constraint
        self.constraintMessage = constraintMessage

    def _subCoerce(self, specimen, ej):
        if isinstance(specimen, Integer):
            if self.constraint is not None and not self.constraint(specimen):
                throw.eject(ej, 'Constraint not satisfied: ' +
                                self.constraintMessage.format(specimen))
            return specimen
        else:
            throw.eject(ej, "%r is not a number" % (specimen,))

intGuard = IntegerGuard()


class FloatGuard(PrintFQN, Guard):
    _m_fqn = "float"
    _m_auditorStamps = (deepFrozenGuard,)

    def __init__(self, constraint=None, constraintMessage=''):
        super(FloatGuard, self).__init__()
        self.constraint = constraint
        self.constraintMessage = constraintMessage

    def _subCoerce(self, specimen, ej):
        if self.constraint is not None and not self.constraint(specimen):
            throw.eject(ej, 'Constraint not satisfied: ' +
                            self.constraintMessage.format(specimen))

        if isinstance(specimen, Integer):
            return Float(specimen.n)
        elif isinstance(specimen, Float):
            return specimen
        else:
            throw.eject(ej, "%r is not a number" % (specimen,))


floatGuard = FloatGuard()

charGuard = PythonTypeGuard(Character, "char")
stringGuard = PythonTypeGuard(Twine, "str")

