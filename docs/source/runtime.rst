.. _safescope:

safeScope
=========

Bindings in the safe scope are available to modules by
default. They are all `DeepFrozen`.

.. todo::
   Fix the `module.name` notation
   resulting from abuse of sphinx python support.

.. todo::
   When ``Bool`` is fixed to reveal its interface,
   re-run mtDocStrings to document and, or, xor, not, butNot, pick, op__cmp.

.. py:module:: safeScope


Basic guards
------------

.. py:class:: Bool

   
   The set of Boolean values: `[true, false].asSet()`
   
   This guard is unretractable.
   

   .. py:staticmethod:: coerce(_, _)

      *no docstring*

   .. py:staticmethod:: getDocstring()

      *no docstring*

   .. py:staticmethod:: getMethods()

      *no docstring*

   .. py:staticmethod:: supersetOf(_)

      *no docstring*



.. py:class:: Str

   An ordered vector space.
   
   As a guard, this object admits any value in the set of objects in
   the space. Comparison operators may be used on this object to
   create subguards which only admit a partition of the set.

   .. py:staticmethod:: _printOn(_)

      *no docstring*

   .. py:staticmethod:: _uncall()

      *no docstring*

   .. py:staticmethod:: add(_)

      *no docstring*

   .. py:staticmethod:: coerce(_, _)

      *no docstring*

   .. py:staticmethod:: makeEmptyRegion()

      *no docstring*

   .. py:staticmethod:: makeRegion(_, _, _, _)

      *no docstring*

   .. py:staticmethod:: op__cmp(_)

      *no docstring*

   .. py:staticmethod:: subtract(_)

      *no docstring*


   .. py:method:: _makeIterator()

      *no docstring*

   .. py:method:: add(_)

      *no docstring*

   .. py:method:: asList()

      *no docstring*

   .. py:method:: asSet()

      *no docstring*

   .. py:method:: contains(_)

      *no docstring*

   .. py:method:: endsWith(_)

      *no docstring*

   .. py:method:: get(_)

      *no docstring*

   .. py:method:: getSpan()

      *no docstring*

   .. py:method:: indexOf(_, _)

      *no docstring*

   .. py:method:: isEmpty()

      *no docstring*

   .. py:method:: join(_)

      *no docstring*

   .. py:method:: lastIndexOf(_)

      *no docstring*

   .. py:method:: multiply(_)

      *no docstring*

   .. py:method:: op__cmp(_)

      *no docstring*

   .. py:method:: quote()

      *no docstring*

   .. py:method:: replace(_, _)

      *no docstring*

   .. py:method:: size()

      *no docstring*

   .. py:method:: slice(_)

      *no docstring*

   .. py:method:: split(_, _)

      *no docstring*

   .. py:method:: startsWith(_)

      Whether this string has `s` as a prefix.

   .. py:method:: toLowerCase()

      *no docstring*

   .. py:method:: toUpperCase()

      *no docstring*

   .. py:method:: trim()

      *no docstring*

   .. py:method:: with(_)

      *no docstring*


.. py:class:: Char

   An ordered vector space.
   
   As a guard, this object admits any value in the set of objects in
   the space. Comparison operators may be used on this object to
   create subguards which only admit a partition of the set.

   .. py:staticmethod:: _printOn(_)

      *no docstring*

   .. py:staticmethod:: _uncall()

      *no docstring*

   .. py:staticmethod:: add(_)

      *no docstring*

   .. py:staticmethod:: coerce(_, _)

      *no docstring*

   .. py:staticmethod:: makeEmptyRegion()

      *no docstring*

   .. py:staticmethod:: makeRegion(_, _, _, _)

      *no docstring*

   .. py:staticmethod:: op__cmp(_)

      *no docstring*

   .. py:staticmethod:: subtract(_)

      *no docstring*


   .. py:method:: add(_)

      *no docstring*

   .. py:method:: asInteger()

      *no docstring*

   .. py:method:: asString()

      *no docstring*

   .. py:method:: getCategory()

      *no docstring*

   .. py:method:: max(_)

      *no docstring*

   .. py:method:: min(_)

      *no docstring*

   .. py:method:: next()

      *no docstring*

   .. py:method:: op__cmp(_)

      *no docstring*

   .. py:method:: previous()

      *no docstring*

   .. py:method:: quote()

      *no docstring*

   .. py:method:: subtract(_)

      *no docstring*


.. py:class:: Double

   An ordered vector space.
   
   As a guard, this object admits any value in the set of objects in
   the space. Comparison operators may be used on this object to
   create subguards which only admit a partition of the set.

   .. py:staticmethod:: _printOn(_)

      *no docstring*

   .. py:staticmethod:: _uncall()

      *no docstring*

   .. py:staticmethod:: add(_)

      *no docstring*

   .. py:staticmethod:: coerce(_, _)

      *no docstring*

   .. py:staticmethod:: makeEmptyRegion()

      *no docstring*

   .. py:staticmethod:: makeRegion(_, _, _, _)

      *no docstring*

   .. py:staticmethod:: op__cmp(_)

      *no docstring*

   .. py:staticmethod:: subtract(_)

      *no docstring*


   .. py:method:: aboveZero()

      *no docstring*

   .. py:method:: abs()

      *no docstring*

   .. py:method:: add(_)

      *no docstring*

   .. py:method:: approxDivide(_)

      *no docstring*

   .. py:method:: atLeastZero()

      *no docstring*

   .. py:method:: atMostZero()

      *no docstring*

   .. py:method:: belowZero()

      *no docstring*

   .. py:method:: cos()

      *no docstring*

   .. py:method:: floor()

      *no docstring*

   .. py:method:: floorDivide(_)

      *no docstring*

   .. py:method:: isZero()

      *no docstring*

   .. py:method:: log()

      *no docstring*

   .. py:method:: multiply(_)

      *no docstring*

   .. py:method:: negate()

      *no docstring*

   .. py:method:: op__cmp(_)

      *no docstring*

   .. py:method:: pow(_)

      *no docstring*

   .. py:method:: sin()

      *no docstring*

   .. py:method:: sqrt()

      *no docstring*

   .. py:method:: subtract(_)

      *no docstring*

   .. py:method:: tan()

      *no docstring*

   .. py:method:: toBytes()

      *no docstring*


