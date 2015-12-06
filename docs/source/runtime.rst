.. _stdlib:

Monte Standard Runtime Library
==============================

.. todo:: doctests with no expected results are not implemented at the
          time of this writing.

Primitive values
----------------

  >>> [true, false, null, NaN, Infinity]
  [true, false, null, nan, inf]


Flow control
------------

`M` provides `call` and `send` methods to invoke methods by name::

  >>> M.call(1, "add", [2])
  3
  >>> M.send(1, "add", [2])
  <Promise>


`throw` is callable as `throw(reason)` to throw an exception or
`throw.eject(optEjector, value)` to either invoke an ejector or throw
an exception if `optEjector` is null::

  >>> throw
  throw
  >>> throw.eject
  <curried>

`__loop` is an iteration primitive. Used in syntax expansion of 'for';
exhausts an iterator, invoking a callable for each item in it.

  >>> def l := [].diverge()
  [].diverge()
  >>> _loop([1,2,3], fn k, v { l.push(v) })
  null
  >>> l
  [1, 2, 3].diverge()


Reference/object operations
---------------------------

 - `Ref` Provides methods for creating and examining references, and
   adding callbacks to them.


DeepFrozen Guard
~~~~~~~~~~~~~~~~

for (i.e., transitively immutable) objects::

   >>> DeepFrozen
   DeepFrozen


Selfless Guard
~~~~~~~~~~~~~~

for selfless (i.e. comparable by value not identity) objects::

  >>> Selfless
  <Selfless>

Transparent Guard
~~~~~~~~~~~~~~~~~

for transparent (i.e. no hidden state) objects.

  >>> Transparent
  <Transparent>

Data Guard
~~~~~~~~~~

for data (i.e. completely serializable) objects.

  >>> Data


PassByCopy Guard
~~~~~~~~~~~~~~~~

for objects that can be copied when passed to another vat, rather than
having to be represented as a far ref.

  >>> PassByCopy


Tracing
-------

To emit a string to the trace log::

  >>> trace("str")
  null

To emit a string followed by a newline to the trace log::

  >>> traceln("str")
  null


Data constructors
-----------------

  >>> __makeList(1, 2, 3)
  [1, 2, 3]
  >>> __makeMap.fromPairs([['k', 'v']])
  ['k' => 'v']

  >>> __makeInt("1")
  1

  >>> __makeInt("100_000")

  >>> [_makeFinalSlot, _makeVarSlot]
  [<FinalSlotMaker>, <VarSlotMaker>]

  >>> _makeOrderedSpace
  <OrderedSpaceMaker>


Basic guards
------------

  >>> [Any, Void]
  [Any, Void]

  >>> [Bool, Str, Char, Double, Int]
  [Bool, Str, Char, Double, Int]

  >>> [List, Map, Set]
  [List, Map, Set]

  >>> Tuple
  >>> __Portrayal
  >>> [Near, Rcvr]
  >>> Audition

Guard utilities
---------------

  >>> [All, Not]
  >>> NotNull

  >>> "abc" :NullOk[Str]
  abc

Guard meta
----------

  >>> [ValueGuard, Guard, __makeGuard]

Interface constructors
----------------------

  >>> [__makeMessageDesc, __makeParamDesc, __makeProtocolDesc]
  [<_makeMessageDesc>, <_makeParamDesc>, <_makeProtocolDesc>]

Quasiparsers
------------

  >>> [simple__quasiParser, m__quasiParser]
  [<simple__quasiParser>, <m__quasiParser>]

  >>> simple`sum: ${1+1}`
  sum: 2

  >>> m`1 + 1`.expand()
  m`1.add(1)`

Utilities for syntax expansions
-------------------------------

  >>> [_accumulateList, _accumulateMap]
  [<_accumulateList>, <_accumulateMap>]

  >>>  _bind
  <_bind>

  >>> [_booleanFlow, _comparer, _equalizer]
  [<_booleanFlow>, <_comparer>, <Equalizer>]

  >>> __iterWhile
  >>> __makeVerbFact
  >>> [_mapEmpty, _mapExtract]
  [Empty, <_mapExtract>]

  >>> [_matchSame, _quasiMatcher]
  [<_matchSame>, <_quasiMatcher>]

  >>> __slotToBinding
  <SlotBinder>

  >>> [_splitList, _suchThat]
  [<_splitList>, <_suchThat>]

  >>> _switchFailed
  <_switchFailed>

  >>> __promiseAllFulfilled

  >>> _validateFor
  Result: <_validateFor>
