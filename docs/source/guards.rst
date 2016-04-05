.. _guards:

Guards and Data
===============

Guards are used constrain pattern bindings and method return values::

  >>> def x :Int := 1
  ... x
  1

  >>> def halves(s) :Pair[Str, Str]:
  ...     return s.split(",")
  ... halves("A,B")
  ["A", "B"]


  >>> def y := -5
  ... escape oops {
  ...     def x :(Int > 0) exit oops := y
  ... }
  "-5 is not in <(0, ∞) <IntGuard> region>"

.. syntax:: guardOpt

   Maybe(Sigil(':', NonTerminal('guard')))


.. syntax:: guard

   Choice(0,
     Ap('GetExpr',
        Ap('NounExpr', 'IDENTIFIER'),
        Brackets('[', SepBy(NonTerminal('expr'), ','), ']')),
     Ap('NounExpr', 'IDENTIFIER'),
     Brackets('(', NonTerminal('expr'), ')'))


Basic Data Guards
-----------------

Guards for basic data include the following; no object passes more
than one of these guards:

* ``Void`` for ``null``, the only value of its type
* ``Bool`` for the Boolean values ``true`` and ``false``
* ``Int`` for integers
* ``Double`` for IEEE 754 floating-point numbers
* ``Char`` for characters, each with its own Unicode code point
* ``Str`` for strings of characters
* ``Bytes`` for sequences of bytes

These guards have useful features for more precisely asserting that the
guarded values are within certain ranges. The ``Char``, ``Double``, ``Int``,
and ``Str`` guards support subranges of values via comparison expressions::

    >>> def x :('a'..'z' | 'A'..'Z') := 'c'
    ... def y :(Double >= 4.2) := 7.0
    ... def z :(Int < 5) := 3
    ... [x, y, z]
    ['c', 7.0, 3]

.. note:: See :ref:`literals` for syntax details for `IntExpr`, `DoubleExpr`,
          `CharExpr`, and `StrExpr`.

Data Structure Guards
---------------------

We also have guards for basic data structures:

* ``List`` for lists of objects
* ``Map`` for maps from keys to values
* ``Set`` for sets

These guards can be specialized on :dfn:`subguards` on their elements::

  >>> def ints :List[Int] := [1, 2, 4, 6, 8]
  ... def setOfUppercaseChars :Set['A'..'Z'] := ['A', 'C', 'E', 'D', 'E', 'C', 'A', 'D', 'E'].asSet()
  ... def scores :Map[Str, Int] := ["Alice" => 10, "Bob" => 5]
  ...
  ... [ints.contains(4), setOfUppercaseChars.contains('B'), scores.contains("Bob")]
  [true, false, true]

Other Builtin Guards
--------------------

Some other builtin guards are worth mentioning:

* ``Any`` is a guard that accepts anything.
* ``NullOk`` accepts ``null``. Specializing it creates a guard that accepts
  ``null`` or whatever the subguard accepts.
* ``Same`` must be specialized, returning a guard which only accepts values
  that are ``==`` to the value on which it was specialized.
* ``Near`` test that an object is in the same vat and hence available for
  synchronous calls