.. py:class:: Int

   An ordered vector space.
   
   As a guard, this object admits any value in the set of objects in
   the space. Comparison operators may be used on this object to
   create subguards which only admit a partition of the set.

   .. py:staticmethod:: _printOn(_)

      *no docstring*

   .. py:staticmethod:: _uncall()

      *no docstring*

   .. py:staticmethod:: add(_)

      *no docstring*

   .. py:staticmethod:: coerce(_, _)

      *no docstring*

   .. py:staticmethod:: makeEmptyRegion()

      *no docstring*

   .. py:staticmethod:: makeRegion(_, _, _, _)

      *no docstring*

   .. py:staticmethod:: op__cmp(_)

      *no docstring*

   .. py:staticmethod:: subtract(_)

      *no docstring*


   .. py:method:: aboveZero()

      *no docstring*

   .. py:method:: abs()

      *no docstring*

   .. py:method:: add(_)

      *no docstring*

   .. py:method:: and(_)

      *no docstring*

   .. py:method:: approxDivide(_)

      *no docstring*

   .. py:method:: asDouble()

      *no docstring*

   .. py:method:: atLeastZero()

      *no docstring*

   .. py:method:: atMostZero()

      *no docstring*

   .. py:method:: belowZero()

      *no docstring*

   .. py:method:: bitLength()

      *no docstring*

   .. py:method:: complement()

      *no docstring*

   .. py:method:: floorDivide(_)

      *no docstring*

   .. py:method:: isZero()

      *no docstring*

   .. py:method:: max(_)

      *no docstring*

   .. py:method:: min(_)

      *no docstring*

   .. py:method:: mod(_)

      *no docstring*

   .. py:method:: modPow(_, _)

      *no docstring*

   .. py:method:: multiply(_)

      *no docstring*

   .. py:method:: negate()

      *no docstring*

   .. py:method:: next()

      *no docstring*

   .. py:method:: op__cmp(_)

      *no docstring*

   .. py:method:: or(_)

      *no docstring*

   .. py:method:: pow(_)

      *no docstring*

   .. py:method:: previous()

      *no docstring*

   .. py:method:: shiftLeft(_)

      *no docstring*

   .. py:method:: shiftRight(_)

      *no docstring*

   .. py:method:: subtract(_)

      *no docstring*

   .. py:method:: xor(_)

      *no docstring*


.. py:class:: Bytes

   An ordered vector space.
   
   As a guard, this object admits any value in the set of objects in
   the space. Comparison operators may be used on this object to
   create subguards which only admit a partition of the set.

   .. py:staticmethod:: _printOn(_)

      *no docstring*

   .. py:staticmethod:: _uncall()

      *no docstring*

   .. py:staticmethod:: add(_)

      *no docstring*

   .. py:staticmethod:: coerce(_, _)

      *no docstring*

   .. py:staticmethod:: makeEmptyRegion()

      *no docstring*

   .. py:staticmethod:: makeRegion(_, _, _, _)

      *no docstring*

   .. py:staticmethod:: op__cmp(_)

      *no docstring*

   .. py:staticmethod:: subtract(_)

      *no docstring*


   .. py:method:: _makeIterator()

      *no docstring*

   .. py:method:: _uncall()

      *no docstring*

   .. py:method:: add(_)

      *no docstring*

   .. py:method:: asList()

      *no docstring*

   .. py:method:: asSet()

      *no docstring*

   .. py:method:: contains(_)

      *no docstring*

   .. py:method:: get(_)

      *no docstring*

   .. py:method:: indexOf(_)

      *no docstring*

   .. py:method:: isEmpty()

      *no docstring*

   .. py:method:: join(_)

      *no docstring*

   .. py:method:: lastIndexOf(_)

      *no docstring*

   .. py:method:: multiply(_)

      *no docstring*

   .. py:method:: op__cmp(_)

      *no docstring*

   .. py:method:: replace(_, _)

      *no docstring*

   .. py:method:: size()

      *no docstring*

   .. py:method:: slice(_)

      *no docstring*

   .. py:method:: split(_, _)

      *no docstring*

   .. py:method:: toLowerCase()

      *no docstring*

   .. py:method:: toUpperCase()

      *no docstring*

   .. py:method:: trim()

      *no docstring*

   .. py:method:: with(_)

      *no docstring*


