Operations on Basic Data
========================

  - ``Bool``

    - and, or, xor, not, butNot, pick
    - op__cmp

  - ``Int``

    - add, subtract, multiply, negate, approxDivide, floorDivide,
      mod, pow, modPow
    - and, or, xor, bitLength, complement, shiftLeft, shiftRight
    - abs
    - next, previous
    - aboveZero, atLeastZero, atMostZero, belowZero, isZero, op__cmp,
      max, min
    - floor, toBytes

  - ``Double``

    - add, subtract, multiply, negate, approxDivide, floorDivide
    - abs, sqrt, log, sin, cos, tan
    - aboveZero, atLeastZero, atMostZero, belowZero, isZero, op__cmp
    - floor, toBytes

  - ``Char``

    - add, subtract
    - asInteger, asString, quote
    - max, min, op__cmp
    - next, previous
    - getCategory

  - ``Str``

    - with, get, size
    - contains, startsWith, endsWith, indexOf
    - add, replace, join, multiply, slice, split, trim, toUpperCase,
      toLowerCase
    - asList, asSet, _makeIterator, quote
    - getSpan
    - op__cmp

  - ``Bytes``

    - with, size, get
    - add, join, multiply, replace, slice, split, toLowerCase,
      toUpperCase, trim
    - contains, indexOf, lastIndexOf
    - asList, asSet
    - _makeIterator


safeScope
=========

Bindings in the safe scope are available to modules by
default. They are all `DeepFrozen`.

.. todo::
   Fix the `module.name` notation
   resulting from abuse of sphinx python support.

.. py:module:: safeScope


Primitive values
----------------

.. py:data:: true

   *cannot get docstring*

.. py:data:: false

   *cannot get docstring*

.. py:data:: null

   *cannot get docstring*

.. py:data:: NaN

   *cannot get docstring*

.. py:data:: Infinity

   *cannot get docstring*


Data Constructors
-----------------

.. py:data:: _makeInt

   
   A maker of `Int`s.
   

   .. py:method:: fromBytes/1

      *no docstring*

   .. py:method:: fromBytes/2

      *no docstring*

   .. py:method:: run/1

      *no docstring*

   .. py:method:: run/2

      *no docstring*


.. py:data:: _makeDouble

   
   A maker of `Double`s.
   

   .. py:method:: run/1

      *no docstring*

   .. py:method:: fromBytes/1

      *no docstring*


.. py:data:: _makeString

   
   A maker of `Str`s.
   

   .. py:method:: fromString/1

      *no docstring*

   .. py:method:: fromString/2

      *no docstring*

   .. py:method:: fromChars/1

      *no docstring*


.. py:data:: _makeBytes

   
   A maker of `Bytes`.
   

   .. py:method:: fromString/1

      *no docstring*

   .. py:method:: fromInts/1

      *no docstring*


.. py:data:: _makeList

   
   A maker of `List`s.
   

   .. py:method:: fromIterable/1

      *no docstring*


.. py:data:: _makeMap

   
   Given a `List[Pair]`, produce a `Map`.
   

   .. py:method:: fromPairs/1

      *no docstring*


.. py:data:: _makeOrderedSpace

   The maker of ordered vector spaces.
   
   This object implements several Monte operators, including those which
   provide ordered space syntax.

   .. py:method:: spaceOfGuard/1

      *no docstring*

   .. py:method:: spaceOfValue/1

      *no docstring*

   .. py:method:: op__till/2

      *no docstring*

   .. py:method:: op__thru/2

      *no docstring*


.. py:data:: _makeTopSet

   

   .. py:method:: run/5

      *no docstring*


.. py:data:: _makeOrderedRegion

   Make regions for sets of objects with total ordering.

   .. py:method:: run/3

      *no docstring*


.. py:data:: _makeSourceSpan

   *no docstring*

   .. py:method:: run/6

      *no docstring*


