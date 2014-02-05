import linecache, sys, uuid
from types import ModuleType as module

from terml.parser import parseTerm
from monte.compiler import ecompile

_absent = object()

def traceln(x):
    print x

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


class Binding(MonteObject):
    def __init__(self, slot):
        self.slot = slot


def getGuard(o, name):
    """
    Returns the guard object for a name in a Monte object's frame.
    """
    raise RuntimeError()


def getBinding(o, name):
    """
    Returns the binding object for a name in a Monte object's frame.
    """
    raise RuntimeError()


def reifyBinding(slot):
    """
    Create a binding object from a slot object.
    """
    return Binding(slot)


class MonteEjection(BaseException):
    pass


class Throw(MonteObject):
    def __call__(self, val):
        raise RuntimeError(val)
    def eject(self, ej, val):
        #XXX this should coerce ej to Ejector
        if ej is None:
            throw(val)
        else:
            wrapEjector(ej)(val)

throw = Throw()

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
    return b.slot


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
    return ConstList(items)


class ConstList(tuple):
    def __repr__(self):
        orig = tuple.__repr__(self)
        return '[' + orig[1:-1] + ']'

    def __str__(self):
        return self.__repr__()


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
    return ConstList(acc)

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

class AnyGuard(MonteObject):
    def coerce(self, specimen, ej):
        return specimen

anyGuard = AnyGuard()

class VoidGuard(MonteObject):
    def coerce(self, specimen, ej):
        if specimen is not None:
            throw.eject(ej, "%r is not null" % (specimen,))

voidGuard = VoidGuard()

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
            throw.eject(ej, "Not empty: %s" % specimen)

def splitList(cut):
    def listSplitter(specimen, ej):
        #XXX coerce to list
        if len(specimen) < cut:
            throw.eject(ej, "A %s size list doesn't match a >= %s size list pattern" % (len(specimen), cut))
        return specimen[:cut] + (specimen[cut:],)

    return listSplitter


def findOneOf(elts, specimen, start):
    for i, c in enumerate(specimen[start:]):
        if c in elts:
            return i + start
    return -1

class Substituter(MonteObject):
    def __init__(self, template):
        self.template = template
        self.segments = segs = []
        last = 0
        i = 0
        while i < len(template):
            i = findOneOf('$@', template, last)
            if i == -1:
                if last < len(template) - 1:
                    segs.append(('literal', self.template[last:]))
                break
            if self.template[i + 1] == self.template[i]:
                segs.append(('literal', self.template[last:i]))
                last = i
            elif self.template[i + 1] != '{':
                i -= 1
            else:
                if last != i and last < len(template) - 1:
                    segs.append(('literal', self.template[last:i]))
                    last = i
                if self.template[i] == '@':
                    typ = 'pattern'
                else:
                    typ = 'value'
                i += 2
                sub = i
                while True:
                    i += 1
                    c = self.template[i]
                    if c == '}':
                        break
                    elif not c.isdigit():
                        raise RuntimeError("Missing '}'", template)
                segs.append((typ, int(self.template[sub:i])))
                last = i + 1

    def substitute(self, values):
        return "".join(self._sub(values))

    def _sub(self, values):
        for typ, val in self.segments:
            if typ == 'literal':
                yield val
            elif typ == 'value':
                yield str(values[val])
            else:
                raise RuntimeError("Can't substitute with a pattern")

    def matchBind(self, values, specimen, ej):
        #XXX maybe put this on a different object?
        i = 0
        bindings = []
        for n in range(len(self.segments)):
            typ, val = self.segments[n]
            if typ == 'literal':
                j = i + len(val)
                if specimen[i:j] != val:
                    throw.eject(ej, "expected %r..., found %r" % (
                        val, specimen[i:j]))
            elif typ == 'value':
                j = i + len(values[val])
                if specimen[i:j] != values[val]:
                    throw.eject(ej, "expected %r... ($-hole %s), found %r" % (
                        values[val], val, specimen[i:j]))
            elif typ == 'pattern':
                nextVal = None
                if n == len(self.segments) - 1:
                    bindings.append(specimen[i:])
                    continue
                nextType, nextVal = self.segments[n + 1]
                if nextType == 'value':
                    nextVal = values[nextVal]
                elif nextType == 'pattern':
                    bindings.append("")
                    continue
                j = specimen.find(nextVal)
                if j == -1:
                    throw.eject(ej, "expected %r..., found %r" % (nextVal, specimen[i:]))
                bindings.append(specimen[i:j])
            i = j
        return ConstList(bindings)

class SimpleQuasiParser(MonteObject):
    def valueMaker(self, template):
        return Substituter(template)

    def matchMaker(self, template):
        return Substituter(template)


def quasiMatcher(matchMaker, values):
    def matchit(specimen, ej):
        return matchMaker.matchBind(values, specimen, ej)
    return matchit

class BooleanFlow(MonteObject):
    def broken(self):
        #XXX should return broken ref
        return object()

    def failureList(self, size):
        #XXX needs broken ref
        return [False] + [object()] * size

booleanFlow = BooleanFlow()

jacklegScope = {
    'true': True,
    'false': False,
    'null': None,
    'NaN': float('nan'),
    'Infinity': float('inf'),

    'any': anyGuard,
    'void': voidGuard,
    'boolean': booleanGuard,
    'ValueGuard': anyGuard,


    #E
    #Ref
    'throw': throw,
    '__loop': monteLooper,

    'traceln': traceln,

    '__iterWhile': iterWhile,
    '__accumulateList': accumulateList,
    '__accumulateMap': accumulateMap,

    '__makeList': makeMonteList,
    '__makeMap': mapMaker,

    #__bind
    '__booleanFlow': booleanFlow,
    '__comparer': comparer,
    '__makeVerbFacet': makeVerbFacet,
    '__mapEmpty': Empty(),
    '__mapExtract': extract,
    '__matchSame': matchSame,
    '__quasiMatcher': quasiMatcher,
    '__slotToBinding': reifyBinding,
    '__splitList': splitList,
    '__suchThat': suchThat,
    '__switchFailed': switchFailed,
    #__promiseAllFulfilled
    '__validateFor': validateFor,


    'simple__quasiParser': SimpleQuasiParser()
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










