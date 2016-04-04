
safeScope
=========


Primitive values
----------------

true :<BoolGuard>
    *cannot get docstring*
false :<BoolGuard>
    *cannot get docstring*
null :Void
    *cannot get docstring*
NaN :<DoubleGuard>
    *cannot get docstring*
Infinity :<DoubleGuard>
    *cannot get docstring*

Data Constructors
-----------------

_makeInt
    *cannot get docstring*
      - fromBytes/1: *no docstring*
      - fromBytes/2: *no docstring*
      - run/1: *no docstring*
      - run/2: *no docstring*

_makeDouble
    *cannot get docstring*
      - run/1: *no docstring*
      - fromBytes/1: *no docstring*

_makeString
    *cannot get docstring*
      - fromString/1: *no docstring*
      - fromString/2: *no docstring*
      - fromChars/1: *no docstring*

_makeBytes
    *cannot get docstring*
      - fromString/1: *no docstring*
      - fromInts/1: *no docstring*

_makeList
    *cannot get docstring*
      - fromIterable/1: *no docstring*

_makeMap
    *cannot get docstring*
      - fromPairs/1: *no docstring*

_makeOrderedSpace
    *cannot get docstring*
      - spaceOfGuard/1: *no docstring*
      - spaceOfValue/1: *no docstring*
      - op__till/2: *no docstring*
      - op__thru/2: *no docstring*

_makeTopSet
    *cannot get docstring*
      - run/5: *no docstring*

_makeOrderedRegion
    *cannot get docstring*
      - run/3: *no docstring*

_makeSourceSpan
    *cannot get docstring*
      - run/6: *no docstring*

_makeFinalSlot
    *cannot get docstring*
      - run/3: *no docstring*
      - asType/0: *no docstring*

_makeVarSlot
    *cannot get docstring*
      - run/3: *no docstring*
      - asType/0: *no docstring*

makeLazySlot
    *cannot get docstring*
      - run/1: *no docstring*


Basic guards
------------

Any
    *cannot get docstring*
      - supersetOf/1: *no docstring*
      - getMethods/0: *no docstring*
      - coerce/2: *no docstring*
      - extractGuards/2: *no docstring*

Void
    *cannot get docstring*
      - supersetOf/1: *no docstring*
      - coerce/2: *no docstring*

Empty
    *cannot get docstring*
      - _printOn/1: *no docstring*
      - coerce/2: *no docstring*

Bool
    *cannot get docstring*
      - supersetOf/1: *no docstring*
      - coerce/2: *no docstring*

Str
    *cannot get docstring*
      - _printOn/1: *no docstring*
      - _uncall/0: *no docstring*
      - coerce/2: *no docstring*
      - op__cmp/1: *no docstring*
      - add/1: *no docstring*
      - subtract/1: *no docstring*
      - makeRegion/4: *no docstring*

Char
    *cannot get docstring*
      - _printOn/1: *no docstring*
      - _uncall/0: *no docstring*
      - coerce/2: *no docstring*
      - op__cmp/1: *no docstring*
      - add/1: *no docstring*
      - subtract/1: *no docstring*
      - makeRegion/4: *no docstring*

Double
    *cannot get docstring*
      - _printOn/1: *no docstring*
      - _uncall/0: *no docstring*
      - coerce/2: *no docstring*
      - op__cmp/1: *no docstring*
      - add/1: *no docstring*
      - subtract/1: *no docstring*
      - makeRegion/4: *no docstring*

Int
    *cannot get docstring*
      - _printOn/1: *no docstring*
      - _uncall/0: *no docstring*
      - coerce/2: *no docstring*
      - op__cmp/1: *no docstring*
      - add/1: *no docstring*
      - subtract/1: *no docstring*
      - makeRegion/4: *no docstring*

Bytes
    *cannot get docstring*
      - _printOn/1: *no docstring*
      - _uncall/0: *no docstring*
      - coerce/2: *no docstring*
      - op__cmp/1: *no docstring*
      - add/1: *no docstring*
      - subtract/1: *no docstring*
      - makeRegion/4: *no docstring*

List
    *cannot get docstring*
      - _printOn/1: *no docstring*
      - coerce/2: *no docstring*
      - get/1: *no docstring*
      - extractGuard/2: *no docstring*