.. py:data:: _makeFinalSlot

   
   A maker of final slots.
   

   .. py:method:: run/3

      *no docstring*

   .. py:method:: asType/0

      *no docstring*


.. py:data:: _makeVarSlot

   
   A maker of var slots.
   

   .. py:method:: run/3

      *no docstring*

   .. py:method:: asType/0

      *no docstring*


.. py:data:: makeLazySlot

   Make a slot that lazily binds its value.

   .. py:method:: run/1

      *no docstring*



Basic guards
------------

.. py:data:: Any

   
   A guard which admits the universal set.
   
   This object specializes to a guard which admits the union of its
   subguards: Any[X, Y, Z] =~ X ∪ Y ∪ Z
   
   This guard is unretractable.
   

   .. py:method:: supersetOf/1

      *no docstring*

   .. py:method:: getMethods/0

      *no docstring*

   .. py:method:: coerce/2

      *no docstring*

   .. py:method:: extractGuards/2

      *no docstring*


.. py:data:: Void

   
   The singleton set of null: `[null].asSet()`
   
   This guard is unretractable.
   

   .. py:method:: supersetOf/1

      *no docstring*

   .. py:method:: coerce/2

      *no docstring*


.. py:data:: Empty

   An unretractable predicate guard.
   
   This guard admits any object which passes its predicate.

   .. py:method:: _printOn/1

      *no docstring*

   .. py:method:: coerce/2

      *no docstring*


.. py:data:: Bool

   
   The set of Boolean values: `[true, false].asSet()`
   
   This guard is unretractable.
   

   .. py:method:: supersetOf/1

      *no docstring*

   .. py:method:: coerce/2

      *no docstring*


.. py:data:: Str

   An ordered vector space.
   
   As a guard, this object admits any value in the set of objects in
   the space. Comparison operators may be used on this object to
   create subguards which only admit a partition of the set.

   .. py:method:: _printOn/1

      *no docstring*

   .. py:method:: _uncall/0

      *no docstring*

   .. py:method:: coerce/2

      *no docstring*

   .. py:method:: op__cmp/1

      *no docstring*

   .. py:method:: add/1

      *no docstring*

   .. py:method:: subtract/1

      *no docstring*

   .. py:method:: makeRegion/4

      *no docstring*


.. py:data:: Char

   An ordered vector space.
   
   As a guard, this object admits any value in the set of objects in
   the space. Comparison operators may be used on this object to
   create subguards which only admit a partition of the set.

   .. py:method:: _printOn/1

      *no docstring*

   .. py:method:: _uncall/0

      *no docstring*

   .. py:method:: coerce/2

      *no docstring*

   .. py:method:: op__cmp/1

      *no docstring*

   .. py:method:: add/1

      *no docstring*

   .. py:method:: subtract/1

      *no docstring*

   .. py:method:: makeRegion/4

      *no docstring*


.. py:data:: Double

   An ordered vector space.
   
   As a guard, this object admits any value in the set of objects in
   the space. Comparison operators may be used on this object to
   create subguards which only admit a partition of the set.

   .. py:method:: _printOn/1

      *no docstring*

   .. py:method:: _uncall/0

      *no docstring*

   .. py:method:: coerce/2

      *no docstring*

   .. py:method:: op__cmp/1

      *no docstring*

   .. py:method:: add/1

      *no docstring*

   .. py:method:: subtract/1

      *no docstring*

   .. py:method:: makeRegion/4

      *no docstring*


.. py:data:: Int

   An ordered vector space.
   
   As a guard, this object admits any value in the set of objects in
   the space. Comparison operators may be used on this object to
   create subguards which only admit a partition of the set.

   .. py:method:: _printOn/1

      *no docstring*

   .. py:method:: _uncall/0

      *no docstring*

   .. py:method:: coerce/2

      *no docstring*

   .. py:method:: op__cmp/1

      *no docstring*

   .. py:method:: add/1

      *no docstring*

   .. py:method:: subtract/1

      *no docstring*

   .. py:method:: makeRegion/4

      *no docstring*


