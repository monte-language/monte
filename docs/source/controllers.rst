===========
Controllers
===========

Sometimes, when designing an API, we want to be able to customize Monte's
behavior while retaining the general Monte idioms for values and layouts.
Controller syntax lets us change behavior of code blocks in a safe and
coherent fashion.

How to Implement a Controller
=============================

Controller Expansion
--------------------

Suppose that we have a standard if-expression::

    if (cond()) {
        advance()
    } else {
        fallback()
    }

Now, suppose that we wished to customize this. We could define a controller
named ``ifController``, and then call it with very similar syntax::

    ifController (cond()) do {
        advance()
    } else {
        fallback()
    }

This expands roughly to the following::

    (ifController :DeepFrozen).control("do", 1, 0, fn {
        [[cond()], fn { advance() }]
    }).control("else", 0, 0, fn {
        [[], fn { fallback() }]
    }).controlRun()

We see that controllers must be ``DeepFrozen``, and that each code block, which
we'll call a "lambda-block", corresponds to a ``.control/4`` call, with a
``.controlRun()`` to indicate the end of blocks.

Control with Lambda-Blocks
--------------------------

The power of controllers is locked within the lambda-blocks. Each block is a
function which returns an ``[args, lambda]`` pair. The controller can choose
how many times it wants to call the block, and similarly, the block can return
new arguments every time it is called. Indeed, note above that ``cond()`` is
called every time its containing lambda-block is called.

What are the other arguments to ``.control(verb :Str, argCount :Int, paramCount
:Int, block)``? The control verb is the bare word preceding each block. The
argument count specifies how many arguments will be returned by the block.
Where are the parameters?

Let us imagine another hypothetical controller::

    m (action) do x { f(x) }

In this situation, ``x`` is the one and only parameter, and so the controller
receives a parameter count of ``1``.
