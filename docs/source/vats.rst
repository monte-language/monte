====
Vats
====

Vats are Monte's response to the vagaries of traditional
operating-system-supported threads of control. Vats extend a modicum of
parallelism and concurrency to Monte programs while removing the difficult
data races and lock management that threads classically require.

What's in a Vat?
================

A vat, by analogy, is like a tab in a modern Web browser. It contains some
objects, which may have near references between themselves, and a queue of
pending messages to deliver to some of those objects. A browser tab might have
some JavaScript to run; a vat might choose to take a **turn**, delivering a
message to an object within the vat and letting the object pass any subsequent
messages to its referents. Vats can be managed just like browser tabs, with
vats being spawned and destroyed according to the whims of anybody with
references to those vats. Indeed, vats can be managed just like any other
object, and vats are correct with regards to capability security.

How do I perform parallel computations?
---------------------------------------

Use the ``makeProcess`` entrypoint capability to run multiple
processes to get node-level parallelism.

.. note::
    Monte doesn't really say anything about parallelism per se. We *should*
    though. If we're going to be agoric, we should say something about CPUs,
    even if it's just that people should spin up more vats and make more code
    use farrefs.

How do I perform concurrent operations?
---------------------------------------

Spawn more vats. All vats are concurrently turning.

References (WIP)
----------------

.. note::
    Messy.

.. todo:: This is a big topic; for now, see the `Reference
          Mechanics`__ section from `ELib`__ for now.

__ http://www.erights.org/elib/concurrency/refmech.html
__ http://www.erights.org/elib/index.html

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

When in doubt, remember that there is a ``Near`` guard which can be used to
confirm that an object is in the same vat as you and thus available for
synchronous calls.