.. py:data:: Bytes

   An ordered vector space.
   
   As a guard, this object admits any value in the set of objects in
   the space. Comparison operators may be used on this object to
   create subguards which only admit a partition of the set.

   .. py:method:: _printOn/1

      *no docstring*

   .. py:method:: _uncall/0

      *no docstring*

   .. py:method:: coerce/2

      *no docstring*

   .. py:method:: op__cmp/1

      *no docstring*

   .. py:method:: add/1

      *no docstring*

   .. py:method:: subtract/1

      *no docstring*

   .. py:method:: makeRegion/4

      *no docstring*


.. py:data:: List

   A guard which admits lists.
   
   Only immutable lists are admitted by this object. Mutable lists created
   with `diverge/0` will not be admitted; freeze them first with
   `snapshot/0`.

   .. py:method:: _printOn/1

      *no docstring*

   .. py:method:: coerce/2

      *no docstring*

   .. py:method:: get/1

      *no docstring*

   .. py:method:: extractGuard/2

      *no docstring*


.. py:data:: Map

   A guard which admits maps.
   
   Only immutable maps are admitted by this object. Mutable maps created
   with `diverge/0` will not be admitted; freeze them first with
   `snapshot/0`.

   .. py:method:: _printOn/1

      *no docstring*

   .. py:method:: coerce/2

      *no docstring*

   .. py:method:: get/2

      *no docstring*

   .. py:method:: extractGuards/2

      *no docstring*


.. py:data:: Set

   A guard which admits sets.
   
   Only immutable sets are admitted by this object. Mutable sets created
   with `diverge/0` will not be admitted; freeze them first with
   `snapshot/0`.

   .. py:method:: _printOn/1

      *no docstring*

   .. py:method:: coerce/2

      *no docstring*

   .. py:method:: get/1

      *no docstring*

   .. py:method:: extractGuard/2

      *no docstring*


.. py:data:: Pair

   A guard which admits immutable pairs.
   
   Pairs are merely lists of size two.

   .. py:method:: _printOn/1

      *no docstring*

   .. py:method:: coerce/2

      *no docstring*

   .. py:method:: get/2

      *no docstring*

   .. py:method:: extractGuards/2

      *no docstring*



Guard utilities
---------------

.. py:data:: NullOk

   A guard which admits `null`.
   
   When specialized, this object returns a guard which admits its subguard
   as well as `null`.

   .. py:method:: coerce/2

      *no docstring*

   .. py:method:: get/1

      *no docstring*

   .. py:method:: extractGuard/2

      *no docstring*


.. py:data:: Same

   
   When specialized, this object yields a guard which only admits precisely
   the object used to specialize it.
   
   In simpler terms, `Same[x]` will match only those objects `o` for which `o
   == x`.
   

   .. py:method:: extractValue/2

      *no docstring*

   .. py:method:: get/1

      *no docstring*


.. py:data:: SubrangeGuard

   
   The maker of subrange guards.
   
   When specialized with a guard, this object produces a auditor for those
   guards which admit proper subsets of that guard.
   

   .. py:method:: get/1

      *no docstring*


.. py:data:: _auditedBy

   
   Whether an auditor has audited a specimen.
   

   .. py:method:: run/2

      *no docstring*



Tracing
-------

.. py:data:: trace

   
   Write a line to the trace log.
   
   This object is a Typhon standard runtime `traceln`. It prints prefixed
   lines to stderr.
   
   Call `.exception(problem)` to print a problem to stderr, including
   a formatted traceback.
   

   .. py:method:: exception/1

      *no docstring*


.. py:data:: traceln

   
   Write a line to the trace log.
   
   This object is a Typhon standard runtime `traceln`. It prints prefixed
   lines to stderr.
   
   Call `.exception(problem)` to print a problem to stderr, including
   a formatted traceback.
   

   .. py:method:: exception/1

      *no docstring*



