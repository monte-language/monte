Answered Questions
==================

Why the name?
-------------

It's like Monty Python, but with E.

What can you know about an object?
----------------------------------

Any object that you can access meets one of three criteria: 

* You created it,
* You were born with it, or
* You received it as a result of passing messages to something that met either
  of the first two criteria.

Additionally, you can use guards and auditors to ensure properties of an
object. 

Note that using ``when`` on a promise for a far reference still results in a
far reference. 


Parallelism?
---------------

Monte doesn't really say anything about parallelism per se. We *should*
though. If we're going to be agoric, we should say something about CPUs, even
if it's just that people should spin up more vats and make more code use
farrefs.

Concurrency?
------------

The one concurrency pattern in Monte is that, if you absolutely have to
perform near-ref operations on a far-ref, you must make a when-expression.
This allows the compiler to transform it into far-ref operations.


How do you send a message to an object?
------------------------------------------

In E (and Monte), there are two ways to send a message to an object.

1) Use the method call, foo.baz()
2) Use eventual send, foo <- baz()


Are all messages eligible for both methods of sending?
---------------------------------------------------------

A call (#1) is immediate and returns the value of whatever in foo handles that
message, probably a method.

An eventual send (#2) returns a promise for the result  (in particular, foo does
not receive the messages until the end of the current turn (event loop
iteration), and eventual messages are delivered in order.) Calls are only
allowed for near, resolved objects. Sends can be made to far or unresolved
objects (promises)

All messages are eligible for both kinds of sending, but not all objects can
receive messages in both ways.

References?
-----------

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

Functions?
----------

Since everything in Monte is an object, you're always calling methods rather
than functions.

A function is actually an object with a single run() method. In other words,
``def f() { ... }`` always desugars to ``object f { to run() { ... } }``.
 

Everything's a method?
----------------------

Well, everything's a message pass, rather.


Does this mean we should never make synchronous calls?
------------------------------------------------------

No. There are many kind of objects on which synchronous calls work, because
they are near references. For example, all literals are near: ``def lue :=
(6).mul(7)``. 

When in doubt, remember that there is a ``near`` guard which can be used to
confirm that an object is in the same vat as you and thus available for
synchronous calls. 


What's Monte's comment syntax?
---------------------------------

.. code-block:: monte

    # This comment goes to the end of the line
    /** This comment is multi-line.
        Yes, it starts with a two stars
        and ends with only one.
        These should only be used for docstrings. */


What does "dynamic" mean, when used to describe Monte?
---------------------------------------------------------

Dynamic typing, dynamic binding, dynamic compiling.


What are ejectors?
------------------

Ejectors can be thought of as named breaks. You can break out of any
expression with them. For example, early returns are implemented with them.
An ejector has indefinite scope, so you can pass it to methods etc and
invoking it unwinds the stack.

Return, Break, and Continue are all implemented as ejectors. If you're
familiar with call/current continuation shenanigans, it's like that, but
delimited so that it can't be called outside the scope that created it.

Blocking operators?
-------------------

Not available in Monte. Because of the no-stale-stack-frames policy, Monte
has neither generators nor threads nor C#-style async/await.

At an 'await' or 'yield' point, you don't know what subset of the code has
already been read. Since Monte is intended to be useful in an environment with
an unbounded amount of code, and 'await' and 'yield' force you to assume that
all of the code has been read, they cannot be available in Monte.


What's a stale stack frame?
---------------------------

A stale stack frame is one that isn't currently running.

Since state is mutable, your code's behavior is always affected by the stack
frames above it. If you violate strict stack ordering (as generators do), you
violate the assumptions that people make when reading and writing such code.

Vats?
-----

http://erights.org/elib/concurrency/vat.html might help

A vat's an object that sits on the border of the runtime and is responsible 
for containing, guarding, and passing messages to the objects inside of it.

"A Vat is vaguely like a traditional OS process -- it bundles together a 
single thread of control and an address space of synchronously accessible data"



Farrefs?
--------

Farrefs are references to far objects, namely objects in different vats. Messages
to far objects can only be sent asynchronously.


Promises?
---------

ES6 promises were derived from E's.
The crucial part is, when promises are resolved they become forwarders to
their values. 


Selfless objects?
-----------------

Some objects can always be near, even if they were initially far, if they can
be serialized in a way that allows them to be reconstituted in another vat.
This quality is known as being selfless, and objects with it include ints,
floats, strings, and objects that you define correctly. 

Selfless objects are "passed by construction", meaning that instructions for
creating a near version are passed over the wire. 

Wait, what about Self?
----------------------

Newcomers to Monte are often surprised to learn that Monte lacks a ``this`` or
``self`` keyword. In fact, Monte does have ways to refer to the current object,
but there's a deeper conceptual difference between Monte and other object-based
languages.

Monte does not have a ``this`` or ``self`` keyword because Monte objects can
refer to their "member" or "private" names without qualification. This is a
consequence of how Monte objects are built. Recall our previous example: ::

    def makeMyObject():
        return object myObject:
            pass

Let's modify it slightly. We want to give this object a "private" value secret
which cannot be accessed directly, and a method ``getSecret/0`` which will
return it. We put "private" in quotation marks to emphasize that Monte does not
have private names. Instead, all names are private in Monte; if one cannot see
a name, then one cannot access it. ::

    def makeMyObject(secret):
        return object myObject:
            to getSecret():
                return secret

And that's it. No declarations of object contents or special references to this
or self.

We can also simulate "member" names for objects. As before, we can achieve this
without this. ::

    def makeMyObject():
        var counter :int := 0
        return object myObject:
            to getCounter():
                return counter += 1

Here, ``counter`` is not visible outside of ``makeMyObject()``, which means
that no other object can directly modify it. Each time we call
``makeMyObject()``, we get a new object called ``myObject`` with a new counter.

(Note: Remember, Monte is an expression language. ``counter += 1`` returns the
value of ``counter``. That's how ``return counter += 1`` can work properly.)


Psuedomonadic joining on promises
---------------------------------

Monte has a mechanic which can be called pseudomonadic joining on promises.

This means that a promise becomes the value for the promise: 

.. code-block:: 

    def p := foo<-bar(); def p2 := p<-baz()

Because when-exprs evaluate to a promise as well, you can have something like

.. code-block:: 

    def p := foo<-bar(); def p2 := when (p) -> { p.doStuff() }; p2<-baz()

Will the iterable control when the computations are performed?
-----------------------------------------------------------------

That's way outside the scope of an iteration protocol

Let's talk about the _lazy_ iteration protocol
-------------------------------------------------

 We can just do like everybody else and have explicit laziness, can't we?
Or do we want language-level extra-lazy stuff?

.. code-block:: monte

 def workItems := [lazyNext(someIter) for _ in 0..!cores]
 # or to be less handwavey
 def workItems := [someIter.lazyNext() for _ in 0..!cores]

lazyNext() is like .next() but it either returns
    1) a near value if it's immediately available
    2) a promise if it's not
    3) a broken promise if you've iterated off the end
Even this isn't right,  but the idea is that you could use something like
twisted's coiterate to serially compute some items in a iterable, a few at a
time  and as they were made available, the promises in workItems would get
resolved

What are M and m?
-----------------

M is a singleton providing runtime services including passing messages to
farrefs. m is the quasiparser for monte source code. 

Novice Errors
=============

::

    monte/monte/test $ python test_lexer.py
    Traceback (most recent call last):
      File "test_lexer.py", line 1, in <module>
        from monte.test import unittest
    ImportError: No module named monte.test

You're not suppsed to run the tests directly. In the root ``monte`` directory,
use::

    trial monte.test.test_lexer

