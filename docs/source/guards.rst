======
Guards
======

.. note::
    This section could be a lot better.

A guard is a syntactic element which ensures that an object has a certain
property. Guards are used to informally prove that sections of code behave
correctly. A guard examines a value and returns a (possibly different) value
which satisfies its property, or ejects or otherwise aborts the computation.

We call this process of a guard **coercion**.

Builtin Guards
==============

Monte comes equipped with several very useful guards.

Void
----

The void guard, ``Void``, is one of the simplest guards. It coerces all values
to ``null`` successfully. ``Void`` is used as the default return value guard;
if a function or method exits without an explicit return value, then ``Void``
destroys the implicit return value.

.. note::
    The above paragraph lies; currently Monte uses ``Any`` as the default
    return value guard and uses syntactic expansion to force the implicit
    return value to ``null``.

Type-checking
-------------

Several builtin guards are used for asserting that a value is of a given type:

* ``Bool`` for Booleans
* ``Char`` for characters
* ``Double`` for floating-point numbers
* ``Int`` for integers
* ``List`` for lists
* ``Map`` for maps
* ``Set`` for sets

These guards have useful features for more precisely asserting that the
guarded values are within certain ranges. The ``Char``, ``Double``, and
``Int`` guards support subranges of values via comparison expressions::

    def x :('a'..'z' | 'A'..'Z') := 'c'
    def y :(Double >= 4.2) := 7.0
    def z :(Int < 5) := 3

Additionally, the ``List`` and ``Set`` guards can be specialized on
*subguards*, which are just regular guards that check each value in the set or
list::

    def ints :List[Int] := [1, 2, 4, 6, 8]
    def setOfUppercaseChars :Set['A'..'Z'] := ['A', 'C', 'E', 'D', 'E', 'C', 'A', 'D', 'E'].asSet()

Other Builtin Guards
--------------------

Some other builtin guards are worth mentioning:

* ``Any`` is a guard that accepts anything.
* ``NullOk`` accepts ``null``. Specializing it creates a guard that accepts
  ``null`` or whatever the subguard accepts.