Brands
------

.. py:data:: makeBrandPair

   Make a [sealer, unsealer] pair.

   .. py:method:: run/1

      *no docstring*



Quasiparsers
------------

.. py:data:: simple__quasiParser

   A quasiparser of Unicode strings.
   
   This object is the default quasiparser. It can interpolate any object
   into a string by pretty-printing it; in fact, that is one of this
   object's primary uses.
   
   When used as a pattern, this object performs basic text matching.
   Patterns always succeed, grabbing zero or more characters non-greedily
   until the next segment. When patterns are concatenated in the
   quasiliteral, only the rightmost pattern can match any characters; the
   other patterns to the left will all match the empty string.

   .. py:method:: patternHole/1

      *no docstring*

   .. py:method:: valueHole/1

      *no docstring*

   .. py:method:: matchMaker/1

      *no docstring*

   .. py:method:: valueMaker/1

      *no docstring*


.. py:data:: b__quasiParser

   A quasiparser for `Bytes`.
   
   This object behaves like `simple__quasiParser`; it takes some textual
   descriptions of bytes and returns a bytestring. It can interpolate
   objects which coerce to `Bytes` and `Str`.
   
   As a pattern, this object performs slicing of bytestrings. Semantics
   mirror `simple__quasiParser` with respect to concatenated patterns and
   greediness.

   .. py:method:: patternHole/1

      *no docstring*

   .. py:method:: valueHole/1

      *no docstring*

   .. py:method:: matchMaker/1

      *no docstring*

   .. py:method:: valueMaker/1

      *no docstring*


.. py:data:: m__quasiParser

   A quasiparser for the Monte programming language.
   
   This object will parse any Monte expression and return an opaque
   value. In the near future, this object will instead return a translucent
   view into a Monte compiler and optimizer.

   .. py:method:: getAstBuilder/0

      *no docstring*

   .. py:method:: valueHole/1

      *no docstring*

   .. py:method:: patternHole/1

      *no docstring*

   .. py:method:: valueMaker/1

      *no docstring*

   .. py:method:: matchMaker/1

      *no docstring*

   .. py:method:: fromStr/1

      *no docstring*



Flow control
------------

.. py:data:: M

   
   Miscellaneous vat management and quoting services.
   

   .. py:method:: send/4

      *no docstring*

   .. py:method:: callWithPair/3

      *no docstring*

   .. py:method:: toString/1

      *no docstring*

   .. py:method:: call/3

      *no docstring*

   .. py:method:: sendOnly/4

      *no docstring*

   .. py:method:: callWithMessage/2

      *no docstring*

   .. py:method:: sendOnly/3

      *no docstring*

   .. py:method:: send/3

      *no docstring*

   .. py:method:: call/4

      *no docstring*

   .. py:method:: callWithPair/2

      *no docstring*

   .. py:method:: toQuote/1

      *no docstring*


.. py:data:: throw

   *no docstring*

   .. py:method:: run/1

      *no docstring*

   .. py:method:: eject/2

      *no docstring*


.. py:data:: _loop

   
   Perform an iterative loop.
   

   .. py:method:: run/2

      *no docstring*


.. py:data:: _iterForever

   Implementation of while-expression syntax.

   .. py:method:: _makeIterator/0

      *no docstring*

   .. py:method:: next/1

      *no docstring*



Evaluation
----------

.. py:data:: eval

   Evaluate Monte source.
   
   This object respects POLA and grants no privileges whatsoever to
   evaluated code. To grant a safe scope, pass `safeScope`.

   .. py:method:: run/2

      *no docstring*

   .. py:method:: evalToPair/2

      *no docstring*


.. py:data:: typhonEval

   *no docstring*

   .. py:method:: evalToPair/2

      *no docstring*

   .. py:method:: fromAST/3

      *no docstring*

   .. py:method:: run/2

      *no docstring*



