Simple expressions
==================

Expressions evaluate to objects and definitions bind objects to names::

  ▲> { def x := 2; x * x }
  Result: 4

Built-in Object Types
---------------------

Monte provides some classic and common value types.

Int
~~~

Monte integer literals are written as usual:

.. code-block:: monte

    def x := 5
    def x := 128 ** 128 ** 128

Integers may be arbitrarily large (a la python long). A variety of
mathematical methods are available::

  ▲> help(5)
  Result: Object type: IntObject
  A numeric value in ℤ.
  Method: op__cmp/1
  Method: aboveZero/0
  Method: atLeastZero/0
  ...

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

  ▲> def x :Double := 1.0
  Result: 1.000000

To convert::

  ▲> 4.0.floor()
  Result: 4

  ▲> 4 * 1.0
  Result: 4.000000

Char
~~~~

Monte's character type represents unicode characters; it is distinct
from the string type. Character literals are always delimited by
apostrophes (``'``).

.. code-block:: monte

    def u := '☃'

Characters are permitted to be adorable.

.. warning:: 

    In Python, you may be accustomed to 'single' and "double" quotes
    functioning interchangeably. In Monte, double quotes can contain any
    number of letters, but single quotes can only hold a single character. 

Structured Types
----------------

Monte has native lists and maps, as well as various other data structures
implemented in the language.

String
~~~~~~

Strings are objects with built-in methods and capabilities, rather than
character arrays. Monte's strings are always unicode, like Python 3 (but
unlike Python 2). String literals are always delimited by
double-quotes (``"``).

.. code-block:: monte

    def s := "Hello World!"
    def t := s.replace("World", "Monte hackers") # Hello Monte hackers!
    def u := "¿Dónde aquí habla Monte o español?"

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

  ▲> { def l := ['I', "love", "Monte", 42, 0.5]; l[3] }
  Result: 42

A list expression evaluates to a ``ConstList``::

  ▲> { def l := ['I', "love", "Monte", 42, 0.5]; l[3] := 0 }
  ...
  Message refused: ([I, love, Monte, 42, 0.500000], Atom(put/2), [3, 0])

Use ``diverge`` and ``snapshot`` to go from ``ConstList`` to mutable
``FlexList`` and back::

  ▲> { def l := ['I', "love", "Monte", 42, 0.5].diverge(); l[3] := 0 }
  Result: 0

Maps: ConstMap and FlexMap
~~~~~~~~~~~~~~~~~~~~~~~~~~

Monte uses the "fat arrow", ``=>`` for map syntax::

  ▲> { def m := ["roses" => "red", "violets" => "blue"]; m["roses"] }
  Result: red

Like list expressions, a map expressions evaluates to an immutable
data structures, a ``ConstMap``::

  ▲> { def m := ["roses" => "red", "violets" => "blue"]; m["roses"] := 3 }
  ...
  Message refused: ([roses => red, violets => blue], Atom(put/2), ["roses", 3])

Use ``diverge`` and ``snapshot`` similarly::

  ▲> { def m := ["roses" => "red", "violets" => "blue"].diverge(); m["roses"] := 3 }
  Result: 3

.. warning:: Maps in monte are ordered::

               ▲> [ "a" => 1, "b" => 2] == [ "b" => 2, "a" => 1]
               Result: false

             To compare without regard to order, use ``sortKeys``::

               ▲> [ "a" => 1, "b" => 2].sortKeys() == [ "b" => 2, "a" => 1].sortKeys()
               Result: true

Comments
--------

This is a single-line comment::

    # Lines starting with a # are single-line comments.
    # They only last until the end of the line.

And this is a multi-line comment::

    /** This comment is multi-line.
        Yes, it starts with two stars,
        but ends with only one.
        These should only be used for docstrings. */

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

examples::

  1
  0x1
  1.0
  'a'
  '\u23b6'
  "some unicode text"
  [1, 2, 'x']
  [1 => 'a', 2 => "b"]

.. syntax:: noun

   Choice(0, "IDENTIFIER", Sequence("::", ".String."))

examples::

  foo
  __equalizer
  ::"hello, world"

.. index: Unary operators

.. syntax:: prefix

   Choice(
    0,
    NonTerminal('unary'),
    NonTerminal('SlotExpression'),
    NonTerminal('BindingExpression'),
    Sequence(NonTerminal('call'), Optional(NonTerminal('guard'))))

.. seealso::

   :ref:`message_passing`

.. syntax:: unary

   Choice(
    0,
    Sequence('-', NonTerminal('prim')),
    Sequence(Choice(0, "~", "!"), NonTerminal('call')))

.. syntax:: SlotExpression

   Sequence('&', NonTerminal('noun'))

.. todo:: discuss, doctest SlotExpression ``&x``

.. syntax:: BindingExpression

   Sequence('&&', NonTerminal('noun'))

.. todo:: discuss, doctest BindingExpression ``&&x``

.. index:: Indexing

.. syntax:: getExpr

   Sequence(
    NonTerminal('calls'),
    Sequence("[", ZeroOrMore(NonTerminal('expr'), ','), "]"))

.. syntax:: curry

   Sequence(
    Choice(0, '.', '<-'),
    Choice(0, "IDENTIFIER", ".String."))

.. syntax:: prim

   Choice(
    0,
    NonTerminal('Literal'),
    NonTerminal('quasiliteral'),
    NonTerminal('noun'),
    Sequence("(", NonTerminal('expr'), ")"),
    Sequence("{", ZeroOrMore(NonTerminal('expr'), ';'), "}"),
    Sequence("[",
             "for", NonTerminal('comprehension'),
             "]"))

.. seealso::

   :ref:`quasiliteral <quasiliteral>`,
   :ref:`comprehension <comprehension>`

.. todo:: figure out how to make the quasiliteral, comprehension links work
