=====
Tubes
=====

.. deprecated:: unstable
    Tubes have been deprecated in favor of :doc:`streamcaps`.

Tutorial
========

Monte provides a unified paradigm for handling streams of structured data. The
paradigm is known as *tubes*.

Tubes come in two flavors: *founts* and *drains*. A fount is an object which
can provide data to another tube. A drain is an object which can receive data
from another tube. A tube can be just a fount, just a drain, or both a fount
and a drain.

This is all pretty abstract. Let's roll up our sleeves and take a look at how
to use some tubes::

    def echo(fount, drain):
        fount.flowTo(drain)

This code instructs ``fount`` to provide data to ``drain``. This providing of
data will happen whenever ``fount`` wants, until either ``fount`` or ``drain``
indicate that flow should cease. While this example might seem trivial, it's
sufficient to use as e.g. a TCP echo server.

Sometimes founts receive their data between turns, and schedule special turns
to send data to drains. Other times founts are eager, and try to feed a drain
immediately during ``flowTo``. If you want to forcibly delay that eagerness
until another turn, just use an eventual send::

    def echo(fount, drain):
        fount<-flowTo(drain)

If a drain is also a fount, then ``flowTo`` will return a new fount which can
be flowed to another drain. This is called *tube composition* or *tube fusion*
and it is an important concept in tube handling.

Pumps
-----

Sometimes an operation on streaming chunks of data only cares about the data
and not about the streaming or chunking. Such an operation can be encapsulated
in a *pump*, which is like a tube but with no flow control. A pump takes one
item at a time and should return zero or more items.

Pumps are mostly useful because they can be wrapped into tubes, which can then
be composed with other tubes::

    def [=> makeMapPump] | _ := import("lib/tubes/mapPump")
    def [=> makePumpTube] | _ := import("lib/tubes/pumpTube")

    def negate(fount, drain):
        def tube := makePumpTube(makeMapPump(fn x {-x}))
        fount<-flowTo(tube)<-flowTo(drain)

This pump uses a mapping function to negate every element that flows through
it, without any concern over flow control.

.. module:: tubes
