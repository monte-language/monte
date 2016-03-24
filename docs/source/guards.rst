.. _guards:

======
Guards
======

Standard Guards
~~~~~~~~~~~~~~~

Monte comes equipped with several very useful guards.

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
guarded values are within certain ranges. The ``Char``, ``Double``, ``Int``,
and ``Str`` guards support subranges of values via comparison expressions::

    def x :('a'..'z' | 'A'..'Z') := 'c'
    def y :(Double >= 4.2) := 7.0
    def z :(Int < 5) := 3

.. todo::
    ``Double`` and ``Str`` are currently broken for this kind of usage.

Additionally, the ``List`` and ``Set`` guards can be specialized on
:dfn:subguards, which are just regular guards that check each value in the set or
list::

    def ints :List[Int] := [1, 2, 4, 6, 8]
    def setOfUppercaseChars :Set['A'..'Z'] := ['A', 'C', 'E', 'D', 'E', 'C', 'A', 'D', 'E'].asSet()

Other Builtin Guards
~~~~~~~~~~~~~~~~~~~~

Some other builtin guards are worth mentioning:

* ``Any`` is a guard that accepts anything.
* ``NullOk`` accepts ``null``. Specializing it creates a guard that accepts
  ``null`` or whatever the subguard accepts.
* ``Same`` must be specialized, returning a guard which only accepts values
  that are ``==`` to the value on which it was specialized.


Are guards expensive?
~~~~~~~~~~~~~~~~~~~~~

Monte does require every guard to be executed on every assignment. This means
that every ``def`` runs its guards once (during definition) and every ``var``
runs its guards every time an assignment occurs. Since guards are Monte
objects and can be user-defined, concerns about performance are well-founded
and reasonable.

Monte implementations are permitted to *elide* any guards which can be
statically proven to always pass their specimens. An ahead-of-time compiler
might use type inference to prove that all specimens at a definition site
might be of a certain type. A just-in-time compiler might recognize at runtime
that a guard's code is redundant with unboxing, and elide both the unboxing
and the guard.

.. note::
    These optimizations aren't hypothetical. Corbin and Allen have talked
    about gradual typing and type inference in Monte, and the Typhon virtual
    machine almost always can remove typical trivial guards like ``Int`` and
    ``Bool``.

Guard Syntax Summary
~~~~~~~~~~~~~~~~~~~~

.. syntax:: guard

   Choice(0,
     Ap('GetExpr',
        Ap('NounExpr', 'IDENTIFIER'),
        Brackets('[', SepBy(NonTerminal('expr'), ','), ']')),
     Ap('NounExpr', 'IDENTIFIER'),
     Brackets('(', NonTerminal('expr'), ')'))

@@ TODO: rename to maybeGuard

.. syntax:: guardOpt

   Maybe(Sigil(':', NonTerminal('guard')))


Guards (@move?)
~~~~~~~~~~~~~~~

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
