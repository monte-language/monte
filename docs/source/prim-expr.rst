Primitive Expressions
=====================

.. syntax:: prim

   Choice(
    0,
    Brackets("(", NonTerminal('expr'), ")"),
    NonTerminal('LiteralExpr'),
    NonTerminal('quasiliteral'),
    NonTerminal('NounExpr'),
    NonTerminal('HideExpr'),
    NonTerminal('MapComprehensionExpr'),
    NonTerminal('ListComprehensionExpr'),
    NonTerminal('ListExpr'),
    NonTerminal('MapExpr'))

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

Parentheses, braces, and square brackets set off primitive expressions.

Parentheses override normal precedence rules::

  >>> 4 + 2 * 3
  10
  >>> (4 + 2) * 3
  18

Noun
----

.. syntax:: NounExpr

   Ap('NounExpr', NonTerminal('name'))

.. syntax:: name

   Choice(0, "IDENTIFIER", Sigil("::", P('stringLiteral')))


A noun is a reference to a final or variable :ref:`slot <slots>`::

  >>> Int
  Int

  >>> _equalizer
  _equalizer

Any string literal prefixed by `::` can be used as an identifier::

  >>> { def ::"hello, world" := 1; ::"hello, world" }
  1

Literal Expression
------------------

.. syntax:: LiteralExpr

   Choice(0,
          NonTerminal('StrExpr'),
	  NonTerminal('IntExpr'),
          NonTerminal('DoubleExpr'),
	  NonTerminal('CharExpr'))


Quasi-Literal Expression
------------------------

.. syntax:: quasiliteral

   Ap('QuasiParserExpr',
    Maybe(Terminal("IDENTIFIER")),
    Brackets('`',
    SepBy(
        Choice(0,
	  Ap('Left', Terminal('QUASI_TEXT')),
          Ap('Right',
            Choice(0,
              Ap('NounExpr', Terminal('DOLLAR_IDENT')),
              Brackets('${', NonTerminal('expr'), '}'))))),
    '`'))

.. seealso::

   :ref:`quasiliteral <quasiliteral>`,

.. _ListExpr:

List Expression
---------------

.. syntax:: ListExpr

     Ap('ListExpr', Brackets("[", SepBy(NonTerminal('expr'), ','), "]"))

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

.. seealso::

   :ref:`comprehension <comprehension>`

Expansion:

  >>> m`[]`.expand()
  m`_makeList.run()`

.. _MapExpr:

Map Expression
---------------

.. syntax:: MapExpr

   Ap('MapExpr',
     Brackets("[", OneOrMore(NonTerminal('mapItem'), ','), "]"))

.. syntax:: mapItem

   Choice(0,
     Ap('Right', Ap('pair', NonTerminal('expr'),
                            Sigil("=>", NonTerminal('expr')))),
     Ap('Left', Sigil("=>", Choice(0,
           NonTerminal('SlotExpr'),
           NonTerminal('BindingExpr'),
           NonTerminal('NounExpr')))))


Monte uses the "fat arrow", ``=>`` for map syntax::

  >>> { def m := ["roses" => "red", "violets" => "blue"]; m["roses"] }
  "red"

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
