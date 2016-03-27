.. _operators:

Operators by precedence and associativity
=========================================

.. epigraph::

    Corporate accounts payable, Nina speaking! Just a moment!

    -- Nina, corporate accounts payable, *Office Space*

The expression subset of the Monte grammar is presented here in
operator precedence order, meaning that later constructs bind tighter
than earlier constructs. For example, `expr "+" expr` is presented
before `expr "*" expr`, so ``*`` binds tighter than ``+``. Therefore,
``a + b * c + d`` is equivalent to ``a + (b * c) + d``. All the
constructs in presented in the same section have the same precedence.

.. sidebar:: Kernel-Monte and Expansion

           .. index: kernel, Kernel Monte, expansion
           .. index:: expansion, syntactic expansion

           The Monte language as seen by the programmer has the rich
           set of syntactic conveniences expected of a modern
           scripting language. However, to avoid complexity that so
           often hampers security, the :doc:`semantics of Monte
           <semantics>` is primarily defined over a smaller language
           called :dfn:`Kernel-Monte`. The rest of E is defined by
           :dfn:`syntactic expansion` to this subset. For example::

              >>> m`1 + 1`.expand()
              m`1.add(1)`

Monte has a rich set of operators above and beyond those in Kernel-Monte. All
operators are overloadable, but overloading follows a very simple set of
rules: Operators expand to message passing, and the message is generally
passed to the left-hand operand, except for a few cases where the message is
passed to a *helper object* which implements the operation. In object
capability shorthand, we are asking the object on the left what it thinks of
the object on the right.

There are some special rules about the behavior of the basic operators
because of E's distributed security.

.. todo:: special operator rules because of security

Sequence
--------

.. syntax:: sequence

   ZeroOrMore(
     Choice(
       0,
       NonTerminal('blockExpr'),
       NonTerminal('expr')),
     ";")

A sequence expressions evaluates to the value of its last item::

  >>> { 4; "x"; "y" }
  "y"

Assignment and Definition
-------------------------

.. syntax:: assign

   Choice(0,
     Ap('DefExpr',
       Sigil("def", NonTerminal("pattern")),
       Maybe(Sigil("exit", NonTerminal("order"))),
       Sigil(":=", NonTerminal("assign"))),
    Ap('DefExpr',
      Choice(0, NonTerminal('VarPatt'), NonTerminal('BindPatt')),
      Ap('return Nothing', Skip()),
      Sigil(":=", NonTerminal("assign"))),
    Ap('AssignExpr',
       NonTerminal('lval'),
       Sigil(":=", NonTerminal("assign"))),
    NonTerminal('VerbAssignExpr'),
    NonTerminal('order'))

.. syntax:: lval

   Choice(0,
    Ap('Left', Ap('pair',
      NonTerminal('order'),
      Brackets("[", SepBy(NonTerminal('expr'), ','), "]"))),
    Ap('Right', NonTerminal('name')))

Assignment is right associative. The list update on the right happens
before the definition on the left::

  >>> def color := ["red", "green", "blue"].diverge()
  ... def c := color[1] := "yellow"
  ... c
  "yellow"

Indexed Update Expansion
~~~~~~~~~~~~~~~~~~~~~~~~

An indexed update expands to a call to ``put``::

   >>> m`x[i] := 1`.expand()
   m`x.put(i, def ares_1 := 1); ares_1`

.. _augmented_assignment:

Augmented Assignment Expansion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. syntax:: VerbAssignExpr

   Ap('VerbAssignExpr',
      NonTerminal('lval'),
      Sigil("VERB_ASSIGN", NonTerminal("assign")))

All binary operators which pass a message to the left-hand operand can be used
as augmented assignment operators. For example, augmented addition is legal::

  >>> { var x := "augmenting "; x += "addition!"; x }
  "augmenting addition!"

Behind the scenes, the compiler transforms augmented operators::

  >>> m`x += "addition!"`.expand()
  m`x := x.add("addition!")`

