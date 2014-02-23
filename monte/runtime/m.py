from monte.runtime.base import MonteObject

class M(MonteObject):

    def call(self, obj, verb, arglist):
        return getattr(obj, 'verb')(arglist)

    def callWithPair(self, obj, (verb, arglist)):
        return getattr(obj, 'verb')(arglist)

    def send(self, obj, verb, arglist):
        raise NotImplementedError()

    def sendOnly(self, obj, verb, arglist):
        raise NotImplementedError()

    def toString(self, obj):
        # XXX use TextWriter.print
        return str(obj).decode('ascii')

    def toQuote(self, obj):
        # XXX use TextWriter.quote
        return "'%s'" % (str(obj).decode('ascii').encode('unicode-escape'),)


theM = M()