Map
    *cannot get docstring*
      - _printOn/1: *no docstring*
      - coerce/2: *no docstring*
      - get/2: *no docstring*
      - extractGuards/2: *no docstring*

Set
    *cannot get docstring*
      - _printOn/1: *no docstring*
      - coerce/2: *no docstring*
      - get/1: *no docstring*
      - extractGuard/2: *no docstring*

Pair
    *cannot get docstring*
      - _printOn/1: *no docstring*
      - coerce/2: *no docstring*
      - get/2: *no docstring*
      - extractGuards/2: *no docstring*


Guard utilities
---------------

NullOk
    *cannot get docstring*
      - coerce/2: *no docstring*
      - get/1: *no docstring*
      - extractGuard/2: *no docstring*

Same
    *cannot get docstring*
      - extractValue/2: *no docstring*
      - get/1: *no docstring*

SubrangeGuard
    *cannot get docstring*
      - get/1: *no docstring*

_auditedBy
    *cannot get docstring*
      - run/2: *no docstring*


Tracing
-------

trace
    *cannot get docstring*
      - exception/1: *no docstring*

traceln
    *cannot get docstring*
      - exception/1: *no docstring*


Brands
------

makeBrandPair
    *cannot get docstring*
      - run/1: *no docstring*


Quasiparsers
------------

simple__quasiParser
    *cannot get docstring*
      - patternHole/1: *no docstring*
      - valueHole/1: *no docstring*
      - matchMaker/1: *no docstring*
      - valueMaker/1: *no docstring*

b__quasiParser
    *cannot get docstring*
      - patternHole/1: *no docstring*
      - valueHole/1: *no docstring*
      - matchMaker/1: *no docstring*
      - valueMaker/1: *no docstring*

m__quasiParser
    *cannot get docstring*
      - getAstBuilder/0: *no docstring*
      - valueHole/1: *no docstring*
      - patternHole/1: *no docstring*
      - valueMaker/1: *no docstring*
      - matchMaker/1: *no docstring*
      - fromStr/1: *no docstring*


Flow control
------------

M
    *cannot get docstring*
      - send/4: *no docstring*
      - callWithPair/3: *no docstring*
      - toString/1: *no docstring*
      - call/3: *no docstring*
      - sendOnly/4: *no docstring*
      - callWithMessage/2: *no docstring*
      - sendOnly/3: *no docstring*
      - send/3: *no docstring*
      - call/4: *no docstring*
      - callWithPair/2: *no docstring*
      - toQuote/1: *no docstring*

throw
    *cannot get docstring*
      - run/1: *no docstring*
      - eject/2: *no docstring*

_loop
    *cannot get docstring*
      - run/2: *no docstring*

_iterForever
    *cannot get docstring*
      - _makeIterator/0: *no docstring*
      - next/1: *no docstring*


Evaluation
----------

eval
    *cannot get docstring*
      - run/2: *no docstring*
      - evalToPair/2: *no docstring*

typhonEval
    *cannot get docstring*
      - evalToPair/2: *no docstring*
      - fromAST/3: *no docstring*
      - run/2: *no docstring*


Reference/object operations
---------------------------

Ref
    *cannot get docstring*
      - isDeepFrozen/1: *no docstring*
      - isSelfish/1: *no docstring*
      - makeProxy/3: *no docstring*
      - promise/0: *no docstring*
      - isSettled/1: *no docstring*
      - broken/1: *no docstring*
      - state/1: *no docstring*
      - isFar/1: *no docstring*
      - optProblem/1: *no docstring*
      - isSelfless/1: *no docstring*
      - isNear/1: *no docstring*
      - isResolved/1: *no docstring*
      - whenResolved/2: *no docstring*
      - isEventual/1: *no docstring*
      - fulfillment/1: *no docstring*
      - isBroken/1: *no docstring*
      - whenResolvedOnly/2: *no docstring*
      - whenBroken/2: *no docstring*

promiseAllFulfilled
    *cannot get docstring*
      - run/1: *no docstring*

DeepFrozen
    *cannot get docstring*
      - audit/1: *no docstring*
      - coerce/2: *no docstring*
      - supersetOf/1: *no docstring*

