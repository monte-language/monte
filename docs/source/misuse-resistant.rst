================================
Misuse-Resistant Language Design
================================

Several of Monte's design decisions are based on the concept of
*misuse-resistant* tools which are designed to frustrate attempts to write
faulty code, whether accidentally or intentionally.

Sealed Exceptions
=================

Monte has exceptions. Exceptions are meant to indicate failures which cannot
be locally recovered from; the throwing object is stuck and has no options
left. However, to whom is the failure indicated? We treat the ability to
handle failures as a capability, because failures may violate containment by
revealing information about the internal state of the throwing object.

Exceptions are unwound like ejectors. Try-finally expressions do not have
access to exceptions. Try-catch expressions do not receive the exception
itself, but a sealed box for the exception. The unsealer, ``unsealException``,
is closely held by the system debugger. As a result, exception handlers form a
structure where escaping ejectors are handled at the lone call site that
spawned them, and thrown exceptions are handled by the nearest caller with the
authority to act as the system debugger.

Why do we allow ``unsealException``? The primary motivation is to allow the
construction of inner interpreters which absorb exception-handling from Monte.
We have built such interpreters as REPLs at the command line and in IRC bots.
Only entrypoints can even ask for ``unsealException``, and of course they may
not get it, or get a stand-in object which is limited in scope and extent.

Other Languages
~~~~~~~~~~~~~~~

Haskell only allows exceptions in the IO Monad. If pure code were truly pure,
then this would allow for pure code to never know about exceptions at all.
(Haskell has escape hatches for throwing exceptions out of pure code.)

Unicode Identifers
==================

Monte has Unicode identifiers, like many contemporary languages. However,
Monte generally rejects bare identifiers which other languages would accept.
Instead, we require arbitrary Unicode identifiers to be wrapped with a slight
decoration which serves as warning plumage.

Here are the examples from `Unicode TR39`_ as valid Monte identifiers::

    ::"pаypаl"
    ::"toys-я-us"
    ::"1iνе"

None of these examples are valid bare identifiers in Monte.

.. _Unicode TR39: http://www.unicode.org/reports/tr39/

Other Languages
~~~~~~~~~~~~~~~

Haskell has had Unicode identifiers since Haskell 98. Haskell support for
Unicode identifiers is detailed in the `Haskell 98 Report Lexical Structure`_.
Haskell accepts "pаypаl" as a bare identifier for names.

Python 3 added Unicode identifiers in `PEP 3131`_. Python 3 accepts "pаypаl"
as a bare identifier for names and attributes.

.. _Haskell 98 Report Lexical Structure: https://www.haskell.org/onlinereport/lexemes.html
.. _PEP 3131: https://www.python.org/dev/peps/pep-3131/

Parenthesized Sub-Expressions
=============================

Whenever an expression is syntactically contained within another expression,
it must be parenthesized, with the sole exception of common guard-exprs used
in patterns. This feature, explained in more detail in `The Power of
Irrelevance`_, improves readability by clearly distinguishing patterns from
expressions.

.. _The Power of Irrelevance: http://erights.org/data/irrelevance.html
