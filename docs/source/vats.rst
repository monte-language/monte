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