Selfless
    *cannot get docstring*
      - audit/1: *no docstring*
      - coerce/2: *no docstring*
      - passes/1: *no docstring*

Transparent
    *cannot get docstring*
      - coerce/2: *no docstring*
      - makeAuditorKit/0: *no docstring*

Near
    *cannot get docstring*
      - coerce/2: *no docstring*

Binding
    *cannot get docstring*
      - supersetOf/1: *no docstring*
      - coerce/2: *no docstring*


Abstract Syntax
---------------

astBuilder
    *cannot get docstring*
      - getAstGuard/0: *no docstring*
      - getPatternGuard/0: *no docstring*
      - getExprGuard/0: *no docstring*
      - getNamePatternGuard/0: *no docstring*
      - getNounGuard/0: *no docstring*
      - LiteralExpr/2: *no docstring*
      - NounExpr/2: *no docstring*
      - TempNounExpr/2: *no docstring*
      - SlotExpr/2: *no docstring*
      - MetaContextExpr/1: *no docstring*
      - MetaStateExpr/1: *no docstring*
      - BindingExpr/2: *no docstring*
      - SeqExpr/2: *no docstring*
      - Module/4: *no docstring*
      - NamedArg/3: *no docstring*
      - NamedArgExport/2: *no docstring*
      - MethodCallExpr/5: *no docstring*
      - FunCallExpr/4: *no docstring*
      - SendExpr/5: *no docstring*
      - FunSendExpr/4: *no docstring*
      - GetExpr/3: *no docstring*
      - AndExpr/3: *no docstring*
      - OrExpr/3: *no docstring*
      - BinaryExpr/4: *no docstring*
      - CompareExpr/4: *no docstring*
      - RangeExpr/4: *no docstring*
      - SameExpr/4: *no docstring*
      - MatchBindExpr/3: *no docstring*
      - MismatchExpr/3: *no docstring*
      - PrefixExpr/3: *no docstring*
      - CoerceExpr/3: *no docstring*
      - CurryExpr/4: *no docstring*
      - ExitExpr/3: *no docstring*
      - ForwardExpr/2: *no docstring*
      - VarPattern/3: *no docstring*
      - DefExpr/4: *no docstring*
      - AssignExpr/3: *no docstring*
      - VerbAssignExpr/4: *no docstring*
      - AugAssignExpr/4: *no docstring*
      - Method/7: *no docstring*
      - To/7: *no docstring*
      - Matcher/3: *no docstring*
      - Catcher/3: *no docstring*
      - Script/4: *no docstring*
      - FunctionScript/5: *no docstring*
      - FunctionExpr/3: *no docstring*
      - ListExpr/2: *no docstring*
      - ListComprehensionExpr/6: *no docstring*
      - MapExprAssoc/3: *no docstring*
      - MapExprExport/2: *no docstring*
      - MapExpr/2: *no docstring*
      - MapComprehensionExpr/7: *no docstring*
      - ForExpr/7: *no docstring*
      - ObjectExpr/6: *no docstring*
      - ParamDesc/3: *no docstring*
      - MessageDesc/5: *no docstring*
      - InterfaceExpr/7: *no docstring*
      - FunctionInterfaceExpr/7: *no docstring*
      - CatchExpr/4: *no docstring*
      - FinallyExpr/3: *no docstring*
      - TryExpr/4: *no docstring*
      - EscapeExpr/5: *no docstring*
      - SwitchExpr/3: *no docstring*
      - WhenExpr/5: *no docstring*
      - IfExpr/4: *no docstring*
      - WhileExpr/4: *no docstring*
      - HideExpr/2: *no docstring*
      - ValueHoleExpr/2: *no docstring*
      - PatternHoleExpr/2: *no docstring*
      - ValueHolePattern/2: *no docstring*
      - PatternHolePattern/2: *no docstring*
      - FinalPattern/3: *no docstring*
      - SlotPattern/3: *no docstring*
      - BindingPattern/2: *no docstring*
      - BindPattern/3: *no docstring*
      - IgnorePattern/2: *no docstring*
      - ListPattern/3: *no docstring*
      - MapPatternAssoc/4: *no docstring*
      - MapPatternImport/3: *no docstring*
      - MapPattern/3: *no docstring*
      - NamedParam/4: *no docstring*
      - NamedParamImport/3: *no docstring*
      - ViaPattern/3: *no docstring*
      - SuchThatPattern/3: *no docstring*
      - SamePattern/3: *no docstring*
      - QuasiText/2: *no docstring*
      - QuasiExprHole/2: *no docstring*
      - QuasiPatternHole/2: *no docstring*
      - QuasiParserExpr/3: *no docstring*
      - QuasiParserPattern/3: *no docstring*


