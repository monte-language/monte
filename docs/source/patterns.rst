.. _patterns:

Pattern matching
================

Monte comes with a powerful and extensible subsystem for destructuring
and viewing objects. A :dfn:`pattern` is a rule which conditionally
matches objects and binds parts of the matched objects to names.

.. syntax:: pattern

   Choice(0,
          NonTerminal('postfixPatt'))

.. syntax:: postfixPatt

   Choice(0,
          NonTerminal('SuchThatPatt'),
          NonTerminal('prefixPatt'))

.. syntax:: prefixPatt

   Choice(0,
          NonTerminal('MapPatt'),
          NonTerminal('ListPatt'),
	  NonTerminal('SamePatt'),
	  NonTerminal('NotSamePatt'),
          NonTerminal('QuasiliteralPatt'),
          NonTerminal('ViaPatt'),
          NonTerminal('IgnorePatt'),
          NonTerminal('namePatt'))

.. syntax:: namePatt

   Choice(0,
           NonTerminal('FinalPatt'),
           NonTerminal('VarPatt'),
           NonTerminal('BindPatt'),
           NonTerminal('SlotPatt'),
           NonTerminal('BindingPatt'))

.. _SuchThatPattern:

The `Such-That` Pattern
-----------------------

.. syntax:: SuchThatPatt

   Ap('SuchThatPatt', NonTerminal('prefixPatt'),
      Sigil("?", Brackets("(", NonTerminal('expr'), ")")))

Non associative.

The such-that pattern contains a subpattern and a **condition**, not unlike
the condition expression in an ``if`` expression. The such-that pattern first
speculatively performs the pattern match in its subpattern, and then succeeds
or fails based on whether the condition evaluates to ``true`` or ``false``::
  
  >>> def players := [object alice{}, object bob{}]
  ...
  ... object game:
  ...     to vote(player ? (players.contains(player)),
  ...             choice ? (players.contains(choice))) :
  ...        return "voted"
  ...
  ... def t1 := game.vote(players[0], players[1])
  ... def t2 := try { game.vote(object alice{}, "bob") } catch _ { "BZZT!" }
  ... [t1, t2]
  ["voted", "BZZT!"]


SuchThat Expansion
~~~~~~~~~~~~~~~~~~

::
   
   >>> m`def patt ? (condition) := value`.expand()
   m`def via (_suchThat) [patt, via (_suchThat.run(condition)) _] := value`

.. _ListPatt:

List, Map Patterns
------------------

.. syntax:: ListPatt

   Ap('ListPatt',
     Brackets("[", SepBy(NonTerminal('pattern'), ','), ']'),
     Maybe(Sigil("+", NonTerminal('pattern'))))

.. syntax:: MapPatt

   Ap('MapPatt',
     Brackets("[", OneOrMore(NonTerminal('mapPattItem'), ','), ']'),
     Maybe(Sigil("|", NonTerminal('pattern'))))

.. syntax:: mapPattItem

   Ap('pair',
     Choice(0,
       Ap('Right', Ap('pair',
         Choice(0,
           NonTerminal('LiteralExpr'),
           Brackets("(", NonTerminal('expr'), ")")),
         Sigil("=>", NonTerminal('pattern')))),
       Ap('Left', Sigil("=>", NonTerminal('namePatt')))),
     Maybe(Sigil(":=", NonTerminal('order'))))

List patterns match lists, matching each subpattern against the items
in the list::

   >>> def [x, y] := [5, 10]; x
   5


If `+ rest` is used, a list pattern of size N is matched
against the first N items in the list, and the `rest` pattern is
matched against the remaining items.::

   >>> def [first] + rest := [1, 2, 3, 4]
   ... rest
   [2, 3, 4]

If ``+`` is not used, the list pattern only matches lists of the same size

