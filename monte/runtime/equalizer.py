import warnings

from monte.runtime.base import MonteObject, toQuote
from monte.runtime.data import (null, true, false, bwrap, Integer, Float,
                                String, Character, Bool)
from monte.runtime.guards.base import deepFrozenGuard, selflessGuard
from monte.runtime.tables import ConstList, ConstMap

def isIn(val, container):
    return any(val is x for x in container)

def _findSofar(left, right, sofar):
    lid, rid = id(left), id(right)
    if rid < lid:
        lid, rid = rid, lid
    return bwrap((lid, rid) in sofar)

def _pushSofar(left, right, sofar):
    lid, rid = id(left), id(right)
    if rid < lid:
        lid, rid = rid, lid
    sofar[(lid, rid)] = (left, right)


def _same(left, right, sofar, dbg=False):
    from monte.runtime.ref import _resolution
    left = _resolution(left)
    right = _resolution(right)

    # Equality by identity. Relatively rare but still useful.
    if left is right:
        return true

    if left is None:
        return bwrap(right is None)

    if sofar and _findSofar(left, right, sofar):
        return true

    t = type(left)
    if t is ConstList:
        if type(right) is not ConstList:
            return false
        if len(left.l) != len(right.l):
            return false
        _pushSofar(left, right, sofar)
        for l, r in zip(left, right):
            result = _same(l, r, sofar, dbg)
            if result is null:
                return null
            if result is false:
                return false
            if result is not true:
                import pdb; pdb.set_trace()
        return true

    if t in DOES_OWN_HASHING:
        return left == right

    if (isIn(selflessGuard, getattr(left, '_m_auditorStamps', ())) and
        isIn(selflessGuard, getattr(right, '_m_auditorStamps', ()))):
        _pushSofar(left, right, sofar)
        return _same(left._uncall(), right._uncall(), sofar)

    # Equality of primitives.
    if type(left) != type(right):
        return false
    if left in (null, true, false):
        return bwrap(left is right)
    if t in (Integer, Float):
        return bwrap(left.n == right.n)
    elif t is Bool:
        return bwrap(left._b == right._b)
    elif t is String: # Other Twines have uncall methods.
        return bwrap(left.s == right.s)
    elif t is Character:
        return bwrap(left._c == right._c)

    warnings.warn("Asked to equalize unknown type %r" % t,
                  RuntimeWarning)
    return false


class Equalizer(MonteObject):
    _m_fqn = "__equalizer"
    _m_auditorStamps = (deepFrozenGuard,)

    def debugSameEver(self, left, right):
        import pdb; pdb.set_trace()
        return self.sameEver(left, right, True)

    def sameEver(self, left, right, dbg=False):
        result = _same(left, right, {}, dbg)
        if result is null:
            raise RuntimeError("Not sufficiently settled: %s == %s" % (
                toQuote(left), toQuote(right)))
        return result

    def sameYet(self, left, right):
        result = _same(left, right, {})
        if result is None:
            return false
        else:
            return result

equalizer = Equalizer()

HASH_DEPTH = 10

def samenessHash(obj, hashDepth=HASH_DEPTH, path=None, fringe=None):
    from monte.runtime.ref import _isSelfless, _isResolved, _resolution
    if hashDepth <= 0:
        if samenessFringe(obj, path, fringe):
            # obj is settled.
            return -1
        elif fringe is None:
            raise RuntimeError("Must be settled")
        else:
            #obj isn't settled.
            return -1

    obj = _resolution(obj)
    if obj is null:
        return 0
    if type(obj) is ConstList:
        result = len(obj.l)
        for i, o in enumerate(obj.l):
            if fringe is None:
                fr = None
            else:
                fr = FringePath(i, path)
            result ^= i ^ samenessHash(o, hashDepth - 1, fr, fringe)
        return result

    if type(obj) in DOES_OWN_HASHING:
        return hash(obj)

    if _isSelfless(obj):
        return samenessHash(obj._uncall(), hashDepth, path, fringe)

    if _isResolved(obj):
        return id(obj)
    elif fringe is None:
        raise RuntimeError("Must be settled")
    else:
        # obj is unresolved
        fringe.append(FringeNode(obj, path))
        return -1


def sameYetHash(obj, fringe):
    result = samenessHash(obj, HASH_DEPTH, None, fringe)
    for f in fringe:
        result ^= f.hash()
    return result


def samenessFringe(original, path, fringe, sofar=None):
    from monte.runtime.ref import _isResolved, _isSelfless, _resolution, _isDeepFrozen
    if sofar is None:
        sofar = set()
    obj = _resolution(original)
    if obj is None:
        return True
    if id(original) in sofar:
        return True
    if _isDeepFrozen(original):
        return True
    if id(obj) in sofar:
        return True
    if type(obj) is ConstList:
        sofar.add(id(original))
        result = True
        for i, o in enumerate(obj.l):
            if fringe is None:
                fr = None
            else:
                fr = FringePath(i, path)
            result &= samenessFringe(o, fr, fringe, sofar)
            if (not result) and fringe is None:
                # Unresolved promise found.
                return False
        return result

    if type(obj) in DOES_OWN_HASHING:
        return True

    if _isSelfless(obj):
        sofar.add(id(original))
        return samenessFringe(obj._uncall(), sofar, path, fringe)

    if _isResolved(obj):
        return True
    else:
        if fringe is not None:
            fringe.append(FringeNode(obj, path))
        return False


class FringePath(object):
    def __init__(self, position, next):
        self.position = position
        self.next = next

    def __eq__(self, right):
        left = self
        while left is not None:
            if right is None or left.position != right.position:
                return False
            left = left.next
            right = right.next

        return right is None

    def hash(self):
        p = self
        h = 0
        shift = 0
        while p is not None:
            h ^= self.position << shift
            shift = (shift + 4) % 32
            p = p.next
        return h


class FringeNode(object):
    def __init__(self, obj, path):
        self.identity = id(obj)
        self.path = path

    def __eq__(self, other):
        return (self.identity, self.path) == (other.identity, other.path)

    def __hash__(self):
        return self.identity ^ self.path.hash()


class TraversalKey(object):
    _m_auditorStamps = (deepFrozenGuard, selflessGuard)
    def __init__(self, wrapped):
        from monte.runtime.ref import _resolution
        self.wrapped = _resolution(wrapped)
        fringeBuild = []
        self.snapHash = sameYetHash(self.wrapped, self.fringeBuild)
        self.fringe = fringeBuild

    def __eq__(self, other):
        if not isinstance(other, TraversalKey):
            return False

        if self.snapHash != other.snapHash:
            return False

        if not equalizer.sameYet(self.wrapped, other.wrapped) is true:
            return False

        if len(other.fringe) != len(self.fringe):
            return False

        return all(s == o for s, o in zip(self.fringe, other.fringe))

    def _printOn(self, out):
        out.raw_print(u'<a traversal key>')

    def __hash__(self):
        return self.snapHash


DOES_OWN_HASHING = (Integer, Float, String, Character, Bool, TraversalKey) #FarRef, DisconnectedRef, ...
