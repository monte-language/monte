Lexical Grammar (Tokens)
========================

Monte source consists of a sequence of characters. Before parsing into
expressions, it is separated into lexical tokens.

Excerpts from the `lib/monte/monte_lexer`__ implementation provide
a reasonably clear, if somewhat circular, definition of Monte lexical
syntax.

__ https://github.com/monte-language/typhon/blob/master/mast/lib/monte/monte_lexer.mt

.. index:: tab, block, indentation

.. _indent_blocks:

Brackets, Indentation, and Blocks
---------------------------------

Opening and closing bracket tokens must be balanced::

  def closers :DeepFrozen := ['(' => ')', '[' => ']', '{' => '}']

A colon (``:``) token begins an :dfn:`indented block`.

.. todo:: specify canStartIndentedBlock, braceStack exactly

Like Python, Monte's blocks are usually indentation-delimited::

    def f(x):
        g()
        return x + 1

Monte also permits curly braces instead of colons for marking blocks::

    def f(x) {
        g()
        return x + 1
    }

And, finally, Monte allows sequences to be separated by semicolons::

    def f(x) { g(); return x + 1 }

Idiomatic Monte can take on any of these styles. Typical Monte code prefers
the colon-indented-block style.

Braces are required only if the surrounding block uses braces. For example,
this is legal Monte::

    def f(x):
        def g(y):
            return x + y
        return g

And so is this::

    def f(x):
        def g(y) { return x + y }
        return g

.. note:: Tabs are a syntax error in Monte.

.. important::
    Monte code should always uses four spaces for each indentation level.


Operators
---------

Many binary operators have corresponding assignment operators:
  
  - xor: ``^`` , ``^=``
  - add: ``+`` , ``+=``
  - subtract: ``-`` , ``-=``
  - shiftLeft: ``<<`` , ``<<=``
  - shiftRight: ``>>`` , ``>>=``
  - pow: ``**`` , ``**=``
  - multiply: ``*`` , ``*=``
  - floorDivide: ``//`` , ``//=``
  - approxDivide: ``/`` , ``/=``
  - mod: ``%`` , ``%=``
  - and: ``&`` , ``&=``
  - or: ``|`` , ``|=``

The remaining operator tokens are:

  - complement: ``~``
  - inclusive range: ``..``
  - exclusive range: ``..!``
  - assign: ``:=``
  - as big as: ``<=>``
  - less: ``<``
  - greater: ``>``
  - less or equal: ``<=``
  - great or equal: ``>=``
  - equal: ``==``
  - not equal: ``!=``
  - match bind: ``=~``
  - not match bind: ``!~``
  - not: ``!``
  - logical and: ``&&``
  - logical or: ``||``
  - but not: ``&!``
  - sequence: ``;``

Other Punctuation
-----------------

  - ``,``
  - treat a string as a noun: ``::``
  - such that: ``?``
  - ignore pattern: ``_``
  - call: ``.``
  - send: ``<-``
  - when: ``->``
  - maps to: ``=>``

Keywords
--------

The Monte keywords are given as::

   def MONTE_KEYWORDS :DeepFrozen := [
       "as", "bind", "break", "catch", "continue", "def", "else", "escape",
       "exit", "extends", "exports", "finally", "fn", "for", "guards", "if",
       "implements", "import", "in", "interface", "match", "meta", "method",
       "object", "pass", "pragma", "return", "switch", "to", "try", "var",
       "via", "when", "while"].asSet()

Monte keywords are case insensitive::

  >>> DEF x := 1
  1

Identifiers
-----------

Identifers start with an element of ``idStart`` followed by any number of
elements of ``idPart``::

   def decimalDigits :DeepFrozen := regionToSet('0'..'9')

   def idStart :DeepFrozen := regionToSet('a'..'z' | 'A'..'Z' | '_'..'_')
   def idPart :DeepFrozen := idStart | decimalDigits

.. _literals:

Literals
--------

In the syntax railroad diagrams and in ``monte_lexer.mt``, the
literal tokens are tagged:

  - ``.int.`` (guard; ``Int``)
  - ``.float64.`` (``Double``)
  - ``.char.`` (``Chr``)
  - ``.String.`` (``Str``)

.. note:: Monte has no booleans literals; rather, the nouns `true` and
          `false` are pre-defined :doc:`primitive values
          <runtime>`.

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

String
~~~~~~

.. syntax:: StrExpr

   Ap('StrExpr', P('stringLiteral'))

.. syntax:: stringLiteral

   Sigil(Char('"'), ManyTill(P('charConstant'), Char('"')))

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
    interpereted as one::

       ▲ def c := 1 + 2 \
       ...   + 3 + 4
       Result: 10

As in Python, ``+`` when used with strings is a concatenation operator
. Unlike Java, it does *not* automatically coerce other types on the
right-hand if the left-hand operand is a string.

Quasi-Literals
--------------

A quasif-literal is somewhat like a string delimited by back-ticks
("`"), but inside, ``${ ... }`` is parsed as an expression and ``@{
... }`` is parsed as a pattern; the curly-braces may be omitted in the
case of simple noun expressions ``$ident`` or ``@ident``.

To escape delimiter characters within a quasi-literal, double them::

  >>> def price := 10.00
  ... `The price is $$$price.`
  "The price is $10.000000."
