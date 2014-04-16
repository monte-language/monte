from monte.runtime.base import throw
from monte.runtime.data import (bwrap, null, true, false, Character, Float,
                                Integer, String)
from monte.runtime.guards.base import PythonTypeGuard, Guard, PrintFQN, deepFrozenGuard


def checkNumber(other):
    if not isinstance(other, (Integer, Float)):
        raise RuntimeError("%r is not a number" % (other,))


class VoidGuard(PrintFQN, Guard):
    _m_fqn = "void"
    _m_auditorStamps = (deepFrozenGuard,)
    def _subCoerce(self, specimen, ej):
        if specimen in [None, null]:
            return specimen
        throw.eject(ej, "%r is not null" % (specimen,))

voidGuard = VoidGuard()


class BooleanGuard(PrintFQN, Guard):
    _m_fqn = "bool"
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

    def __init__(self, constraintName=None, constraintVal=None):
        super(IntegerGuard, self).__init__()
        self.constraintName = constraintName
        self.constraintVal = constraintVal

    def _subCoerce(self, specimen, ej):
        if isinstance(specimen, Integer):
            if self.constraintName == 'gt' and specimen <= self.constraintVal:
                throw.eject(ej, 'Constraint not satisfied: {0} > {1}'
                                .format(specimen, self.constraintVal))
            if self.constraintName == 'lt' and specimen >= self.constraintVal:
                throw.eject(ej, 'Constraint not satisfied: {0} < {1}'
                                .format(specimen, self.constraintVal))
            if self.constraintName == 'gte' and specimen < self.constraintVal:
                throw.eject(ej, 'Constraint not satisfied: {0} >= {1}'
                                .format(specimen, self.constraintVal))
            if self.constraintName == 'lte' and specimen > self.constraintVal:
                throw.eject(ej, 'Constraint not satisfied: {0} <= {1}'
                                .format(specimen, self.constraintVal))
            if self.constraintName == 'eq' and specimen == self.constraintVal:
                throw.eject(ej, 'Constraint not satisfied: {0} == {1}'
                                .format(specimen, self.constraintVal))

            return specimen
        else:
            throw.eject(ej, "%r is not a number")

    def op__cmp(self, other):
        if self.constraintName is not None:
            throw("Can't constrain an already constrained guard.")
        return self._IntegerGuardComparer(self, other)

    class _IntegerGuardComparer(object):
        def __init__(self, originalGuard, other):
            checkNumber(other)
            self.originalGuard = originalGuard
            self.other = other

        def belowZero(self):
            return IntegerGuard('lt', self.other)

        def atMostZero(self):
            return IntegerGuard('lte', self.other)

        def isZero(self):
            return IntegerGuard('eq', self.other)

        def atLeastZero(self):
            return IntegerGuard('gte', self.other)

        def aboveZero(self):
            return IntegerGuard('gt', self.other)

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
            throw.eject(ej, "%r is not a number")

floatGuard = FloatGuard()

charGuard = PythonTypeGuard(Character, "char")
stringGuard = PythonTypeGuard(String, "str")

