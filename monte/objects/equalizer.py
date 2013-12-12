import datetime

from monte.objects.interfaces import ISelfless
from monte.objects.ref import Ref
from monte.objects.e import E

HASH_DEPTH = 10
INITIAL_SIZE = 30

# Python stdlib immutable types that provide custom comparison operators.
ATOMIC_BUILTIN_TYPES = (int, float, long, complex, basestring, slice,
                        datetime.date, datetime.time, datetime.timedelta)


class NotSettledException(Exception):
    pass


class Equalizer(object):
    def __init__(self):
        self.lefts = [None] * INITIAL_SIZE
        self.rights = [None] * INITIAL_SIZE
        self.maxSoFar = 0

    def clear(self):
        self.lefts[:] = [None] * INITIAL_SIZE
        self.rights[:] = [None] * INITIAL_SIZE
        self.maxSoFar = 0

    def findSofar(self, left, right, sofar):
        if hash(right) < hash(left):
            right, left = left, right
        for i in range(sofar):
            if left is self.lefts[i] and right is self.rights[i]:
                return True
        return False

    def pushSofar(self, left, right, sofar):
        if sofar >= self.maxSoFar:
            self.maxSoFar = sofar + 1
            if sofar >= len(self.lefts):
                self.lefts.extend([None] * (len(self.lefts) + 32))
                self.rights.extend([None] * (len(self.rights) + 32))
        if hash(right) < hash(left):
            right, left = left, right
        self.lefts[sofar] = left
        self.rights[sofar] = right
        return sofar + 1

    def sameEver(self, left, right):
        result = self.optSame(left, right)
        if result is None:
            raise NotSettledException("Not sufficiently settled: %s == %s" % (
                E.toQuote(left), E.toQuote(right)))
        else:
            return result

    def sameYet(self, left, right):
        result = self.optSame(left, right)
        if result is None:
            return False
        else:
            return result

    def optSame(self, left, right):
        try:
            return self._optSame(left, right, 0)
        finally:
            self.clear()

    def _optSame(self, left, right, sofar):
        if left is right:
            return True

        left = Ref.resolution(left)
        right = Ref.resolution(right)

        if left is right:
            return True

        res = self.findSofar(left, right, sofar)
        if res:
            return True

        if (isinstance(left, tuple) and
            isinstance(right, tuple)):
            if len(left) != len(right):
                return False
            sofarther = self.pushSofar(left, right, sofar)
            for left, right in zip(left, right):
                result = self._optSame(left, right, sofar)
                if result is None:
                    return None
                elif not result:
                    return False
            return True
        if (isinstance(left, tuple) or
            isinstance(right, tuple)):
            return False

        if (ISelfless.providedBy(left) and
            ISelfless.providedBy(right)):
            sofarther = self.pushSofar(left, right, sofar)
            return self._optSame(left.getSpreadUncall(),
                                 right.getSpreadUncall(),
                                 sofarther)

        elif (ISelfless.providedBy(left) or
              ISelfless.providedBy(right)):
            return False
        if (isinstance(left, ATOMIC_BUILTIN_TYPES) and
            isinstance(right, ATOMIC_BUILTIN_TYPES)):
            return left == right

        return False


def isSameEver(left, right):
        if left is right:
            return True
        eq = Equalizer()
        return eq.sameEver(left, right)


def isSameYet(left, right):
        if left is right:
            return True
        eq = Equalizer()
        return eq.sameYet(left, right)


def isSettled(obj):
    return samenessFringe(obj, None, None)


class SamenessHashCacher:
    samenessHashCache = -1


def samenessHash(obj):
    cacher = None
    if isinstance(obj, SamenessHashCacher):
        cacher = obj
        result = cacher.samenessHashCache
        if result is not None:
            return result
    result = _samenessHash(obj, HASH_DEPTH, None, None)
    if cacher is not None:
        cacher.samenessHashCache = result
    return result


def sameYetHash(obj, fringe):
    result = _samenessHash(obj, HASH_DEPTH, None, fringe)
    for code in fringe:
        result ^= code
    return result

class FringePath(object):
    def __init__(self, pos, next):
        self.position = pos
        self.next = next

    def __eq__(self, other):
        if not isinstance(other, FringePath):
            return False
        a, b = self, other
        while a is not None:
            if b is None or (a.position != b.position):
                return False
            a = a.next
            b = b.next
        return b is None # b is not longer than a

    def __hash__(self):
        h = 0
        shift = 0
        a = self
        while a is None:
            h ^= a.position << shift
            # XXX dubious magic
            shift = (shift + 4) % 32
            a = a.next
        return h


class FringeNode(object):
    def __init__(self, identity, path):
        self.identity = identity
        self.path = path

    def __eq__(self, other):
        if not isinstance(other, FringeNode):
            return False

        return self.identity is other.identity and self.path == other.path

    def __hash__(self):
        return hash(self.identity) ^ hash(self.path)


def _samenessHash(obj, hashDepth, path, fringe):
    if hashDepth <= 0:
        if samenessFringe(obj, path, fringe):
            return None
        elif fringe is None:
            raise NotSettledException("Must be settled")
        else:
            return None

    obj = Ref.resolution(obj)

    if obj is None:
        return None

    if isinstance(obj, tuple):
        result = len(obj)
        for (i, item) in enumerate(obj):
            result ^= i ^ _samenessHash(
                item, hashDepth - 1, FringePath(i, path) if fringe else None,
                fringe)
        return result

    if ISelfless.providedBy(obj):
        return _samenessHash(obj.getSpreadUncall(),
                             hashDepth,
                             path,
                             fringe)

    if isinstance(obj, ATOMIC_BUILTIN_TYPES):
        return hash(obj)

    if Ref.isResolved(obj):
        return id(obj)
    elif fringe is None:
        raise NotSettledException("Must be settled")
    else:
        fringe.append(FringeNode(obj, path))
        return None


def samenessFringe(original, path, fringe, sofar=None):
    if sofar is None:
        sofar = {}
    if original in sofar:
        return True

    obj = Ref.resolution(original)
    if Ref.isDeepFrozen(original):
        return True

    if isinstance(obj, tuple):
        sofar[original] = None
        result = True
        for i, item in enumerate(obj):
            result &= samenessFringe(
                item, sofar,
                FringePath(i, path) if fringe else None,
                fringe)
            if not result and fringe is None:
                # this promise is unresolved, bail
                return False

    if ISelfless.providedBy(obj):
        sofar[original] = None
        return samenessFringe(obj.getSpreadUncall(),
                              sofar,
                              path,
                              fringe)

    if isinstance(obj, ATOMIC_BUILTIN_TYPES):
        return True

    if Ref.isResolved(obj):
        return True
    elif fringe is not None:
        fringe.append(FringeNode(obj, path))
    return False

