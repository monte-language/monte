===================
Monte (for Wizards)
===================

Why Monte?
==========

Every new language should solve a problem. What problem does Monte solve?

E and Python
------------

Monte is based on E, a language intended for secure distributed computation.
Monte also incorporates many syntactic ideas from Python, a language designed
for readability and simplicity. The design of Monte incorporates both of these
languages' philosophies, with the goal of supporting environments that are
orders of magnitude more complex than existing systems.

For a history of E's ideas, see http://www.erights.org/history/index.html

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

The Semantics
=============

Architect's View
----------------

Monte programs are a collection of vats, running in one or more processes on
one or more hosts. Vats contain three elements: a stack, a queue, and a heap.
All three contain Monte objects. The queue contains messages to objects in the
heap; messages consist of a verb and may contain objects passed as arguments.
Execution of code in a vat progresses by **turns**; each turn is started by
delivering the next message in the queue to its recipient, which can result in
activation records being placed on the stack and further messages going into
the queue. The turn progresses until the stack is empty. A new turn begins
with the next message on the queue.

Hacker's View
-------------

Monte is a pure object-based language in the Smalltalk tradition. All values
are objects and all computation is done by sending messages to objects.
Unlike Smalltalk, Python, Java, etc., objects are not instances of classes.
Unlike Self or JavaScript, objects are not derived from prototypes. Monte
objects are defined via object literal syntax as closures over variable
bindings. Specifically unlike Python, objects don't have attributes, merely
responses to messages.

Compiler's View
---------------

Monte provides both immediate, synchronous calls to methods and eventual,
asynchronous sends to methods. The former provides the usual
subroutine-invocation semantics, whereas the latter enqueues a message to be
delivered in a subsequent vat turn. Monte names for objects are encapsulated
in bindings.

A Monte name binding consists of a slot and a slot guard. Assignment to names
and accessing names invokes methods on that name's slot. This can be used to
share state between objects, and perform actions on reads from/writes to
names. Slot guards for bindings closed over an object are revealed to
auditors, during auditing.

Name bindings may have guards, which are given objects and may either accept,
coerce, or reject them. Coercion results in the value produced by the guard
being different from the specimen given. The specimen may be asked to conform
itself to the guard as part of coercion.

Interface expressions are a tool for creating trivial guards; an object
expression may declare that it implements an interface, and the interface
object may be used as a guard to accept only objects that declare that
interface.

Network's View
--------------

This is a big topic and you should read
http://www.erights.org/elib/concurrency/refmech.html for now.