Monte permits this augmented construction for any verb, not just those used by
operators. For example, the ``with`` verb of lists can be used to
incrementally build a list::

  >>> { var l := []; for i in (1..10) { l with= (i) }; l }
  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

And even non-unary messages can get in on the fun, with a properly placed pair
of parentheses::

  >>> { var x := 7; x modPow= (129, 3) }
  1

.. todo:: VERB_ASSIGN lexical details


Assignment operators
~~~~~~~~~~~~~~~~~~~~

::

   >>> var x := 5; [ x += 2, x -= 1, x *= 2, x **= 3 ]
   [7, 6, 12, 1728]
   >>> var x := 50; [ x //= 3, x %= 7, x /= 4]
   [16, 2, 0.500000]
   >>> var x := 5; [ x ^= 3, x |= 15, x &= 7, x <<= 3, x >>= 2]
   [6, 15, 7, 56, 14]


Conditional-Or
--------------

.. syntax:: logical_or

   Sequence(
    NonTerminal('logical_and'),
    Optional(Sequence('||', NonTerminal('logical_or'))))

Monte uses C syntax for the basic logical operators::

   >>> false || true
   true

Evaluates left to right until it finds a true condition.

  >>> {((1 =~ x) || (2 =~ x)); x}
  1
  >>> {((1 =~ [x, y]) || (2 =~ x)); x}
  2

Conditional-And
---------------

.. syntax:: logical_and

   Sequence(
    NonTerminal('comp'),
    Optional(Sequence('&&', NonTerminal('logical_and'))))

Logical Expansion
~~~~~~~~~~~~~~~~~

Boolean conditionals expand to ``if`` expressions::

    >>> m`a || b`.expand()
    m`if (a) { true } else if (b) { true } else { false }`

    >>> m`a && b`.expand()
    m`if (a) { if (b) { true } else { false } } else { false }`


.. _comparisons:

Comparisons and Bitwise/Logical Operators
-----------------------------------------

.. syntax:: comp

   Choice(0,
     Ap('BinaryExpr',
       NonTerminal('order'),
       Choice(0,
	 Choice(0, "=~", "!~"),
         Choice(0, "==", "!="),
         "&!",
         Choice(0, "^", "&", "|")),
       NonTerminal('comp')),
    NonTerminal('order'))

.. syntax:: order

   Choice(0,
     NonTerminal('CompareExpr'),
     NonTerminal('RangeExpr'),
     NonTerminal('BinaryExpr'),
     NonTerminal('prefix'))

These are non-associative: ``x == y == z`` is a syntax error.

  >>> false == true
  false

  >>> false != true
  true

You can compare with a pattern and use the resulting bindings::

  >>> [1, "x"] =~ [_ :Int, _ :Str]
  true

  >>> [1, 2] =~ [a, b]; b
  2

  >>> "<p>" =~ `<@tag>`; tag
  "p"

  >>> "<p>" !~ `</@tag>`
  true

Comparison is more strict than you might expect::

  >>> 3 == "3"
  false

  >>> 1 + 1 == 2.0
  false

We also have negated implication operator::

   >>> true &! false
   true

Boolean Comparisons (non-associative)::

  >>> false & true
  false

  >>> false | true
  true

  >>> false ^ true
  true

Comparison Expansion
~~~~~~~~~~~~~~~~~~~~

Comparisons expand to use of a helper object::

::

   >>> m`x == y`.expand()
   m`_equalizer.sameEver(x, y)`
   >>> m`x != y`.expand()
   m`_equalizer.sameEver(x, y).not()`

::

   >>> m`"value" =~ pattern`.expand()
   m`def sp_1 := "value"; def [ok_2, &&pattern] := escape fail_3 { def pattern exit fail_3 := sp_1; _makeList.run(true, &&pattern) } catch problem_4 { def via (_slotToBinding) &&broken_5 := Ref.broken(problem_4); _makeList.run(false, &&broken_5) }; ok_2`
   >>> m`"value" !~ pattern`.expand()
   m`(def sp_1 := "value"; def [ok_2, &&pattern] := escape fail_3 { def pattern exit fail_3 := sp_1; _makeList.run(true, &&pattern) } catch problem_4 { def via (_slotToBinding) &&broken_5 := Ref.broken(problem_4); _makeList.run(false, &&broken_5) }; ok_2).not()`

::

   >>> m`x ^ y`.expand()
   m`x.xor(y)`
   >>> m`x & y`.expand()
   m`x.and(y)`
   >>> m`x | y`.expand()
   m`x.or(y)`
   >>> m`x &! y`.expand()
   m`x.butNot(y)`

Partial Ordering
----------------

.. syntax:: CompareExpr

   Ap('CompareExpr', NonTerminal('prefix'),
     Choice(0, ">", "<", ">=", "<=", "<=>"), NonTerminal('order'))

Monte has the usual ordering operators::

  >>> 3 < 2
  false
  >>> 3 > 2
  true
  >>> 3 < 3
  false
  >>> 3 <= 3
  true

They are non-associative and only partial:

  >>> try { 3 < "3" } catch _ { "ouch! no order defined" }
  "ouch! no order defined"

Use ``<=>`` aka ``asBigAs`` to compare magnitudes::

  >>> 2.0 <=> 1 + 1
  true

  >>> 2 + 1 <=> 3.0
  true

Ordering Expansion
~~~~~~~~~~~~~~~~~~

Ordering operators expand to use of a helper object::

  >>> m`3 < 2`.expand()
  m`_comparer.lessThan(3, 2)`

  >>> m`2.0 <=> 1 + 1`.expand()
  m`_comparer.asBigAs(2.000000, 1.add(1))`

Interval
--------

.. syntax:: RangeExpr

   Ap('RangeExpr', NonTerminal('prefix'),
     Choice(0, "..", "..!"), NonTerminal('order'))

Non-associative.

We can build a half-open interval with the range operator::

  >>> [for x in (1..!4) x * 2]
  [2, 4, 6]

Or we can build closed intervals with the inclusive range operator::

  >>> [for x in (1..4) x * 2]
  [2, 4, 6, 8]

Half-open intervals are more typical, though they are in most ways
equivalent to closed intervals::
  
  >>> (0..!10) <=> (0..9)
  true

Expansion::

   >>> m`lo..hi`.expand()
   m`_makeOrderedSpace.op__thru(lo, hi)`

   >>> m`lo..!hi`.expand()
   m`_makeOrderedSpace.op__till(lo, hi)`

Shift
-----

.. syntax:: shift

   Ap('BinaryExpr', NonTerminal('prefix'),
     Choice(0, "<<", ">>"), NonTerminal('order'))

Left associative.

Among built-in data types, this is only defined on integers, and has the
traditional meaning but with no precision limit.

Expansion::

   >>> m`i << bits`.expand()
   m`i.shiftLeft(bits)`

   >>> m`i >> bits`.expand()
   m`i.shiftRight(bits)`

Additive
--------

.. syntax:: additiveExpr

   Ap('BinaryExpr', NonTerminal('multiplicativeExpr'),
     Choice(0, "+", "-"), NonTerminal('additiveExpr'))

Left associative.

::
   >>> [1, 2] + [3, 4]
   [1, 2, 3, 4]

   >>> "abc" + "def"
   "abcdef"

   >>> ["square" => 4] | ["triangle" => 3]
   ["square" => 4, "triangle" => 3]
   
   >>> def sides := ["square" => 4, "triangle" => 3]
   ... sides.without("square")
   ["triangle" => 3]

Expansion::

   >>> m`x + y`.expand()
   m`x.add(y)`

   >>> m`x - y`.expand()
   m`x.subtract(y)`

Multiplicative
--------------

.. syntax:: multiplicativeExpr

   Ap('BinaryExpr', NonTerminal('exponentiationExpr'),
     Choice(0, "*", "/", "//", "%"), NonTerminal('order'))            

Left associative.

  >>> 2 * 3
  6

Modular exponentiation::

   >>> 5 ** 3 % 13
   8

expansion::

   >>> m`base ** exp % mod`.expand()
   m`base.modPow(exp, mod)`

Exponentiation
--------------

.. syntax:: exponentiationExpr

   Ap('BinaryExpr', NonTerminal('prefix'),
      "**", NonTerminal('order'))

Non-associative.

  >>> 2 ** 3
  8

Expansion::

  >>> m`2 ** 3`.expand()
  m`2.pow(3)`

Unary Prefix
------------

.. syntax:: prefix

   Choice(
    0,
    Ap("PrefixExpr", '-', NonTerminal('prim')),
    Ap("PrefixExpr", Choice(0, "~", "!"), NonTerminal('calls')),
    NonTerminal('SlotExpr'),
    NonTerminal('BindingExpr'),
    NonTerminal('CoerceExpr'),
    NonTerminal('calls'))

.. syntax:: SlotExpr

   Ap('SlotExpr', Sigil('&', NonTerminal('name')))

.. syntax:: BindingExpr

   Ap('BindingExpr', Sigil('&&', NonTerminal('name')))

Monte has logical, bitwise, and arithmetic negation operators::

  >>> - (1 + 3)
  -4
  >>> ~ 0xff
  -256
  >>> ! true
  false

.. todo:: discuss, doctest SlotExpression ``&x``, BindingExpression ``&&x``

Expansions::

  >>> m`! false`.expand()
  m`false.not()`

Unary Postfix
-------------

.. syntax:: MetaExpr

   Sequence(
    "meta", ".",
    Choice(0,
           Sequence("context", "(", ")"),
           Sequence("getState", "(", ")")))

.. syntax:: CoerceExpr

   Ap("CoerceExpr", NonTerminal('calls'), Sigil(":", NonTerminal('guard')))

::

  meta.getState()
  meta.context()

A guard can be used as an operator to coerce a value::

  >>> 1 :Int
  1


.. _message_passing:

Call
----

.. syntax:: calls

   Ap('callExpr',
       NonTerminal('prim'),
       SepBy(
         Choice(0,
           Ap('Right',
             Choice(0,
               Ap('Right', NonTerminal('call')),
               Ap('Left', NonTerminal('send')))),
           Ap('Left', NonTerminal('index')))),
       Maybe(NonTerminal('curryTail')))

.. syntax:: call

   Ap('pair', Maybe(Sigil(".", NonTerminal('verb'))), NonTerminal('argList'))

.. syntax:: send

   Sigil("<-", Ap('pair', Maybe(NonTerminal('verb')), NonTerminal('argList')))

.. syntax:: curryTail

   Choice(0,
     Ap('Right', Sigil(".", NonTerminal('verb'))),
     Ap('Left', Sigil("<-", NonTerminal('verb'))))

.. syntax:: index

   Brackets("[", SepBy(NonTerminal('expr'), ','), "]")

.. syntax:: verb

   Choice(0, "IDENTIFIER", ".String.")

.. syntax:: argList

   Brackets("(", SepBy(NonTerminal('expr'), ","), ")")

.. todo:: named args in argList

There are two ways to pass a message. First, the **immediate call**::

  >>> { def x := 2; def result := x.add(3) }
  5

And, second, the **eventual send**::

  >>> { def x; def prom := x<-message(3); null }
  null

Calls may be curried::

  >>> { def x := 2; def xplus := x.add; xplus(4) }
  6

.. todo:: discuss matchers in object expressions

Call Expansion
~~~~~~~~~~~~~~

Function call syntax elaborates to a call to ``run`` (
and likewise :ref:`vice-versa<def-fun>`)::

  >>> m`f(x)`.expand()
  m`f.run(x)`

Indexing elaborates to a call to ``get``::

  >>> { object parity { to get(n) { return n % 2 }}; parity[3] }
  1
