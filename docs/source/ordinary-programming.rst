Practical Security: The Mafia game
==================================

Let's look a bit deeper at Monte, working up to an implementation of
the `Mafia party game`__.

__ https://en.wikipedia.org/wiki/Mafia_%28party_game%29

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

Object constructors and encapsulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

.. sidebar:: Assignment Expressions

   Remember, Monte is an expression language.  The expression ``value
   += 1`` returns the resulting sum. That's why ``return value += 1``
   works.

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

A critical feature of Monte is **complete encapsulation**: ``value``
is not visible outside of ``makeCounter()``; this means that *no other
object can directly modify it*. Monte objects have no public
attributes or fields or even a notion of public and private. Instead,
all names are private: if a name is not visible (i.e. in scope), there
is no way to use it.

.. sidebar:: Augmented Assignment

   Just as you would read ``x += 1`` short-hand for ``x := x + 1``,
   read the :ref:`augmented assignment <augmented_assignment>`
   ``players without= (victim)`` as ``players :=
   players.without(victim)`` .


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

.. _def-fun:

Functions are objects too
~~~~~~~~~~~~~~~~~~~~~~~~~

Functions are simply objects with a ``run`` method. There is no
difference between this function::

  >>> def square(x):
  ...     return x * x
  ... square.run(4)
  16

... and this object::

  >>> object square:
  ...     to run(x):
  ...         return x * x
  ... square(4)
  16

.. todo:: document docstrings


Traditional Datatypes and Operators
-----------------------------------

The :ref:`basic data types <primitive-data>` in Monte are ``Int``,
``Double``, ``Str``, ``Char``, and ``Boolean``. All integer arithmetic
is unlimited precision, as if all integers were python longs.

The operators ``+``, ``-``, and ``*`` have their traditional meanings
for ``Int`` and ``Double``. The normal division operator ``/`` always
gives you a ``Double`` result. The floor divide operator ``//`` always
gives you an ``Int``, truncated towards negative infinity. So::

  >>> -3.5 // 1
  -4

.. sidebar:: Comments

   Monte uses the same ``# ...`` syntax for comments as python and
   shell programming.

Strings are enclosed in double quotes. Characters are enclosed in
single quotes.

The function ``traceln`` sends diagnostic output to the console. The
``if`` statement looks much like its Python equivalent, as do lists
such as ``[4, 14]``.

Operator precedence is generally the same as in Java, Python, or C. In
a few cases, Monte will throw a syntax error and require the use of
parentheses.

With that, let's set aside our game sketch and look at a more complete
rendition:

.. literalinclude:: tut/mafia.mt
    :linenos:
    :lines: 15-
    :lineno-start: 15

Dynamic "type checking" with Guards
-----------------------------------

Monte :ref:`guard <guards>` perform many of the functions usually
thought of as type checking, though they are so flexible that they
also work as concise assertions. Guards can be placed on variables
(such as ``mafiososCount :Int``), parameters (such as ``players
:Set``), and return values (such as ``getState() :MafiaState``).

Guards are not checked during compilation. They are checked during
execution and will throw exceptions if the value cannot be coerced to
pass the guard.

We can also build Guards at runtime. The call to ``makeEnum`` returns
a list where the first item is a new guard and the remaining items are
distinct new objects that pass the guard. No other objects pass the
guard.

.. todo:: **show**: Guards play a key role in protecting security
          properties.

Final, Var, and DeepFrozen
--------------------------

Bindings in Monte are final (immutable) by default.

Wherever a name appears in a pattern, it can also have a guard; in
particular, the :ref:`DeepFrozen guard <deepfrozen>` means that the
object and everything it refers to are immutable.  The ``def
makeMafia(...) as DeepFrozen`` expression results in this sort of
binding as well as patterns such as ``DAY :DeepFrozen``.

Using a ``var`` pattern in a definition (such as ``mafiosos``) or
parameter (such as ``players``) lets you assign to that variable again
later.


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


Data Structures for Game Play
-----------------------------

Monte has ``Set``, ``List``, and ``Map`` data structures that let us
express the rules of the game concisely.

A game of mafia has some finite number of players. They don't come in
any particular order, though, so we write ``var players :Set`` to
ensure that ``players`` is always bound to a ``Set``,
though it may be assigned to different sets at different times.

We use ``.size()`` to get the number of players and ``.slice()`` to
get the subsets ``mafiosos`` and ``innocents``.

We initialize ``votes`` to the empty ``Map``, written ``[].asMap()``
and add to it using ``votes with= (player, choice)``.

To ``lynch``, we use ``counter`` as a map from player to votes cast
against that player. We initialize it to an empty mutable map with
``[].asMap().diverge()`` and then iterate over the votes with ``for _
=> v in votes:``.

A list of players that got more than a quorum of votes is written
``[for k => v in (counter) if (v >= quorum) k]``. Provided there
is one such player, we remove the player from the
game with ``players without= (victim)``.


Destructuring with Patterns
---------------------------

:ref:`Patterns <patterns>` are used in several ways in Monte:

  1. The left-hand side of a ``def`` expression has a pattern. A
     single name is typical, but the first ``def`` expression above
     binds ``MafiaState``, ``DAY``, and ``NIGHT`` to the items from
     ``makeEnum`` using a :ref:`list pattern<ListPatt>`. An exception
     is raised (or an ejector is fired) if the match fails.
  2. Parameters to methods are patterns which are matched against
     arguments. Match failure raises an exception. A :ref:`final
     pattern<FinalPatt>` such as ``to _printOn(out)`` or with a guard
     ``to lynch(quorum :Int)`` should look familiar, but the
     :ref:`such-that patterns <SuchThatPattern>` in ``to vote(player ?
     (players.contains(player)), ...)`` are somewhat novel. The pattern
     matches only if the expression after the ``?`` is true.
  3. Each matcher in a ``switch`` expression has a pattern. In the
     ``advance`` method, if ``state`` matches the ``==DAY``
     pattern--that is, if ``state == DAY``--then ``NIGHT`` is assigned
     to ``state``. Likewise for the pattern ``==NIGHT`` and the
     expression ``DAY``. An exception would be raised if neither
     pattern matched, but that can't happen because we have ``state
     :MafiaState``.
  4. Match-bind :ref:`comparisons <comparisons>` such as
     :literal:`"<p>" =~ \`<@tag>\`` test the value on the left against
     the pattern on the right.
  5. Matchers in objects expressions provide flexible handlers for
     :ref:`message passing <message_passing>`.

The ``[=> makeEnum]`` pattern syntax is short for ``["makeEnum" =>
makeEnum]``, which picks out the value corresponding to the key
``"makeEnum"``. The :ref:`module_expansion` section explains how
imports turn out to be a special case of method parameters.
     

String Interpolation with quasi-literals
----------------------------------------

Monte's :ref:`quasi-literals<quasiliteral>` enable the easy processing
of complex strings as described in detail later;
``out.print(`currently $state>`)`` is a simple example wherein the
back-ticks denote a quasi-literal, and the dollar sign denotes a
variable whose value is to be embedded in the string.
