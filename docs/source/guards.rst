.. _guards:

======
Guards
======

.. note::
    This section sucks less. It still has a harsh opening though. Maybe
    something could be said about typical guard usage, or some more source
    code examples could be written?

::

    def someName :SomeGuard exit ej := someExpr

A guard is a syntactic element which ensures that an object has a certain
property. Guards are used to (in)formally prove that sections of code behave
correctly. A guard examines a value and returns a (possibly different) value
which satisfies its property, or ejects or otherwise aborts the computation.

We call the process of a guard examining an object **coercion**. The object
being examined and coerced is called the **specimen**.

Builtin Guards
==============

Monte comes equipped with several very useful guards.

Type-checking
-------------

Several builtin guards are used for asserting that a value is of a given type:

* ``Void`` for ``null``, the only value of its type
* ``Bool`` for the Boolean values ``true`` and ``false``
* ``Char`` for Unicode code points
* ``Double`` for IEEE 754 floating-point numbers
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
* ``Same`` must be specialized, returning a guard which only accepts values
  that are ``==`` to the value on which it was specialized.

Glossary
--------

.. glossary::

    retractable
        A guard that is not :term:`unretractable`.

    unretractable
        An unretractable guard, informally, cannot be fooled by impostor
        objects that only pretend to be guarded, and it also will not change
        its mind about an object on two different coercions.

        Formally, an :dfn:`unretractable` guard Un is a guard such that for
        all Monte objects, if any given object is successfully coerced by Un,
        then it will always be successfully coerced by Un, regardless of the
        internal state of Un or the object.

Guard Syntax Summary
--------------------

@@ TODO: rename to maybeGuard

.. syntax:: guardOpt

   Maybe(Sigil(':',
    Choice(
        0,
        Ap('GetExpr',
           Ap('NounExpr', 'IDENTIFIER'),
           Brackets('[', SepBy(NonTerminal('expr'), ','), ']')),
	Ap('NounExpr', 'IDENTIFIER'),
        Brackets('(', NonTerminal('expr'), ')'))))

