Practical Security: The Mafia game
==================================

Let's look a bit deeper at Monte, using an implementation of the
`Mafia party game`__ as an example.

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

  >>> # Point constructor
  ... def makePoint(x,y):
  ...     object point:
  ...         to getX():
  ...             return x
  ...         to getY():
  ...             return y
  ...         to makeOffsetPoint(offsetX, offsetY):
  ...             return makePoint(x + offsetX, y + offsetY)
  ...
  ...         to makeOffsetPoint(offset):
  ...             return makePoint(x + offset, y + offset)
  ...     return point
  ...
  ... # Create a point
  ... def origin := makePoint(0,0)
  ... # get the y value of the origin
  ... origin.getY()
  0

Inside the function makePoint, we define a point and return it. As
demonstrated by the ``makeOffsetPoint method``, the function (``makePoint``)
can be referenced from within its own body. Also note that you can
overload method names (two versions of ``makeOffsetPoint``) as long as
they can be distinguished by the number of parameters they take.

The ``(x, y)`` passed into the function are not ephemeral parameters
that go out of existence when the function exits. Rather, they are
true variables (implicitly declared with ``def``), and they persist as
long as any of the objects that use them persist. Since the point uses
these variables, ``x`` and ``y`` will exist as long as the point
exists. This saves us the often tedious business in python or Java of
copying the arguments from the parameter list into instance variables:
``x`` and ``y`` already are instance variables.

We refer to an object-making function such as makePoint as a
"Maker". Let us look at a more serious example, with additional
instance variables:

  >>> def makeCar(var name):
  ...     var x := 0
  ...     var y := 0
  ...     return object car:
  ...         to moveTo(newX, newY):
  ...             x := newX
  ...             y := newY
  ...
  ...         to getX():
  ...             return x
  ...         to getY():
  ...             return y
  ...         to setName(newName):
  ...             name := newName
  ...         to getName():
  ...             return name
  ...
  ... # Now use the makeCar function to make a car, which we will move and print
  ... def sportsCar := makeCar("Ferrari")
  ... sportsCar.moveTo(10,20)
  ... `The car ${sportsCar.getName()} is at X location ${sportsCar.getX()}`
  "The car Ferrari is at X location 10"


Finally, just like with functions, methods can have guards on their parameters
and return value::

    object deck:
        to size(suits :Int, ranks :Int) :Int:
            return suits * ranks

Newcomers to Monte may be surprised to learn that Monte lacks a ``this`` or
``self`` keyword. In fact, Monte does have ways to refer to the current object,
but there's a deeper conceptual difference between Monte and other object-based
languages.

Monte does not have a ``this`` or ``self`` keyword because Monte objects can
refer to their "member" or "private" names without qualification. This is a
consequence of how Monte objects are built. Consider this object maker::

    def makeMyObject():
        return object myObject:
            pass

Let's modify it slightly. We want to give this object a "private" value secret
which cannot be accessed directly, and a method ``getSecret/0`` which will
return it. We put "private" in quotation marks to emphasize that Monte does not
have private names. Instead, all names are private in Monte; if one cannot see
a name, then one cannot access it.

::

    def makeMyObject(secret):
        return object myObject:
            to getSecret():
                return secret

And that's it. No declarations of object contents or special references to ``this``
or ``self``.

We can also simulate "member" names for objects. As before, we can achieve
this effect without ``this``.

::

    def makeMyObject():
        var counter :Int := 0
        return object myObject:
            to getCounter():
                return counter += 1

Here, ``counter`` is not visible outside of ``makeMyObject()``, which means
that no other object can directly modify it. Each time we call
``makeMyObject()``, we get a new object called ``myObject`` with a new counter.

.. note::
    Remember, Monte is an expression language. ``counter += 1`` returns the
    value of ``counter``. That's why ``return counter += 1`` works.


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
