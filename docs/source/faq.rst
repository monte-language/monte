===
FAQ
===

Unusual Monteisms
=================

Do I have to specify a default matcher for a switch expression?
---------------------------------------------------------------

The short answer: No. You might want to read on for the consequences of
omitting it, though.

Switch expressions expand to a tree of possibilities, with each matcher being
tried in turn until one matches. If none of them match, then an exception is
thrown with a short description of the failing specimen.

To override this behavior, specify a matcher that cannot fail. Examples of
patterns that cannot fail include final and var patterns without guards, and
ignore patterns::

    switch (specimen):
        match ==x:
            traceln(`$specimen was just like $x`)
        match i :Int:
            traceln(`$i is an Int`)
        match _:
            traceln(`Default matcher!`)

In this example, since the final matcher always succeeds, the default behavior
of throwing an exception is effectively overridden.

The long answer: When Monte expands ``switch`` expressions into Kernel-Monte, the
entire expression becomes a long series of ``if`` expressions. The final
``else`` throws an exception using the ``_switchFailed`` helper object. If the
penultimate ``if`` test cannot fail, then the final ``else`` is unreachable,
and it will be pruned by the optimizer during compilation.

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

When in doubt, remember that there is a ``Near`` guard which can be used to
confirm that an object is in the same vat as you and thus available for
synchronous calls.

Guards
======

How do I force an object to be a certain type?
----------------------------------------------

Use a guard that coerces objects to be of that type. Guards for all of the
primitive types in Monte are already builtin; see the documentation on
:doc:`guards` for more details.

Are guards expensive?
---------------------

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
