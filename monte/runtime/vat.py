from collections import deque

from monte.runtime.helpers import BooleanFlow
from monte.runtime.m import M
from monte.runtime.ref import _makePromise, RefOps
from monte.runtime.scope import safeScope
from monte.runtime.load import monteImport


class Vat(object):
    """
    A container which contains some objects and is aware of pending calls to
    be made to objects within its domain.
    """

    def __init__(self, reactor):
        self.reactor = reactor
        self.pending = deque()

    def send(self, obj, verb, args):
        promise, resolver = _makePromise(self)
        self.pending.append((resolver, obj, verb.s, args))
        return promise

    # XXX boooo
    sendAll = sendAllOnly = sendOnly = send

    def hasTurns(self):
        return bool(self.pending)

    def turn(self):
        resolver, obj, verb, args = self.pending.popleft()
        resolver.resolve(getattr(obj, verb)(*args))


def createVatScope(vat, scope):
    # __booleanFlow
    scope["__booleanFlow"] = BooleanFlow(vat)

    # M: Flow control and string formation
    scope["M"] = M(vat)

    # Ref: Primitive reference operations
    scope["Ref"] = RefOps(vat)

    # import: Simple code loading
    scope["import"] = monteImport(vat)

    vat.scope = scope
