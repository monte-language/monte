from monte.runtime.audit import auditedBy
from monte.runtime.base import throw
from monte.runtime.bindings import reifyBinding, FinalSlot, VarSlot
from monte.runtime.data import (makeCharacter, makeFloat, makeInteger, String,
                                true, false, nan, infinity, null,
                                theTwineMaker, makeSourceSpan)
from monte.runtime.equalizer import equalizer
from monte.runtime.flow import monteLooper
from monte.runtime.guards.base import (anyGuard, deepFrozenGuard, nullOkGuard,
                                       sameGuardMaker, selflessGuard,
                                       subrangeGuardMaker,
                                       transparentGuard, ParamDesc,
                                       MessageDesc, ProtocolDesc)
from monte.runtime.guards.data import (booleanGuard, charGuard, intGuard,
                                       floatGuard, stringGuard, twineGuard,
                                       voidGuard)
from monte.runtime.guards.tables import listGuard, mapGuard
from monte.runtime.helpers import (accumulateList, accumulateMap, BooleanFlow,
                                   comparer, extract, Empty, iterWhile,
                                   makeVerbFacet, makeViaBinder, matchSame,
                                   switchFailed, suchThat, splitList,
                                   validateFor)
from monte.runtime.load import monteImport
from monte.runtime.ref import RefOps
from monte.runtime.tables import makeMonteList, mapMaker
from monte.runtime.m import theM
from monte.runtime.text import simpleQuasiParser, quasiMatcher
from monte.runtime.trace import trace, traceln


class Func(object):
    def __init__(self, f):
        self._m_auditorStamps = getattr(f, '_m_auditorStamps', ())
        self.f = f

    def __call__(self, *a, **kw):
        return self.f(*a, **kw)

    def run(self, *a, **kw):
        return self.f(*a, **kw)

bootScope = {
    ## Primitive non-literal values
    'true': true,
    'false': false,
    'null': null,
    'NaN': nan,
    'Infinity': infinity,

    ## Primitive: flow control
    # XXX Create this properly per-vat, when we have vats.
    'M': theM,
    'throw': throw,
    '__loop': Func(monteLooper),

    ## Primitive reference/object operations
    # XXX Create this properly per-vat, when we have vats.
    "Ref": RefOps(None),
    "DeepFrozen": deepFrozenGuard,

    # XXX move these somewhere importable instead, eventually
    "Same": sameGuardMaker,
    "SubrangeGuard": subrangeGuardMaker,

    ## Primitive: tracing
    'trace': Func(trace),
    'traceln': Func(traceln),

    ## Data constructors
    '__makeList': makeMonteList,
    '__makeMap': mapMaker,
    '__makeCharacter': Func(makeCharacter),
    '__makeInt': Func(makeInteger),
    '__makeFloat': Func(makeFloat),
    '__makeFinalSlot': FinalSlot,
    '__makeVarSlot': VarSlot,
    # '__makeCoercedSlot': makeCoercedSlot,
    # '__makeGuardedSlot': makeGuardedSlot,
    '__makeString': theTwineMaker,
    # 'term__quasiParser': makeQBuilder,

    ## Primitive: guards
    'any': anyGuard,
    'Any': anyGuard,
    'void': voidGuard,
    'Void': voidGuard,

    ## Primitive: atomic data guards
    'boolean': booleanGuard,
    'Bool': booleanGuard,
    'str': stringGuard,
    'Str': stringGuard,
    'Twine': twineGuard,
    # 'TextWriter': textWriterGuard,
    ## XXX wrap as ordered spaces
    'char': charGuard,
    'Char': charGuard,
    'float': floatGuard,
    'Double': floatGuard,
    'int': intGuard,
    'Int': intGuard,

    ## data guards
    # 'all': makeIntersectionGuard,
    # 'not': makeNegatedGuard,
    # 'Tuple': makeTupleGuard,
    # '__Portrayal': lazyEval("Tuple[any, String, List[any]]")
    'List': listGuard,
    'Map': mapGuard,
    # 'set': setGuard,

    ## Protocol/guard constructors
    '__makeMessageDesc': Func(MessageDesc),
    '__makeParamDesc': Func(ParamDesc),
    '__makeProtocolDesc': ProtocolDesc,

    ## guard meta
    'ValueGuard': anyGuard,
    # 'Guard': guardGuard,
    # '__makeGuard': makeGuard,

    ## Utility guards
    # 'notNull': notNullGuard,
    'nullOk': nullOkGuard,
    'NullOk': nullOkGuard,

    ## Primitive: reference conditions
    'Selfless': selflessGuard,
    'Transparent': transparentGuard,
    ## Reference conditions
    'Data': null,
    # 'near': nearGuard,
    # 'PassByCopy': passByCopyGuard,
    # 'pbc': passByConstructionGuard,
    # 'rcvr': rcvrGuard,

    ## Primitive: reference operations
    '__auditedBy': auditedBy,
    '__equalizer': equalizer,

    # 'monte__quasiParser': monteQuasiParser,
    # 'Audition': auditionGuard,

    ## quasiparsers
    'simple__quasiParser': simpleQuasiParser,

    ## expansion utilities
    '__accumulateList': Func(accumulateList),
    '__accumulateMap': Func(accumulateMap),
    '__bind': Func(makeViaBinder),
    #XXX vat
    '__booleanFlow': BooleanFlow(None),
    '__comparer': comparer,
    '__iterWhile': Func(iterWhile),
    '__makeVerbFacet': makeVerbFacet,
    '__mapEmpty': Empty(),
    '__mapExtract': Func(extract),
    '__matchSame': Func(matchSame),
    '__quasiMatcher': Func(quasiMatcher),
    '__slotToBinding': Func(reifyBinding),
    '__splitList': Func(splitList),
    '__suchThat': Func(suchThat),
    '__switchFailed': Func(switchFailed),
    # '__promiseAllFulfilled': promiseAllFulfilled,
    '__validateFor': Func(validateFor),

    ## misc
    # '__identityFunc': identityFunc,

    'help': help,

    # move this into something importable
    'makeSourceSpan': Func(makeSourceSpan),

}

def createSafeScope(scope):
    loader = monteImport(bootScope)
    bits = loader(String(u"prim"))
    scope = scope.copy()
    for k, v in bits.d.iteritems():
        scope[k.bare().s] = v
    return scope

# ioScope = {
#     'timer': theTimer,
#     'entropy': rng,
#     'filesystem': filesystemRoot,
#     'stdin': stdin,
#     'stdout': stdout,
#     'stderr': stderr,
#     'python': evalPython,
#     'exceptionUnsealer': exceptionUnsealer,
# }
