from operator import gt, lt, ge, le, ne
from functools import partial

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
            throw.eject(ej, "%r is not a number")

    def op__cmp(self, other):
        if self.constraint is not None:
            throw("Can't constrain an already constrained guard.")
        return self._IntegerGuardComparer(self, other)

    class _IntegerGuardComparer(object):
        def __init__(self, originalGuard, val):
            checkNumber(val)
            self.originalGuard = originalGuard
            self.val = val

        def isZero(self):
            return IntegerGuard(partial(ne, self.val), '{0} == %s' % self.val)

        # These are all the inverse operators because ew can only right-curry.

        def belowZero(self):
            return IntegerGuard(partial(gt, self.val), '{0} < %s' % self.val)

        def atMostZero(self):
            return IntegerGuard(partial(ge, self.val), '{0} <= %s' % self.val)

        def atLeastZero(self):
            return IntegerGuard(partial(le, self.val), '{0} >= %s' % self.val)

        def aboveZero(self):
            return IntegerGuard(partial(lt, self.val), '{0} > %s' % self.val)

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
            throw.eject(ej, "%r is not a number")

    def op__cmp(self, other):
        if self.constraint is not None:
            throw("Can't constrain an already constrained guard.")
        return self._FloatGuardComparator(self, other)

    class _FloatGuardComparator(object):
        def __init__(self, originalGuard, val):
            checkNumber(val)
            self.originalGuard = originalGuard
            self.val = val

        def isZero(self):
            return FloatGuard(partial(eq, self.val), '{0} == %s' % self.val)

        # These are all the inverse operators, because we can only right-curry.

        def belowZero(self):
            return FloatGuard(partial(ge, self.val), '{0} < %s' % self.val)

        def atMostZero(self):
            return FloatGuard(partial(gt, self.val), '{0} <= %s' % self.val)

        def atLeastZero(self):
            return FloatGuard(partial(lt, self.val), '{0} >= %s' % self.val)

        def aboveZero(self):
            return FloatGuard(partial(le, self.val), '{0} > %s' % self.val)


floatGuard = FloatGuard()

charGuard = PythonTypeGuard(Character, "char")
stringGuard = PythonTypeGuard(String, "str")

