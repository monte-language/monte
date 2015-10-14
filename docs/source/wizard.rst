=====================
Monte Language Sketch
=====================

Syntax
======

Monte's syntax is largely C-derived with an offside rule like Python's
and Haskell's. However, it's an expression language like Scheme. The
compromise is achieved by using braces and semicolons to delineate
blocks and separate expressions in general, but use indentation and
newlines for this in "statement position", which is chiefly the
toplevel of the file and inside an indented block.

  >>> { def f(x) { return x * x }; f(4) }
  16

Expansion
---------

Monte's syntax is sugar over a kernel language, Kernel-E. Every Monte
syntax construct expands to a Kernel-E expression.

  >>> m`1 + 1`.expand()
  m`1.add(1)`


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

.. todo:: This is a big topic; for now, see the `Reference
          Mechanics`__ section from `ELib`__ for now.

__ http://www.erights.org/elib/concurrency/refmech.html
__ http://www.erights.org/elib/index.html
