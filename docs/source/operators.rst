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

Monte has rich support for destructuring assignment using pattern matching::

  >>> { def [x, y] := [1, 2]; x }
  1

.. syntax:: PatternBinding

   Sequence('def',
             NonTerminal('pattern'),
             Optional(Sequence("exit", NonTerminal('order'))),
             Optional(Sequence(":=", NonTerminal('assign'))))

The :ref:`patterns` section discusses pattern matching in detail.

.. _message_passing:

Message Passing
---------------

There are two ways to pass a message. First, the **immediate call**::

  >>> { def x := 2; def result := x.add(3) }
  5

And, second, the **eventual send**::

  >>> { def x; def prom := x<-message(3); null }
  null

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

.. todo:: document curry

.. syntax:: curry

   Sequence(
    Choice(0, '.', '<-'),
    Choice(0, "IDENTIFIER", ".String."))

Operators
---------

Monte has a rich set of operators above and beyond those in Kernel-Monte. All
operators are overloadable, but overloading follows a very simple set of
rules: Operators desugar into message passing, and the message is generally
passed to the left-hand operand, except for a few cases where the message is
passed to a *helper object* which implements the operation. In object
capability shorthand, we are asking the object on the left what it thinks of
the object on the right.

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

  >>> 3 < 2
  false
  >>> 3 > 2
  true
  >>> 3 < 3
  false
  >>> 3 <= 3
  true

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

.. todo:: document match bind `x =~ p`

.. todo:: what is `&!`?


Logical
~~~~~~~

  `&&`
    And. 

   >>> true && true
   true
   >>> true && false
   false
   >>> false && false
   false

.. syntax:: logical

   Sequence(
    NonTerminal('comp'),
    Optional(Sequence(Choice(0, '||', '&&'), NonTerminal('logical'))))

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
    Exponentiation.
  `*`
    Multiplication.

  >>> 2 ** 3
  8
  >>> 2 * 3
  6

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

.. todo:: document `..` and `..!` (ranges?)


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

Noun
~~~~

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
~~~~~~~~~~~~~~~

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


Indexing
~~~~~~~~

.. syntax:: getExpr

   Sequence(
    NonTerminal('calls'),
    Sequence("[", ZeroOrMore(NonTerminal('expr'), ','), "]"))
