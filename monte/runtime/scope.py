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
                                       floatGuard, stringGuard, voidGuard)
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
    '__loop': monteLooper,

    ## Primitive reference/object operations
    # XXX Create this properly per-vat, when we have vats.
    "Ref": RefOps(None),
    "DeepFrozen": deepFrozenGuard,

    # XXX move these somewhere importable instead, eventually
    "Same": sameGuardMaker,
    "SubrangeGuard": subrangeGuardMaker,

    ## Primitive: tracing
    'trace': trace,
    'traceln': traceln,

    ## Data constructors
    '__makeList': makeMonteList,
    '__makeMap': mapMaker,
    '__makeCharacter': makeCharacter,
    '__makeInt': makeInteger,
    '__makeFloat': makeFloat,
    '__makeFinalSlot': FinalSlot,
    '__makeVarSlot': VarSlot,
    # '__makeCoercedSlot': makeCoercedSlot,
    # '__makeGuardedSlot': makeGuardedSlot,
    '__makeString': theTwineMaker,
    # 'term__quasiParser': makeQBuilder,

    ## Primitive: guards
    'any': anyGuard,
    'void': voidGuard,

    ## Primitive: atomic data guards
    'boolean': booleanGuard,
    'str': stringGuard,
    # 'Twine': twineGuard,
    # 'TextWriter': textWriterGuard,
    ## XXX wrap as ordered spaces
    'char': charGuard,
    'float': floatGuard,
    'int': intGuard,

    ## data guards
    # 'all': makeIntersectionGuard,
    # 'not': makeNegatedGuard,
    # 'Tuple': makeTupleGuard,
    # '__Portrayal': lazyEval("Tuple[any, String, List[any]]")
    'List': listGuard,
    'Map': mapGuard,
    # 'set': setGuard,

    ## Protocol/guard constructors
    '__makeMessageDesc': MessageDesc,
    '__makeParamDesc': ParamDesc,
    '__makeProtocolDesc': ProtocolDesc,

    ## guard meta
    'ValueGuard': anyGuard,
    # 'Guard': guardGuard,
    # '__makeGuard': makeGuard,

    ## Utility guards
    # 'notNull': notNullGuard,
    'nullOk': nullOkGuard,

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
    '__accumulateList': accumulateList,
    '__accumulateMap': accumulateMap,
    '__bind': makeViaBinder,
    #XXX vat
    '__booleanFlow': BooleanFlow(None),
    '__comparer': comparer,
    '__iterWhile': iterWhile,
    '__makeVerbFacet': makeVerbFacet,
    '__mapEmpty': Empty(),
    '__mapExtract': extract,
    '__matchSame': matchSame,
    '__quasiMatcher': quasiMatcher,
    '__slotToBinding': reifyBinding,
    '__splitList': splitList,
    '__suchThat': suchThat,
    '__switchFailed': switchFailed,
    # '__promiseAllFulfilled': promiseAllFulfilled,
    '__validateFor': validateFor,

    ## misc
    # '__identityFunc': identityFunc,

    'help': help,

    # move this into something importable
    'makeSourceSpan': makeSourceSpan,

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
