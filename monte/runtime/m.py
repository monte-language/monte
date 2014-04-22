from monte.runtime.base import MonteObject, toString, toQuote
from monte.runtime.data import String

class M(MonteObject):

    def __init__(self, vat):
        self.vat = vat

    def call(self, obj, verb, arglist):
        return getattr(obj, verb)(*arglist)

    def callWithPair(self, obj, (verb, arglist)):
        #XXX typecheck
        return getattr(obj, verb.s)(*arglist.l)

    def send(self, obj, verb, arglist):
        return self.vat.send(obj, verb, arglist)

    def sendOnly(self, obj, verb, arglist):
        # XXX optimize
        return self.send(obj, verb, arglist)

    def toString(self, obj):
        # XXX use TextWriter.print
        return String(toString(obj))

    def toQuote(self, obj):
        return String(toQuote(obj))
