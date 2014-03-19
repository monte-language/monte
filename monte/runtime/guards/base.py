from monte.runtime.base import MonteObject, ejector, throw
from monte.runtime.data import true, false

class PrintFQN(object):
    def _printOn(self, out):
        out._m_print(self._m_fqn)

class Guard(MonteObject):
    def coerce(self, specimen, ej):
        from monte.runtime.ref import _resolution
        specimen = _resolution(specimen)
        tryej = ejector("coercion")
        try:
            return self._subCoerce(specimen, tryej)
        except tryej._m_type, p:
            problem = p.args[0]
        finally:
            tryej.disable()
        conform = getattr(specimen, '_conformTo', None)
        if conform is not None:
            newspec = conform(self)
            if newspec is not specimen:
                return self._subCoerce(newspec, ej)
        throw.eject(ej, problem)

    def supersetOf(self, other):
        return false


class PythonTypeGuard(PrintFQN, Guard):
    def __init__(self, typ, name):
        self.typ = typ
        self._m_fqn = name
    def _subCoerce(self, specimen, ej):
        if isinstance(specimen, self.typ):
            return specimen
        else:
            throw.eject(ej, "is not a %s" % (self.typ,))


class AnyGuard(PrintFQN, MonteObject):
    _m_fqn = "any"
    def coerce(self, specimen, ej):
        return specimen

    def get(self, *guards):
        if not guards:
            raise RuntimeError("unneeded any[]")
        return UnionGuard(guards)

    def supersetOf(self, other):
        return true

anyGuard = AnyGuard()


class UnionGuard(MonteObject):
    _m_fqn = "any$UnionGuard"
    def __init__(self, guards):
        self.guards = guards

    def _printOn(self, out):
        #XXX pretty printing would be nice here too
        out.raw_print(u'any[')
        it = iter(self.guards)
        out.quote(next(it))
        for g in it:
            out.raw_print(u', ')
            out.quote(g)
        out.raw_print(u']')

    def coerce(self, specimen, ej):
        cej = ejector("next")
        for guard in self.guards:
            try:
                return guard.coerce(specimen, cej)
            except cej._m_type:
                continue
        throw.eject(ej, "doesn't match any of %s" % (self.guards,))

    def supersetOf(self, other):
        for g in self.guards:
            if other == g or g.supersetOf(other):
                return true
        return false


class SelflessGuard(Guard):
    def _subCoerce(self, specimen, ej):
        if not selflessGuard in specimen._m_auditorStamps:
            throw.eject(ej, "is not Selfless")

selflessGuard = SelflessGuard()