Map patterns match maps. Keys are either literal strings or
expressions in parentheses. The subpatterns are matched against the
values for the keys::

  >>> def sides := ["square" => 4, "triangle" => 3]
  ... def shape := "triangle"
  ...
  ... def ["square" => squareSides, (shape) => qty1] := sides
  ...
  ... def ["triangle" => qty2] | _ := sides
  ...
  ... [squareSides, shape, qty1, qty2]
  [4, "triangle", 3, 3]

':=' may be used to specify a default value to match a subpattern
against if the key is absent::

  >>> def sides := ["square" => 4, "triangle" => 3]
  ...
  ... def ["octogon" => octoSides := 8] | _ := sides
  ... octoSides
  8

.. _importer:
.. index:: importer

The :dfn:`importer` syntax without keys is a shortcut for binding names
identical to string keys in a map::

    >>> def sides := ["square" => 4, "triangle" => 3]
    ...
    ... def [=> triangle, => square] := sides
    ... [triangle, square]
    [3, 4]

List Pattern Expansion
~~~~~~~~~~~~~~~~~~~~~~

::

   >>> m`def [item1, item2] + rest := stuff`.expand()
   m`def via (_splitList.run(2)) [item1, item2, rest] := stuff`

Map Pattern Expansion
~~~~~~~~~~~~~~~~~~~~~

::

   >>> m`def ["key" => patt] := data`.expand()
   m`def via (_mapExtract.run("key")) [patt, _ :_mapEmpty] := data`
   
   >>> m`def ["key1" => patt1] | rest := data`.expand()
   m`def via (_mapExtract.run("key1")) [patt1, rest] := data`

   >>> m`def ["key1" => patt1 := fallback] := data`.expand()
   m`def via (_mapExtract.withDefault("key1", fallback)) [patt1, _ :_mapEmpty] := data`

The Same and Not Same Patterns
------------------------------

Non-associative.

.. syntax:: SamePatt

   Ap('SamePatt', Sigil("==", NonTerminal('prim')))

.. syntax:: NotSamePatt

   Ap('NotSamePatt', Sigil("!=", NonTerminal('prim')))

Same patterns match objects that compare same to their value.

   >>> def state := "night"
   ...
   ... switch (state) {
   ...     match =="day" {"night"}
   ...     match =="night" {"day"}
   ... }
   "day"

Not-same patterns match objects that do not compare same to their value::

.. todo:: test "bigMoney" =~ !="bankrupt"


Exact Pattern Expansion
~~~~~~~~~~~~~~~~~~~~~~~

::

   >>> m`def ==specimen := value`.expand()
   m`def via (_matchSame.run(specimen)) _ := value`

   >>> m`def !=specimen := value`.expand()
   m`def via (_matchSame.different(specimen)) _ := value`


The `Quasi-Literal` Pattern
---------------------------

Non-associative.

.. syntax:: QuasiliteralPatt

   Ap('QuasiliteralPatt',
    Maybe(Terminal("IDENTIFIER")),
    Brackets('`',
    SepBy(
        Choice(0,
	  Ap('Left', Terminal('QUASI_TEXT')),
          Ap('Right',
            Choice(0,
              Ap('(\\n -> FinalPatt n Nothing)', Terminal('AT_IDENT')),
              Brackets('@{', NonTerminal('pattern'), '}'))))),
    '`'))

Quasiliteral patterns invoke a quasiparser with text containing
pattern holes. The resulting matcher object is invoked with the object
to be matched, and the patterns in the holes are matched against the
specimens it extracts::

    >>> "The cat and the hat." =~ simple`The cat and the @what.`
    true

    >>> "The cat and the hat." =~ `The cat and the @{what :Str}.`; what
    "hat"

    >>> "The cat and the hat." =~ simple`The cat and the @{what :Int}.`
    false

Quasi-Literal Pattern Expansion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   >>> m`def ``quasi @@patt`` := value`.expand()
   m`def via (_quasiMatcher.run(simple__quasiParser.matchMaker(_makeList.run("quasi ", simple__quasiParser.patternHole(0), "")), _makeList.run())) [patt] := value`

