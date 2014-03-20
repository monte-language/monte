from monte.runtime.base import MonteObject, toString, toQuote

class M(MonteObject):

    def call(self, obj, verb, arglist):
        return getattr(obj, verb)(*arglist)

    def callWithPair(self, obj, (verb, arglist)):
        return getattr(obj, verb)(*arglist)

    def send(self, obj, verb, arglist):
        raise NotImplementedError()

    def sendOnly(self, obj, verb, arglist):
        raise NotImplementedError()

    def toString(self, obj):
        # XXX use TextWriter.print
        return toString(obj)

    def toQuote(self, obj):
        return toQuote(obj)


theM = M()