.. py:class:: List

   A guard which admits lists.
   
   Only immutable lists are admitted by this object. Mutable lists created
   with `diverge/0` will not be admitted; freeze them first with
   `snapshot/0`.

   .. py:staticmethod:: _printOn(_)

      *no docstring*

   .. py:staticmethod:: coerce(_, _)

      *no docstring*

   .. py:staticmethod:: extractGuard(_, _)

      *no docstring*

   .. py:staticmethod:: get(_)

      *no docstring*


   .. py:method:: _makeIterator()

      *no docstring*

   .. py:method:: _printOn(_)

      *no docstring*

   .. py:method:: _uncall()

      *no docstring*

   .. py:method:: add(_)

      *no docstring*

   .. py:method:: asMap()

      *no docstring*

   .. py:method:: asSet()

      *no docstring*

   .. py:method:: contains(_)

      *no docstring*

   .. py:method:: diverge()

      *no docstring*

   .. py:method:: empty()

      *no docstring*

   .. py:method:: get(_)

      *no docstring*

   .. py:method:: indexOf(_)

      *no docstring*

   .. py:method:: isEmpty()

      *no docstring*

   .. py:method:: join(_)

      *no docstring*

   .. py:method:: last()

      *no docstring*

   .. py:method:: multiply(_)

      *no docstring*

   .. py:method:: op__cmp(_)

      *no docstring*

   .. py:method:: put(_, _)

      *no docstring*

   .. py:method:: reverse()

      *no docstring*

   .. py:method:: size()

      *no docstring*

   .. py:method:: slice(_)

      *no docstring*

   .. py:method:: snapshot()

      *no docstring*

   .. py:method:: sort()

      *no docstring*

   .. py:method:: startOf(_, _)

      *no docstring*

   .. py:method:: with(_, _)

      *no docstring*


.. py:class:: Map

   A guard which admits maps.
   
   Only immutable maps are admitted by this object. Mutable maps created
   with `diverge/0` will not be admitted; freeze them first with
   `snapshot/0`.

   .. py:staticmethod:: _printOn(_)

      *no docstring*

   .. py:staticmethod:: coerce(_, _)

      *no docstring*

   .. py:staticmethod:: extractGuards(_, _)

      *no docstring*

   .. py:staticmethod:: get(_, _)

      *no docstring*


   .. py:method:: _makeIterator()

      *no docstring*

   .. py:method:: _printOn(_)

      *no docstring*

   .. py:method:: _uncall()

      *no docstring*

   .. py:method:: asSet()

      *no docstring*

   .. py:method:: contains(_)

      *no docstring*

   .. py:method:: diverge()

      *no docstring*

   .. py:method:: empty()

      *no docstring*

   .. py:method:: fetch(_, _)

      *no docstring*

   .. py:method:: get(_)

      *no docstring*

   .. py:method:: getKeys()

      *no docstring*

   .. py:method:: getValues()

      *no docstring*

   .. py:method:: isEmpty()

      *no docstring*

   .. py:method:: or(_)

      *no docstring*

   .. py:method:: reverse()

      *no docstring*

   .. py:method:: size()

      *no docstring*

   .. py:method:: slice(_)

      *no docstring*

   .. py:method:: snapshot()

      *no docstring*

   .. py:method:: sortKeys()

      *no docstring*

   .. py:method:: sortValues()

      *no docstring*

   .. py:method:: with(_, _)

      *no docstring*

   .. py:method:: without(_)

      *no docstring*


.. py:class:: Set

   A guard which admits sets.
   
   Only immutable sets are admitted by this object. Mutable sets created
   with `diverge/0` will not be admitted; freeze them first with
   `snapshot/0`.

   .. py:staticmethod:: _printOn(_)

      *no docstring*

   .. py:staticmethod:: coerce(_, _)

      *no docstring*

   .. py:staticmethod:: extractGuard(_, _)

      *no docstring*

   .. py:staticmethod:: get(_)

      *no docstring*


   .. py:method:: _makeIterator()

      *no docstring*

   .. py:method:: _printOn(_)

      *no docstring*

   .. py:method:: _uncall()

      *no docstring*

   .. py:method:: and(_)

      *no docstring*

   .. py:method:: asList()

      *no docstring*

   .. py:method:: asSet()

      *no docstring*

   .. py:method:: butNot(_)

      *no docstring*

   .. py:method:: contains(_)

      *no docstring*

   .. py:method:: diverge()

      *no docstring*

   .. py:method:: empty()

      *no docstring*

   .. py:method:: isEmpty()

      *no docstring*

   .. py:method:: op__cmp(_)

      *no docstring*

   .. py:method:: or(_)

      *no docstring*

   .. py:method:: size()

      *no docstring*

   .. py:method:: slice(_, _)

      *no docstring*

   .. py:method:: snapshot()

      *no docstring*

   .. py:method:: subtract(_)

      *no docstring*

   .. py:method:: with(_)

      *no docstring*

   .. py:method:: without(_)

      *no docstring*


.. py:data:: Pair

   A guard which admits immutable pairs.
   
   Pairs are merely lists of size two.

   .. py:method:: _printOn(_)

      *no docstring*

   .. py:method:: coerce(_, _)

      *no docstring*

   .. py:method:: extractGuards(_, _)

      *no docstring*

   .. py:method:: get(_, _)

      *no docstring*


.. py:class:: FinalSlot

   
   A guard which emits makers of FinalSlots.
   

   .. py:staticmethod:: coerce(_, _)

      *no docstring*

   .. py:staticmethod:: extractGuard(_, _)

      *no docstring*

   .. py:staticmethod:: get(_)

      *no docstring*

   .. py:staticmethod:: getDocstring()

      *no docstring*

   .. py:staticmethod:: getGuard()

      *no docstring*

   .. py:staticmethod:: getMethods()

      *no docstring*

   .. py:staticmethod:: supersetOf(_)

      *no docstring*



.. py:class:: VarSlot

   
   A guard which admits makers of VarSlots.
   

   .. py:staticmethod:: coerce(_, _)

      *no docstring*

   .. py:staticmethod:: extractGuard(_, _)

      *no docstring*

   .. py:staticmethod:: get(_)

      *no docstring*

   .. py:staticmethod:: getDocstring()

      *no docstring*

   .. py:staticmethod:: getGuard()

      *no docstring*

   .. py:staticmethod:: getMethods()

      *no docstring*

   .. py:staticmethod:: supersetOf(_)

      *no docstring*




