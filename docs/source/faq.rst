Turns, References, and Vats
===========================

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
