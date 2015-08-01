Basics: expressions, definitions, and variables
===============================================

Everything is an object. The expression ``1 + 1`` is actually
short-hand for a method call: ``1.plus(1)``.

Definitions bind objects to names::

  ▲> { def x := 2; x * x }
  Result: 4

The ``def`` syntax makes final (aka immutable) bindings::

  ▲> { def x := 2; x := 3 }
  ...
  Parse error: [Can't assign to final nouns, [x].asSet()]

To signal that you want a variable binding, use ``var``::

  ▲> { var v := 6; v := 12; v - 4 }
  Result: 8

Note the use of ``:=`` rather than ``=`` for assignment.
Comparison in Monte is ``==`` and the single-equals, ``=``, has no meaning. This
all but eliminates the common issue of ``if (foo = baz)`` suffered by all
languages where you can compile after typo-ing ``==``.

Monte has rich support for destructuring assignment using pattern matching::

  ▲> { def [x, y] := [1, 2]; x }
  Result: 1

The :ref:`patterns` section discusses pattern matching in detail.


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

.. note:: Lexical details of monte syntax are currently specified
	  only by implementation; see `lib/monte/monte_lexer.mt`__

__ https://github.com/monte-language/typhon/blob/master/mast/lib/monte/monte_lexer.mt

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

Operators
---------

Comparison
~~~~~~~~~~

  `<=>`
    "As big as". Think of it as merging `<=` with `>=`
  `==`
    Equality comparison. Can compare references, integers, etc.
  `<`
    Less than
  `>`
    Greater than. 
  `<=`
    Less than or equal to
  `>=`
    Greater than or equal to. 

.. code-block:: monte

    3 < 2 == False
    3 > 2 == True
    3 < 3 == False
    3 <= 3 == True

Logical
~~~~~~~

  `&&`
    And. 

.. code-block:: monte

    True && True == True
    True && False == False
    False && False == False

How do I perform a conditional expression? What is Monte's ternary operator?
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Monte does not have a ternary operator. However, in exchange, the ``if``
expression can be used where any other expression might be placed. As an
example, consider a function that tests whether an argument is even::

    def even(i :Int) :Str:
        if (i % 2 == 0):
            return "yes"
        else:
            return "no"

Monte lacks the ternary operator, but permits using regular conditional
expressions in its place. We can refactor this example to pull the ``return``
outside of the ``if``::

    def even(i :Int) :Str:
        return if (i % 2 == 0) {"yes"} else {"no"}

Don't forget that Monte requires ``if`` expressions to evaluate their
condition to a ``Bool``.


Boolean Operators
-----------------

  `**`
    Exponentiation. `2 ** 3 == 8`
  `*`
    Multiplication. `2 * 3 == 6`


Expression Syntax Summary
-------------------------

.. syntax:: expr

   Choice(
    0,
    NonTerminal('assign'),
    Sequence(
        Choice(0, "continue", "break", "return"),
        Choice(0,
               Sequence("(", ")"),
               ";",
               NonTerminal('blockExpr'))))

.. seealso::

   :ref:`loopExpr`
      on ``continue``, ``break``, and ``return``
   :ref:`blocks`
      on *blockExpr*

.. syntax:: assign

   Choice(
    0,
    Sequence('def',
             NonTerminal('pattern'),
             Optional(Sequence("exit", NonTerminal('order'))),
             Optional(Sequence(":=", NonTerminal('assign')))),
    Sequence(Choice(0, 'var', 'bind'),
             NonTerminal('pattern'),
             # XXX the next two seem to be optional in the code.
             ":=", NonTerminal('assign')),
    Sequence(NonTerminal('lval'), ":=", NonTerminal('assign')),
    Comment("@op=...XXX"),
    Comment("VERB_ASSIGN XXX"),
    NonTerminal('logical'))

.. seealso::

   :ref:`patterns`

.. syntax:: lval

   Choice(
    0,
    NonTerminal('noun'),
    NonTerminal('getExpr'))

.. syntax:: logical

   Sequence(
    NonTerminal('comp'),
    Optional(Sequence(Choice(0, '||', '&&'), NonTerminal('logical'))))

.. syntax:: comp

   Sequence(
    NonTerminal('order'),
    Optional(Sequence(Choice(
        0,
	Choice(0, "=~", "!~"),
        Choice(0, "==", "!="),
        "&!",
        Choice(0, "^", "&", "|")
    ), NonTerminal('comp'))))

.. syntax:: order

   Sequence(
    NonTerminal('prefix'),
    Optional(Sequence(Choice(
        0,
        "**",
        Choice(0, "*", "/", "//", "%"),
        Choice(0, "+", "-"),
        Choice(0, "<<", ">>"),
        Choice(0, "..", "..!"),
        Choice(0, ">", "<", ">=", "<=", "<=>")
    ), NonTerminal('order'))))

.. syntax:: prefix

   Choice(
    0,
    Sequence('-', NonTerminal('prim')),
    Sequence(Choice(0, "~", "!"), NonTerminal('call')),
    Sequence('&', NonTerminal('noun')),
    Sequence('&&', NonTerminal('noun')),
    Sequence(NonTerminal('call'), Optional(NonTerminal('guard'))))

.. syntax:: call

   Sequence(
    NonTerminal('calls'),
    Optional(Sequence(NonTerminal('curry'))))

*TODO: subordinate calls, as it's a purely syntactic notion*

.. syntax:: calls

    Choice(
        0, NonTerminal('prim'),
        Sequence(
            NonTerminal('calls'),
            Optional(
                Sequence(Choice(0, ".", "<-"),
                         Choice(0, "IDENTIFIER", ".String."))),
            Sequence("(", ZeroOrMore(NonTerminal('expr'), ','), ")")),
        NonTerminal('getExpr'))

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
    ".String.", ".int.", ".float64.", ".char.",
    NonTerminal('quasiliteral'),
    Choice(0, "IDENTIFIER", Sequence("::", ".String.")),
    Sequence("(", NonTerminal('expr'), ")"),
    Sequence("{", ZeroOrMore(NonTerminal('expr'), ';'), "}"),
    Sequence("[",
             Choice(
                 0,
                 Skip(),
                 OneOrMore(NonTerminal('expr'), ','),
                 OneOrMore(Sequence(NonTerminal('expr'),
                                    "=>", NonTerminal('expr')),
                           ','),
                 Sequence("for", NonTerminal('comprehension'))),
             "]"))

.. syntax:: comprehension

   Choice(
    0,
    Sequence(NonTerminal('pattern'),
             "in", NonTerminal('iter'),
             NonTerminal('expr')),
    Sequence(NonTerminal('pattern'), "=>", NonTerminal('pattern'),
             "in", NonTerminal('iter'),
             NonTerminal('expr'), "=>", NonTerminal('expr')))

.. syntax:: iter

   Sequence(
    NonTerminal('order'),
    Optional(Sequence("if", NonTerminal('comp'))))

.. syntax:: noun

   Choice(0, "IDENTIFIER", Sequence("::", ".String."))