Guard utilities
---------------

.. py:class:: Any

   
   A guard which admits the universal set.
   
   This object specializes to a guard which admits the union of its
   subguards: Any[X, Y, Z] =~ X ∪ Y ∪ Z
   
   This guard is unretractable.
   

   .. py:staticmethod:: coerce(_, _)

      *no docstring*

   .. py:staticmethod:: extractGuards(_, _)

      *no docstring*

   .. py:staticmethod:: getMethods()

      *no docstring*

   .. py:staticmethod:: supersetOf(_)

      *no docstring*



.. py:class:: Void

   
   The singleton set of null: `[null].asSet()`
   
   This guard is unretractable.
   

   .. py:staticmethod:: coerce(_, _)

      *no docstring*

   .. py:staticmethod:: getDocstring()

      *no docstring*

   .. py:staticmethod:: getMethods()

      *no docstring*

   .. py:staticmethod:: supersetOf(_)

      *no docstring*



.. py:data:: Empty

   An unretractable predicate guard.
   
   This guard admits any object which passes its predicate.

   .. py:method:: _printOn(_)

      *no docstring*

   .. py:method:: coerce(_, _)

      *no docstring*


.. py:data:: NullOk

   A guard which admits `null`.
   
   When specialized, this object returns a guard which admits its subguard
   as well as `null`.

   .. py:method:: coerce(_, _)

      *no docstring*

   .. py:method:: extractGuard(_, _)

      *no docstring*

   .. py:method:: get(_)

      *no docstring*


.. py:data:: Same

   
   When specialized, this object yields a guard which only admits precisely
   the object used to specialize it.
   
   In simpler terms, `Same[x]` will match only those objects `o` for which `o
   == x`.
   

   .. py:method:: extractValue(_, _)

      *no docstring*

   .. py:method:: get(_)

      *no docstring*


.. py:data:: Vow

   A guard which admits promises and their entailments.
   
   Vows admit the union of unfulfilled promises, fulfilled promises, broken
   promises, and `Near` values. The unifying concept is that of a partial
   future value to which messages will be sent but that is not `Far`.
   
   When specialized, this guard returns a guard which ensures that promised
   prizes either conform to its subguard or are broken.

   .. py:method:: _printOn(_)

      *no docstring*

   .. py:method:: coerce(_, _)

      *no docstring*

   .. py:method:: extractGuard(_, _)

      *no docstring*

   .. py:method:: get(_)

      *no docstring*


.. py:data:: SubrangeGuard

   
   The maker of subrange guards.
   
   When specialized with a guard, this object produces a auditor for those
   guards which admit proper subsets of that guard.
   

   .. py:method:: get(_)

      *no docstring*


.. py:data:: _auditedBy

   
   Whether an auditor has audited a specimen.
   

   .. py:method:: run(_, _)

      *no docstring*



Primitive values
----------------

.. py:data:: true

   :Bool

.. py:data:: false

   :Bool

.. py:data:: null

   :Void

.. py:data:: NaN

   :Double

.. py:data:: Infinity

   :Double


Data Constructors
-----------------

.. py:data:: _makeInt

   
   A maker of `Int`s.
   
   This maker can handle radices from 2 to 36:
   
   ▲> _makeInt.withRadix(36)("zxcvasdfqwer1234")
   7942433573816828193485776
   

   .. py:method:: fromBytes(_, _)

      *no docstring*

   .. py:method:: run(_)

      *no docstring*

   .. py:method:: withRadix(_)

      *no docstring*


.. py:data:: _makeDouble

   
   The maker of `Double`s.
   

   .. py:method:: fromBytes(_, _)

      *no docstring*

   .. py:method:: run(_, _)

      *no docstring*


.. py:data:: _makeStr

   
   The maker of `Str`s.
   

   .. py:method:: fromChars(_)

      *no docstring*

   .. py:method:: fromStr(_, _)

      *no docstring*


.. py:data:: _makeString

   
   The maker of `Str`s.
   

   .. py:method:: fromChars(_)

      *no docstring*

   .. py:method:: fromStr(_, _)

      *no docstring*


.. py:data:: _makeBytes

   
   The maker of `Bytes`.
   

   .. py:method:: fromInts(_)

      *no docstring*

   .. py:method:: fromStr(_)

      *no docstring*


.. py:data:: _makeList

   
   The maker of `List`s.
   

   .. py:method:: fromIterable(_)

      *no docstring*


.. py:data:: _makeMap

   
   Given a `List[Pair]`, produce a `Map`.
   

   .. py:method:: fromPairs(_)

      *no docstring*


.. py:data:: _makeOrderedSpace

   The maker of ordered vector spaces.
   
   This object implements several Monte operators, including those which
   provide ordered space syntax.

   .. py:method:: op__thru(_, _)

      *no docstring*

   .. py:method:: op__till(_, _)

      *no docstring*

   .. py:method:: spaceOfGuard(_)

      *no docstring*

   .. py:method:: spaceOfValue(_)

      *no docstring*


.. py:data:: _makeTopSet

   

   .. py:method:: run(_, _, _, _, _)

      *no docstring*


.. py:data:: _makeOrderedRegion

   Make regions for sets of objects with total ordering.

   .. py:method:: run(_, _, _)

      *no docstring*


.. py:data:: _makeSourceSpan

   *no docstring*

   .. py:method:: run(_, _, _, _, _, _)

      *no docstring*


.. py:data:: _makeFinalSlot

   
   A maker of final slots.
   

   .. py:method:: asType()

      *no docstring*

   .. py:method:: run(_, _, _)

      *no docstring*


