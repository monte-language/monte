.. _roadmap:

===================
Roadmap: Montefesto
===================

.. epigraph::

    .ia lo snura faircu'u kanji ka'e na'e nandu ("Secure distributed computation should not be hard.")

    -- Corbin, on Monte

This is the roadmap for Monte development according to Allen and Corbin. If
you want to work on anything on this list, let us know; we're very accepting
of new contributors.

2015
====

* Finish key language features

  * ✓ Named arguments
  * ✓ m``
  * ✓ Bytes
  * ✓ Finalize on-disk (on-wire) compiled code format
  * ✓ Auditors

* Finish key runtime features

  * Expose key C libraries to user-level code

    * ✓ libsodium
    * ✓ libuv

* Finish key compiler features

  * ✓ Compiler error messages are informative

* Finish key integration features

  * Profiling

    * ✓ Time (vmprof)

2016
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
  * Printer features
  * Tubes
  * Farrefs
  * Arity overloading deprecation?

* Finish key compiler features

  * The compiler should be much faster. Concrete goal: Compile a single Monte
    module of at least 2KLoC within 500ms on a typical reference machine
    (two-core laptop circa 2012.)
  * While proving the compiler correct would be arduous, it should certainly
    be more solid than it currently is.

* Finish key integration features

  * Debugger
  * IDE support

    * vim (Corbin)
    * emacs (Allen)
    * sublime/atom (Mike, Justin)

  * Profiling

    * Space
    * Coverage
    * Turns
    * Vats
    * IPC/Networking

2017
====

We currently don't know what we're going to do for 2017. Possibilities range
from MonteCon to The Monte Foundation to nothing at all. Who knows? It is a
mystery~

Contributing
============

If you'd like to get involved with developing or using the Monte language,
start by getting in touch with us on IRC. It is useful, but not necessary, to
be acquainted with Python_'s syntax and/or the computational concepts of E_.

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
