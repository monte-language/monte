from monte.runtime.base import MonteObject, throw
from monte.runtime.data import null
from monte.runtime.guards.base import Guard, anyGuard, deepFrozenFunc, deepFrozenGuard, isDeepFrozen, selflessGuard
from monte.runtime.tables import ConstList

class FinalSlot(MonteObject):
    _m_fqn = "FinalSlot"
    _m_auditorStamps = (deepFrozenGuard,)
    @classmethod
    def asType(cls):
        return theFinalSlotGuard

    def __init__(self, val, guard=null, ej=throw, unsafe=False):
        if guard is not null:
            self.guard = guard
            #XXX separate coercing invocations available from Monte
            #and non-coercing invocations made from compiler internals
            if unsafe:
                self.val = val
            else:
                self.val = self.guard.coerce(val, ej)
        else:
            self.guard = anyGuard
            self.val = val

    @classmethod
    def run(cls, val):
        """
        __makeFinalSlot.run(val), basically.
        """

        return cls(val)

    def getGuard(self):
        return FinalSlotGuard(self.guard)

    def get(self):
        return self.val

    def _printOn(self, out):
        out.raw_print(u'<& ')
        out._m_print(self.val)
        out.raw_print(u'>')

_absent = object()
class VarSlot(MonteObject):
    _m_fqn = "VarSlot"

    @classmethod
    def asType(self):
        return VarSlotGuard(null, maker=True)

    def __init__(self, guard, val=_absent, ej=None):
        if guard is null:
            guard = anyGuard
        self.guard = guard
        if val is not _absent:
            self._m_init(val, ej)


    def _m_init(self, val, ej):
        if self.guard is not null:
            self.val = self.guard.coerce(val, ej)
        else:
            self.val = val

    def get(self):
        return self.val

    def put(self, val):
        if self.guard is not null:
            self.val = self.guard.coerce(val, throw)
        else:
            self.val = val

    def _printOn(self, out):
        out.raw_print(u'<var ')
        out._m_print(self.val)
        out.raw_print(u'>')

class FinalSlotGuard(Guard):
    _m_fqn = "FinalSlot"
    def __init__(self, valueGuard, maker=False):
        #XXX separate guard maker from FinalSlot[any]
        self.maker = maker
        if valueGuard is null:
            valueGuard = anyGuard
        self.valueGuard = valueGuard
        if isDeepFrozen(valueGuard):
            self._m_auditorStamps = (selflessGuard, deepFrozenGuard)
        else:
            self._m_auditorStamps = (selflessGuard,)

    def getValueGuard(self):
        return self.valueGuard

    def get(self, valueGuard):
        if self.maker:
            return FinalSlotGuard(valueGuard)
        else:
            raise RuntimeError("no method 'get'")

    def _subCoerce(self, specimen, ej):

        if isinstance(specimen, FinalSlot) and self.valueGuard == specimen.valueGuard:
            if (self.valueGuard is null or
                self.valueGuard.supersetOf(specimen.valueGuard) or
                self.valueGuard == specimen.valueGuard):
                return specimen
        throw.eject(ej, "is not a %s" % (self,))

    def _uncall(self):
        return ConstList([ConstList([FinalSlot, "asType", ConstList([])]), "get", self.valueGuard])

    def _printOn(self, out):
        out.raw_print(u'FinalSlot[')
        out._m_print(self.valueGuard)
        out.raw_print(u']')

theFinalSlotGuard = FinalSlotGuard(null, maker=True)

class VarSlotGuard(Guard):
    _m_fqn = "VarSlot"
    _m_auditorStamps = (selflessGuard, deepFrozenGuard)
    def __init__(self, valueGuard, maker=False):
        #XXX separate guard maker from FinalSlot[any]
        self.maker = maker
        if valueGuard is null:
            valueGuard = anyGuard
        self.valueGuard = valueGuard

    def getValueGuard(self):
        return self.valueGuard

    def get(self, valueGuard):
        if self.maker:
            return VarSlotGuard(valueGuard)
        else:
            raise RuntimeError("no method 'get'")

    def _subCoerce(self, specimen, ej):

        if isinstance(specimen, VarSlot) and self.valueGuard == specimen.valueGuard:
            if (self.valueGuard.supersetOf(specimen.valueGuard) or
                self.valueGuard == specimen.valueGuard):
                return specimen
        throw.eject(ej, "is not a %s" % (self,))

    def _uncall(self):
        return ConstList([ConstList([VarSlot, "asType", ConstList([])]), "get", self.valueGuard])

    def _printOn(self, out):
        out.raw_print(u'VarSlot[')
        out._m_print(self.valueGuard)
        out.raw_print(u']')


class Binding(MonteObject):
    _m_fqn = "Binding"
    def __init__(self, slot, guard):
        self.slot = slot
        self.guard = guard

    def get(self):
        return self.slot

    def getGuard(self):
        return self.guard

    def put(self, o):
        raise RuntimeError("Not an assignable slot: %r" % (self,))

    def _printOn(self, out):
        out.raw_print(u'<&& ')
        out._m_print(self.slot)
        out.raw_print(u': ')
        out.m_print(self.guard)
        out.raw_print(u'>')


def getBinding(o, name):
    """
    Returns the binding object for a name in a Monte object's frame.
    """
    return Binding(*o._m_slots[name])

def getSlot(o, name):
    raise NotImplementedError()

@deepFrozenFunc
def reifyBinding(arg, ej=_absent):
    """
    Create a binding object from a slot object.
    """
    if ej is _absent:
        def guardedSlotToBinding(specimen, ejector):
            return Binding(arg.coerce(specimen, ejector), arg)
        return guardedSlotToBinding
    else:
        return Binding(arg, anyGuard)

@deepFrozenFunc
def slotFromBinding(b):
    return b.slot