.. py:data:: _makeVarSlot

   
   A maker of var slots.
   

   .. py:method:: asType()

      *no docstring*

   .. py:method:: run(_, _, _)

      *no docstring*


.. py:data:: makeLazySlot

   Make a slot that lazily binds its value.

   .. py:method:: run(_)

      *no docstring*



Tracing
-------

.. py:data:: trace

   
   Write a line to the trace log.
   
   This object is a Typhon standard runtime `traceln`. It prints prefixed
   lines to stderr.
   
   Call `.exception(problem)` to print a problem to stderr, including
   a formatted traceback.
   

   .. py:method:: exception(_)

      *no docstring*


.. py:data:: traceln

   
   Write a line to the trace log.
   
   This object is a Typhon standard runtime `traceln`. It prints prefixed
   lines to stderr.
   
   Call `.exception(problem)` to print a problem to stderr, including
   a formatted traceback.
   

   .. py:method:: exception(_)

      *no docstring*



Brands
------

.. py:data:: makeBrandPair

   Make a [sealer, unsealer] pair.

   .. py:method:: run(_)

      *no docstring*



Quasiparsers
------------

.. py:data:: ``

   A quasiparser of Unicode strings.
   
   This object is the default quasiparser. It can interpolate any object
   into a string by pretty-printing it; in fact, that is one of this
   object's primary uses.
   
   When used as a pattern, this object performs basic text matching.
   Patterns always succeed, grabbing zero or more characters non-greedily
   until the next segment. When patterns are concatenated in the
   quasiliteral, only the rightmost pattern can match any characters; the
   other patterns to the left will all match the empty string.

   .. py:method:: matchMaker(_)

      *no docstring*

   .. py:method:: patternHole(_)

      *no docstring*

   .. py:method:: valueHole(_)

      *no docstring*

   .. py:method:: valueMaker(_)

      *no docstring*


.. py:data:: b``

   A quasiparser for `Bytes`.
   
   This object behaves like `simple__quasiParser`; it takes some textual
   descriptions of bytes and returns a bytestring. It can interpolate
   objects which coerce to `Bytes` and `Str`.
   
   As a pattern, this object performs slicing of bytestrings. Semantics
   mirror `simple__quasiParser` with respect to concatenated patterns and
   greediness.

   .. py:method:: matchMaker(_)

      *no docstring*

   .. py:method:: patternHole(_)

      *no docstring*

   .. py:method:: valueHole(_)

      *no docstring*

   .. py:method:: valueMaker(_)

      *no docstring*


.. py:data:: m``

   A quasiparser for the Monte programming language.
   
   This object will parse any Monte expression and return an opaque
   value. In the near future, this object will instead return a translucent
   view into a Monte compiler and optimizer.

   .. py:method:: fromStr(_)

      *no docstring*

   .. py:method:: getAstBuilder()

      *no docstring*

   .. py:method:: matchMaker(_)

      *no docstring*

   .. py:method:: patternHole(_)

      *no docstring*

   .. py:method:: valueHole(_)

      *no docstring*

   .. py:method:: valueMaker(_)

      *no docstring*


.. py:data:: mpatt``

   A quasiparser for the Monte programming language's patterns.
   
   This object is like m``, but for patterns.

   .. py:method:: fromStr(_)

      *no docstring*

   .. py:method:: getAstBuilder()

      *no docstring*

   .. py:method:: matchMaker(_)

      *no docstring*

   .. py:method:: patternHole(_)

      *no docstring*

   .. py:method:: valueHole(_)

      *no docstring*

   .. py:method:: valueMaker(_)

      *no docstring*



Flow control
------------

.. py:data:: M

   
   Miscellaneous vat management and quoting services.
   

   .. py:method:: call(_, _, _, _)

      *no docstring*

   .. py:method:: callWithMessage(_, _)

      *no docstring*

   .. py:method:: send(_, _, _, _)

      *no docstring*

   .. py:method:: sendOnly(_, _, _, _)

      *no docstring*

   .. py:method:: toQuote(_)

      *no docstring*

   .. py:method:: toString(_)

      *no docstring*


.. py:data:: throw

   *no docstring*

   .. py:method:: eject(_, _)

      *no docstring*

   .. py:method:: run(_)

      *no docstring*


.. py:data:: _loop

   
   Perform an iterative loop.
   

   .. py:method:: run(_, _)

      *no docstring*


.. py:data:: _iterForever

   Implementation of while-expression syntax.

   .. py:method:: _makeIterator()

      *no docstring*

   .. py:method:: next(_)

      *no docstring*



Evaluation
----------

.. py:data:: eval

   Evaluate Monte source.
   
   This object respects POLA and grants no privileges whatsoever to
   evaluated code. To grant a safe scope, pass `safeScope`.

   .. py:method:: evalToPair(_, _)

      *no docstring*

   .. py:method:: run(_, _)

      *no docstring*


.. py:data:: astEval

   *no docstring*

   .. py:method:: evalToPair(_, _)

      *no docstring*

   .. py:method:: run(_, _)

      *no docstring*



Reference/object operations
---------------------------

