===============
Design of Monte
===============

This is a gentle overview of the design features of Monte and how it fits into
the larger genealogy of programming languages.

E and Python
------------

Monte is based on E, a language intended for secure distributed computation.
Monte also incorporates many syntactic ideas from Python, a language designed
for readability and simplicity. The design of Monte incorporates both of these
languages' philosophies, with the goal of supporting environments that are
orders of magnitude more complex than existing systems.

See also `a history of E's ideas`__.

__ http://www.erights.org/history/index.html

Networking
----------

Unlike many other contemporary programming languages, Monte does not need an
additional networking library to provide solid primitive and high-level
networking operations. This is because Monte was designed to handle networking
as easily as any other kind of input or output.

Distributed Systems
-------------------

Monte comes with builtin explicit parallelism suitable for scaling to
arbitrary numbers of processes or machines, and a well-defined concurrency
system that simplifies and streamlines the task of writing event-driven code.

Monte has one parallel primitive: the **vat**. Vats are objects which
encapsulate an entire Monte runtime and isolate other objects from objects in
other vats. Vats are able to communicate across a variety of gulfs, from
inter-process threads to separate machines on a network.

Monte also has one concurrent operation. Monte permits messages to be passed
as **eventual sends**. An eventually-sent message will be passed to the target
object at a later time, generating a **promise** which can have more messages
sent to it. Unlike similar mechanisms in Twisted, Node.js, etc., Monte builds
promises and eventual sending directly into the language and runtime, removing
the need for extraneous libraries.

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
