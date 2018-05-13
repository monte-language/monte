=============================
Ejectors & Escape Expressions
=============================

.. _ejector:

Ejectors can be hard to explain with words alone, so we will start with code::

    # 42
    escape ej { 42 }

    # 42
    escape ej { ej(42) }

    # null
    escape ej { ej() }

.. sidebar:: What's in a Name?

    Ejectors are traditionally named ``ej``, from the E programming language,
    but other names are common too. ``k`` is a traditional name from Scheme
    meaning "continuation", referring to the technical definition of ejectors
    as single-use delimited continuations. For catch clauses, the traditional
    name ``problem`` (or ``p`` for short) is common.

An :dfn:`escape expression` creates an :dfn:`ejector`, which is an
ordinary-looking object, and then evaluates its body. Calling ``.run()`` on an
ejector will change the return value from the body's return value to whatever
is passed, or ``null`` by default.

We can also optionally catch the value and manipulate it. However, any
``catch`` clause will only be run if the ejector is called::

    # 42
    escape ej { 42 } catch p { 5 }

    # 5
    escape ej { ej() } catch p { 5 }

    # 7
    escape ej { ej(42) } catch p { p // 6 }

Ejector-based Control Flow
==========================

The first major use for ejectors is in implementing several common kinds of
control flow. By themselves, ejectors can be used to prematurely end or
'short-circuit' a computation; calling an ejector prevents any future
computation::

    # 42, no exception
    escape ej { ej(42); 5 // 0 }

Ejectors even work when called by other objects::

    # 6
    def f(x, ej):
        return ej(x) * 7
    escape ej { f(6, ej) }

Conditional Definitions
-----------------------

::

    # 0
    escape ej {
        def x :Int exit ej := "five"
        x
    } catch problem { 0 }

``throw.eject``
---------------

Often we might want to ensure that the object we are calling will actually
alter control flow. We will see many motivating examples shortly. In these
cases, we can use ``throw.eject/2`` to ensure that we will not continue
computation::

    if (weAreFinished):
        throw.eject(ej, "finished")
    launchMissiles<-()

This is equivalent to ``ej("finished")`` but will only launch missiles
conditionally. We might imagine a simple implementation of this method::

    def throwEject(ej, problem):
        ej(problem)
        throw(problem)
