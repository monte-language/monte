Design Q&A
==========


.. _ejector:

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

Does Monte have functions?
--------------------------

No. Since everything in Monte is an object, you're always calling methods
rather than functions. See :ref:`def-fun`.

Where did ``self`` go?
~~~~~~~~~~~~~~~~~~~~~~

Newcomers to Monte may be surprised to learn that Monte lacks a ``this`` or
``self`` keyword. In fact, Monte does have ways to refer to the current object,
but there's a deeper conceptual difference between Monte and other object-based
languages. See :ref:`maker`.