.. index:: view, transformation

The `via` Pattern
-----------------

.. syntax:: ViaPatt

   Ap('ViaPatt',
     Sigil("via", Brackets("(", NonTerminal('expr'), ')')),
     NonTerminal('pattern'))

Via patterns contain a :dfn:`view` (sometimes called a
:dfn:`transformation`) and a subpattern. The view is an expression
which takes a specimen and ejector and returns a transformed specimen
on success or ejects on failure. This is similar to a guard but
permits much richer transformations in addition to simple tests::

  >>> def via (_splitList.run(1)) [x, xs] := [1, 2, 3]
  ... [x, xs]
  [1, [2, 3]]


.. _FinalPatt:

FinalPatt (kernel)
~~~~~~~~~~~~~~~~~~~~~

.. syntax:: FinalPatt

   Ap('FinalPatt', NonTerminal('name'), NonTerminal('guardOpt'))

Final patterns match an object and bind a name to them, optionally
testing them for guard conformance.  One of the most ubiquitous
patterns. Binds a name unconditionally to a ``FinalSlot`` and
prohibits reassignment::

    def name := value

Guard conformance failure causes pattern match failure::

    def name :Guard := value

::

  ::"hello, world"

The `var` Pattern (kernel)
--------------------------

.. syntax:: VarPatt

   Ap('VarPatt', Sigil("var", NonTerminal('name')), NonTerminal('guardOpt'))


Var patterns match an object and bind a mutable name to them,
optionally testing them for guard conformance. Guard
conformance failure causes pattern match failure. Later assignments to
'x' will be tested for guard conformance as well.

::

    var name := value
    var name :Guard := value

Like a final pattern, but with ``VarSlot`` as the slot, which permits
reassignment to the name later on using an assign expression.

.. note::

    While ``var`` can be used to introduce a var pattern, the overall
    expression is still a def expression, and it can alternatively be
    expressed as::

        def var name := value

    This is useful for nesting var patterns within other patterns::

        def [first, var second] := value

Bind Pattern
------------

.. syntax:: BindPatt

   Ap('BindPatt', Sigil("bind", NonTerminal('name')), NonTerminal('guardOpt'))

Bind patterns match an object and bind it to a forward-declared name,
optionally testing for guard conformance.

::

  bind x
  bind x ::"hello, world"
  bind x :G

Expansion
~~~~~~~~~

::

  >>> m`def bind x := 2`.expand()
  m`def via (_bind.run(x_Resolver, null)) _ := 2`

Slot Pattern
------------

.. syntax:: SlotPatt

   Ap('SlotPatt', Sigil("&", NonTerminal('name')), NonTerminal('guardOpt'))

Slot patterns match an object and bind them to the slot of the
pattern's name, optionally testing the object for guard conformance.

::

    def &name := slot


Slot Pattern Expansion
~~~~~~~~~~~~~~~~~~~~~~

::

  >>> m`def &x := 1`.expand()
  m`def via (_slotToBinding) &&x := 1`

Binding Pattern (kernel)
------------------------

.. syntax:: BindingPatt

   Ap('BindingPatt', Sigil("&&", NonTerminal('name')))

Binding patterns match an object and use it as the binding for the
given name.

::

  &&x
  &&::"hello, world"

A bind pattern does not bind a name, but binds a *binding*.

::

    def &&name := binding

Ignore Pattern (kernel)
-----------------------

.. syntax:: IgnorePatt

   Ap('IgnorePatt', Sigil("_", NonTerminal('guardOpt')))

::

  _
  _ :G

IgnorePattern matches an object, optionally requiring conformance to a
guard.

::

    def _ := value

Equivalent to ``value``. Does nothing.

::

    def _ :Guard := value

Performs :ref:`guard <guards>` coercion and discards the result.
