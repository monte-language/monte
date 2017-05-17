==========
Streamcaps
==========

Stream capabilities ("streamcaps") are objects which implement a protocol for
streaming data. Monte directly supports the streamcap protocol with unsafe
objects and standard library tooling. The protocol is designed to be simple to
implement and easy to reason about.

Quick Overview
==============

There are three interfaces to the streamcap protocol, called **sources**,
**sinks**, and **pumps**. Objects may only implement one interface at a time.
Sources generate data, sinks consume data, and pumps transform data.

The simplest usage is delivering a single datum from a source to a sink::

    source(sink)

We can enqueue an action to execute after delivery has succeeded::

    when (source(sink)) -> { action() }

We can also handle errors in case of failed delivery::

    when (source(sink)) -> { action() } catch problem { rescue(problem) }

Hand-delivering data to a sink is easy::

    for datum in (data) { sink(datum) }

To receive data from a source, write an inline sink object::

    object sink:
        to run(datum):
            return process<-(datum)
        to complete():
            success()
        to abort(problem):
            throw(problem)
    source(sink)

In the standard library, the "lib/streams" module has tools for manipulating
streamcaps. To deliver all (zero or more) data from a source to a sink, we can
use the ``flow`` helper::

    import "lib/streams" =~ [=> flow]
    when (flow(source, sink)) -> { done() }

Object Protocol
===============

Pumps
-----

Pumps are transformers of data. A pump does not participate in any sort of
flow control, but merely operates on data passing through.

The sole method of pumps is ``run/1``, which takes a single datum and returns
a list of zero or more data.

::

    var acc :Int := 0
    def accumulatingPump(i :Int) :List[Int] as Pump:
        "Accumulate a sum of integers."
        acc += i
        return [acc]

.. warning::
    Unlike the rest of the streamcap protocol, pumps must currently be
    synchronous; they must return ``List``. In the future, pumps should be
    able to return ``Vow[List]``.

Sinks
-----

Sinks are data consumers. A sink receives data and returns asynchronous
signals indicating the fate of each received datum.

Sinks have three methods: ``run/1``, ``complete/0``, and ``abort/1``.
``run/1`` is for delivering data to the sink, and returns a ``Vow[Void]``
which succeeds when delivery completes, or breaks when delivery fails::

    when (sink(datum)) ->
        traceln("Delivery complete!")
    catch problem:
        traceln("Delivery failed:")
        traceln.exception(problem)

The ``complete/0`` and ``abort/1`` methods inform the sink that no more data
will be delivered. ``complete/0`` is for successful termination, and
``abort/1`` is for failed termination, with a problem. After a sink has
terminated, further deliveries may behave in arbitrary ways. In general, sinks
will usually raise exceptions or return broken promises if data is delivered
after termination.

Sink Semantics
~~~~~~~~~~~~~~

What does "delivery" really mean? A sink could decide that data is delivered
when it is enqueued in an internal buffer, or sent onward to a remote
resource. A sink should not indicate that delivery has succeeded until the
sink is ready to receive more data, in order to provide implicit backpressure.

Aborting a sink may alter the behavior of the sink with regards to enqueued or
processing data. In particular, TCP connections and streaming file handles may
close uncleanly after being aborted. Sinks are allowed to have this behavior
because sinks are only required to flush upon being cleanly terminated.

Sources
-------

Sources are data emitters. A source receives sinks and delivers data to those
sinks.

Sources only have one method, ``run/1``, which takes a sink::

    source(sink)

Just like ``run/1`` of sinks, sources return a ``Vow[Void]`` indicating
whether the sink was called successfully::

    when (source(sink)) -> { success() }

A typical source will return the sink's delivery notification directly::

    def cat():
        return "meow"

    def catSource(sink) as Source:
        return sink(cat)

Patterns
========

Flow
----

The most common pattern for streamcaps is *flowing* all data from a source to
a sink. Use the ``flow`` helper from "lib/streams" to make this easy. Here's a
complete TCP echo server::

    import "lib/streams" =~ [=> flow :DeepFrozen]
    exports (main)

    def main([via (_makeInt) port], => makeTCP4ServerEndpoint) as DeepFrozen:
        def handler(source, sink):
            return flow(source, sink)
        def ep := makeTCP4ServerEndpoint(port)
        ep.listenStream(handler)
        return 0