Reference/object operations
---------------------------

.. py:data:: Ref

   
   Ref management and utilities.
   

   .. py:method:: isDeepFrozen/1

      *no docstring*

   .. py:method:: isSelfish/1

      *no docstring*

   .. py:method:: makeProxy/3

      *no docstring*

   .. py:method:: promise/0

      *no docstring*

   .. py:method:: isSettled/1

      *no docstring*

   .. py:method:: broken/1

      *no docstring*

   .. py:method:: state/1

      *no docstring*

   .. py:method:: isFar/1

      *no docstring*

   .. py:method:: optProblem/1

      *no docstring*

   .. py:method:: isSelfless/1

      *no docstring*

   .. py:method:: isNear/1

      *no docstring*

   .. py:method:: isResolved/1

      *no docstring*

   .. py:method:: whenResolved/2

      *no docstring*

   .. py:method:: isEventual/1

      *no docstring*

   .. py:method:: fulfillment/1

      *no docstring*

   .. py:method:: isBroken/1

      *no docstring*

   .. py:method:: whenResolvedOnly/2

      *no docstring*

   .. py:method:: whenBroken/2

      *no docstring*


.. py:data:: promiseAllFulfilled

   

   .. py:method:: run/1

      *no docstring*


.. py:data:: DeepFrozen

   
   Auditor and guard for transitive immutability.
   

   .. py:method:: audit/1

      *no docstring*

   .. py:method:: coerce/2

      *no docstring*

   .. py:method:: supersetOf/1

      *no docstring*


.. py:data:: Selfless

   
   A stamp for incomparable objects.
   
   `Selfless` objects are generally not equal to any objects but themselves.
   They may choose to implement alternative comparison protocols such as
   `Transparent`.
   

   .. py:method:: audit/1

      *no docstring*

   .. py:method:: coerce/2

      *no docstring*

   .. py:method:: passes/1

      *no docstring*


.. py:data:: Transparent

   Objects that Transparent admits have reliable ._uncall() methods, in the sense
   that they correctly identify their maker and their entire state, and that
   invoking the maker with the given args will produce an object with the same
   state. Objects that are both Selfless and Transparent are compared for sameness
   by comparing their uncalls.

   .. py:method:: coerce/2

      *no docstring*

   .. py:method:: makeAuditorKit/0

      *no docstring*


.. py:data:: Near

   
   A guard over references to near values.
   
   This guard admits any near value, as well as any resolved reference to any
   near value.
   
   This guard is unretractable.
   

   .. py:method:: coerce/2

      *no docstring*


.. py:data:: Binding

   
   A guard which admits bindings.
   

   .. py:method:: supersetOf/1

      *no docstring*

   .. py:method:: coerce/2

      *no docstring*



Abstract Syntax
---------------

