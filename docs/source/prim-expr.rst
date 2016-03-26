Primitive Expressions (WIP)
===========================

Parentheses, braces, and square brackets set off primitive expressions.

.. syntax:: prim

   Choice(
    0,
    NonTerminal('LiteralExpr'),
    NonTerminal('quasiliteral'),
    NonTerminal('NounExpr'),
    Brackets("(", NonTerminal('expr'), ")"),
    NonTerminal('HideExpr'),
    NonTerminal('MapComprehensionExpr'),
    NonTerminal('ListComprehensionExpr'),
    NonTerminal('ListExpr'),
    NonTerminal('MapExpr'))

A sequence expressions evaluates to the value of its last item::

  >>> { 4; "x"; "y" }
  "y"

.. syntax:: HideExpr

   Ap('HideExpr',
      Brackets("{", SepBy(NonTerminal('expr'), ';', fun='wrapSequence'), "}"))

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

.. syntax:: NounExpr

   Ap('NounExpr', NonTerminal('name'))

.. syntax:: name

   Choice(0, "IDENTIFIER", Sigil("::", P('stringLiteral')))


examples::

  >>> Int
  Int

  .>> __equalizer
  <Equalizer>

Any string literal prefixed by `::` can be used as an identifier::

  >>> { def ::"hello, world" := 1; ::"hello, world" }
  1


.. syntax:: FunctionExpr

   Sequence('def', '(', ZeroOrMore(NonTerminal('pattern'), ','), ')',
     NonTerminal('block'))

::

  def fun(p, q) :optionalGuard { body }

.. syntax:: ObjectExpr

   Sequence(
    "object",
    Choice(0, Sequence("bind", NonTerminal('name')),
           "_",
           NonTerminal('name')),
    Optional(NonTerminal('guard')), Comment("objectExpr"))

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

.. syntax:: InterfaceExpr

   Sequence(
    "interface",
    NonTerminal('namePattern'),
    Optional(Sequence("guards", NonTerminal('pattern'))),
    Optional(Sequence("extends", OneOrMore(NonTerminal('order'), ','))),
    Comment("implements_@@"), Comment("msgs@@"))

::

  interface Foo { to interfaceMethod(p, q) { ... } }
  interface Foo guards FooStamp { ... }

.. todo:: interface syntax diagram

.. syntax:: IfExpr

   Sequence(
    "if", "(", NonTerminal('expr'), ")", NonTerminal('block'),
    Optional(Sequence("else", Choice(
        0, Sequence("if", Comment('blockExpr@@')),
        NonTerminal('block')))))

::

  if (test) { consq } else if (test2) { consq2 } else { alt }

.. todo:: report bug with else if blockExpr

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

Additional flow of control
--------------------------

We have already seen the if/then/else structure. Other traditional
structures include:

 - ``while (booleanExpression) {...}``
 - ``try{...} catch errorVariable {...} finally{...}``
 - ``throw (ExceptionExpressionThatCanBeAString)``
 - ``break`` (which jumps out of a while or for loop; if the break
   keyword is followed by an expression, that expression is returned
   as the value of the loop)
 - ``continue`` (which jumps to the end of a while or for, and starts
   the next cycle)
 - ``switch (expression) {match==v1{...} match==v2{...}
   ... match _{defaultAction}}``

::

  for valuePatt in iterableExpression { body }
  for keyPatt => valuePatt in iterableExpression { body }
  for valuePatt in iterableExpression { body } catch p { catchblock }

.. syntax:: WhileExpr

   Sequence(
    "while", "(", NonTerminal('expr'), ")", NonTerminal('blockCatch'))

::

  while (test) { body }
  while (test) { body } catch p { catchblock }

.. syntax:: SwitchExpr

   Sequence(
    "switch", "(", NonTerminal('expr'), ")",
    "{", NonTerminal('matchers'), "}")

.. syntax:: matchers

   OneOrMore(Sequence("match",
             NonTerminal('pattern'),
             NonTerminal('block')))

::

  switch (candidate) { match p { body } ... }

.. syntax:: EscapeExpr

   Sequence(
    "escape", NonTerminal('pattern'),
    NonTerminal('blockCatch'))

::

  escape e { body } catch p { catchbody }

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

  try { block } catch p { catchblock1 } catch q { catchblock2 } finally { finblock }

.. syntax:: WhenExpr

   Sequence(
    "when",
    "(", OneOrMore(NonTerminal('expr'), ','), ")",
    "->", NonTerminal('block'),
    NonTerminal('catchers'))

::

  when (x, y) -> { whenblock } catch p { catchblock }

.. syntax:: LambdaExpr

   Sequence(
    "fn",
    ZeroOrMore(NonTerminal('pattern'), ','),
    NonTerminal('block'))

::

  /** docstring */ fn p, q { body }

.. todo:: doctest ``/** docstring */``

.. syntax:: block

   Sequence(
    "{",
    Choice(
        0,
        NonTerminal('sequence'),
        "pass"),
    "}")

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

.. syntax:: bind

   Sequence(
    "bind",
    NonTerminal('name'),
    Optional(NonTerminal('guard')), Comment("objectExpr@@"))

.. _def:

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

.. todo:: refactor w.r.t. FunctionExpr

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
