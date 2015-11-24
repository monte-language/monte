========
Promises
========

.. epigraph::

    Promises are a great way of dealing with eventual values, allowing one to
    compose and synchronise processes that depend on values that are computed
    asynchronously.

    -- `Quil <http://robotlolita.me/2015/11/15/how-do-promises-work.html>`_

Monte provides user-controllable transparent proxy objects, **promises**, for
highly customized asynchronous workflows.

Basic Promises
==============

The basic usage of promises is to create a pair of objects, called the promise
and the **resolver**::

    # Traditionally, promises are named "p" and resolvers are named "r".
    def [p, r] := Ref.promise()

The ``Ref`` object in the safe scope can produce promise/resolver pairs. It
also has many utility methods for manipulating promises.

A promise is a **transparent proxy**; it does not expose its own behavior via
message passing, but instead forwards all received messages to another object.
Instead, the resolver and ``Ref`` object coordinate to control the behavior of
the promise::

    # This next line will throw an exception; the promise isn't yet resolved,
    # so it can't deliver this immediate call.
    p.add(5)
    # We can resolve the promise, at which point the promise will forward
    # immediate calls to its resolved value.
    r.resolve(7)
    # And now we succeed!
    p.add(12)

Promises do not just resolve; they can also **break**. A **broken** promise
will never resolve, but instead refers to a **problem**, which is an object
(often a string) describing a failure.

::

    # Here we create a promise...
    def [p, r] := Ref.promise()
    # And now we break the promise!
    r.smash(`Promise was broken, sorry!`)
    # Referencing or using the promise will throw...
    p.add(12)
    # ...but some operations are still safe.
    Ref.optProblem(p)

When-expressions and Delayed Actions
====================================

Promises are commonly used to perform delayed actions which will execute at
some later time.

To queue an action, use an eventual send::

    # This message will be delivered on some later turn.
    def q := p<-add(5)

What is ``q``? ``q`` is *another* promise. It will be resolved automatically,
sometime after ``p`` resolves, with the value that ``p`` returned from its
sent message; in this case, if ``p`` was ``7``, then ``q`` would be ``12``.

Suppose that the action that we want to enqueue is more complex than a single
passed message. In that case, Monte provides the when-expression::

    # When the promise resolves, notify the user and start the next section.
    when (p) ->
        traceln(`Attention user: The promise $p has resolved.`)
        # This funny-looking syntax means to use the default verb of "run",
        # just like with a normal call.
        nextSection<-()
    catch problem:
        # Something went wrong. Better notify the user.
        traceln(`Attention user: There was a problem: $problem`)
        nextSection<-failed()

The when-expression consists of a when-block and an optional catch-block. When
the promise given to the when-expression becomes resolved, the when-block will
run on its own turn; if the promise is broken, then the catch-block will run
instead.
