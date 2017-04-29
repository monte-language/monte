.. _vats:

====
Vats
====

Vats are Monte's response to the vagaries of traditional
operating-system-supported threads of control. Vats extend a modicum of
parallelism and concurrency to Monte programs while removing the difficult
data races and lock management that threads classically require.

Quickstart
==========

From an entrypoint, the ``currentVat`` named argument will refer to the "top"
or "first" vat::

    ▲> currentVat
    Result: <vat(pa, immortal, 2 turns pending)>

.. note::

    This vat is named "pa", is "immortal", which means that it will never
    terminate computation abruptly, and has two turns of computation pending in
    its turn queue. All of this diagnostic information is Typhon-specific and
    may not be available in all implementations.

We can *sprout* a new vat at any time from an existing vat. The two vats will
be distinct::

    ▲> def newVat := currentVat.sprout("re")
    Result: <vat(re, immortal, 0 turns pending)>
    ▲> newVat == currentVat
    Result: false

We can also *seed* a vat with a computation. The computation must be ``DeepFrozen``, but otherwise any object can be used as a seed. This example is a bit dry but shows off the possibilities::

    ▲> newVat
    Result: <vat(re, immortal, 0 turns pending)>
    ▲> def seed() as DeepFrozen { traceln("Seeding!"); return fn x { traceln(`I was sent $x`) } }
    Result: <seed>
    ▲> def seeded := newVat.seed(seed)
    TRACE: From vat re
     ~ "Seeding!"
    Result: <promise>
    ▲> seeded<-(42)
    Result: <promise>
    TRACE: From vat re
     ~ "I was sent 42"
    ▲> seeded<-(object popsicle as DeepFrozen {})
    Result: <promise>
    TRACE: From vat re
     ~ "I was sent <popsicle>"
    ▲> seeded<-(object uncopyable {})
    Result: <promise>
    TRACE: From vat re
     ~ "I was sent <promise>"

Seeding produces a far reference to the result of the seed's call, which might
not be itself ``DeepFrozen``. To interact with this reference, send messages to
it. Note how sending ``popsicle`` caused the seeded object to receive a near
(and thus printable) reference to it; this is because ``DeepFrozen`` objects
travel between near vats directly.

What's in a Vat?
================

The Browser Analogy
-------------------

A vat, by analogy, is like a tab in a modern Web browser. It contains some
objects, which may have near references between themselves, and a queue of
pending messages to deliver to some of those objects. A browser tab might have
some JavaScript to run; a vat might choose to take a **turn**, delivering a
message to an object within the vat and letting the object pass any subsequent
messages to its referents. Vats can be managed just like browser tabs, with
vats being spawned and destroyed according to the whims of anybody with
references to those vats. Indeed, vats can be managed just like any other
object, and vats are correct with regards to capability security.

Vats, Formally and Informally
-----------------------------

This is all confusing. What, precisely, **is** a vat?

Formally, a vat is just a container of objects. Vats have a **turn queue**, a
list of messages yet to be delivered to objects within the vat, along with an
optional resolver for each message. Vats compute by repeatedly delivering
individual messages in the turn queue; each delivery is called a **turn**.
Turns are taken in the order that they are enqueued, FIFO.

If a resolver is provided for a turn, then the resolver is resolved with the
result of delivery. If delivery causes an exception, then the vat catches the
exception, sealing it, and smashes the resolver with the exception instead. In
either case, a **membrane** is applied to all objects which come into or leave
the vat, including the result of delivery; this membrane replaces all
non-``DeepFrozen`` values with far references.

Informally, a vat isolates an object graph. Objects inside the vat can only
refer to things outside the vat by far reference; there is no way to perform
an immediate call across a vat boundary.

Whenever an object sends a message into a vat, the vat prepares to take a
**turn**, whence the message will be delivered to the correct object inside
the vat. Sends out of the vat produce promises for references to results of
those sends, and the promises have normal error-handling behavior; if you send
a message to another vat, and an exception happens in that other vat, then
you'll get a broken promise.

Vat Interface
=============

Vats have two methods, ``.sprout/1`` and ``.seed/1``.

.. sidebar:: Why is ``.sprout/1`` synchronous?

    A common theme in Monte's vat design is implicit and convenient
    asynchronous computation. So why is vat sprouting synchronous? Well,
    Monte's guiding philosophy is to never block. But producing a vat is a
    non-blocking operation, since a sprouted vat starts out empty, and vats are
    isolated, so the new vat cannot affect the current vat's current turn.

    In general, vats queue up work to do later. Since adding things to turn
    queues is non-blocking, vats return promises for the work to be done later.

    However, this isn't the whole story. It's true that vats aren't *totally*
    empty; they generally acquire a safe scope as a result of pass-by-copy
    semantics. A Monte implementation which supports many small vats is
    expected to implement a copy-on-write semantics for objects in vats. This
    is one of the compelling use cases for ``DeepFrozen``; a ``DeepFrozen``
    object graph, like the safe scope or a vat seed, can live on a shared heap
    and be zero-copy shared between all vats.

To sprout a new vat, call ``vat.sprout(name :Str) :Any``, which returns a new vat.
The new vat starts out empty, with an empty turn queue.

