from monte.runtime.audit import auditedBy
from monte.runtime.base import throw
from monte.runtime.bindings import reifyBinding, FinalSlot, VarSlot
from monte.runtime.data import (Integer, true, false, nan, infinity, null)
from monte.runtime.equalizer import equalizer
from monte.runtime.flow import monteLooper
from monte.runtime.guards.base import (anyGuard, deepFrozenGuard, nullOkGuard,
                                       selflessGuard, transparentGuard,
                                       ParamDesc, MessageDesc, ProtocolDesc)
from monte.runtime.guards.data import (booleanGuard, charGuard, intGuard,
                                       floatGuard, stringGuard, voidGuard)
from monte.runtime.guards.tables import listGuard, mapGuard
from monte.runtime.helpers import (accumulateList, accumulateMap, comparer,
                                   extract, Empty, iterWhile, makeVerbFacet,
                                   makeViaBinder, matchSame, switchFailed,
                                   suchThat, splitList, validateFor)
from monte.runtime.io import stdin, stdout
from monte.runtime.tables import makeMonteList, mapMaker
from monte.runtime.text import simpleQuasiParser, quasiMatcher
from monte.runtime.trace import trace, traceln, traceback

safeScope = {
    ## Primitive non-literal values
    'true': true,
    'false': false,
    'null': null,
    'NaN': nan,
    'Infinity': infinity,

    ## Primitive: flow control
    'throw': throw,
    '__loop': monteLooper,

    ## Primitive reference/object operations
    "DeepFrozen": deepFrozenGuard,

    ## Primitive: tracing
    'trace': trace,
    'traceln': traceln,
    'traceback': traceback,

    ## Data constructors
    '__makeList': makeMonteList,
    '__makeMap': mapMaker,
    '__makeInt': Integer,
    '__makeFinalSlot': FinalSlot,
    '__makeVarSlot': VarSlot,
    # '__makeCoercedSlot': makeCoercedSlot,
    # '__makeGuardedSlot': makeGuardedSlot,
    # '__makeTwine': makeTwine,
    # 'term__quasiParser': makeQBuilder,
    # '__makeOrderedSpace': null,

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

    ## Code loading
    # 'monte__quasiParser': monteQuasiParser,
    # 'Audition': auditionGuard,

    ## quasiparsers
    'simple__quasiParser': simpleQuasiParser,

    ## expansion utilities
    '__accumulateList': accumulateList,
    '__accumulateMap': accumulateMap,
    '__bind': makeViaBinder,
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

    # XXX hack
    "Ref": None,
    "__booleanFlow": None,
    "M": None,
}

ioScope = {
#     'timer': theTimer,
#     'entropy': rng,
#     'filesystem': filesystemRoot,
    'stdin': stdin,
    'stdout': stdout,
#     'stderr': stderr,
#     'python': evalPython,
#     'exceptionUnsealer': exceptionUnsealer,
}