Utilities for syntax expansions
-------------------------------

_accumulateList
    *cannot get docstring*
      - run/2: *no docstring*

_accumulateMap
    *cannot get docstring*
      - run/2: *no docstring*

_bind
    *cannot get docstring*
      - run/2: *no docstring*

_booleanFlow
    *cannot get docstring*
      - broken/0: *no docstring*
      - failureList/1: *no docstring*

_comparer
    *cannot get docstring*
      - asBigAs/2: *no docstring*
      - geq/2: *no docstring*
      - greaterThan/2: *no docstring*
      - leq/2: *no docstring*
      - lessThan/2: *no docstring*

_equalizer
    *cannot get docstring*
      - sameYet/2: *no docstring*
      - isSettled/1: *no docstring*
      - makeTraversalKey/1: *no docstring*
      - optSame/2: *no docstring*
      - sameEver/2: *no docstring*

_makeVerbFacet
    *cannot get docstring*
      - curryCall/2: *no docstring*

_mapEmpty
    *cannot get docstring*
      - _printOn/1: *no docstring*
      - coerce/2: *no docstring*

_mapExtract
    *cannot get docstring*
      - run/1: *no docstring*
      - withDefault/2: *no docstring*

_matchSame
    *cannot get docstring*
      - run/1: *no docstring*
      - different/1: *no docstring*

_quasiMatcher
    *cannot get docstring*
      - run/2: *no docstring*

_slotToBinding
    *cannot get docstring*
      - run/1: *no docstring*
      - run/2: *no docstring*

_splitList
    *cannot get docstring*
      - run/1: *no docstring*

_suchThat
    *cannot get docstring*
      - run/1: *no docstring*
      - run/2: *no docstring*

_switchFailed
    *cannot get docstring*

_validateFor
    *cannot get docstring*
      - run/1: *no docstring*


Interface constructors
----------------------

_makeMessageDesc
    *cannot get docstring*
      - run/4: *no docstring*

_makeParamDesc
    *cannot get docstring*
      - run/2: *no docstring*

_makeProtocolDesc
    *cannot get docstring*
      - run/5: *no docstring*
      - makePair/5: *no docstring*


Unsafe Scope
============


Time
----

Timer
    *cannot get docstring*
      - fromNow/1: *no docstring*
      - run/1: *no docstring*
      - unsafeNow/0: *no docstring*
      - sendTimestamp/1: *no docstring*


I/O
---

makeStdErr
    *cannot get docstring*
      - run/0: *no docstring*

makeStdIn
    *cannot get docstring*
      - run/0: *no docstring*

makeStdOut
    *cannot get docstring*
      - run/0: *no docstring*

makeFileResource
    *cannot get docstring*
      - run/1: *no docstring*


Networking
----------

makeTCP4ClientEndpoint
    *cannot get docstring*
      - run/2: *no docstring*

makeTCP4ServerEndpoint
    *cannot get docstring*
      - run/1: *no docstring*

getAddrInfo
    *cannot get docstring*
      - run/2: *no docstring*


Runtime
-------

currentRuntime
    *cannot get docstring*
      - getReactorStatistics/0: *no docstring*
      - getDisassembler/0: *no docstring*
      - getCrypt/0: *no docstring*
      - getHeapStatistics/0: *no docstring*

unsealException
    *cannot get docstring*
      - run/2: *no docstring*


Processes and Vats
------------------

currentProcess
    *cannot get docstring*
      - interrupt/0: *no docstring*
      - getEnvironment/0: *no docstring*
      - getArguments/0: *no docstring*
      - getPID/0: *no docstring*

currentVat
    *cannot get docstring*
      - seed/1: *no docstring*
      - sprout/2: *no docstring*
      - run/0: *no docstring*

makeProcess
    *cannot get docstring*

