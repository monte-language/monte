==================
Answered Questions
==================

Community
~~~~~~~~~

What is the origin of Monte's name?
-----------------------------------

The Monte language has its roots in the E and Python languages. We took
"Monty" from "Monty Python", and put an "e" in there. Thus, "Monte".

Why is Monte called a "dynamic language"?
-----------------------------------------

Monte is dynamic in three ways.

Dynamic Typing
    Monte is **unityped**, in formal type theory. For the informal engineer,
    Monte is "untyped" or "dynamically typed"; the type of a value might not
    be known at runtime, and "types are open".
Dynamic Binding
    Monte's polymorphism is late-binding. It is possible to pass a message to
    an object that will never able to handle that message.
Dynamic Compiling
    Monte can compile and run Monte code at runtime, as part of its core
    language.

Object Capabilities
~~~~~~~~~~~~~~~~~~~

How do I know which capabilities I have?
----------------------------------------

Any object that you can access meets one of three criteria:

* You created it,
* You were born with it, or
* You received it as a result of passing messages to something that met either
  of the first two criteria.

An object has the capabilities of all objects that it can access with these
three rules.

.. note::
    This answer still isn't satisfying. Neither is this question, really.

Monte in Theory
~~~~~~~~~~~~~~~

How do I perform parallel computations?
---------------------------------------

Currently, we haven't specified it. Run multiple processes to get node-level
parallelism.

.. note::
    Monte doesn't really say anything about parallelism per se. We *should*
    though. If we're going to be agoric, we should say something about CPUs,
    even if it's just that people should spin up more vats and make more code
    use farrefs.

How do I perform concurrent operations?
---------------------------------------

Spawn more vats. All vats are concurrently turning.

Are all messages eligible for both methods of sending?
------------------------------------------------------

In short, yes. The details follow.

Nearly all Monte objects are unable to distinguish passed messages based on
how they were delivered. A few extremely special runtime objects can make the
distinction, but they are the only exception. User-defined objects cannot tell
whether they received a message via call or send.

References?
-----------

.. note::
    Messy.

There are three words about references:

near/far, settled/unsettled, resolved/unresolved

http://www.erights.org/elib/concurrency/refmech.html

A near reference is to an object in the same vat, whereas a far reference is
to an object elsewhere.

References are settled if they won't change to a different reference state.
They can be compared with == and used as hashtable keys.

Settled/unsettled is more or less the same as resolved/unresolved, although
edge cases in previous implementations have required the distinction.

A reference is either a promise or resolved. A resolved reference is either
near, far, or broken. Near references can have synchronous calls made on them.
Promises, far references, and broken references will raise an exception if
synchronous calls are made.

Does Monte have functions?
--------------------------

No. Since everything in Monte is an object, you're always calling methods
rather than functions.

Monte does have a convention that objects with a single method with the verb
``run`` are functions. There is no difference, to Monte, between this
function::

    def f():
        pass

And this object::

    object f:
        to run():
            pass

Does this mean we should never make synchronous calls?
------------------------------------------------------

.. note::
    Ugh. This could probably be its own page!

No. There are many kind of objects on which synchronous calls work, because
they are near references. For example, all literals are near: ``def lue :=
(6).mul(7)``.

When in doubt, remember that there is a ``near`` guard which can be used to
confirm that an object is in the same vat as you and thus available for
synchronous calls.

What are ejectors?
------------------

An ejector is an object that aborts the current computation and returns to
where it was created. They are created by ``escape`` expressions.

An ejector can be passed as deeply as one wants, but cannot be used outside of
the ``escape`` that created it. This is called the **delimited** property of
ejectors.

Ejectors cannot be used multiple times. The first time an ejector is used, the
``escape`` block aborts computation, resulting in the value of the ejector.
Subsequent clever uses of the ejector will fail. This is called the **single
use** property.

Monte implements the ``return``, ``break``, and ``continue`` expressions with
ejectors.

To be fully technical, ejectors are "single-use delimited continuations".

Monte in Practice
~~~~~~~~~~~~~~~~~

How do I force an object to be a certain type?
----------------------------------------------

Use a guard that coerces objects to be of that type. Guards for all of the
primitive types in Monte are already builtin; see the documentation on
:doc:`guards` for more details.

How do I pass a message to an object?
-------------------------------------

There are two ways to pass a message. First, the **immediate call**::

    def result := obj.message(argument)

And, second, the **eventual send**::

    def promisedResult := obj<-message(argument)

How do I perform a conditional expression? What is Monte's ternary operator?
----------------------------------------------------------------------------

Monte does not have a ternary operator. However, in exchange, the ``if``
expression can be used where any other expression might be placed. As an
example, consider a function that tests whether an argument is even::

    def even(i :Int) :Str:
        if (i % 2 == 0):
            return "yes"
        else:
            return "no"

Monte lacks the ternary operator, but permits using regular conditional
expressions in its place. We can refactor this example to pull the ``return``
outside of the ``if``::

    def even(i :Int) :Str:
        return if (i % 2 == 0) {"yes"} else {"no"}

Don't forget that Monte requires ``if`` expressions to evaluate their
condition to a ``Bool``.

What's the difference between the ``m`` and ``M`` objects?
----------------------------------------------------------

``M`` is a helper object that provides several runtime services. It can pass
messages on behalf of other objects and quote strings.

``m`` is a quasiparser which parses Monte source code. It is part of the
runtime Monte compiler.

Differences With Python
~~~~~~~~~~~~~~~~~~~~~~~

Where did ``self`` go?
----------------------

Newcomers to Monte are often surprised to learn that Monte lacks a ``this`` or
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

What's the "no stale stack frame" policy?
-----------------------------------------

A stale stack frame is one that isn't currently running; it is neither the
current stack frame nor below the current stack frame.

The "no stale stack frame" policy is a policy in Monte's design: Monte forbids
suspending computation mid-frame. There are no coroutines or undelimited
continuations in Monte. Monte also does not have an "async/await" syntax,
since there is no way to implement this syntax without stale stack frames.

The policy is justified by readability concerns. Since Monte permits mutable
state, one author's code's behavior could be affected by another author's code
running further up the frame stack. Stale frames make comprehension of code
much harder as a result.
