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

.. syntax:: controller

    Ap("Controller",
      NonTerminal("identifier"),
      OneOrMore(
        Ap("params",
          Brackets("(", SepBy(NonTerminal("expr"), ","), ")"),
          Sigil("COMMAND", ZeroOrMore(NonTerminal("pattern")),
            Brackets("{", NonTerminal("expr"), "}")))))

Control with Lambda-Blocks
--------------------------

The `.control/4` method takes a parsed bareword, called a *command*, and the
arities of the command's parameters and patterns, as well as a lambda-block.
Lambda-blocks are thunks which return ``[args :List, lambda]`` pairs. The
first arity indicates how many parameters will be evaluated, and thus how
large ``args`` is. The other arity indicates how many arguments ``lambda``
wants to receive.

The power of controllers is locked within the lambda-blocks. As each block is
defined, the controller receives the corresponding command and interprets it.
Each block might be called multiple times, and can return a different
``lambda`` each time. Each call will re-evaluate the parameter expressions,
too. Indeed, note above that ``cond()`` is called every time its containing
lambda-block is called.

Let us imagine another hypothetical controller::

    m (action) do x { f(x) }

In this situation, ``x`` is the one and only parameter, and so the controller
receives a parameter count of ``1``.

Lambda Refusal
--------------

A ``lambda`` might not like the arguments which it receives. While it could
throw an exception, it could also politely refuse by triggering an ejector. To
facilitate this, an extra parameter is implied by the compiler to exist
whenever the third argument of `.control/4` is non-zero. In those situations,
the controller should pass an ejector along with the other arguments, at the
end of the argument list.
