===============
Design of Monte
===============

This is a gentle overview of the design features of Monte and how it fits into
the larger genealogy of programming languages.

Types
=====

Monte features strong dynamic types. By "strong" we mean that Monte's types
resist automatic coercion; by "dynamic" we mean that objects are not
necessarily specialized to any specific type.

As an example of strong typing in Monte, consider the following statement::

    def x := 42 + true

This statement will result in an error, because ``true`` is a boolean value
and cannot be automatically transformed into an integer, float, or other value
which integers will accept for addition.

Functional Features
===================

Monte has support for the various language features required for programming
in the so-called "functional" style. Monte supports closing over values (by
reference and by binding), and Monte also supports creating new function
objects at runtime. This combination of features enables functional
programming patterns.

Monte also has several features similar to those found in languages in the
Lisp and ML families which are often conflated with the functional style, like
strict lexical scoping, immutable builtin value types, and currying for
message passing.

Object-Based Features
=====================

Monte is descended from the Smalltalk family of languages, and as such,
is an **object-based** language. "Object-oriented" styles of programming are
largely available in Monte.

.. _ocap:

Capability Model
================

.. note:: Not sure whether this should be here, or in a separate page.

No object created within a scope will be accessible outside of that scope,
unless a message about it is passed out. In Monte, the only way for object A
to know that B exists is:

* If B created A or A was created with knowledge of B
* If A created B
* If any object that A knows about passed A a message about B

For example::

    def scope():
        def a := 1
        def innerScope():
            def b := 2
            traceln(`a is $a and b is $b`)

        # This line would cause a compile-time error, since the name `b` isn't
        # accessible in this scope!
        # traceln(`I cannot access $b here`)

        return innerScope

    scope()()

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