.. py:data:: astBuilder

   

   .. py:method:: getAstGuard/0

      *no docstring*

   .. py:method:: getPatternGuard/0

      *no docstring*

   .. py:method:: getExprGuard/0

      *no docstring*

   .. py:method:: getNamePatternGuard/0

      *no docstring*

   .. py:method:: getNounGuard/0

      *no docstring*

   .. py:method:: LiteralExpr/2

      *no docstring*

   .. py:method:: NounExpr/2

      *no docstring*

   .. py:method:: TempNounExpr/2

      *no docstring*

   .. py:method:: SlotExpr/2

      *no docstring*

   .. py:method:: MetaContextExpr/1

      *no docstring*

   .. py:method:: MetaStateExpr/1

      *no docstring*

   .. py:method:: BindingExpr/2

      *no docstring*

   .. py:method:: SeqExpr/2

      *no docstring*

   .. py:method:: Module/4

      *no docstring*

   .. py:method:: NamedArg/3

      *no docstring*

   .. py:method:: NamedArgExport/2

      *no docstring*

   .. py:method:: MethodCallExpr/5

      *no docstring*

   .. py:method:: FunCallExpr/4

      *no docstring*

   .. py:method:: SendExpr/5

      *no docstring*

   .. py:method:: FunSendExpr/4

      *no docstring*

   .. py:method:: GetExpr/3

      *no docstring*

   .. py:method:: AndExpr/3

      *no docstring*

   .. py:method:: OrExpr/3

      *no docstring*

   .. py:method:: BinaryExpr/4

      *no docstring*

   .. py:method:: CompareExpr/4

      *no docstring*

   .. py:method:: RangeExpr/4

      *no docstring*

   .. py:method:: SameExpr/4

      *no docstring*

   .. py:method:: MatchBindExpr/3

      *no docstring*

   .. py:method:: MismatchExpr/3

      *no docstring*

   .. py:method:: PrefixExpr/3

      *no docstring*

   .. py:method:: CoerceExpr/3

      *no docstring*

   .. py:method:: CurryExpr/4

      *no docstring*

   .. py:method:: ExitExpr/3

      *no docstring*

   .. py:method:: ForwardExpr/2

      *no docstring*

   .. py:method:: VarPattern/3

      *no docstring*

   .. py:method:: DefExpr/4

      *no docstring*

   .. py:method:: AssignExpr/3

      *no docstring*

   .. py:method:: VerbAssignExpr/4

      *no docstring*

   .. py:method:: AugAssignExpr/4

      *no docstring*

   .. py:method:: Method/7

      *no docstring*

   .. py:method:: To/7

      *no docstring*

   .. py:method:: Matcher/3

      *no docstring*

   .. py:method:: Catcher/3

      *no docstring*

   .. py:method:: Script/4

      *no docstring*

   .. py:method:: FunctionScript/5

      *no docstring*

   .. py:method:: FunctionExpr/3

      *no docstring*

   .. py:method:: ListExpr/2

      *no docstring*

   .. py:method:: ListComprehensionExpr/6

      *no docstring*

   .. py:method:: MapExprAssoc/3

      *no docstring*

   .. py:method:: MapExprExport/2

      *no docstring*

   .. py:method:: MapExpr/2

      *no docstring*

   .. py:method:: MapComprehensionExpr/7

      *no docstring*

   .. py:method:: ForExpr/7

      *no docstring*

   .. py:method:: ObjectExpr/6

      *no docstring*

   .. py:method:: ParamDesc/3

      *no docstring*

   .. py:method:: MessageDesc/5

      *no docstring*

   .. py:method:: InterfaceExpr/7

      *no docstring*

   .. py:method:: FunctionInterfaceExpr/7

      *no docstring*

   .. py:method:: CatchExpr/4

      *no docstring*

   .. py:method:: FinallyExpr/3

      *no docstring*

   .. py:method:: TryExpr/4

      *no docstring*

   .. py:method:: EscapeExpr/5

      *no docstring*

   .. py:method:: SwitchExpr/3

      *no docstring*

   .. py:method:: WhenExpr/5

      *no docstring*

   .. py:method:: IfExpr/4

      *no docstring*

   .. py:method:: WhileExpr/4

      *no docstring*

   .. py:method:: HideExpr/2

      *no docstring*

   .. py:method:: ValueHoleExpr/2

      *no docstring*

   .. py:method:: PatternHoleExpr/2

      *no docstring*

   .. py:method:: ValueHolePattern/2

      *no docstring*

   .. py:method:: PatternHolePattern/2

      *no docstring*

   .. py:method:: FinalPattern/3

      *no docstring*

   .. py:method:: SlotPattern/3

      *no docstring*

   .. py:method:: BindingPattern/2

      *no docstring*

   .. py:method:: BindPattern/3

      *no docstring*

   .. py:method:: IgnorePattern/2

      *no docstring*

   .. py:method:: ListPattern/3

      *no docstring*

   .. py:method:: MapPatternAssoc/4

      *no docstring*

   .. py:method:: MapPatternImport/3

      *no docstring*

   .. py:method:: MapPattern/3

      *no docstring*

   .. py:method:: NamedParam/4

      *no docstring*

   .. py:method:: NamedParamImport/3

      *no docstring*

   .. py:method:: ViaPattern/3

      *no docstring*

   .. py:method:: SuchThatPattern/3

      *no docstring*

   .. py:method:: SamePattern/3

      *no docstring*

   .. py:method:: QuasiText/2

      *no docstring*

   .. py:method:: QuasiExprHole/2

      *no docstring*

   .. py:method:: QuasiPatternHole/2

      *no docstring*

   .. py:method:: QuasiParserExpr/3

      *no docstring*

   .. py:method:: QuasiParserPattern/3

      *no docstring*



