Block Expressions
=================

.. syntax:: blockExpr

   Choice(
    0,
    NonTerminal('FunctionExpr'),
    NonTerminal('ObjectExpr'),
    NonTerminal('bind'),
    NonTerminal('def'),
    NonTerminal('InterfaceExpr'),
    NonTerminal('IfExpr'),
    NonTerminal('ForExpr'),
    NonTerminal('WhileExpr'),
    NonTerminal('SwitchExpr'),
    NonTerminal('EscapeExpr'),
    NonTerminal('TryExpr'),
    NonTerminal('WhenExpr'),
    NonTerminal('LambdaExpr'),
    NonTerminal('MetaExpr'))

.. syntax:: block

   Sequence(
    "{",
    Choice(
        0,
        NonTerminal('sequence'),
        "pass"),
    "}")

Nested Block
------------

.. syntax:: HideExpr

   Ap('HideExpr',
      Brackets("{", SepBy(NonTerminal('expr'), ';', fun='wrapSequence'), "}"))


The `if` Expression
-------------------

.. syntax:: IfExpr

   Sequence(
    "if", "(", NonTerminal('expr'), ")", NonTerminal('block'),
    Optional(Sequence("else", Choice(
        0, Sequence("if", Comment('blockExpr@@')),
        NonTerminal('block')))))

::

   >>> if (2 < 3) { "expected" } else { "unexpected" }
   "expected"

   >>> def x := 5
   ... def y := 10
   ... if (x < y) { "less" } else if (x > y) { "greater" } else { "neither" }
   "less"

The `switch` Expression
-----------------------

.. syntax:: SwitchExpr

   Sequence(
    "switch", "(", NonTerminal('expr'), ")",
    "{", NonTerminal('matchers'), "}")

.. syntax:: matchers

   OneOrMore(Sequence("match",
             NonTerminal('pattern'),
             NonTerminal('block')))

::

   >>> def state := "day"
   ...
   ... switch (state) {
   ...     match =="day" {"night"}
   ...     match =="night" {"day"}
   ... }
   "night"

Switch Expansion
~~~~~~~~~~~~~~~~

::

   >>> m`switch (specimen) { match pat1 { expr1 } }`.expand()
   m`{ def specimen_1 := specimen; escape ej_2 { def pat1 exit ej_2 := specimen_1; expr1 } catch failure_3 { _switchFailed.run(specimen_1, failure_3) } }`

The `try` Expression
--------------------

.. syntax:: TryExpr

   Sequence(
    "try", NonTerminal('block'), NonTerminal('catchers'))

.. syntax:: catchers

   Sequence(
    ZeroOrMore(Sequence("catch",
                        NonTerminal('pattern'),
                        NonTerminal('block'))),
    Optional(Sequence("finally", NonTerminal('block'))))

::

  >>> try { 3 < "3" } catch _ { "ouch! no order defined" }
  "ouch! no order defined"

.. todo:: expansion of various forms of ``try``

The `escape` Expression
-----------------------

.. syntax:: EscapeExpr

   Sequence(
    "escape", NonTerminal('pattern'),
    NonTerminal('blockCatch'))

If `hatch` is called during `expr`, complete with `hatch`'s argument::

  >>> escape hatch { def x :Int exit hatch := 1.0 }
  "1.000000 does not conform to <IntGuard>"

The `while` Loop
----------------

.. syntax:: WhileExpr

   Sequence(
    "while", "(", NonTerminal('expr'), ")", NonTerminal('blockCatch'))

::

  while (test) { body }
  while (test) { body } catch p { catchblock }

.. todo:: `while` doctests, expansion

The `for` Loops
---------------

.. syntax:: ForExpr

   Sequence(
    "for",
    NonTerminal('pattern'),
    Optional(Sequence("=>", NonTerminal('pattern'))),
    "in", NonTerminal('comp'),
    NonTerminal('blockCatch'))

.. syntax:: blockCatch

   Sequence(
    NonTerminal('block'),
    Optional(
        Sequence("catch", NonTerminal('pattern'),
                 NonTerminal('block'))))

::

  for valuePatt in iterableExpression { body }
  for keyPatt => valuePatt in iterableExpression { body }
  for valuePatt in iterableExpression { body } catch p { catchblock }

.. todo:: `for` doctests, expansion

The `when` Expression
---------------------

.. syntax:: WhenExpr

   Sequence(
    "when",
    "(", OneOrMore(NonTerminal('expr'), ','), ")",
    "->", NonTerminal('block'),
    NonTerminal('catchers'))

::

  when (x, y) -> { whenblock } catch p { catchblock }

The `fn` Expression
---------------------

.. syntax:: LambdaExpr

   Sequence(
    "fn",
    ZeroOrMore(NonTerminal('pattern'), ','),
    NonTerminal('block'))

::

  /** docstring */ fn p, q { body }

.. todo:: doctest ``/** docstring */``

.. _def:

Defining Objects
----------------

.. syntax:: def

   Sequence(
    "def",
    Choice(
        0,
        Sequence(
            Choice(
                0,
                Sequence("bind", NonTerminal("name"),
                         Optional(NonTerminal('guard'))),
                NonTerminal("name")),
            Choice(0, Comment("objectFunction@@"), NonTerminal('assign'))),
        NonTerminal('assign')))

.. syntax:: bind

   Sequence(
    "bind",
    NonTerminal('name'),
    Optional(NonTerminal('guard')), NonTerminal("objectExpr"))

.. syntax:: ObjectExpr

   Sequence(
    "object",
    Choice(0, Sequence("bind", NonTerminal('name')),
           "_",
           NonTerminal('name')),
    NonTerminal("objectExpr"))

.. syntax:: objectExpr

   Sequence(
    Optional(Sequence('extends', NonTerminal('order'))),
    NonTerminal('auditors'),
    '{', ZeroOrMore(NonTerminal('objectScript'), ';'), '}')

.. syntax:: objectScript

   Sequence(
    Optional(NonTerminal('doco')),
    Choice(0, "pass", ZeroOrMore("@@meth")),
    Choice(0, "pass", ZeroOrMore(NonTerminal('matchers'))))

.. syntax:: matchers

   OneOrMore(Sequence("match",
             NonTerminal('pattern'),
             NonTerminal('block')))

.. syntax:: doco

   Terminal('.String')

.. syntax:: FunctionExpr

   Sequence('def', '(', ZeroOrMore(NonTerminal('pattern'), ','), ')',
     NonTerminal('block'))

::

  object foo {
      to someMethod(p, q) {
          methBody
      }
  
      method rawMethod(p, q) {
          methBody
      }
       match [verb, arglist] {
           matcherBody
       }
  }
  object foo as someAuditor { ... }
  object foo implements firstAuditor, secondAuditor { ... }
  object foo extends baz { ... }

  /** doc string */
  object foo as someAuditor implements firstAuditor, secondAuditor extends baz { ... }

::

  def fun(p, q) :optionalGuard { body }

Defining Interfaces
-------------------

.. syntax:: InterfaceExpr

   Sequence(
    "interface",
    NonTerminal('namePattern'),
    Optional(Sequence("guards", NonTerminal('pattern'))),
    Optional(Sequence("extends", OneOrMore(NonTerminal('order'), ','))),
    Comment("implements_@@"), Comment("msgs@@"))

.. todo:: interface syntax diagram @@s

::

  interface Foo { to interfaceMethod(p, q) { ... } }
  interface Foo guards FooStamp { ... }

.. todo:: various items marked "@@" in railroad diagrams.
          Also, finish re-organizing them around precedence (use
          haskell codegen to test).
