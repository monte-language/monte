========================
Operators and Assignment
========================

.. epigraph::

    Corporate accounts payable, Nina speaking! Just a moment!

    -- Nina, corporate accounts payable, *Office Space*

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


Augmented Assignment
--------------------

All binary operators which pass a message to the left-hand operand can be used
as augmented assignment operators. For example, augmented addition is legal::

    var x := "augmenting "
    x += "addition!"

Behind the scenes, the compiler transforms augmented operators into standard
operator usage, and then into calls::

    var x := "augmenting "
    x := x.add("addition!")

Monte permits this augmented construction for any verb, not just those used by
operators. For example, the ``with`` verb of lists can be used to
incrementally build a list::

    var l := []
    for i in 1..10:
        l with= (i)

And even non-unary messages can get in on the fun, with a properly placed pair
of parentheses::

    var x := 7
    x modPow= (129, 3)

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

Syntax Summary
--------------

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

   Sequence('def', NonTerminal('noun'))

.. todo:: find forward declaration in ``monte_parser.mt``; doctest

.. syntax:: PatternBinding

   Sequence('def',
             NonTerminal('pattern'),
             Optional(Sequence("exit", NonTerminal('order'))),
             Optional(Sequence(":=", NonTerminal('assign'))))

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