Utilities for syntax expansions
-------------------------------

.. py:data:: _accumulateList

   Implementation of list comprehension syntax.

   .. py:method:: run/2

      *no docstring*


.. py:data:: _accumulateMap

   Implementation of map comprehension syntax.

   .. py:method:: run/2

      *no docstring*


.. py:data:: _bind

   Resolve a forward declaration.

   .. py:method:: run/2

      *no docstring*


.. py:data:: _booleanFlow

   Implementation of implicit breakage semantics in conditionally-defined
   names.

   .. py:method:: broken/0

      *no docstring*

   .. py:method:: failureList/1

      *no docstring*


.. py:data:: _comparer

   A comparison helper.
   
   This object implements the various comparison operators.

   .. py:method:: asBigAs/2

      *no docstring*

   .. py:method:: geq/2

      *no docstring*

   .. py:method:: greaterThan/2

      *no docstring*

   .. py:method:: leq/2

      *no docstring*

   .. py:method:: lessThan/2

      *no docstring*


.. py:data:: _equalizer

   
   A perceiver of identity.
   
   This object can discern whether any two objects are distinct from each
   other.
   

   .. py:method:: sameYet/2

      *no docstring*

   .. py:method:: isSettled/1

      *no docstring*

   .. py:method:: makeTraversalKey/1

      *no docstring*

   .. py:method:: optSame/2

      *no docstring*

   .. py:method:: sameEver/2

      *no docstring*


.. py:data:: _makeVerbFacet

   The operator `obj`.`method`.

   .. py:method:: curryCall/2

      *no docstring*


.. py:data:: _mapEmpty

   An unretractable predicate guard.
   
   This guard admits any object which passes its predicate.

   .. py:method:: _printOn/1

      *no docstring*

   .. py:method:: coerce/2

      *no docstring*


.. py:data:: _mapExtract

   Implementation of key pattern-matching syntax in map patterns.

   .. py:method:: run/1

      *no docstring*

   .. py:method:: withDefault/2

      *no docstring*


.. py:data:: _matchSame

   

   .. py:method:: run/1

      *no docstring*

   .. py:method:: different/1

      *no docstring*


.. py:data:: _quasiMatcher

   Implementation of quasiliteral pattern syntax.

   .. py:method:: run/2

      *no docstring*


.. py:data:: _slotToBinding

   
   Implementation of bind-pattern syntax for forward declarations.
   

   .. py:method:: run/1

      *no docstring*

   .. py:method:: run/2

      *no docstring*


.. py:data:: _splitList

   Implementation of tail pattern-matching syntax in list patterns.
   
   m`def [x] + xs := l`.expand() ==
   m`def via (_splitList.run(1)) [x, xs] := l`

   .. py:method:: run/1

      *no docstring*


.. py:data:: _suchThat

   The pattern patt ? (expr).

   .. py:method:: run/1

      *no docstring*

   .. py:method:: run/2

      *no docstring*


.. py:data:: _switchFailed

   The implicit default matcher in a switch expression.
   
   This object throws an exception.


