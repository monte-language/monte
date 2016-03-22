Introduction
============

Why Monte?
----------

Don't we have enough languages already? This is a fair question.  We
can only explain why Monte is interesting to us and leave you to
judge.


Because Security Matters
~~~~~~~~~~~~~~~~~~~~~~~~

Because **secure distributed computing should not be hard**. Computers
are getting faster, smaller, more connected, and more capable, but
when it comes to security, `everything is broken`__. We propose to
reconsider the identity-based access control approach dominant in
today's dominant languages and frameworks [#]_. Monte takes the
object-capability paradigm of E [#]_ and updates it for the metamodern
era:

__ https://medium.com/message/everything-is-broken-81e5f33a24e1

.. sidebar:: Object Capabilities

   Monte inherits from E a specific flavor of capability-based security known
   as object capabilities. With object capabilities, capability-oriented
   programming has the same flavor as object-oriented programming, except that
   capability-oriented programming takes the usual object-oriented constraints
   more seriously. Often when using object capabilities for security, one
   finds that a more secure program is simply a program that follows
   object-oriented principles of modularization more closely.

- Monte, like E before it, has dramatic advantages for secure distributed
  systems.

   - Monte promises benefit from a *promise-pipelining* architecture which
     ensures that *most deadlocks cannot occur*. [*]_

   - Monte offers cryptographic services directly to its users, easing the use
     of good cryptographic primitives.

   - Capability-based security enables the concise composition of powerful
     patterns of interoperation, patterns that enable extensive cooperation
     even in the presence of severely limited trust.

   - The fractal nature of POLA encourages short and readable modules, leading
     to applications having relatively low amounts of code. As a consequence,
     the attack surface of an application is decreased and code review is
     easier. The implementors of E and CapDesk boast of implementing
     peer-to-peer chat systems and digital-money bank servers in hundreds,
     *not* tens of thousands, of lines of code.

     When the time comes for a security inspection, capability security allows
     simple reachability analysis to exclude huge swaths of code because they
     cannot embody a threat. As a consequence, auditing a system for security
     becomes cost-effective to an extent that is simply unimaginable with
     other approaches [#darpa]_.

   - With Monte, it is straightforward to create systems that run across the
     Internet that are as secure and safe as if the entire system were running
     on a single computer in your basement. As one of the original developers
     of Smalltalk observed, upon learning about the object-capability paradigm
     from E, capability security is "natural security": if you shouldn't use
     it, you just can't see it.

- Monte enables the fearless yet powerful use of multi-party
  limited-trust mobile code, as we shall discuss in the chapter on
  :ref:`secure-distributed-computing`.

.. [*] As with all sufficiently complex concurrency systems, deadlock is
       possible. That said, it has not been observed outside of
       specially-constructed pathological object graphs.


Because Readability Matters
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. sidebar:: The origin of Monte's name

   The Monte language has its roots in the E and Python languages. We
   took "Monty" from "Monty Python", and put an "e" in there. Thus,
   "Monte".

Monte wraps its strengths in a Python-like syntax to make it quickly
comfortable for a large number of software engineers. It is built with objects
at the core of its design, making it easy to write modular, readable,
maintainable software using the strategies familiar from Python, JavaScript,
Ruby, Java, and other object-based languages. It has the kind of powerful
string handling that will be recognized and seized upon by the Perl
hacker.

Because Stability Matters
~~~~~~~~~~~~~~~~~~~~~~~~~

Monte is dynamically typed, like Smalltalk, and not statically typed, like
Java. Users of Perl and Python will immediately recognize this is an
advantage; Java and C++ programmers may not be so sure. Fortunately, Monte has
a novel type system based heavily on guard syntax from E, which permits type
annotations to be as precise as desired while still permitting extreme
customization in type complexity. Additionally, dedicated syntax for interface
declarations enables contract-based programming.

Why not Monte?
--------------

.. note:: While Monte's usable and most architectural issues are resolved, it
          is still undergoing rapid development. See :ref:`roadmap` for
          details.

Monte assumes automatic memory management; the current reference
implementation uses the PyPy garbage collector, and any other implementation
will have to choose a similar scheme. As such, it is not a good language for
low level machine manipulation. So do not try to use Monte for writing device
drivers.

Monte's performance is currently quite unfavorable compared to raw C, and
additionally, Monte's target niches are largely occupied by other dynamic
languages with JIT-compiler-based runtimes, so it is not a design goal to
compete with C or other memory-unsafe languages.

Preface to Monte Documentation
------------------------------

We begin with an introduction to practical Monte programming. Comparisons
to Python are frequent, so some understanding of Python is desirable.

Later sections form the :ref:`spec` and the :ref:`stdlib`.

This largely follows the structure of `E in a Walnut`__ by Marc Stiegler
and `The E Language`__ and `ELib`__ by Mark Miller.

We welcome feedback:
  - `issues in monte pypy vm implementation (typhon)`__
  - `issues in monte documentation`__

Or come say hi on IRC, in `#monte` on `irc.freenode.net`!

__ http://wiki.erights.org/wiki/Walnut
__ http://erights.org/elang/index.html
__ http://erights.org/elib/index.html
__ https://github.com/monte-language/monte/issues
__ https://github.com/monte-language/typhon/issues


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