To put computation into a vat, call ``vat.seed(seed :DeepFrozen) :Vow``, which
does several things. First, the seeded vat copies the ``seed`` and its object
graph into itself, isolating them from the calling vat. Then, the vat adds
``seed<-()`` to its turn queue, and returns a promise for that pending turn.

FAQ
===

Vats are one of the more confusing parts of Monte, and some questions occur
frequently.

.. _threads:

So, no threads?
---------------

Correct. Monte does not have any way to block on I/O, so there is no need for
threads at the application level.

Are vats parallel or concurrent?
--------------------------------

It is implementation-dependent. Currently, Typhon is designed for an M:N
threading model where up to M vats may take N turns in parallel on N distinct
threads. However, Typhon currently only takes 1 turn in parallel. Other
implementations may choose to do different parallelism models.

A key insight with vats is that a computation that is broken up into
*concurrent* pieces on distinct vats can be transformed into *parallel*
execution with maximal parallelism just by altering the underlying
interpreter. The correctness of the computation does not change. This concept
is from the `actor model`_, which forms the theoretical basis for vats.

.. _actor model: https://en.wikipedia.org/wiki/Actor_model

How do I perform parallel computations today?
---------------------------------------------

Today, using Typhon, use the ``makeProcess`` entrypoint capability to run
multiple processes to get node-level parallelism. We recognize that this is a
very unsatisfactory solution for all involved, and we plan to eventually
implement automatic parallel vats in Typhon.

For the future… Try to structure your code into modules; Typhon may
parallelize module loading in the future. Also try to structure your code into
vats, since we expect most interpreters to eventually implement parallel vat
execution.

How do I perform concurrent operations?
---------------------------------------

Spawn more vats. All vats are concurrently turning. A vat will only ever lie
fallow when it has no turns queued.

.. _why-calls:

Why should we ever make synchronous calls?
------------------------------------------

In a nutshell, always make calls unless you intentionally want to create an
asynchronous "edge" where your control flow stops, only to resume later. And
also when you're working with promises and far references, since you can't
make calls on those values!

Synchronous calls are very common. There are many kind of objects on which
synchronous calls work, because they are near references. For example, all
literals are near, and so is all operator syntax::

    def lue := 6 * 7

There are many objects in the safe scope which are perfectly fine to use
with either calls or sends.

Here are some handy idioms. To check whether a value is near::

    Ref.isNear(value)

A variant that might be more useful in the future::

    value =~ n :Near

.. _why-not-only-sends:

No, you misunderstood; why doesn't Monte have only eventual sends?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ah! There are several reasons, to be taken together as a measure of how
difficult such a system would be to work with.

Execution speed is very bad in these systems. This is because it is quite
difficult for any compiler to see, even with cutting-edge technology, where a
sent message will be delivered to, since it travels in both time and space
before being resolved. While our general feeling is that speed is a secondary
concern in most cases, we are motivated to care here for two reasons. First,
practical compilers tend to do enormous amounts of work to convert chains of
monomorphic sends into calls; `GHC`_ has a strictness analyzer to avoid lazy
thunk chains on the heap, which have similar delayed-evaluation properties to
sends. Second, `Joule`_, an ancestor of Monte, tried this design approach and
found speed to be a serious problem.

Some edges of Monte's interaction with the external world are much
better-modeled with calls than sends. A chauvanist argument can be made about
how arithmetic should at least occasionally be lowered to a sequence of CPU
instructions. However, we have found that a trickier and more important
problem is dealing with object graph recursion, since Monte object graphs
already can be quite treacherous. In Monte, object graphs can be cyclical and
can hold delayed or eventual values. This poses a serious challenge, since
sends for traversal can end up interleaved with sends which alter the
structure or contents of the graph being traversed. Concretely:

 * Equality testing: ``x == y`` is a question that can, if they are
   ``Transparent``, traverse the full transitive closures of both ``x`` and
   ``y``.
 * Serialization: Pretty-printing, databases, RPC, DOT files, and all other
   serialization must traverse the full object graph as-is in order to not
   write out corrupted snapshots.
 * Hashing: Implementations may choose to define internal object hashes to
   speed up sets and maps. Application-level probabalistic data structures
   also often perform hashing. Like serialization, but just different enough
   to justify three sentences and a bullet point.
 * Garbage collection: GCs in the current state of the art are increasingly
   concurrent, running alongside mutators or only performing collections on
   per-mutator heaps. Nonetheless, when the GC would like to perform a
   collection, it often does need to traverse the object graph without
   worrying that an object will not race its own impending deletion with an
   incoming message delivery. This could be dealt with by requiring all sends
   to go through the vat turn queue, and pausing the vat in-between turns to
   collect. But then speed concerns pop up, and really this is a very deep
   rabbit hole…

So, for these reason, we distinguish promises at the edges of our object
graphs, and we implement these traversals using calls. As a practical
consequence, :ref:`uncalls <uncall>` are calls and must return near values.
This also influenced the design of printers, which serialize by
pretty-printing, and vats, which could optionally be implemented with per-vat
GC.

.. _GHC: https://en.wikipedia.org/wiki/Glasgow_Haskell_Compiler
.. _Joule: https://en.wikipedia.org/wiki/Joule_(programming_language)