.. py:data:: _validateFor

   Ensure that `flag` is `true`.
   
   This object is a safeguard against malicious loop objects. A flag is set
   to `true` and closed over by a loop body; once the loop is finished, the
   flag is set to `false` and the loop cannot be reëntered.

   .. py:method:: run/1

      *no docstring*



Interface constructors
----------------------

.. py:data:: _makeMessageDesc

   Describe a message.

   .. py:method:: run/4

      *no docstring*


.. py:data:: _makeParamDesc

   Describe a parameter.

   .. py:method:: run/2

      *no docstring*


.. py:data:: _makeProtocolDesc

   Produce an interface.

   .. py:method:: run/5

      *no docstring*

   .. py:method:: makePair/5

      *no docstring*



Entrypoint Arguments
====================

.. todo::
   Fix the `module.name` notation
   resulting from abuse of sphinx python support.

.. py:module:: __entrypoint_io__


Time
----

.. py:data:: Timer

   
   An unsafe nondeterministic clock.
   
   This object provides a useful collection of time-related methods:
   * `fromNow(delay :Double)`: Produce a promise which will fully resolve
   after at least `delay` seconds have elapsed in the runtime.
   * `sendTimestamp(callable)`: Send a `Double` representing the runtime's
   clock to `callable`.
   
   There is extremely unsafe functionality as well:
   * `unsafeNow()`: The current system time.
   
   Use with caution.
   

   .. py:method:: fromNow/1

      *no docstring*

   .. py:method:: run/1

      *no docstring*

   .. py:method:: unsafeNow/0

      *no docstring*

   .. py:method:: sendTimestamp/1

      *no docstring*



I/O
---

.. py:data:: makeStdErr

   *no docstring*

   .. py:method:: run/0

      *no docstring*


.. py:data:: makeStdIn

   *no docstring*

   .. py:method:: run/0

      *no docstring*


.. py:data:: makeStdOut

   *no docstring*

   .. py:method:: run/0

      *no docstring*


.. py:data:: makeFileResource

   
   Make a file Resource.
   

   .. py:method:: run/1

      *no docstring*



Networking
----------

.. py:data:: makeTCP4ClientEndpoint

   
   Make a TCPv4 client endpoint.
   

   .. py:method:: run/2

      *no docstring*


.. py:data:: makeTCP4ServerEndpoint

   
   Make a TCPv4 server endpoint.
   

   .. py:method:: run/1

      *no docstring*


.. py:data:: getAddrInfo

   *no docstring*

   .. py:method:: run/2

      *no docstring*



Runtime
-------

.. py:data:: currentRuntime

   
   The Typhon runtime.
   
   This object is a platform-specific view into the configuration and
   performance of the current runtime in the current process.
   
   This object is necessarily unsafe and nondeterministic.
   

   .. py:method:: getReactorStatistics/0

      *no docstring*

   .. py:method:: getDisassembler/0

      *no docstring*

   .. py:method:: getCrypt/0

      *no docstring*

   .. py:method:: getHeapStatistics/0

      *no docstring*


.. py:data:: unsealException

   
   Unseal a specimen.
   

   .. py:method:: run/2

      *no docstring*



Processes and Vats
------------------

.. py:data:: currentProcess

   
   The current process on the local node.
   

   .. py:method:: interrupt/0

      *no docstring*

   .. py:method:: getEnvironment/0

      *no docstring*

   .. py:method:: getArguments/0

      *no docstring*

   .. py:method:: getPID/0

      *no docstring*


.. py:data:: currentVat

   
   Turn management and object isolation.
   

   .. py:method:: seed/1

      *no docstring*

   .. py:method:: sprout/2

      *no docstring*

   .. py:method:: run/0

      *no docstring*


.. py:data:: makeProcess

   
   Create a subordinate process on the current node from the given
   executable, arguments, and environment.
   
   `=> stdinFount`, if not null, will be treated as a fount and it will be
   flowed to a drain representing stdin. `=> stdoutDrain` and
   `=> stderrDrain` are similar but should be drains which will have founts
   flowed to them.
