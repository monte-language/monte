import linecache, sys, uuid
from types import ModuleType as module

from terml.parser import parseTerm
from monte.compiler import ecompile

_absent = object()

class MonteObject(object):
    _m_matcherNames = ()
    def _conformTo(self, guard):
        return self

    def _m_audit(self, auditors):
        expr = parseTerm(self._m_objectExpr.decode('base64').decode('zlib'))
        for auditor in auditors:
            pass

    def _m_guardMethods(self, guards):
        self._m_methodGuards = guards

    def _m_guardForMethod(self, name):
        return self._m_methodGuards[name]

    def _m_install(self, name, slot):
        setattr(self.__class__, name, _SlotDescriptor(slot))

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
        return self.op__cmp(other)

    def __eq__(self, other):
        raise NotImplementedError()
        return equalizer.sameEver(self, other)

    def __hash__(self):
        raise NotImplementedError()
        if Selfless.stamped(self):
            return hash(self.getSpreadUncall())
        else:
            return id(self)

    def __getattr__(self, verb):
        if self._m_matcherNames:
            return _MonteMatcher(self, verb)
        else:
            raise AttributeError(verb)

    def __call__(self, *args):
        return self.run(*args)


class _MonteMatcher(object):
    def __init__(self, obj, verb):
        self.obj = obj
        self.verb = verb

    def __call__(self, *a):
        for name in self.obj._m_matcherNames:
            try:
                return getattr(self.obj, name)([self.verb, a])
            except _MatchFailure, e:
                continue
        raise e


class _SlotDescriptor(object):

    def __init__(self, slot):
        self.slot = slot

    def __get__(self, obj, typ):
        return self.slot.get()

    def __set__(self, obj, val):
        return self.slot.put(val)


class MonteInt(int):
    def add(self, other):
        return MonteInt(self + other)
    def subtract(self, other):
        return MonteInt(self - other)
    def multiply(self, other):
        return MonteInt(self * other)
    def approxDivide(self, other):
        return MonteInt(int.__truediv__(self, other))
    def floorDivide(self, other):
        return MonteInt(int.__floordiv__(self, other))
    shiftLeft = int.__lshift__
    shiftRight = int.__rshift__
    mod = int.__mod__
    _m_and = int.__and__
    _m_or = int.__or__
    xor = int.__xor__
    pow = int.__pow__
    #butNot
    #remainder

class String(unicode):
    add = unicode.__add__
    multiply = unicode.__mul__


def wrap(pyobj):
    if isinstance(pyobj, str):
        return Bytes(pyobj)
    if isinstance(pyobj, unicode):
        return String(pyobj)
    if isinstance(pyobj, int):
        return MonteInt(pyobj)
    if isinstance(pyobj, float):
        return MonteFloat64(pyobj)
    if isinstance(pyobj, list):
        return FlexList(pyobj)
    if isinstance(pyobj, tuple):
        return List(pyobj)
    if isinstance(pyobj, dict):
        # probably need to make it flex here since other python code
        # can mutate it and we don't want surprises
        return FlexMap(pyobj)
    if isinstance(pyobj, set):
        return FlexSet(pyobj)
    if isinstance(pyobj, frozenset):
        return Set(pyobj)


def getGuard(o, name):
    """
    Returns the guard object for a name in a Monte object's frame.
    """


def getBinding(o, name):
    """
    Returns the binding object for a name in a Monte object's frame.
    """


def reifyBinding(slot):
    """
    Create a binding object from a slot object.
    """


class MonteEjection(BaseException):
    pass


def throw(val):
    raise RuntimeError(val)


def ejector(_name):
    class ejtype(MonteEjection):
        name = _name
        pass
    class ej(MonteObject):
        _m_type = ejtype
        _m_active = True

        def __call__(self, val=None):
            if not self._m_active:
                throw("Ejector is not active")
            raise ejtype(val)

        def disable(self):
            self._m_active = False

    return ej()


class StaticContext(object):

    def __init__(self, fqn, fields, objectExpr):
        self.fqn = fqn
        self.fields = fields
        self.objectExpr = objectExpr


class FinalSlot(object):
    def __init__(self, val, guard=None, ej=throw):
        self.guard = guard
        if self.guard is not None:
            self.val = self.guard.coerce(self.val, ej)
        else:
            self.val = val

    def get(self):
        return self.val


class VarSlot(object):
    def __init__(self, guard, val=_absent, ej=None):
        self.guard = guard
        if val is not _absent:
            self._m_init(val, ej)

    def _m_init(self, val, ej):
        if self.guard is not None:
            self.val = self.guard.coerce(self.val, ej)
        else:
            self.val = val

    def get(self):
        return self.val

    def put(self, val):
        if self.guard is not None:
            self.val = self.guard.coerce(self.val, throw)
        else:
            self.val = val


def slotFromBinding(b):
    pass


def wrapEjector(e):
    def ej(val):
        e(val)
        raise RuntimeError("Ejector did not exit")
    return ej


class _MatchFailure(Exception):
    pass


def matcherFail(v):
    raise _MatchFailure(v)


class GeneratedCodeLoader(object):
    """
    Object for use as a module's __loader__, to display generated
    source.
    """
    def __init__(self, source):
        self.source = source
    def get_source(self, name):
        return self.source

pyeval = eval

