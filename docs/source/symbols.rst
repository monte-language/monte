Lexical Grammar (Tokens) (WIP)
==============================

.. _primitive-data:

.. todo:: separate discussion of expression syntax from datatypes.

Scalars
-------

Monte provides some classic and common value types [#e_scalars]_.

Int
~~~

.. syntax:: IntExpr

   Ap('IntExpr', Choice(0, P('hexLiteral'), P('decLiteral')))

.. syntax:: decLiteral

   Ap('(read :: String -> Integer)', P('digits'))

.. syntax:: digits

   Ap("filter ((/=) '_')",
     Ap('(:)', P('digit'), Many(Choice(0, P('digit'), Char('_')))))

.. syntax:: digit

   OneOf('0123456789')

.. syntax:: hexLiteral

   Ap('(read :: String -> Integer)',
     Ap('(:)', Char('0'),
       Ap('(:)', Choice(0, Char('x'), Char('X')), P('hexDigits'))))

.. syntax:: hexDigits

   Ap("filter ((/=) '_')",
     Ap('(:)', P('hexDigit'), Many(Choice(0, P('hexDigit'), Char('_')))))

.. syntax:: hexDigit

   OneOf('0123456789abcdefABCDEF')


Monte integer literals are written as usual::

  >>> 5
  5

  >>> 0xF
  15

Integers may be arbitrarily large, *à la* Python's `long` or Haskell's
`Integer`::

  >>> 128 ** 20
  1393796574908163946345982392040522594123776

Integers respond to a variety of mathematical methods,
and :ref:`operators<operators>` provide traditional syntax::

  ▲> help(5)
  Result: Object type: IntObject
  A numeric value in ℤ.
  Method: op__cmp/1
  Method: aboveZero/0
  ...
  Method: add/1
  ...

  >>> 5 + 2
  7

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

.. syntax:: DoubleExpr

   Ap('DoubleExpr', P('floatLiteral'))

.. syntax:: floatLiteral

   Ap('(read :: String -> Double)',
     Ap('(++)',
       P('digits'),
       Choice(0,
         Ap('(++)',
           Ap('(:)', Char('.'), P('digits')),
           Optional(P('floatExpn'), x='""')),
         P('floatExpn'))))

.. syntax:: floatExpn

   Ap('(:)',
     OneOf("eE"),
     Ap('(++)',
       Optional(Ap('pure', OneOf('-+')), x='""'),
       P('digits')))


Bool
~~~~

There are only two boolean values, known as `true` and `false`. Here
are the applicable operators in precedence order.

Logical Or::

  >>> false || true
  true

Evaluates left to right until it finds a true condition.

  >>> {((1 =~ x) || (2 =~ x)); x}
  1
  >>> {((1 =~ [x, y]) || (2 =~ x)); x}
  2

Logical And::

  >>> false && true
  false

Boolean Comparisons (non-associative)::

  >>> false == true
  false

  >>> false != true
  true

  >>> false & true
  false

  >>> false | true
  true

  >>> false ^ true
  true

Unary::

  >>> ! false
  true

Expansions::

  >>> m`! false`.expand()
  m`false.not()`

  >>> m`false & true`.expand()
  m`false.and(true)`


Char
~~~~

Monte's character type represents Unicode characters; it is distinct
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

.. syntax:: CharExpr

   Ap('CharExpr',
     Brackets(Char("'"), P('charConstant'), Char("'")))

.. syntax:: charConstant

   Sigil(Many(String("\\\n")),
     Choice(0,
       NoneOf("'\\\t"),
       Sigil(Char("\\"),
         Choice(0,
           Ap('hexChar', Choice(0,
               Sigil(Char("U"), Count(8, P('hexDigit'))),
               Sigil(Char("u"), Count(4, P('hexDigit'))),
               Sigil(Char("x"), Count(2, P('hexDigit'))))),
           Ap('decodeSpecial', OneOf(r'''btnfr\'"'''))))))

@@TODO: test for '	' (tab) not allowed


Collections
-----------

Monte has native lists and maps, as well as various other data structures
implemented in the language.

String
~~~~~~

Strings are objects with built-in methods and capabilities, rather than
character arrays. Monte's strings are always Unicode, like Python 3 (but
unlike Python 2). String literals are always delimited by
double-quotes (``"``)::

    >>> "Hello World!".replace("World", "Monte hackers")
    "Hello Monte hackers!"
    >>> "¿Dónde aquí habla Monte o español?".size()
    34


String Escapes
++++++++++++++

Monte has string escape syntax much like Python or Java:

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
| ``\xhh``        | Character with 8-bit hex value  |
|                 | *hh* (Unicode code point)       |
+-----------------+---------------------------------+
| ``\uxxxx``      | Character with 16-bit hex value |
|                 | *xxxx* (Unicode code point)     |
+-----------------+---------------------------------+
| ``\Uxxxxxxxx``  | Character with 32-bit hex value |
|                 | *xxxxxxxx* (Unicode code point) |
+-----------------+---------------------------------+

(table mostly from `the Python docs <https://docs.python.org/2/_sources/reference/lexical_analysis.txt>`_)

.. warning::
    Monte intentionally avoids providing escape notation for ASCII vertical
    tabs (``\v``) and octal values (``\o00``). These are rare enough that we
    chose to omit them from the grammar. Hexadecimal escapes are still valid
    for vertical tabs; use ``\x0b``.

    .. epigraph::
        "Because [Monte] is a language of the future, and in the future, nobody
        uses [vertical tabs]." ~ Allen

.. note::

    As with Python, a backslash (``\``) as the final character of a line
    escapes the newline and causes that line and its successor to be
    interpereted as one.

 ▲ def c := 1 + 2 \
 ...   + 3 + 4
 Result: 10

``+`` when used with strings is a concatenation operator as in Python. Unlike
Java, it does *not* automatically coerce other types on the right-hand if the
left-hand operand is a string.

.. todo:: "What is the end-of-statement delineator in Monte?"

.. syntax:: StrExpr

   Ap('StrExpr', P('stringLiteral'))

.. syntax:: stringLiteral

   Sigil(Char('"'), ManyTill(P('charConstant'), Char('"')))


.. rubric:: Footnotes

.. [#e_scalars] Sclar types in monte are thes same as the `Scalar Data
                Types in E`__.

__ http://erights.org/elang/scalars/index.html
