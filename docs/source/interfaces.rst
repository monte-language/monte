Objects and Functions (TODO)
"""""""""""""""""""""


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


.. include:: guards.rst


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



Interfaces
----------

An :dfn:`interface` is a syntactic expression which defines an object
protocol. An interface has zero or more method signatures, and can be
implemented by any object which has methods with equivalent signatures to the
interface.

Let's jump right in::

    interface Trivial:
        "A trivial interface."

This interface comes with a docstring, which is not required but certainly a
good idea, and nothing else. Any object could implement this interface::

    object trivia implements Trivial:
        "A trivial object implementing a trivial interface."

When an object **implements** an interface, the interface behaves like any
other auditor and examines the object for compliance with the object protocol.
As with other auditors, the difference between the "implements" and "as"
keywords is whether the object is required to pass the auditor::

    object levity as Trivial:
        "A trivial object which is proven to implement Trivial."

Let's look at a new interface. This interface carries some **method
signatures**.

::

    interface GetPut:
        "Getting and putting."
        to get()
        to put(value)

    object getAndPut as GetPut:
        "A poor getter and putter."

        to get():
            return "get"

        to put(_):
            null

We can see that ``getAndPut`` implements the ``GetPut`` interface, but it
isn't very faithful to that interface. Interfaces cannot enforce behavior,
only signatures.


.. syntax:: interface

   Sequence(
    "interface",
    NonTerminal('namePattern'),
    Optional(Sequence("guards", NonTerminal('pattern'))),
    Optional(Sequence("extends", OneOrMore(NonTerminal('order'), ','))),
    Comment("implements_@@"), Comment("msgs@@"))

.. _under-cover-objects:

Under the covers: Everything is an object
-----------------------------------------

.. todo:: Under the covers: Everything is an object


Getting Help about an Object
----------------------------

Monte strives to provide useful error messages and self-documenting objects::

  ▲> help(Ref)
  Result: Object type: RefOps
  Ref management and utilities.
  Method: broken/1
  Method: isBroken/1
  Method: isDeepFrozen/1
  ...

.. rubric:: Notes

.. [#] in Java, compare to inner classes
