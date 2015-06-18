==========
Montefesto
==========

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
  * Named arguments
  * m``
  * Bytes
  * Finalize on-disk (on-wire) compiled code format
  * printer features
  * Tubes
  * Auditors
  * Farrefs
  * Arity overloading deprecation

* Finish key runtime features

  * Decide whether key C/etc. libraries should be bound and exposed (unsafely)
    to user-level code:

    * libsodium
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

    * Time
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
