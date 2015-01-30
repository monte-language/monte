"""
Bottom level of Monte runtime object support.
"""
import StringIO

from monte import ast

class _SlotDescriptor(object):

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, typ):
        return obj._m_slots[self.name][0].get()

    def __set__(self, obj, val):
        return obj._m_slots[self.name][0].put(val)


class MonteObject(object):
    _m_matcherNames = ()
    _m_auditorStamps = ()
    _m_auditorCache = None
    _m_fqn = "<no name>"
    def __init__(self):
        self._m_slots = {}

    def _conformTo(self, guard):
        return self

    def _m_audit(self, auditors, scope):
        if self.__class__._m_auditorCache is None:
            self.__class__._m_auditorCache = {}
        from monte.runtime.audit import Audition
        expr = ast.load(self._m_objectExpr)
        bindingGuards = dict([(k, v[1]) for k, v in self._m_slots.iteritems()])
        bindingGuards.update(self._m_outers)
        audition = Audition(
            self._m_fqn,
            expr,
            bindingGuards,
            self,
            scope.keys(),
            self.__class__._m_auditorCache)
        for auditor in auditors:
            audition.ask(auditor)
        audition._active = False
        self._m_auditorStamps = audition.approvers

    def _m_guardMethods(self, guards):
        self._m_methodGuards = guards

    def _m_guardForMethod(self, name):
        return self._m_methodGuards[name]

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
        return self.op__cmp(other).n

    def __eq__(self, other):
        from monte.runtime.equalizer import equalizer
        return equalizer.sameEver(self, other)

    def __hash__(self):
        from monte.runtime.equalizer import samenessHash
        return samenessHash(self)

    def __getattr__(self, verb):
        if self._m_matcherNames:
            return _MonteMatcher(self, verb)
        else:
            # Has to be AttributeError because some Python code might use getattr()
            raise AttributeError("No such method: %s.%s()" % (self._m_fqn, verb))

    def __call__(self, *args):
        return self.run(*args)

    def _printOn(self, out):
        out.raw_print(u'<')
        out.raw_print(self._m_fqn)
        out.raw_print(u'>')

    def __repr__(self):
        return "<m: %s>" % (toString(self),)

    def __str__(self):
        return toString(self)

    def __iter__(self):
        for pair in self._makeIterator():
            from monte.runtime.data import Integer
            yield pair.get(Integer(1))


def toString(obj):
    from monte.runtime.text import TextWriter
    out = StringIO.StringIO()
    t = TextWriter(out)
    t._m_print(obj)
    return out.getvalue().decode('utf-8')

def toQuote(obj):
    from monte.runtime.text import TextWriter
    out = StringIO.StringIO()
    t = TextWriter(out)
    t.quote(obj)
    return out.getvalue().decode('utf-8')


class _MatchFailure(Exception):
    pass


class _MonteMatcher(object):
    def __init__(self, obj, verb):
        self.obj = obj
        self.verb = verb

    def __call__(self, *a):
        from monte.runtime.data import String
        from monte.runtime.tables import ConstList
        for name in self.obj._m_matcherNames:
            try:
                return getattr(self.obj, name)([String(self.verb.decode('ascii')), ConstList(a)])
            except _MatchFailure, e:
                continue
        raise e


class MonteEjection(BaseException):
    pass


def wrapEjector(e):
    from monte.runtime.data import null
    def ej(val=null):
        e(val)
        raise RuntimeError("Ejector did not exit")
    return ej


def ejector(_name):
    from monte.runtime.data import null
    class ejtype(MonteEjection):
        name = _name
        pass
    class ej(MonteObject):
        _m_fqn = "Ejector"
        _m_type = ejtype
        _m_active = True

        def __call__(self, val=null):
            if not self._m_active:
                throw("Ejector is not active")
            raise ejtype(val)

        def disable(self):
            self._m_active = False

    return ej()


class Throw(MonteObject):
    _m_fqn = "throw"
    ## This is patched later to avoid import circularity
    #_m_auditorStamps = (deepFrozenGuard,)
    def __call__(self, val):
        from monte.runtime.data import Twine
        from monte.runtime.ref import _resolution
        val = _resolution(val)
        if isinstance(val, Twine):
            val = val.bare().s
        raise RuntimeError(val)
    def eject(self, ej, val):
        from monte.runtime.data import null
        if ej is null:
            throw(val)
        else:
            wrapEjector(ej)(val)

throw = Throw()
