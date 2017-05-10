================================
Misuse-Resistant Language Design
================================

Several of Monte's design decisions are based on the concept of
*misuse-resistant* tools which are designed to frustrate attempts to write
faulty code, whether accidentally or intentionally.

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
