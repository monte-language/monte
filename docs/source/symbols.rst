Primitive Data Types
====================

Scalars
-------

Monte provides some classic and common value types.

Int
~~~

Monte integer literals are written as usual::

  >>> 5
  5

  >>> 0xF
  15

Integers may be arbitrarily large (a la python long)::

  >>> 128 ** 20
  1393796574908163946345982392040522594123776

A variety of mathematical methods are available::

  ▲> help(5)
  Result: Object type: IntObject
  A numeric value in ℤ.
  Method: op__cmp/1
  Method: aboveZero/0
  Method: atLeastZero/0
  ...

  >>> 5 < 2
  false


Double
~~~~~~

Monte has floating point numbers as well::

  ▲> help(1.2)
  Result: Object type: DoubleObject
  A numeric value in ℝ, with IEEE 754 semantics and at least double
  precision.
  Method: op__cmp/1
  Method: abs/0
  Method: add/1
  ...

Note that integers do not automatically coerce to doubles::

  ▲> def x :Double := 1
  ...
  Parse error: [Failed guard (Double):, 1]

  >>> def x :Double := 1.0
  1.000000

To convert::

  >>> 4.0.floor()
  4

  >>> 4 * 1.0
  4.000000

Char
~~~~

Monte's character type represents unicode characters; it is distinct
from the string type. Character literals are always delimited by
apostrophes (``'``).

.. warning::

    In Python, you may be accustomed to 'single' and "double" quotes
    functioning interchangeably. In Monte, double quotes can contain any
    number of letters, but single quotes can only hold a single character. 

Characters are permitted to be adorable::

  >>> '☃'
  '☃'
  >>> '\u23b6'
  '⎶'


Collections
-----------

Monte has native lists and maps, as well as various other data structures
implemented in the language.

String
~~~~~~

Strings are objects with built-in methods and capabilities, rather than
character arrays. Monte's strings are always unicode, like Python 3 (but
unlike Python 2). String literals are always delimited by
double-quotes (``"``)::

    >>> "Hello World!".replace("World", "Monte hackers")
    "Hello Monte hackers!"
    >>> "¿Dónde aquí habla Monte o español?".size()
    34


String Escapes
++++++++++++++

Monte has string escape syntax much like python or Java:

+-----------------+---------------------------------+
| Escape Sequence | Meaning                         |
+=================+=================================+
| ``\\``          | Backslash (``\``)               |
+-----------------+---------------------------------+
| ``\'``          | Single quote (``'``)            |
+-----------------+---------------------------------+
| ``\"``          | Double quote (``"``)            |
+-----------------+---------------------------------+
| ``\b``          | ASCII Backspace (BS)            |
+-----------------+---------------------------------+
| ``\f``          | ASCII Formfeed (FF)             |
+-----------------+---------------------------------+
| ``\n``          | ASCII Linefeed (LF)             |
+-----------------+---------------------------------+
| ``\r``          | ASCII Carriage Return (CR)      |
+-----------------+---------------------------------+
| ``\t``          | ASCII Horizontal Tab (TAB)      |
+-----------------+---------------------------------+
| ``\uxxxx``      | Character with 16-bit hex value |
|                 | *xxxx* (Unicode only)           |
+-----------------+---------------------------------+
| ``\Uxxxxxxxx``  | Character with 32-bit hex value |
|                 | *xxxxxxxx* (Unicode only)       |
+-----------------+---------------------------------+
| ``\xhh``        | Character with hex value *hh*   |
+-----------------+---------------------------------+

(table mostly from `the Python docs <https://docs.python.org/2/_sources/reference/lexical_analysis.txt>`_)

.. note:: 

    Monte intentionally avoids providing escape notation for ASCII vertical
    tabs (``\v``) and octal values (``\o00``) because it is a language of the
    future and in the future, nobody uses those. Hexadecimal escapes are still
    valid for vertical tabs.

.. note::

    As with Python, a backslash (``\``) as the final character of a line
    escapes the newline and causes that line and its successor to be
    interpereted as one.

Lists: ConstList and FlexList
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Among Monte's collection types, the list is a very common type. Lists are
heterogenous ordered unsorted collections with sequencing and indexing, and
have the performance characteristics of arrays in C, vectors in C++, or lists
in Python::

  >>> ['I', "love", "Monte", 42, 0.5][3]
  42

A list expression evaluates to a ``ConstList``::

  ▲> { def l := ['I', "love", "Monte", 42, 0.5]; l[3] := 0 }
  ...
  Message refused: ([I, love, Monte, 42, 0.500000], Atom(put/2), [3, 0])

Use ``diverge`` and ``snapshot`` to go from ``ConstList`` to mutable
``FlexList`` and back::

  >>> { def l := ['I', "love", "Monte", 42, 0.5].diverge(); l[3] := 0 }
  0

Maps: ConstMap and FlexMap
~~~~~~~~~~~~~~~~~~~~~~~~~~

Monte uses the "fat arrow", ``=>`` for map syntax::

  >>> { def m := ["roses" => "red", "violets" => "blue"]; m["roses"] }
  "red"

.. todo:: output of repl should be quoted like this.

.. todo:: handle multi-line REPL examples when generating tests

Like list expressions, a map expressions evaluates to an immutable
data structures, a ``ConstMap``::

  ▲> { def m := ["roses" => "red", "violets" => "blue"]; m["roses"] := 3 }
  ...
  Message refused: ([roses => red, violets => blue], Atom(put/2), ["roses", 3])

Use ``diverge`` and ``snapshot`` similarly::

  >>> { def m := ["roses" => "red", "violets" => "blue"].diverge(); m["roses"] := 3 }
  3

.. warning:: Maps in monte are ordered::

               >>> [ "a" => 1, "b" => 2] == [ "b" => 2, "a" => 1]
               false

             To compare without regard to order, use ``sortKeys``::

               >>> [ "a" => 1, "b" => 2].sortKeys() == [ "b" => 2, "a" => 1].sortKeys()
               true

Syntax Summary
--------------

.. note:: Lexical details of monte syntax are currently specified
	  only by implementation; see `lib/monte/monte_lexer.mt`__

__ https://github.com/monte-language/typhon/blob/master/mast/lib/monte/monte_lexer.mt

.. syntax:: Literal

   Choice(0,
     ".int.", ".float64.", ".char.", ".String.",
     Sequence("[", ZeroOrMore(NonTerminal('expr'), ','), "]"),
     Sequence("[", ZeroOrMore(Sequence(NonTerminal('expr'),
                                       "=>", NonTerminal('expr')), ','), "]"))
