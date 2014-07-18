from monte.runtime.base import MonteObject, toString, toQuote
from monte.runtime.data import String, Twine, unicodeFromTwine
from monte.runtime.tables import ConstList, FlexList
from monte.runtime.guards.base import deepFrozenGuard

class M(MonteObject):
    _m_fqn = "M"
    _m_auditorStamps = (deepFrozenGuard,)
    def call(self, obj, verb, arglist):
        return getattr(obj, verb)(*arglist)

    def callWithPair(self, obj, (verb, arglist)):
        if not isinstance(verb, Twine):
            raise RuntimeError("%r is not a string" % (verb,))
        if not isinstance(arglist, (FlexList, ConstList)):
            raise RuntimeError("%r is not a list" % (arglist,))
        return getattr(obj, unicodeFromTwine(verb))(*arglist.l)

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
