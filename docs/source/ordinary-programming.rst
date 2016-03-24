Practical Security: The Mafia game
==================================

Let's look a bit deeper at Monte, working up to an implementation of
the `Mafia party game`__.


Objects
-------

Monte has a simpler approach to object composition and inheritance than many
other object-based and object-oriented languages.

A Singleton Object
~~~~~~~~~~~~~~~~~~

We will start our exploration of objects with a simple singleton
object. Methods can be attached to objects with the ``to`` keyword::

  >>> object origin:
  ...     to getX():
  ...         return 0
  ...     to getY():
  ...         return 0
  ... # Now invoke the methods
  ... origin.getY()
  0

.. warning:: Python programmers beware, methods are not
             functions. Methods are just the public hooks to the
             object that receive messages; functions are standalone
             objects.

Unlike Java, Monte objects are not constructed from classes. Unlike JavaScript
or Python, Monte objects are not constructed from prototypes. As a result, it
might not be obvious at first how to build multiple objects which are similar
in behavior.


.. _maker:

Stateful objects and object constructors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Monte has a very simple idiom for class-like constructs::

  >>> def makeCounter(var value :Int):
  ...     return object counter:
  ...         to increment() :Int:
  ...             return value += 1
  ...         to makeOffsetCounter(delta :Int):
  ...             return makeCounter(value + delta)
  ...
  ... def c1 := makeCounter(1)
  ... c1.increment()
  ... def c2 := c1.makeOffsetCounter(10)
  ... c1.increment()
  ... c2.increment()
  ... [c1.increment(), c2.increment()]
  [4, 14]

And that's it. No declarations of object contents or special
references to ``this`` or ``self``.

Inside the function ``makeCounter``, we simply define an object called
``counter`` and return it. Each time we call ``makeCounter()``, we get
a new counter object. As demonstrated by the ``makeOffsetCounter``
method, the function (``makeCounter``) can be referenced from within
its own body.

The lack of a ``this`` or ``self`` keyword may be
surprising. But this straightforward use of lexical scoping saves us
the often tedious business in python or Java of copying the arguments
from the parameter list into instance variables: ``value`` is already
an instance variable.

The ``value`` passed into the function is not an ephemeral parameter
that goes out of existence when the function exits. Rather, it is a
true variable, and it persists as long as any of the objects that uses
it persist. Since the counter uses this variable, ``value`` will exist
as long as the counter exists.

.. note::
    Remember, Monte is an expression language. ``value += 1`` returns the
    resulting sum. That's why ``return value += 1`` works.

A critical feature of Monte is **complete encapsulation**: ``value``
is not visible outside of ``makeCounter()``; this means that *no other
object can directly modify it*. Monte objects have no public
attributes or fields or even a notion of public and private. Instead,
all names are private: if a name is not visible (i.e. in scope), there
is no way to use it.

We refer to an object-making function such as ``makeCounter`` as a
"Maker". As a more serous example, let's make a sketch of our game::

  >>> def makeMafia(var players :Set):
  ...     def mafiosoCount :Int := players.size() // 3
  ...     var mafiosos :Set := players.slice(0, mafiosoCount)
  ...     var innocents :Set := players.slice(mafiosoCount)
  ...
  ...     return object mafia:
  ...         to getWinner():
  ...             if (mafiosos.size() == 0):
  ...                 return "village"
  ...             if (mafiosos.size() >= innocents.size()):
  ...                 return "mafia"
  ...             return null
  ...
  ...         to lynch(victim):
  ...             players without= (victim)
  ...             mafiosos without= (victim)
  ...             innocents without= (victim)
  ...
  ... def game1 := makeMafia(["Alice", "Bob", "Charlie"].asSet())
  ... game1.lynch("Bob")
  ... game1.lynch("Charlie")
  ... game1.getWinner()
  "mafia"

.. note:: Just as you would read ``x += 1`` short-hand for ``x := x +
          1``, read the :ref:`augmented assignment
          <augmented_assignment>` ``players without= (victim)`` as
          ``players := players.without(victim)`` .


.. _def-fun:

Secret Life of Functions, Multiple Constructors and "Static Methods"
--------------------------------------------------------------------

Monte does have a convention that objects with a single method with the verb
``run`` are functions. There is no difference, to Monte, between this
function::

    def f():
        pass

And this object::

    object f:
        to run():
            pass

Functions
---------

A basic function looks like this::

  >>> def addNumbers(a, b):
  ...     return a + b
  ...
  ... # Now use the function::
  ... def answer := addNumbers(3, 4)
  ... answer
  7

