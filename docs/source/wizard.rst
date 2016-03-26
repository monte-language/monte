=====================
Monte Language Sketch
=====================

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


Scoping Rules
-------------

Monte is lexically scoped, with simple scoping rules. In general, names are
only accessible within the scope in which they were defined.

After an object has been created, the names visible to it aren't accessible
from outside the object. This is because Monte objects cannot share their
internal state; they can only respond to messages. For programmers coming from
object-oriented languages with access modifiers, such as ``private`` and
``protected``, this is somewhat like if there were only one access modifier
for variables, ``private``. (And only one access modifier for methods,
``public``.)


Closing Over Bindings
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: monte

    var x := 42
    object obj:
        to run():
            return x += 1

Here, ``obj`` can see ``x``, permitting the usage of ``x`` within ``obj``'s
definition. When ``obj.run()`` is called, ``x`` will be mutated. Monte does
not require any "global" or "nonlocal" keywords to do this.
