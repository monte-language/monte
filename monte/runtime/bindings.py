from monte.runtime.base import MonteObject, throw
from monte.runtime.data import null

class FinalSlot(MonteObject):
    _m_fqn = "FinalSlot"

    @classmethod
    def asType(cls):
        return FinalSlotGuard()

    def __init__(self, val, guard=null, ej=throw):
        self.guard = guard
        if self.guard is not null:
            self.val = self.guard.coerce(val, ej)
        else:
            self.val = val

    def get(self):
        return self.val

_absent = object()
class VarSlot(MonteObject):
    _m_fqn = "VarSlot"

    @classmethod
    def asType(self):
        return VarSlotGuard()

    def __init__(self, guard, val=_absent, ej=None):
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


class Binding(MonteObject):
    _m_fqn = "Binding"
    def __init__(self, slot):
        self.slot = slot

def getBinding(o, name):
    """
    Returns the binding object for a name in a Monte object's frame.
    """
    raise NotImplementedError()

def getSlot(o, name):
    raise NotImplementedError()

def reifyBinding(slot):
    """
    Create a binding object from a slot object.
    """
    return Binding(slot)


def slotFromBinding(b):
    return b.slot







