from terml.parser import parseTerm

_absent = object()

class MonteObject(object):
    _m_matcherNames = ()
    def _m_audit(self, auditors):
        expr = parseTerm(self._m_objectExpr.decode('base64').decode('zlib'))
        for auditor in auditors:
            pass

    def _m_guardMethods(self, guards):
        self._m_methodGuards = guards

    def _m_guardForMethod(self, name):
        return self._m_methodGuards[name]

    def _m_install(self, name, slot):
        self.__class__.__dict__[name] = _SlotDescriptor(slot)

    def __mul__(self, other):
        return self.multiply(other)

    def __div__(self, other):
        return self.approxDivide(other)

    def __floordiv__(self, other):
        return self.floorDivide(other)

    def __mod__(self, other):
        return self.mod(other)

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.subtract(other)

    def __lshift__(self, other):
        return self.shiftLeft(other)

    def __rshift__(self, other):
        return self.shiftRight(other)

    def __cmp__(self, other):
        return self.op__cmp(other)

    def __eq__(self, other):
            return equalizer.sameEver(self, other)

    def __hash__(self):
        if Selfless.stamped(self):
            return hash(self.getSpreadUncall())
        else:
            return id(self)

    def __getattr__(self, verb):
        if self._m_matcherNames:
            return _MonteMatcher(self, verb)
        else:
            raise AttributeError(verb)


class _MonteMatcher(object):
    def __init__(self, obj, verb):
        self.obj = obj
        self.verb = verb

    def __call__(self, *a):
        for name in self.obj._m_matcherNames:
            try:
                return getattr(self.obj, name)([self.verb, a])
            except _MatchFailure, e:
                continue
        raise e


class _SlotDescriptor(object):

    def __init__(self, slot):
        self.slot = slot

    def __get__(self):
        return self.slot.get()

    def __put__(self, val):
        return self.slot.put(val)


def wrap(pyobj):
    if isinstance(pyobj, str):
        return Bytes(pyobj)
    if isinstance(pyobj, unicode):
        return String(pyobj)
    if isinstance(pyobj, int):
        return EInt(pyobj)
    if isinstance(pyobj, float):
        return EFloat64(pyobj)
    if isinstance(pyobj, list):
        return FlexList(pyobj)
    if isinstance(pyobj, tuple):
        return List(pyobj)
    if isinstance(pyobj, dict):
        # probably need to make it flex here since other python code
        # can mutate it and we don't want surprises
        return FlexMap(pyobj)
    if isinstance(pyobj, set):
        return FlexSet(pyobj)
    if isinstance(pyobj, frozenset):
        return Set(pyobj)


def getGuard(o, name):
    """
    Returns the guard object for a name in a Monte object's frame.
    """


def getBinding(o, name):
    """
    Returns the binding object for a name in a Monte object's frame.
    """


def reifyBinding(slot):
    """
    Create a binding object from a slot object.
    """


class MonteEjection(Exception):
    pass


def throw(val):
    raise RuntimeError(val)


def ejector(name):
    class ejtype(MonteEjection):
        name = name
        pass

    def eject(val):
        raise ejtype(val)
    eject._m_type = ejtype

    return eject


class StaticContext(object):

    def __init__(self, fqn, fields, objectExpr):
        self.fqn = fqn
        self.fields = fields
        self.objectExpr = objectExpr


class FinalSlot(object):
    def __init__(self, guard, val, ej):
        self.guard = guard
        if self.guard is not None:
            self.val = self.guard.coerce(self.val, ej)
        else:
            self.val = val

    def get(self):
        return self.val


class VarSlot(object):
    def __init__(self, guard, val=_absent, ej=None):
        self.guard = guard
        if val is not _absent:
            self._m_init(val, ej)

    def _m_init(self, val, ej):
        if self.guard is not None:
            self.val = self.guard.coerce(self.val, ej)
        else:
            self.val = val

    def get(self):
        return self.val

    def put(self, val):
        if self.guard is not None:
            self.val = self.guard.coerce(self.val, throw)
        else:
            self.val = val


def slotFromBinding(b):
    pass


def wrapEjector(e):
    def ej(val):
        e(val)
        raise RuntimeError("Ejector did not exit")
    return ej


class _MatchFailure(Exception):
    pass


def matcherFail(v):
    raise _MatchFailure(v)
