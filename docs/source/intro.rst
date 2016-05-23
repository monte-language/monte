Introduction
============

Why Monte?
----------

Don't we have enough languages already? This is a fair question.  Here we'll
explain why we created Monte and what's interesting about it.


Because Security Matters
~~~~~~~~~~~~~~~~~~~~~~~~

**Secure distributed computing should not be hard**. Computers are getting
faster, smaller, more connected, and more capable, but when it comes to
security, `everything is broken`__. We propose to reconsider the
identity-based access control approach dominant in today's dominant languages
and frameworks [#]_. Monte takes the object-capability paradigm of E [#]_ and
updates it for the metamodern era:

__ https://medium.com/message/everything-is-broken-81e5f33a24e1

Monte, like E before it, has dramatic advantages for secure distributed
systems:

   - Monte promises benefit from a *promise-pipelining* architecture which
     ensures that *most deadlocks cannot occur*. [*]_

   - Monte offers cryptographic services directly to its users, easing the use
     of good cryptographic primitives.

   - Capability-based security enables the concise composition of powerful
     patterns of interoperation--patterns that enable extensive cooperation
     even in the presence of severely limited trust.


Because Readability Matters
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. sidebar:: The origin of Monte's name

   The Monte language has its roots in the E and Python languages. We
   took "Monty" from "Monty Python", and put an "e" in there. Thus,
   "Monte".

Monte wraps its strengths in a Python-like syntax to make it quickly
comfortable for a large number of software engineers.

Monte is a pure object-based language in the Smalltalk tradition.  making it
easy to write modular, readable, maintainable software using the strategies
familiar from Python, JavaScript, Ruby, Java, and other object-based
languages.  All values are objects and all computation is done by sending
messages to objects. It has the kind of powerful string handling that will be
recognized and seized upon by the Perl hacker.

Because Stability Matters
~~~~~~~~~~~~~~~~~~~~~~~~~

Monte is dynamically typed [#unityped]_, like Smalltalk, rather than
statically typed, like Java. Users of Perl and Python will immediately
recognize this is an advantage; Java and C++ programmers may not be so
sure. Fortunately, Monte inherits two forms of contract-based programming from
E: :ref:`guards<guards>` and :ref:`interfaces<interfaces>`.

Monte is dynamic in three ways:

Dynamic Typing
    The type of a variable might not be known until runtime, and "types are
    open".
Dynamic Binding
    It is possible to pass a message to an object that will never able to
    handle that message. This provides a late-binding sort of polymorphism.
Dynamic Compiling
    Monte can compile and run Monte code at runtime, as part of its core
    runtime.

While "arbitrary code execution" is a notorious security vulnerability, Monte
enables the fearless yet powerful use of multi-party limited-trust mobile
code.

.. _ocap:

Object Capability Discipline
----------------------------

A :dfn:`capability` is a reference to an object and represents authority to
invoke methods on the object. The key to supporting dynamic code execution
without vulnerability is :dfn:`object capability discipline`, which consists
of:

Memory safety and encapsulation
  There is no way to get a reference to an object except by creating one or
  being given one at creation or via a message; no casting integers to
  pointers, for example.

  From outside an object, there is no way to access the internal state of the
  object without the object's consent (where consent is expressed by
  responding to messages).
Primitive effects only via references
  The only way an object can affect the world outside itself is via references
  to other objects. All primitives for interacting with the external world are
  embodied by primitive objects and anything globally accessible is immutable
  data. There is no ``open(filename)`` function in the global namespace, nor
  can such a function be imported. The runtime passes all such objects to an
  :ref:`entrypoint<entrypoints>`, which then explicitly delegates to other
  objects.

We'll demonstrate how this leads to natural expression of the *Principle of
Least Power* briefly in :ref:`taste` and in more detail in
:ref:`secure_distributed_computing`.


Why not Monte?
--------------

Monte assumes automatic memory management; the current reference
implementation uses the PyPy garbage collector, and any other implementation
will have to choose a similar scheme. As such, it is not a good language for
low level machine manipulation. So do not try to use Monte for writing device
drivers.

Monte's performance is currently quite unfavorable compared to raw C, and
additionally, Monte's target niches are largely occupied by other dynamic
languages with JIT-compiler-based runtimes, so it is not a design goal to
compete with C or other memory-unsafe languages.

.. note:: While Monte's usable and most architectural issues are resolved, it
          is still undergoing rapid development. See :ref:`roadmap` for
          details.


Getting Started
---------------

Installation: Docker Image (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: docker image via nix (`#77`__)
          Meanwhile, see `Getting Started`__
          in the Monte wiki.

__ https://github.com/monte-language/typhon/issues/77
__ https://github.com/monte-language/monte/wiki/Getting-Started


Interacting with the Monte REPL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Monte has a traditional "Read - Evaluate - Print Loop", or REPL, for
exploration. Invoke it as `mt repl`. For example::

  >>> 1 + 1
  2

  >>> "abc".size()
  3


Getting Help about an Object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Monte strives to provide useful error messages and self-documenting objects::

  ▲> help(Ref)
  Result: Object type: RefOps
  Ref management and utilities.
  Method: broken/1
  Method: isBroken/1
  Method: isDeepFrozen/1
  ...


Editor Syntax Highlighting
~~~~~~~~~~~~~~~~~~~~~~~~~~

Emacs and Flycheck
++++++++++++++++++

The `monte-emacs repository`__ provides emacs syntax highlighting
on-the-fly syntax checking with flycheck__.

__ https://github.com/monte-language/monte-emacs
__ http://www.flycheck.org/


Vim
+++

The `monte-vim repository`__ provides vim syntax highlighting, and linter
integration is available via a private `Syntastic repository`__.

__ https://github.com/monte-language/monte-vim

__ https://github.com/mostawesomedude/syntastic


Atom
++++

Use Atom to install the package `language-monte`__.

__ https://atom.io/packages/language-monte


Support and Feedback
~~~~~~~~~~~~~~~~~~~~

We welcome feedback:
  - `issues in monte pypy vm implementation (typhon)`__
  - `issues in monte documentation`__

Or come say hi on IRC, in `#monte` on `irc.freenode.net`!

__ https://github.com/monte-language/monte/issues
__ https://github.com/monte-language/typhon/issues


Acknowledgements
----------------

Monte design and documentation borrow heavily from `E in a Walnut`__
by Marc Stiegler and `The E Language`__ and `ELib`__ by Mark Miller.

__ http://wiki.erights.org/wiki/Walnut
__ http://erights.org/elang/index.html
__ http://erights.org/elib/index.html

.. rubric:: Notes

.. [#] Disciplined use of existing languages such as Java and
       JavaScript can be used to build object capability systems, but
       the standard practices and libraries are not compatible with
       this discipline.

.. [#] Miller, M.S.: `Robust Composition: Towards a Unified Approach to
       Access Control and Concurrency Control`__. PhD thesis, Johns
       Hopkins University, Baltimore, Maryland, USA (May 2006)

       See also `a history of E's ideas`__.

.. [*] As with all sufficiently complex concurrency systems, deadlock is
       possible. That said, it has not been observed outside of
       specially-constructed pathological object graphs.


.. [#unityped] in formal type theory, Monte is `unityped`.

__ http://erights.org/talks/thesis/index.html
__ http://www.erights.org/history/index.html