def getIterator(coll):
    if isinstance(coll, dict):
        return coll.iteritems()
    elif isinstance(coll, (tuple, list)):
        return ((wrap(i), v) for (i, v) in enumerate(coll))
    else:
        gi = getattr(coll, "getIterator", None)
        if gi is not None:
            return gi()
        else:
            return ((wrap(i), v) for (i, v) in enumerate(coll))

def monteLooper(coll, obj):
    it = getIterator(coll)
    for key, item in it:
        obj.run(key, item)

def makeMonteList(*items):
    return items

class MonteMap(dict):

    __setitem__ = None
    get = dict.__getitem__


class mapMaker(object):
    @staticmethod
    def fromPairs(pairs):
        return MonteMap(pairs)

def validateFor(flag):
    if not flag:
        raise RuntimeError("For-loop body isn't valid after for-loop exits.")

def accumulateList(coll, obj):
    it = getIterator(coll)
    acc = []
    skip = ejector("listcomp_skip")
    for key, item in it:
        try:
            acc.append(obj.run(key, item, skip))
        except skip._m_type:
            continue
    return tuple(acc)

def accumulateMap(coll, obj):
    return mapMaker.fromPairs(accumulateList(coll, obj))

def iterWhile(f):
    return (v for v in iter(f, False))

class Comparer(MonteObject):
    def greaterThan(self, left, right):
        return left > right

    def geq(self, left, right):
        return left >= right

    def lessThan(self, left, right):
        return left < right

    def leq(self, left, right):
        return left <= right

    def asBigAs(self, left, right):
        return (left <= right) and (left >= right)

comparer = Comparer()

class BooleanGuard(MonteObject):
    def coerce(self, specimen, ej):
        # XXX SHORTEN
        tryej = ejector("coercion")
        try:
            return self._subCoerce(specimen, tryej)
        except tryej._m_type, p:
            problem = p.args[0]
        finally:
            tryej.disable()
        newspec = specimen._conformTo(self)
        if newspec is not specimen:
            return self._subCoerce(newspec, ej)
        tryej(problem)

    def _subCoerce(self, specimen, ej):
        if specimen is True or specimen is False:
            return specimen
        ejector("%r is not a boolean" % (specimen,))

booleanGuard = BooleanGuard()

class MakeVerbFacet(MonteObject):
    def curryCall(self, obj, verb):
        def facet(*a):
            return getattr(obj, verb)(*a)
        return facet

makeVerbFacet = MakeVerbFacet()

def matchSame(expected):
    def sameMatcher(specimen, ej):
        #XXX equalizer
        if specimen == expected:
            return expected
        else:
            ej("%r is not %r" % (specimen, expected))
    return sameMatcher

def switchFailed(specimen, *failures):
    raise RuntimeError("%s did not match any option: [%s]" % (
        specimen,
        " ".join(str(f) for f in failures)))


def suchThat(x, y=_absent):
    if y is _absent:
        # 1-arg invocation.
        def suchThatMatcher(specimen, ejector):
            if not x:
                ejector("such-that expression was false")
        return suchThatMatcher
    else:
        return [x, None]

def extract(x, instead=_absent):
    if instead is _absent:
        # 1-arg invocation.
        def extractor(specimen, ejector):
            value = specimen[x]
            without = dict(specimen)
            del without[x]
            return [value, without]
        return extractor
    else:
        def extractor(specimen, ejector):
            value = specimen.get(x, _absent)
            if value is _absent:
                return [instead(), specimen]
            without = dict(specimen)
            del without[x]
            return [value, without]
        return extractor

class Empty:
    def coerce(self, specimen, ej):
        if len(specimen) == 0:
            return specimen
        else:
            ej("Not empty: %s" % specimen)

def splitList(cut):
    def listSplitter(specimen, ej):
        #XXX coerce to list
        if len(specimen) < cut:
            ej("A %s size list doesn't match a >= %s size list pattern" % (len(specimen), cut))
        return specimen[:cut] + (specimen[cut:],)

    return listSplitter

jacklegScope = {
    'true': True,
    'false': False,
    'null': None,
    'NaN': float('nan'),
    'Infinity': float('inf'),

    '__comparer': comparer,

    'throw': throw,

    '__makeList': makeMonteList,
    '__makeMap': mapMaker,
    '__loop': monteLooper,
    '__validateFor': validateFor,
    '__accumulateList': accumulateList,
    '__accumulateMap': accumulateMap,
    '__iterWhile': iterWhile,

    'boolean': booleanGuard,

    '__makeVerbFacet': makeVerbFacet,
    '__matchSame': matchSame,
    '__switchFailed': switchFailed,
    '__suchThat': suchThat,
    '__extract': extract,
    '__Empty': Empty(),
    '__splitList': splitList,
}

def eval(source, scope=jacklegScope):
    name = uuid.uuid4().hex + '.py'
    mod = module(name)
    mod.__name__ = name
    mod._m_outerScope = scope
    pysrc, _, lastline = ecompile(source, scope).rpartition('\n')
    pysrc = '\n'.join(["from monte import runtime as _monte",
                       pysrc,
                       "_m_evalResult = " + lastline])
    mod.__loader__ = GeneratedCodeLoader(pysrc)
    code = compile(pysrc, name, "exec")
    pyeval(code, mod.__dict__)
    sys.modules[name] = mod
    linecache.getlines(name, mod.__dict__)
    return mod._m_evalResult



