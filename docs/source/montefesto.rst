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

  * ✓ Why Monte exists
  * ✓ How to get started using Monte

* Have stories for:

  * ✓ Developing modular Monte codebases

* Finish key language features

  * ✓ Streamcaps
  * ✓ Vats

* Finish key integration features

  * Initial IDE support

    * ✓ vim (Corbin)
    * ✓ emacs (Allen)
    * ✓ Sublime/Atom (Mike, Justin)

2017
====

* Make Monte desireable

  * ✓ Branding
  * ✓ Object capability community outreach

* Improve the core

  * ✓ Speed: Nobody should have to wait for code to compile
  * Safe objects

    * ✓ Many method improvements to builtin collections
    * ✓ Semitransparent
    * ✓ Vow

  * Unsafe objects

    * ✓ Timers
    * ✓ Property tests

  * Typhon-specific improvements

    * ✓ Even faster interpreting

* Develop important libraries

  * ✓ HTTP
  * ✓ Records

* Monte-related R&D

  * ✓ Capn Proto

2018
====

* Advanced safe objects

  * PassByCopy
  * makeWeakMap
  * Twines
  * Elusive Eight: Useful numerical analysis methods for doubles

* Production-ready unsafe objects

  * FS
  * Tamed timers

  * Typhon-specific improvements

    * Even faster interpreting

* Develop Monte packaging

  * ✓ Muffins
  * Packages
  * Environments
  * mtpkgs

* Develop important libraries

  * Debugger
  * Pretty-printers

* Monte-related R&D

  * Rationals
  * Capn Proto: Message generation, CapTP/VatTP
  * kubeless integration

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
trackers. It's also worth grepping for ``TODO`` in the source of both
projects. 

.. _Monte: https://github.com/monte-language/monte/issues
.. _Typhon: https://github.com/monte-language/typhon/issues
.. _Python: https://docs.python.org/2/tutorial/
.. _E: http://www.skyhunter.com/marcs/ewalnut.html
.. _repo: https://github.com/monte-language/monte
.. _pastebin: https://bpaste.net/