You can nest the definitions of functions and objects inside other
functions and objects [#]_. Nested functions and objects play a crucial
role in Monte, notably in the construction of objects as described
shortly.

Functions can of course call themselves recursively, as in::

  >>> def factorial(n):
  ...     if (n == 0):
  ...         return 1
  ...     else:
  ...         return n * factorial(n-1)
  ... factorial(3)
  6


.. todo:: document docstrings

@@@@@@@@@

In :file:`mafia.mt`, after the comment, we start with a :ref:`module
declaration <module-decl>` that declares a dependency on the
`lib/enum` module, imports ``makeEnum``, and exports ``makeMafia``:

__ https://en.wikipedia.org/wiki/Mafia_%28party_game%29

.. literalinclude:: tut/mafia.mt
    :linenos:
    :language: monte
    :lines: 15-28
    :lineno-start: 15

Dynamic "type checking" with Guards
-----------------------------------

Monte :ref:`guard <guards>` perform many of the functions usually
thought of as type checking, though they are so flexible that they
also work as concise assertions. Guards can be placed on variables
(such as ``Int`` on ``mafiososCount``), parameters (such as ``Set`` on
``players``), and return values (such as ``MafiaState`` on
``getState`` below).

Guards are not checked during compilation. They are checked during
execution and will throw exceptions if the value cannot be coerced to
pass the guard. Guards play a key role in protecting security
properties.

This `lib/enum` module lets us build enumerations.  The call to
``makeEnum`` returns a list where the first item is a new guard and
the remaining items are distinct new objects that pass the guard. No
other objects pass the guard.

Destructuring with Patterns
---------------------------

The first ``def`` expression binds ``MafiaState``, ``DAY``, and
``NIGHT`` to the guard and the items using a :ref:`list
pattern<ListPatt>`.

Final, Var, and DeepFrozen
--------------------------

Bindings in Monte are final (immutable) by default.

Wherever a name appears in a pattern, it can also have a guard; in
particular, the :ref:`DeepFrozen guard <deepfrozen>` means that not
only is the variable binding immutable, but the object that is stored
there and everything it refers to are immutable.  The ``def
makeMafia(...) as DeepFrozen`` expression results in this sort of
binding as well as patterns such as ``DAY :DeepFrozen``.

Using a ``var`` pattern in a definition (such as ``mafiosos``) or
parameter (such as ``players``) lets you assign to that variable again
later.


Traditional Types and Operators
-------------------------------

The :ref:`basic types <primitive-data>` in Monte are ``Int``,
``Double``, ``Str``, ``Char``, and ``Boolean``. All integer arithmetic
is unlimited precision, as if all integers were longs.

The operators ``+``, ``-``, and ``*`` have their traditional meanings
for ``Int`` and ``Double``. The normal division operator ``/`` always
gives you a ``Double`` result. The floor divide operator ``//`` always
gives you an ``Int``, truncated towards negative infinity. So::

  >>> -3.5 // 1
  -4

Strings are enclosed in double quotes. Characters are enclosed in
single quotes.

The function ``traceln`` sends diagnostic output to the console. The
``if`` statement looks much like its Python equivalent, as do lists.

Operator precedence is generally the same as in Java, Python, or C. In
a few cases, Monte will throw a syntax error and require the use of
parentheses.

With that, let's look at the rest of ``makeMafia``:

.. literalinclude:: tut/mafia.mt
    :linenos:
    :lines: 23-
    :lineno-start: 23


Maps: building, iterating, and matching
---------------------------------------

Maps in monte are written ``["key1" => 1, "key2" => 2]``.  The
``[].asMap()`` expression builds an empty map from an empty list.
These are constant (immutable) maps. Use ``diverge()`` to get
a FlexList, as in ``def counter := [].asMap().diverge()``.

The ``for _ => v in votes:`` loop iterates over the values of the
``votes`` map. The ``[for k => v in (counter) if (v >= quorum) k]``
expression iterates over ``k => v`` pairs in the ``counter`` map and
returns a list of each ``k`` where ``v >= quorum``.

The ``[=> makeEnum]`` pattern syntax is short for ``["makeEnum" =>
makeEnum]``, which picks out the value corresponding to the key
``"makeEnum"``.


Assignment and Equality
-----------------------

Assignment uses the ``:=`` operator. The single equal sign ``=`` is
never legal in Monte; use ``:=`` for assignment and ``==`` for testing
equality.

``==`` and ``!=`` are the boolean tests for equality and inequality
respectively. When the equality test is used between appropriately
designated :ref:`transparent immutables<selfless>`, such as
integers, the values are compared to see if the values are equal; for
other objects the references are compared to see if both the left and
right sides of the operator refer to the same object. Chars, booleans,
integers, and floating point numbers are all compared by value, as are
Strings, ConstLists, and ConstMaps.

String Interpolation with quasi-literals
----------------------------------------

Monte's :ref:`quasi-literals<quasiliteral>` enable the easy processing
of complex strings as described in detail later;
``out.print(`currently $state>`)`` is a simple example wherein the
back-ticks denote a quasi-literal, and the dollar sign denotes a
variable whose value is to be embedded in the string.

.. todo:: integrate functions and objects with mafia.mt

.. todo:: discuss the actual game design and security properties.
