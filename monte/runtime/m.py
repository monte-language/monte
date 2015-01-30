from monte.runtime.base import MonteObject, toString, toQuote, throw
from monte.runtime.data import String
from monte.runtime.guards.base import deepFrozenGuard
from monte.runtime.guards.data import twineGuard
from monte.runtime.guards.tables import listGuard

class M(MonteObject):
    _m_fqn = "M"
    _m_auditorStamps = (deepFrozenGuard,)

    def call(self, obj, verb, arglist):
        return getattr(obj, verb)(*arglist)

    def callWithPair(self, obj, (verb, arglist)):
        verb = twineGuard.coerce(verb, throw)
        arglist = listGuard.coerce(arglist, throw)
        return getattr(obj, verb.bare().s)(*arglist.l)

    def send(self, obj, verb, arglist):
        raise NotImplementedError()

    def sendOnly(self, obj, verb, arglist):
        raise NotImplementedError()

    def toString(self, obj):
        # XXX use TextWriter.print
        return String(toString(obj))

    def toQuote(self, obj):
        return String(toQuote(obj))


theM = M()
