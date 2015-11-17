Primitive Data Types
====================

Scalars
-------

Monte provides some classic and common value types [#e_scalars]_.

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

.. todo:: un-mask failing test cases such as .expan(), bigint parsing, ...

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

.. syntax:: IntExpr

   Sequence(".int.")


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

   Sequence(".float64.")

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

.. syntax:: CharExpr

   Sequence(".char.")

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

.. syntax:: StrExpr

   Sequence(".String.")

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

Literal Syntax Summary
----------------------

.. note:: Lexical details of monte syntax are currently specified
	  only by implementation; see `lib/monte/monte_lexer.mt`__

__ https://github.com/monte-language/typhon/blob/master/mast/lib/monte/monte_lexer.mt

.. syntax:: literal

   Choice(0,
	  NonTerminal('IntExpr'),
	  NonTerminal('DoubleExpr'),
	  NonTerminal('CharExpr'),
	  NonTerminal('StringExpr'))

.. todo:: list "literals"
     Sequence("[", ZeroOrMore(NonTerminal('expr'), ','), "]"),
     Sequence("[", ZeroOrMore(Sequence(NonTerminal('expr'),
                                       "=>", NonTerminal('expr')), ','), "]"))


Monte Syntax Builder
--------------------

stuff from `monte_parser.mt`:

AndExpr(lhs, rhs
AssignExpr(lval, assign(ej)
AugAssignExpr(op, lval, assign(ej)
BinaryExpr(lhs, opName, rhs
BindingExpr(noun(ej)
BindingExpr(noun(ej)
BindingPattern(n
BindPattern(n, g
BindPattern(n, null
Catcher(cp, cb
CatchExpr(n, cp, cb
CoerceExpr(base, guard(ej)
CompareExpr(lhs, opName, rhs
DefExpr(patt, ex, assign(ej)
DefExpr(patt, null, assign(ej)
EscapeExpr(p1, e1, null, null
EscapeExpr(p1, e1, p2, e2
ExitExpr(ex, null
ExitExpr(ex, val
FinallyExpr(n, finallyblock
FinalPattern(
FinalPattern(noun(ej), null
ForExpr(it, k, v, body, catchPattern, catchBody
ForwardExpr(name
FunctionExpr(patt, body
FunctionInterfaceExpr(doco, name, guards_, extends_, implements_,
FunctionScript(patts, namedPatts, resultguard, body, span), span)
GetExpr(n, g
HideExpr(e
IfExpr(test, consq, alt
IgnorePattern(g
IgnorePattern(null
InterfaceExpr(doco, name, guards_, extends_, implements_, msgs,
ListComprehensionExpr(it, filt, k, v, body,
ListExpr(items
ListPattern(items, tail
LiteralExpr(sub.getName(), null)
LiteralExpr("&" + sub.getNoun().getName(), null)
LiteralExpr("&&" + sub.getNoun().getName(), null)
LiteralExpr(t[1], t[2])
MapComprehensionExpr(it, filt, k, v, body, vbody,
MapExprAssoc, ej)
MapExpr(items
MapPatternImport, ej)
MapPattern(items, tail
MatchBindExpr(lhs, rhs
Matcher(pp, bl
MessageDesc(doco, "run", params, resultguard
MessageDesc(doco, verb, params, resultguard
MetaContextExpr(
MetaStateExpr(
"Method"
MismatchExpr(lhs, rhs
"Module"(importsList, exportsList, body,
NamedArg, ej)
NamedParamImport, ej)
NamedParam(null, p, null
NounExpr(t[1]
NounExpr(t[1], t[2])
ObjectExpr(doco, name, oAs, oImplements,
OrExpr(lhs, rhs
ParamDesc(name, g
PatternHoleExpr(advance(ej)[1]
PrefixExpr(op, call(ej)
PrefixExpr("-", prim(ej)
QuasiExprHole(
QuasiExprHole(subexpr
QuasiParserExpr(name, parts.snapshot()
QuasiParserPattern(name, parts.snapshot()
QuasiPatternHole(patt, t[2]))
QuasiPatternHole(subpatt
QuasiText(t[1], t[2]))
RangeExpr(lhs, opName, rhs
SameExpr(lhs, rhs, false
SameExpr(lhs, rhs, true
SamePattern(prim(ej), false
SamePattern(prim(ej), true
Script(oExtends, methods, matchers
SeqExpr([], advance(ej)[2])
SeqExpr(exprs.snapshot()
SeqExpr([], null)
SeqExpr([], null)
SlotExpr(noun(ej)
SlotExpr(noun(ej)
SlotPattern(n, g
SuchThatPattern(p, e
SwitchExpr(
"To"
ValueHoleExpr(advance(ej)[1]
ValueHoleExpr(advance(ej)[1]
ValueHolePattern(advance(ej)[1]
VarPattern(n, g
VerbAssignExpr(verb, lval, acceptList(expr),
ViaPattern(e, pattern(ej)
WhenExpr(exprs, whenblock, catchers.snapshot(),
WhileExpr(test, whileblock, catchblock


.. rubric:: Footnotes

.. [#e_scalars] Sclar types in monte are thes same as the `Scalar Data
                Types in E`__.

__ http://erights.org/elang/scalars/index.html