.. py:data:: Ref

   
   Ref management and utilities.
   

   .. py:method:: broken(_)

      *no docstring*

   .. py:method:: fulfillment(_)

      *no docstring*

   .. py:method:: isBroken(_)

      *no docstring*

   .. py:method:: isDeepFrozen(_)

      *no docstring*

   .. py:method:: isEventual(_)

      *no docstring*

   .. py:method:: isFar(_)

      *no docstring*

   .. py:method:: isNear(_)

      *no docstring*

   .. py:method:: isResolved(_)

      *no docstring*

   .. py:method:: isSelfish(_)

      *no docstring*

   .. py:method:: isSelfless(_)

      *no docstring*

   .. py:method:: makeProxy(_, _, _)

      *no docstring*

   .. py:method:: optProblem(_)

      *no docstring*

   .. py:method:: promise()

      *no docstring*

   .. py:method:: state(_)

      *no docstring*

   .. py:method:: whenBroken(_, _)

      *no docstring*

   .. py:method:: whenBrokenOnly(_, _)

      *no docstring*

   .. py:method:: whenResolved(_, _)

      *no docstring*

   .. py:method:: whenResolvedOnly(_, _)

      *no docstring*


.. py:data:: promiseAllFulfilled

   

   .. py:method:: run(_)

      *no docstring*


.. py:data:: DeepFrozen

   
   Auditor and guard for transitive immutability.
   

   .. py:method:: audit(_)

      *no docstring*

   .. py:method:: coerce(_, _)

      *no docstring*

   .. py:method:: supersetOf(_)

      *no docstring*


.. py:data:: Selfless

   
   A stamp for incomparable objects.
   
   `Selfless` objects are generally not equal to any objects but themselves.
   They may choose to implement alternative comparison protocols such as
   `Transparent`.
   

   .. py:method:: audit(_)

      *no docstring*

   .. py:method:: coerce(_, _)

      *no docstring*

   .. py:method:: passes(_)

      *no docstring*


.. py:data:: Transparent

   Objects that Transparent admits have reliable ._uncall() methods, in the sense
   that they correctly identify their maker and their entire state, and that
   invoking the maker with the given args will produce an object with the same
   state. Objects that are both Selfless and Transparent are compared for sameness
   by comparing their uncalls.

   .. py:method:: coerce(_, _)

      *no docstring*

   .. py:method:: makeAuditorKit()

      *no docstring*


.. py:data:: Near

   
   A guard over references to near values.
   
   This guard admits any near value, as well as any resolved reference to any
   near value.
   
   This guard is unretractable.
   

   .. py:method:: coerce(_, _)

      *no docstring*


.. py:class:: Binding

   
   A guard which admits bindings.
   

   .. py:staticmethod:: coerce(_, _)

      *no docstring*

   .. py:staticmethod:: getDocstring()

      *no docstring*

   .. py:staticmethod:: getMethods()

      *no docstring*

   .. py:staticmethod:: supersetOf(_)

      *no docstring*




Abstract Syntax
---------------

