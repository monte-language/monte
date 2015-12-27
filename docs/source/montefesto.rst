.. _roadmap:

===================
Roadmap: Montefesto
===================

.. epigraph::

    Secure distributed computation should not be hard.

    -- Corbin, on Monte

This is the roadmap for Monte development according to Allen and Corbin. If
you want to work on anything on this list, let us know; we're very accepting
of new contributors.

2015
====

* "Exit stealth mode"; display a sleek and friendly front page to neophytes
  and visitors which explains:

  * Why Monte exists
  * What Monte can do
  * How to get started using Monte
  * Licensing and code reuse policies
  * Monte branding

* Have stories for:

  * Writing high-performance Monte code
  * Debugging faulty Monte code
  * Writing large-scale Monte code
  * Developing modular Monte codebases

* Finish key language features

  * Records
  * ✓ Named arguments
  * ✓ m``
  * ✓ Bytes
  * Finalize on-disk (on-wire) compiled code format
  * printer features
  * Tubes
  * ✓ Auditors
  * Farrefs
  * Arity overloading deprecation

* Finish key runtime features

  * Decide whether key C/etc. libraries should be bound and exposed (unsafely)
    to user-level code:

    * libsodium
    * ✓ libuv
    * sqlite

* Finish key compiler features

  * The compiler should be much faster. Concrete goal: Compile a single Monte
    module of at least 2KLoC within 500ms on a typical reference machine
    (two-core laptop circa 2012.)
  * While proving the compiler correct would be arduous, it should certainly
    be more solid than it currently is.
  * Compiler error messages are currently completely lost. This is not what we
    wanted.

* Finish key integration features

  * Debugger
  * IDE support

    * vim (Corbin)
    * emacs (Allen)
    * sublime/atom (Mike?)

  * Profiling

    * ✓ Time (vmprof)
    * Space
    * Coverage
    * Turns
    * Vats
    * IPC/Networking

2016
====

We currently don't know what we're going to do for 2016. Possibilities range
from MonteCon to The Monte Foundation to nothing at all. Who knows? It is a
mystery~

Contributing
============

If you'd like to get involved with developing or using the Monte language,
start by getting acquainted with Python_'s syntax and the computational
concepts of E_. 

Then clone the repo_ and follow the directions below to begin running Monte
code. If you have problems, join us in #monte on irc.freenode.net, ask your
question (use a pastebin_ to share any errors, rather than pasting into the
channel), and wait a few hours if nobody is around. 

If you'd like to contribute to Monte, check out the Monte_ and Typhon_ issue
trackers and the `pipe dreams`_ wiki page. It's also worth grepping for
``TODO`` in the source of both projects. 

.. _Monte: https://github.com/monte-language/monte/issues
.. _Typhon: https://github.com/monte-language/typhon/issues
.. _pipe dreams: https://github.com/monte-language/monte/wiki/Pipe-Dreams
.. _Python: https://docs.python.org/2/tutorial/
.. _E: http://www.skyhunter.com/marcs/ewalnut.html
.. _repo: https://github.com/monte-language/monte
.. _pastebin: https://bpaste.net/


Using Monte
===========

.. warning:: This section largely obsolete. The `monte wiki`__ may
             have more up-to-date info.

__ https://github.com/monte-language/monte/wiki

To use the Monte implementation hosted in Python, it's best to set up a
virtualenv:

.. code-block:: console

    $ virtualenv v
    $ source v/bin/activate
    $ pip install -r requirements.txt

To run Monte code (with your virtualenv activated):

.. code-block:: console

    $ bin/monte monte/src/examples/hello.mt

