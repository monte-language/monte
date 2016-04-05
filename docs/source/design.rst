Practical Security II: The Mafia IRC Bot (WIP)
==============================================

To demonstrate secure distributed programming in Monte, let's take the
:doc:`mafia game code <ordinary-programming>` developed earlier and make it
into an IRC bot.

The :download:`mafiabot.mt<tut/mafiabot.mt>` module begins by importing the
``mafia`` module, an ``irc/client`` library, and the same modules for dealing
with entropy that we saw before:

.. literalinclude:: tut/mafiabot.mt
    :linenos:
    :lines: 1-6
    :lineno-start: 1

The ``main`` entry point is provided with a number of powerful references as
named arguments:

  - To seed our random number generator, we use ``currentRuntime`` to get a
    source of true randomness, i.e. secure entropy.

  - To give ``makeIRCService`` access to TCP/IP networking and event
    scheduling, we use ``makeTPC4ClientEndPoint``, ``getAddrInfo``, and
    ``Timer``.

.. literalinclude:: tut/mafiabot.mt
    :linenos:
    :lines: 192-
    :lineno-start: 192


Networking
----------

Unlike many other contemporary programming languages, Monte does not need an
additional networking library to provide solid primitive and high-level
networking operations. This is because Monte was designed to handle networking
as easily as any other kind of input or output.

.. literalinclude:: tut/mafiabot.mt
    :linenos:
    :lines: 8-28
    :lineno-start: 8

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

.. literalinclude:: tut/mafiabot.mt
    :linenos:
    :lines: 30-67
    :lineno-start: 30


Principal of Least Authority
----------------------------

Straightforwad object-oriented design results in each object having the least
authority it needs:

  - ``makeIRCService`` provides the full range of IRC client behavior
  - ``makeChannelVow`` provides access to one channel
  - ``makeModerator`` encapsulates the play of one game
  - ``makePlayer`` represents the role of one player in one game
  - ``makeMafiaBot`` starts games on request, routes messages to the relevant
    moderator during game play, and disposes of moderators when games end.

Even if one of these components is buggy or compromised, its ability to
corrupt the system is limited to using the capabilities in its static scope.

Contrast this with traditional identity-based systems, where programs execute
with all privileges granted to a user or role. In such a system, any
compromise lets the attacker do anything that the user could do. A simple game
such as solitaire executes with all authority necessary to corrupt,
exfiltrate, or ransom the user's files.

With object capability disciplne, when the time comes for a security
inspection, we do not have to consider the possibility that any compromise in
any part of our program leaves the whole system wide open in this way. Each
component in the system can be reviewed independently and auditing a system
for security becomes cost-effective to an extent that is infeasible with other
approaches [#darpa]_.

.. literalinclude:: tut/mafiabot.mt
    :linenos:
    :lines: 68-132
    :lineno-start: 68

Note the way ``makeMafiaBot`` provides a secret channel for the mafiosos to
collude at night:

.. literalinclude:: tut/mafiabot.mt
    :linenos:
    :lines: 133-192
    :lineno-start: 133

.. rubric:: Notes

.. [#darpa] As documented in `the DarpaBrowser report
            <http://www.combex.com/papers/darpa-report/index.html>`_

