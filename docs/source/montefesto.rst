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

* Develop Monte packaging

  * ✓ Muffins

2019
====

* Develop important libraries

  * ✓ Pretty-printers

* Monte-related R&D

  * ✓ Rationals
  * ✓ Capn Proto: Message generation, RPC primitives
  * ✓ kubeless integration

2020
====

Everybody was on vacation.

* ✓ Elusive Eight: Useful numerical analysis methods for doubles (Typhon 212_)
* ✓ Muffins: Package-to-module compilation toolchain
* ✓ CapTP on AMP_

  * ✓ Ampoule_, but in Monte: Process pooling for multicore distributed workloads

.. _212: https://github.com/monte-language/typhon/issues/212
.. _AMP: https://amp-protocol.net/
.. _Ampoule: https://github.com/twisted/ampoule

2021
====

* Iterate the bootstrap and turn over the compost heap:

  * Migrate from montec to tools/muffin,
  * Switch from interpreted prelude to compiled-in/tree-shaken prelude,
  * Build out lib/mim as an alternative to lib/monte,
  * Iterate the Typhon low-level module loader (loader.mt_)

  * Issue to be filed pending resolution of dependencies

    * There are like a dozen relevant open issues

* Monte, but native: Implement ENative_ by
  compiling to C with Cello_

  * Issue to be filed pending resolution of obvious pun problems with
    nomenclature

* makeWeakMap: Safe maker of weakref-keyed maps (Typhon 128_)
* User package repositories

  * Issue to be filed pending resolution of scope

    * Not PyPI
    * Not NPM
    * Not Cargo
    * Not go get
    * Not AUR

      * Maybe NUR

* CapTP over `Capn Proto RPC`_

  * Issue to be filed pending resolution of dependencies

    * Typhon 220_ is a hard blocker

.. _128: https://github.com/monte-language/typhon/issues/128
.. _220: https://github.com/monte-language/typhon/issues/220
.. _Capn Proto RPC: https://capnproto.org/rpc.html
.. _Cello: http://libcello.org/
.. _ENative: http://erights.org/enative/
.. _loader.mt: https://github.com/monte-language/typhon/blob/master/mast/loader.mt

Bonus Content
=============

These are projects that we'd like to prioritize, but they either involve
unbelievable amounts of work, or we don't know how to do them. In either case,
come chat on IRC and we can probably figure out how to make progress.

* Twines: String-like objects with embedded span information
* Pass-by-copy construction semantics for CapTP
* Better filesystem APIs
* Better timer APIs
* virtualenvs, but for Monte
* Line-by-line debugging
* Expression-by-expression debugging

Contributing
============

If you'd like to get involved with developing or using the Monte language,
start by getting in touch with us on IRC. It is useful, but not necessary, to
be acquainted with Python_'s syntax and/or the computational concepts of E_.

Then clone the repo_ and follow the `installation instructions`_ to begin
running Monte code. If you have problems, join us in #monte on
irc.freenode.net, ask your question (use a pastebin_ to share any errors,
rather than pasting into the channel), and wait a few hours if nobody is
around.

If you'd like to contribute to Monte, check out the Monte_ and Typhon_ issue
trackers. It's also worth grepping for ``TODO`` in the source of both
projects. 

.. _E: http://www.skyhunter.com/marcs/ewalnut.html
.. _Monte: https://github.com/monte-language/monte/issues
.. _Python: https://docs.python.org/2/tutorial/
.. _Typhon: https://github.com/monte-language/typhon/issues
.. _installation instructions: https://monte.readthedocs.io/en/latest/intro.html#getting-started
.. _pastebin: https://bpa.st/
.. _repo: https://github.com/monte-language/monte