.. py:data:: astBuilder

   

   .. py:method:: AndExpr(_, _, _)

      *no docstring*

   .. py:method:: AssignExpr(_, _, _)

      *no docstring*

   .. py:method:: AugAssignExpr(_, _, _, _)

      *no docstring*

   .. py:method:: BinaryExpr(_, _, _, _)

      *no docstring*

   .. py:method:: BindPattern(_, _, _)

      *no docstring*

   .. py:method:: BindingExpr(_, _)

      *no docstring*

   .. py:method:: BindingPattern(_, _)

      *no docstring*

   .. py:method:: CatchExpr(_, _, _, _)

      *no docstring*

   .. py:method:: Catcher(_, _, _)

      *no docstring*

   .. py:method:: CoerceExpr(_, _, _)

      *no docstring*

   .. py:method:: CompareExpr(_, _, _, _)

      *no docstring*

   .. py:method:: CurryExpr(_, _, _, _)

      *no docstring*

   .. py:method:: DefExpr(_, _, _, _)

      *no docstring*

   .. py:method:: EscapeExpr(_, _, _, _, _)

      *no docstring*

   .. py:method:: ExitExpr(_, _, _)

      *no docstring*

   .. py:method:: FinalPattern(_, _, _)

      *no docstring*

   .. py:method:: FinallyExpr(_, _, _)

      *no docstring*

   .. py:method:: ForExpr(_, _, _, _, _, _, _)

      *no docstring*

   .. py:method:: ForwardExpr(_, _)

      *no docstring*

   .. py:method:: FunCallExpr(_, _, _, _)

      *no docstring*

   .. py:method:: FunSendExpr(_, _, _, _)

      *no docstring*

   .. py:method:: FunctionExpr(_, _, _, _)

      *no docstring*

   .. py:method:: FunctionInterfaceExpr(_, _, _, _, _, _, _)

      *no docstring*

   .. py:method:: FunctionScript(_, _, _, _, _)

      *no docstring*

   .. py:method:: GetExpr(_, _, _)

      *no docstring*

   .. py:method:: HideExpr(_, _)

      *no docstring*

   .. py:method:: IfExpr(_, _, _, _)

      *no docstring*

   .. py:method:: IgnorePattern(_, _)

      *no docstring*

   .. py:method:: InterfaceExpr(_, _, _, _, _, _, _)

      *no docstring*

   .. py:method:: ListComprehensionExpr(_, _, _, _, _, _)

      *no docstring*

   .. py:method:: ListExpr(_, _)

      *no docstring*

   .. py:method:: ListPattern(_, _, _)

      *no docstring*

   .. py:method:: LiteralExpr(_, _)

      *no docstring*

   .. py:method:: MapComprehensionExpr(_, _, _, _, _, _, _)

      *no docstring*

   .. py:method:: MapExpr(_, _)

      *no docstring*

   .. py:method:: MapExprAssoc(_, _, _)

      *no docstring*

   .. py:method:: MapExprExport(_, _)

      *no docstring*

   .. py:method:: MapPattern(_, _, _)

      *no docstring*

   .. py:method:: MapPatternAssoc(_, _, _, _)

      *no docstring*

   .. py:method:: MapPatternImport(_, _, _)

      *no docstring*

   .. py:method:: MatchBindExpr(_, _, _)

      *no docstring*

   .. py:method:: Matcher(_, _, _)

      *no docstring*

   .. py:method:: MessageDesc(_, _, _, _, _)

      *no docstring*

   .. py:method:: MetaContextExpr(_)

      *no docstring*

   .. py:method:: MetaStateExpr(_)

      *no docstring*

   .. py:method:: Method(_, _, _, _, _, _, _)

      *no docstring*

   .. py:method:: MethodCallExpr(_, _, _, _, _)

      *no docstring*

   .. py:method:: MismatchExpr(_, _, _)

      *no docstring*

   .. py:method:: Module(_, _, _, _)

      *no docstring*

   .. py:method:: NamedArg(_, _, _)

      *no docstring*

   .. py:method:: NamedArgExport(_, _)

      *no docstring*

   .. py:method:: NamedParam(_, _, _, _)

      *no docstring*

   .. py:method:: NamedParamImport(_, _, _)

      *no docstring*

   .. py:method:: NounExpr(_, _)

      *no docstring*

   .. py:method:: ObjectExpr(_, _, _, _, _, _)

      *no docstring*

   .. py:method:: OrExpr(_, _, _)

      *no docstring*

   .. py:method:: ParamDesc(_, _, _)

      *no docstring*

   .. py:method:: PatternHoleExpr(_, _)

      *no docstring*

   .. py:method:: PatternHolePattern(_, _)

      *no docstring*

   .. py:method:: PrefixExpr(_, _, _)

      *no docstring*

   .. py:method:: QuasiExprHole(_, _)

      *no docstring*

   .. py:method:: QuasiParserExpr(_, _, _)

      *no docstring*

   .. py:method:: QuasiParserPattern(_, _, _)

      *no docstring*

   .. py:method:: QuasiPatternHole(_, _)

      *no docstring*

   .. py:method:: QuasiText(_, _)

      *no docstring*

   .. py:method:: RangeExpr(_, _, _, _)

      *no docstring*

   .. py:method:: SameExpr(_, _, _, _)

      *no docstring*

   .. py:method:: SamePattern(_, _, _)

      *no docstring*

   .. py:method:: Script(_, _, _, _)

      *no docstring*

   .. py:method:: SendExpr(_, _, _, _, _)

      *no docstring*

   .. py:method:: SeqExpr(_, _)

      *no docstring*

   .. py:method:: SlotExpr(_, _)

      *no docstring*

   .. py:method:: SlotPattern(_, _, _)

      *no docstring*

   .. py:method:: SuchThatPattern(_, _, _)

      *no docstring*

   .. py:method:: SwitchExpr(_, _, _)

      *no docstring*

   .. py:method:: TempNounExpr(_, _)

      *no docstring*

   .. py:method:: To(_, _, _, _, _, _, _)

      *no docstring*

   .. py:method:: TryExpr(_, _, _, _)

      *no docstring*

   .. py:method:: ValueHoleExpr(_, _)

      *no docstring*

   .. py:method:: ValueHolePattern(_, _)

      *no docstring*

   .. py:method:: VarPattern(_, _, _)

      *no docstring*

   .. py:method:: VerbAssignExpr(_, _, _, _)

      *no docstring*

   .. py:method:: ViaPattern(_, _, _)

      *no docstring*

   .. py:method:: WhenExpr(_, _, _, _, _)

      *no docstring*

   .. py:method:: WhileExpr(_, _, _, _)

      *no docstring*

   .. py:method:: getAstGuard()

      *no docstring*

   .. py:method:: getExprGuard()

      *no docstring*

   .. py:method:: getNamePatternGuard()

      *no docstring*

   .. py:method:: getNounGuard()

      *no docstring*

   .. py:method:: getPatternGuard()

      *no docstring*



Utilities for syntax expansions
-------------------------------

.. py:data:: _accumulateList

   Implementation of list comprehension syntax.

   .. py:method:: run(_, _)

      *no docstring*


.. py:data:: _accumulateMap

   Implementation of map comprehension syntax.

   .. py:method:: run(_, _)

      *no docstring*


.. py:data:: _bind

   Resolve a forward declaration.

   .. py:method:: run(_, _)

      *no docstring*


.. py:data:: _booleanFlow

   Implementation of implicit breakage semantics in conditionally-defined
   names.

   .. py:method:: broken()

      *no docstring*

   .. py:method:: failureList(_)

      *no docstring*


.. py:data:: _comparer

   A comparison helper.
   
   This object implements the various comparison operators.

   .. py:method:: asBigAs(_, _)

      *no docstring*

   .. py:method:: geq(_, _)

      *no docstring*

   .. py:method:: greaterThan(_, _)

      *no docstring*

   .. py:method:: leq(_, _)

      *no docstring*

   .. py:method:: lessThan(_, _)

      *no docstring*


.. py:data:: _equalizer

   
   A perceiver of identity.
   
   This object can discern whether any two objects are distinct from each
   other.
   

   .. py:method:: isSettled(_)

      *no docstring*

   .. py:method:: makeTraversalKey(_)

      *no docstring*

   .. py:method:: optSame(_, _)

      *no docstring*

   .. py:method:: sameEver(_, _)

      *no docstring*

   .. py:method:: sameYet(_, _)

      *no docstring*


.. py:data:: _makeVerbFacet

   The operator `obj`.`method`.

   .. py:method:: curryCall(_, _)

      *no docstring*

   .. py:method:: currySend(_, _)

      *no docstring*


.. py:data:: _mapEmpty

   An unretractable predicate guard.
   
   This guard admits any object which passes its predicate.

   .. py:method:: _printOn(_)

      *no docstring*

   .. py:method:: coerce(_, _)

      *no docstring*


