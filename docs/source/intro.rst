Introduction
============

Why Monte?
----------

Don't we have enough languages already? How could we justify bringing
yet another programming language into the world?

Because **secure distributed computing should not be hard**. We have
entered the age of globally distributed computing with a vengeance,
and `everything is broken`__. The hodgepodge of today's dominant
languages and frameworks offer no comprehensive solution [#]_. Monte
combines much of the expressive convenience of Python with the secure
distributed computing features of E [#]_:

__ https://medium.com/message/everything-is-broken-81e5f33a24e1

.. sidebar:: Object Capabilities

   Monte inherits from E a specific flavor of capability-based security known
   as object capabilities. With object capabilities, capability-oriented
   programming has the same flavor as object-oriented programming, except that
   capability-oriented programming takes the usual object-oriented constraints
   more seriously. Often when using object capabilities for security, one
   finds that a more secure program is simply a program that follows
   object-oriented principles of modularization more closely.

- Distributed computing benefits from a *promise-pipelining*
  architecture that ensures that *most deadlocks cannot occur*. [*]_

- Monte, like E before it, has dramatic advantages for secure distributed
  systems.

   - Monte offers cryptographic services directly to its users, easing the use
     of good cryptographic primitives.

   - Capability-based security enables the concise composition of
     powerful patterns of interoperation, patterns that enable
     extensive cooperation even in the presence of severely limited
     trust.

   - The fractal nature of POLA encourages short and readable modules, leading
     to applications having relatively low amounts of code. As a consequence,
     the attack surface of an application is decreased and code review is
     easier. The implementors of E and CapDesk boast of implementing
     peer-to-peer chat systems and digital-money bank servers in hundreds,
     *not* tens of thousands, of lines of code.

     When the time comes for a security inspection, capability security allows
     simple reachability analysis to exclude huge swaths of code because they
     cannot embody a threat. As a consequence, auditing a system for security
     becomes cost- effective to an extent that is simply unimaginable with
     other approaches [#darpa]_.

   - With Monte, it is straightforward to create systems that run across
     the Internet that are as secure and safe as if the entire system
     were running on a single computer in your basement. As one of the
     original developers of Smalltalk observed, upon learning about
     the object-capability paradigm from E, capability security is
     "natural security": if you shouldn't use it, you just can't see
     it.

- Monte enables the fearless yet powerful use of multi-party limited-trust
  mobile code.

These qualities cannot be achieved with traditional security
approaches. Do not expect the next release of Java, Windows, or Linux
to fix the problem: the flaws in these systems lie at the heart of
their architectures, unfixable without breaking upward compatibility,
as we shall discuss in the chapter on
:ref:`secure-distributed-computing`.

.. sidebar:: The origin of Monte's name

   The Monte language has its roots in the E and Python languages. We
   took "Monty" from "Monty Python", and put an "e" in there. Thus,
   "Monte".

Monte wraps these strengths in a Python-like syntax to make it quickly
comfortable for a large number of software engineers. It is built with objects
at the core of its design, making it easy to write modular, readable,
maintainable software using the strategies familiar from Python, Java, and the
like. It has the kind of powerful string handling that will be recognized and
seized upon by the Perl programmer.

For both better and for worse, Monte is a dynamically typed language like
Smalltalk, not a statically typed language like Java. Users of Perl and Python
will immediately recognize this is an advantage; Java and C++ programmers may
not be so sure. While a thorough discussion of the merits and demerits of
static typing is well beyond the scope of this document, many of the most
complex yet most reliable systems in the world today have been developed with
dynamically typed languages. We invite you to try Monte first and form your
conclusions later. We believe you will find the experience both pleasant and
productive, as the long heritage of programmers from Scheme to Smalltalk to
Perl and Python have found in the past.

.. note:: While Monte's usable and most architectural issues are
          resolved, it is still undergoing rapid development.
          See :ref:`roadmap` for details.


.. [*] As with all sufficiently complex concurrency systems, deadlock is
       possible. That said, it has not been observed outside of
       specially-constructed pathological objects.

Why not Monte?
--------------

Monte assumes automatic memory management; the current reference
implementation uses the PyPy garbage collector, and any other implementation
will have to choose a similar scheme. As such, it is not a good language for
low level machine manipulation. So do not try to use Monte for writing device
drivers.

Monte's performance is currently quite unfavorable compared to raw C at the
moment, and additionally, Monte's target niches are largely occupied by other
dynamic languages with JIT-compiler-based runtimes, so it is not a design goal
to compete with C or other memory-unsafe languages.


Preface to Monte Documentation
------------------------------

We begin with an introduction to practical Monte programming. Comparisons
to Python are frequent, so some understanding of Python is desirable.

Later sections form the :ref:`spec` and the :ref:`stdlib`.

This largely follows the structure of `E in a Walnut`__ by Marc Stiegler
and `The E Language`__ and `ELib`__ by Mark Miller.

.. todo:: To what extent do we want to invite feedback and offer
          support? i.e. what to write where Walnut says "If you
          encounter some surprising behavior not explained here,
          please join the e-lang discussion group and ask there"?

__ http://wiki.erights.org/wiki/Walnut
__ http://erights.org/elang/index.html
__ http://erights.org/elib/index.html


Fireworks In Part II
--------------------

Though Monte is a powerful language for writing single-CPU programs, the main
power of Monte becomes evident only after you move into distributed
programming. It would be tempting to introduce the distributed computing
features first, but one can't really do any meaningful computing without the
basic data, flow, function, and object structures. So we introduce
:ref:`ordinary-programming` in Part I before getting into the serious
distributed computing facilities.

However, since Monte was designed in the Python syntax tradition, an experienced
programmer can probably glean enough from the Quick Reference Card to skip
directly to Part II on :ref:`distributed-computing`. If you are short of time
and have the requisite background, we recommend that strategy. Go back and
read :ref:`Part I<ordinary-programming>` when you are convinced that Monte's
power for distributed programming meets your needs.

.. todo:: quick reference card


Getting Started
---------------

.. note:: Monte's installation process is in transition. See :ref:`roadmap`
    and the `monte wiki`__ for more.

__ https://github.com/monte-language/monte/wiki


Interacting with the Monte REPL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Monte has a traditional "Read - Evaluate - Print Loop", or REPL, for
exploration. For example::

  >>> 1 + 1
  2

  >>> "abc".size()
  3


Editor Syntax Highlighting
~~~~~~~~~~~~~~~~~~~~~~~~~~

Atom
++++

Use Atom to install the package `language-monte`__.

__ https://atom.io/packages/language-monte

.. note:: See also `tooling ideas`__ in the wiki.

__ https://github.com/monte-language/monte/wiki/Pipe-Dreams#tooling


.. rubric:: Notes

.. [#] Disciplined use of existing languages such as Java and
       JavaScript can be used to build object capability systems, but
       the standard practices and libraries are not compatible with
       this discipline.

.. [#] Miller, M.S.: `Robust Composition: Towards a Unified Approach to
       Access Control and Concurrency Control`__. PhD thesis, Johns
       Hopkins University, Baltimore, Maryland, USA (May 2006)

.. [#darpa] As documented in `the DarpaBrowser report
            <http://www.combex.com/papers/darpa-report/index.html>`_

__ http://erights.org/talks/thesis/index.html
