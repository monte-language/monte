========================
Operators and Assignment
========================

.. epigraph::

    Corporate accounts payable, Nina speaking! Just a moment!

    -- Nina, corporate accounts payable, *Office Space*

.. _def:

The ``def`` syntax makes final (aka immutable) bindings::

  ▲> { def x := 2; x := 3 }
  ...
  Parse error: [Can't assign to final nouns, [x].asSet()]

To signal that you want a variable binding, use ``var``::

  >>> { var v := 6; v := 12; v - 4 }
  8

Note the use of ``:=`` rather than ``=`` for assignment.
Comparison in Monte is ``==`` and the single-equals, ``=``, has no meaning. This
all but eliminates the common issue of ``if (foo = baz)`` suffered by all
languages where you can compile after typo-ing ``==``.

Monte has rich support for destructuring assignment using
:ref:`pattern matching <patterns>`::

  >>> { def [x, y] := [1, 2]; x }
  1

.. syntax:: DefExpr

   Sequence('def',
             NonTerminal('pattern'),
             Optional(Sequence("exit", NonTerminal('order'))),
             Sequence(":=", NonTerminal('assign')))

.. syntax:: ForwardExpr

   Sequence('def',
             NonTerminal('pattern'),
             Optional(Sequence("exit", NonTerminal('order'))),
             Optional(Sequence(":=", NonTerminal('assign'))))

.. _message_passing:

Message Passing
---------------

There are two ways to pass a message. First, the **immediate call**::

  >>> { def x := 2; def result := x.add(3) }
  5

And, second, the **eventual send**::

  >>> { def x; def prom := x<-message(3); null }
  null

Function call syntax elaborates to a call to ``run`` (
and likewise :ref:`vice-versa<def-fun>`)::

  >>> m`f(x)`.expand()
  m`f.run(x)`

Indexing elaborates to a call to ``get``::

  >>> { object parity { to get(n) { return n % 2 }}; parity[3] }
  1

Calls may be curried::

  >>> { def x := 2; def xplus := x.add; xplus(4) }
  6

.. syntax:: call

   Sequence(
    NonTerminal('calls'),
    Optional(Sequence(NonTerminal('curry'))))

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

.. _operators:

Operators
---------

Monte has a rich set of operators above and beyond those in Kernel-Monte. All
operators are overloadable, but overloading follows a very simple set of
rules: Operators desugar into message passing, and the message is generally
passed to the left-hand operand, except for a few cases where the message is
passed to a *helper object* which implements the operation. In object
capability shorthand, we are asking the object on the left what it thinks of
the object on the right.

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

.. syntax:: logical

   Sequence(
    NonTerminal('comp'),
    Optional(Sequence(Choice(0, '||', '&&'), NonTerminal('logical'))))

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


Comparison
~~~~~~~~~~

Monte has the usual comparison operators::

  >>> 3 < 2
  false
  >>> 3 > 2
  true
  >>> 3 < 3
  false
  >>> 3 <= 3
  true

They expand to use of a helper object::

  >>> m`x == y`.expand()
  m`__equalizer.sameEver(x, y)`

  >>> m`3 < 2`.expand()
  m`_comparer.lessThan(3, 2)`

.. todo:: elaborate on sameness

Comparison is more strict than you might expect::

  >>> 3 == "3"
  false

  >>> 1 + 1 == 2.0
  false

  ▲> 3 < "3"
  Parse error: Object was wrong type: Not an integer!

Use ``<=>`` aka ``asBigAs`` to compare magnitudes::

  >>> 2.0 <=> 1 + 1
  true

  >>> 2 + 1 <=> 3.0
  true

expansion::
  >>> m`2.0 <=> 1 + 1`.expand()
  m`_comparer.asBigAs(2.000000, 1.add(1))`

You can also compare with a pattern::

  >>> [1, 2] =~ [a, b]
  true

  >>> [1, "x"] =~ [_ :Int, _ :Str]
  true

  >>> "abc" =~ `a@rest`
  true

  >>> "xbc" =~ `a@rest`
  false

  >>> "xbc" !~ `a@rest`
  true

Logical
~~~~~~~

.. sidebar:: ternary conditional expression

   While monte does not have the ``c ? x : y`` ternary conditional
   operator, the ``if`` expression works just as well. For example, to
   tests whether ``i`` is even::

     >>> { def i := 3; if (i % 2 == 0) { "yes" } else { "no" } }
     "no"

   Don't forget that Monte requires ``if`` expressions to evaluate
   their condition to a ``Bool``::

     ▲> if (1) { "yes" } else { "no" }
     Parse error: Not a boolean!

Monte uses C syntax for the basic logical operators::
   >>> true && true
   true

We also have negated implication operator::
   >>> true &! false
   true

   >>> m`x &! y`.expand()
   m`x.butNot(y)`


Boolean Operators
-----------------

We have the usual exponentiation, multiplication, etc.::

  >>> 2 ** 3
  8
  >>> 2 * 3
  6

We can build a half-open interval with the range operator::

  >>> [for x in (1..!4) x * 2]
  [2, 4, 6]

The inclusive range operator is a syntactic shortcut::

  >>> 1..4
  1..!5

  >>> [for x in (1..4) x * 2]
  [2, 4, 6, 8]


Augmented Assignment
--------------------

All binary operators which pass a message to the left-hand operand can be used
as augmented assignment operators. For example, augmented addition is legal::

  >>> { var x := "augmenting "; x += "addition!"; x }
  "augmenting addition!"

Behind the scenes, the compiler transforms augmented operators into standard
operator usage, and then into calls::

  >>> { var x := "augmenting "; x := x.add("addition!") }
  "augmenting addition!"

Monte permits this augmented construction for any verb, not just those used by
operators. For example, the ``with`` verb of lists can be used to
incrementally build a list::

  >>> { var l := []; for i in 1..10 { l with= (i) }; l }
  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

And even non-unary messages can get in on the fun, with a properly placed pair
of parentheses::

  >>> { var x := 7; x modPow= (129, 3) }
  1


Assignment operators
~~~~~~~~~~~~~~~~~~~~

.. todo:: find these in ``monte_parser.mt``; doctest

::

  a := b
  a += b
  a -= b
  a *= b
  a /= b
  a //= b
  a %= b
  a %%= b
  a **= b
  a >>= b
  a <<= b
  a &= b
  a |= b
  a ^= b
  a foo= b

.. syntax:: assign

   Choice(
    0,
    NonTerminal('PatternBinding'),
    Sequence(Choice(0, 'var', 'bind'),
             NonTerminal('pattern'),
             # XXX the next two seem to be optional in the code.
             ":=", NonTerminal('assign')),
    Sequence(NonTerminal('lval'), ":=", NonTerminal('assign')),
    Comment("@op=...XXX"),
    Comment("VERB_ASSIGN XXX"),
    NonTerminal('logical'))

.. syntax:: ForwardDeclaration

   Sequence('def', NonTerminal('name'))

.. todo:: find forward declaration in ``monte_parser.mt``; doctest

.. syntax:: lval

   Choice(
    0,
    NonTerminal('name'),
    NonTerminal('getExpr'))


Primitive Expressions
---------------------

Parentheses, braces, and square brackets set off primitive expressions.

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

A sequence expressions evaluates to the value of its last item::

  >>> { 4; "x"; "y" }
  "y"

Parentheses override normal precedence rules::

  >>> 4 + 2 * 3
  10
  >>> (4 + 2) * 3
  18

.. seealso::

   :ref:`quasiliteral <quasiliteral>`,
   :ref:`comprehension <comprehension>`


Noun
----

A noun is a reference to a final or variable slot.

.. syntax:: noun

   Choice(0, "IDENTIFIER", Sequence("::", ".String."))

examples::

  >>> Int
  Int

  .>> __equalizer
  <Equalizer>

Any string literal prefixed by `::` can be used as an identifier::

  >>> { def ::"hello, world" := 1; ::"hello, world" }
  1


Unary operators
---------------

Monte has logical, bitwise, and arithmetic negation operators::

  >>> - (1 + 3)
  -4
  >>> ~ 0xff
  -256
  >>> ! true
  false

A guard can be used as an operator to coerce a value::

  >>> 1 :Int
  1

.. todo:: discuss, doctest SlotExpression ``&x``, BindingExpression ``&&x``

.. syntax:: prefix

   Choice(
    0,
    NonTerminal('unary'),
    NonTerminal('SlotExpression'),
    NonTerminal('BindingExpression'),
    Sequence(NonTerminal('call'), NonTerminal('guardOpt')))

.. syntax:: unary

   Choice(
    0,
    Sequence('-', NonTerminal('prim')),
    Sequence(Choice(0, "~", "!"), NonTerminal('call')))

.. syntax:: SlotExpression

   Sequence('&', NonTerminal('noun'))

.. syntax:: BindingExpression

   Sequence('&&', NonTerminal('noun'))
