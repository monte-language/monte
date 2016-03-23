.. _stdlib:

Runtime Objects
===============

.. todo:: doctests with no expected results are not implemented at the
          time of this writing.

Primitive values
----------------

  >>> [true, false, null, NaN, Infinity]
  [true, false, null, NaN, Infinity]


Flow control
------------

`M` provides `call` and `send` methods to invoke methods by name::

  >>> M.call(1, "add", [2])
  3

  .>> M.send(1, "add", [2])
  <Promise>


`throw` is callable as `throw(reason)` to throw an exception or
`throw.eject(optEjector, value)` to either invoke an ejector or throw
an exception if `optEjector` is null::

  >>> throw
  throw

  .>> throw.eject
  <curried>


`_loop` is an iteration primitive. Used in syntax expansion of 'for';
exhausts an iterator, invoking a callable for each item in it.

  >>> def l := [].diverge()
  ... _loop([1,2,3], fn k, v { l.push(v) })
  ... l.snapshot()
  [1, 2, 3]


Reference/object operations
---------------------------

 - `Ref` Provides methods for creating and examining references, and
   adding callbacks to them.

Data Guard
~~~~~~~~~~

for data (i.e. completely serializable) objects.

  .>> Data


PassByCopy Guard
~~~~~~~~~~~~~~~~

for objects that can be copied when passed to another vat, rather than
having to be represented as a far ref.

  .>> PassByCopy


.. _trace:

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

  >>> _makeList(1, 2, 3)
  [1, 2, 3]
  >>> _makeMap.fromPairs([['k', 'v']])
  ['k' => 'v']

  >>> _makeInt("1")
  1

  .>> __makeInt("100_000")  # BUG!

  >>> [_makeFinalSlot, _makeVarSlot]
  [_makeFinalSlot, _makeVarSlot]

  >>> _makeOrderedSpace
  _makeOrderedSpace


Basic guards
------------

  >>> [Any, Void]
  [Any, Void]

  >>> [Bool, Str, Char, Double, Int]
  [Bool, Str, Char, Double, Int]

  >>> [List, Map, Set]
  [List, Map, Set]

  .>> Tuple
  .>> __Portrayal
  .>> [Near, Rcvr]
  .>> Audition

Guard utilities
---------------

  .>> [All, Not]
  .>> NotNull

  >>> "abc" :NullOk[Str]
  "abc"

Guard meta
----------

  .>> [ValueGuard, Guard, __makeGuard]

Interface constructors
----------------------

  >>> [_makeMessageDesc, _makeParamDesc, _makeProtocolDesc]
  [_makeMessageDesc, _makeParamDesc, _makeProtocolDesc]

Quasiparsers
------------

  >>> [simple__quasiParser, m__quasiParser]
  [simple__quasiParser, m__quasiParser]

  >>> simple`sum: ${1+1}`
  "sum: 2"

  >>> m`1 + 1`.expand()
  m`1.add(1)`

Utilities for syntax expansions
-------------------------------

  >>> [_accumulateList, _accumulateMap]
  [_accumulateList, _accumulateMap]

  >>> _bind
  _bind

  >>> [_booleanFlow, _comparer, _equalizer]
  [_booleanFlow, _comparer, _equalizer]

  .>> __iterWhile
  .>> __makeVerbFact
  >>> [_mapEmpty, _mapExtract]
  [_mapEmpty, _mapExtract]

  >>> [_matchSame, _quasiMatcher]
  [_matchSame, _quasiMatcher]

  >>> _slotToBinding
  _slotToBinding

  >>> [_splitList, _suchThat]
  [_splitList, _suchThat]

  >>> _switchFailed
  _switchFailed

  .>> __promiseAllFulfilled

  >>> _validateFor
  _validateFor
