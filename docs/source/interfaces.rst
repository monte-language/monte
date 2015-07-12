==========
Interfaces
==========

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