.. py:data:: _mapExtract

   Implementation of key pattern-matching syntax in map patterns.

   .. py:method:: run(_)

      *no docstring*

   .. py:method:: withDefault(_, _)

      *no docstring*


.. py:data:: _matchSame

   

   .. py:method:: different(_)

      *no docstring*

   .. py:method:: run(_)

      *no docstring*


.. py:data:: _quasiMatcher

   Implementation of quasiliteral pattern syntax.

   .. py:method:: run(_, _)

      *no docstring*


.. py:data:: _slotToBinding

   
   Implementation of bind-pattern syntax for forward declarations.
   

   .. py:method:: run(_, _)

      *no docstring*


.. py:data:: _splitList

   
   Implementation of tail pattern-matching syntax in list patterns.
   
   m`def [x] + xs := l`.expand() == m`def via (_splitList.run(1)) [x, xs] := l`
   

   .. py:method:: run(_)

      *no docstring*


.. py:data:: _suchThat

   The pattern patt ? (expr).

   .. py:method:: run(_, _)

      *no docstring*


.. py:data:: _switchFailed

   The implicit default matcher in a switch expression.
   
   This object throws an exception.


.. py:data:: _validateFor

   Ensure that `flag` is `true`.
   
   This object is a safeguard against malicious loop objects. A flag is set
   to `true` and closed over by a loop body; once the loop is finished, the
   flag is set to `false` and the loop cannot be reëntered.

   .. py:method:: run(_)

      *no docstring*



Interface constructors
----------------------

.. py:data:: _makeMessageDesc

   Describe a message.

   .. py:method:: run(_, _, _, _)

      *no docstring*


.. py:data:: _makeParamDesc

   Describe a parameter.

   .. py:method:: run(_, _)

      *no docstring*


.. py:data:: _makeProtocolDesc

   Produce an interface.

   .. py:method:: makePair(_, _, _, _, _)

      *no docstring*

   .. py:method:: run(_, _, _, _, _)

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
   after at least `delay` seconds have elapsed in the runtime. The promise
   will resolve to a `Double` representing the precise amount of time
   elapsed, in seconds.
   * `sendTimestamp(callable)`: Send a `Double` representing the runtime's
   clock to `callable`.
   
   There is extremely unsafe functionality as well:
   * `unsafeNow()`: The current system time.
   
   Use with caution.
   

   .. py:method:: fromNow(_)

      *no docstring*

   .. py:method:: sendTimestamp(_)

      *no docstring*

   .. py:method:: unsafeNow()

      *no docstring*



I/O
---

.. py:data:: stdio

   
   A producer of streamcaps for the ancient standard I/O bytestreams.
   

   .. py:method:: stderr()

      *no docstring*

   .. py:method:: stdin()

      *no docstring*

   .. py:method:: stdout()

      *no docstring*


.. py:data:: makeStdErr

   *no docstring*

   .. py:method:: run()

      *no docstring*


.. py:data:: makeStdIn

   *no docstring*

   .. py:method:: run()

      *no docstring*


.. py:data:: makeStdOut

   *no docstring*

   .. py:method:: run()

      *no docstring*


.. py:data:: makeFileResource

   
   Make a file Resource.
   

   .. py:method:: run(_)

      *no docstring*



Networking
----------

.. py:data:: makeTCP4ClientEndpoint

   
   Make a TCPv4 client endpoint.
   

   .. py:method:: run(_, _)

      *no docstring*


.. py:data:: makeTCP4ServerEndpoint

   
   Make a TCPv4 server endpoint.
   

   .. py:method:: run(_)

      *no docstring*


.. py:data:: makeTCP6ClientEndpoint

   
   Make a TCPv6 client endpoint.
   

   .. py:method:: run(_, _)

      *no docstring*


.. py:data:: makeTCP6ServerEndpoint

   
   Make a TCPv4 server endpoint.
   

   .. py:method:: run(_)

      *no docstring*


.. py:data:: getAddrInfo

   *no docstring*

   .. py:method:: run(_, _)

      *no docstring*



Runtime
-------

.. py:data:: currentRuntime

   
   The Typhon runtime.
   
   This object is a platform-specific view into the configuration and
   performance of the current runtime in the current process.
   
   This object is necessarily unsafe and nondeterministic.
   

   .. py:method:: getCrypt()

      *no docstring*

   .. py:method:: getHeapStatistics()

      *no docstring*

   .. py:method:: getReactorStatistics()

      *no docstring*


.. py:data:: unsealException

   
   Unseal a specimen.
   

   .. py:method:: run(_, _)

      *no docstring*



Processes and Vats
------------------

.. py:data:: currentProcess

   
   The current process on the local node.
   

   .. py:method:: getArguments()

      *no docstring*

   .. py:method:: getEnvironment()

      *no docstring*

   .. py:method:: getPID()

      *no docstring*

   .. py:method:: interrupt()

      *no docstring*


.. py:data:: makeProcess

   
   Create a subordinate process on the current node from the given
   executable, arguments, and environment.
   
   `=> stdin`, `=> stdout`, and `=> stderr` control the same-named methods on
   the resulting process object, which will return a sink, source, and source
   respectively. If any of these named arguments are `true`, then the
   corresponding method on the process will return a live streamcap which
   is connected to the process; otherwise, the returned streamcap will be a
   no-op.
   
   `=> stdinFount`, if not null, will be treated as a fount and it will be
   flowed to a drain representing stdin. `=> stdoutDrain` and
   `=> stderrDrain` are similar but should be drains which will have founts
   flowed to them.
   

   .. py:method:: run(_, _, _)

      *no docstring*


