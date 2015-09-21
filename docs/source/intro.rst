Introduction
============

What's Monte?
-------------

Monte is a high-level programming language whose design philosophy is
that **secure distributed computing should not be hard**. It provides
much of the expressive convenience of python but also robust
composition using object capabilities in the tradition of E [#]_.

.. note:: While Monte usable and most architectural issues are
	  resolved, it is still undergoing rapid development.
	  See :ref:`roadmap` for details.

.. sidebar:: The origin of Monte's name

   The Monte language has its roots in the E and Python languages. We
   took "Monty" from "Monty Python", and put an "e" in there. Thus,
   "Monte".


Why Monte?
----------

Because `everything is broken`__. Python has great usability, borne
out by a large developer community, but it shares a fundamentally
brittle architecture with much of today's programming languages and
platforms: *insecurity anywhere is a threat to security everywhere*.
While E is comparatively obscure, its object capability discipline
naturally supports the *principle of least authority* so that
malicious or faulty code in one part of a system is straightforwardly
contained. Monte provides the robust composition features of E
in a form that's convenient to the Python developer community.

__ https://medium.com/message/everything-is-broken-81e5f33a24e1

A Taste of Monte
----------------

Let's compose a simple web server from a main program and a handler:

.. literalinclude:: tut/web1mt
    :linenos:
    :language: monte

The basics of defining functions and calling methods should be
familiar to anyone with exposure to python or even ruby or the C/C++
family (Java, JavaScript, PHP).

.. note:: You can read the ``smallBody`` import as: ``from
	  lib.http.resource import smallBody`` and likewise for the
	  others. See :ref:`modules` and :ref:`patterns` for details.

The powerful objects `currentProcess` and `makeTCP4ServerEndpoint` are
provided explicitly to the main function. Unless these powerful
objects are passed explicitly to other code (such as the various
library modules) executing it can do nothing more than create objects
(including functions) in memory. It cannot write to files [#]_, access
the network, clobber global state, or launch missiles.

Only when access to make an HTTP endpoint is passed to start() can
this code interact with the network. And by inspection of
`makeWebServer()`, we can see that it can only use the HTTP protocol,
and only on the port given by the last command-line argument.

.. todo:: rewrite the two previous paragraphs.

This aspect of monte's design is discussed further in :ref:`ocap`.

.. todo:: use new `main(=> makeTCP4ServerEndpoint)` idiom (`issue 33`__).

__ https://github.com/monte-language/typhon/issues/33


Getting Started
---------------

.. note:: Installing monte is in transition. The original python
	  implementation in the monte repository is largely obsolete
	  in favor of typhon.  See :ref:`roadmap` and the `monte
	  wiki`__ for more.

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


.. _trace:

Diagnostics, Documentation, and Debugging
-----------------------------------------

Monte strives to provide useful error messages and self-documenting objects::

  ▲> help(Ref)
  Result: Object type: RefOps
  Ref management and utilities.
  Method: broken/1
  Method: isBroken/1
  Method: isDeepFrozen/1
  ...

Currently the most convenient way to print out messages from your program is
with the ``trace()`` and ``traceln()`` built-in functions. The only difference
between them is that ``traceln()`` automatically adds a newline.

.. rubric:: Notes

.. [#] Miller, M.S.: `Robust Composition: Towards a Unified Approach to
       Access Control and Concurrency Control`__. PhD thesis, Johns
       Hopkins University, Baltimore, Maryland, USA (May 2006)

.. [#] As a practical concession, the safe scope includes ``trace()``
       and ``traceln()``. See :ref:`trace`.

__ http://erights.org/talks/thesis/index.html
