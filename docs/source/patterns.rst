.. _patterns:

Pattern matching
================

Monte comes with a powerful and extensible subsystem for destructuring and
viewing objects, called the **pattern subsystem**. A *pattern* is a rule which
conditionally matches objects and binds parts of the matched objects to names.

.. todo:: blend wizards text with doc text

.. todo:: change pseudocode into real code (updoc/doctest style)

.. todo:: document expansion of non-kernel patterns

.. todo:: consider the fate of this Pronounciation stuff

   Speak the name of the pattern, followed by "pattern": "This is a
   via pattern with a such-that pattern inside."

Usage
-----

There are five places where patterns are used:

Method parameters
~~~~~~~~~~~~~~~~~

Parameters to methods are patterns which are matched against
arguments. Match failure raises an exception.

.. todo:: fwd ref parameters?

Matchers
~~~~~~~~

::

  match patt {}

When 'match' is used in an object expression, 'patt' is
matched against a message (a [verb, arglist] pair) sent to the object.

.. todo:: fwd ref object expression?

def expressions
~~~~~~~~~~~~~~~

::

  def patt := val

The pattern 'patt' is matched against the object 'val' and an
exception is raised if the match fails.

::

  def patt exit e := val

The pattern 'patt' is matched against the object 'val' and the ejector
'e' is invoked if the match fails.

Match-bind expressions
~~~~~~~~~~~~~~~~~~~~~~

::

  val =~ patt

The pattern 'patt' is matched against the object 'val'. If the match
fails, 'false' is returned. On success, 'true' is returned.

::

  val !~ patt

The pattern 'patt' is matched against the object 'val'. If the match
fails, 'true' is returned. On success, 'false' is returned.

Switch expressions
~~~~~~~~~~~~~~~~~~

::

  switch (val) {
      match patt1 {}
      match patt2 {}
  }

The pattern 'patt1' is matched against the object 'val'. If the match
fails, the next matcher is invoked, matching 'patt2' against
'val'. The first pattern to match results in its associated block
being evaluated. If no patterns match, an exception is raised.

Patterns
--------

.. syntax:: pattern

   Choice(0,
          NonTerminal('namePatt'),
	  Choice(0,
	    NonTerminal('SamePatt'),
	    NonTerminal('NotSamePatt')),
          NonTerminal('QuasiliteralPatt'),
          NonTerminal('ViaPatt'),
          NonTerminal('IgnorePatt'),
          NonTerminal('ListPatt'),
          NonTerminal('MapPatt'),
          NonTerminal('SuchThatPatt'))

.. syntax:: namePatt

   Choice(0,
           NonTerminal('FinalPatt'),
           NonTerminal('VarPatt'),
           NonTerminal('BindPatt'),
           NonTerminal('SlotPatt'),
           NonTerminal('BindingPatt'))


FinalPatt (kernel)
~~~~~~~~~~~~~~~~~~~~~

::

  x
  ::"hello, world"
  x :G

.. syntax:: FinalPatt

   Ap('FinalPatt', NonTerminal('name'), NonTerminal('guardOpt'))

Final patterns match an object and bind a name to them, optionally
testing them for guard conformance. Guard conformance
failure causes pattern match failure.

Final
*****

::

    def name := value

One of the most ubiquitous patterns. Binds a name unconditionally to a
``FinalSlot`` and prohibits reassignment.

::

    def name :Guard := value

Like above, but coerced by a :ref:`guard <guards>`.


VarPatt (kernel)
~~~~~~~~~~~~~~~~

Var patterns match an object and bind a mutable name to them,
optionally testing them for guard conformance. Guard
conformance failure causes pattern match failure. Later assignments to
'x' will be tested for guard conformance as well.

Var
***

May be pronounced "var" or "variable".

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

.. syntax:: VarPatt

   Ap('VarPatt', Sigil("var", NonTerminal('name')), NonTerminal('guardOpt'))


BindPatt
~~~~~~~~

::

  bind x
  bind x ::"hello, world"
  bind x :G

Bind patterns match an object and bind it to a forward-declared name,
optionally testing for guard conformance.

.. syntax:: BindPatt

   Ap('BindPatt', Sigil("bind", NonTerminal('name')), NonTerminal('guardOpt'))


Expansion
*********

::

  >>> m`def bind x := 2`.expand()
  m`def via (_bind.run(x_Resolver, null)) _ := 2`

SlotPatt
~~~~~~~~

::

    def &name := slot

Slot patterns match an object and bind them to the slot of the
pattern's name, optionally testing the object for guard conformance.

.. syntax:: SlotPatt

   Ap('SlotPatt', Sigil("&", NonTerminal('name')), NonTerminal('guardOpt'))

Expansion
*********

::

  >>> m`def &x := 1`.expand()
  m`def via (__slotToBinding) &&x := 1`

BindingPatt (kernel)
~~~~~~~~~~~~~~~~~~~~

.. syntax:: BindingPatt

   Ap('BindingPatt', Sigil("&&", NonTerminal('name')))

::

  &&x
  &&::"hello, world"

Binding patterns match an object and use it as the binding for the
given name.

::

    def &&name := binding

A bind pattern does not bind a name, but binds a *binding*.



IgnorePatt (kernel)
~~~~~~~~~~~~~~~~~~~

::

  _
  _ :G

IgnorePattern matches an object, optionally requiring conformance to a
guard.

Ignore
******

::

    def _ := value

Equivalent to ``value``. Does nothing.

::

    def _ :Guard := value

Performs :ref:`guard <guards>` coercion and discards the result.

.. syntax:: IgnorePatt

   Ap('IgnorePatt', Sigil("_", NonTerminal('guardOpt')))


ListPatt (kernel)
~~~~~~~~~~~~~~~~~

::

  [p, q]
  [p, q] + rest

List patterns match lists, matching each subpattern against the items
in the list.  if '+' is used, a list pattern of size N is matched
against the first N items in the list, and the 'rest' pattern is
matched against the remaining items. If '+' is not used the list
pattern only matches lists of the same size.

Kernel list patterns do not allow '+ rest'.

List
****

::

    def [first, second] + tail := value

A list pattern has two pieces, the **head** and the **tail**, joined by ``+``.
This mirrors construction of a list via addition. The head can be any sequence
of patterns. The tail is an optional pattern and defaults to ``==[]``,
matching exactly the empty list.

List patterns match ``ConstLists`` of at least the same length as the head,
where each subpattern in the head matches the corresponding element in the
list. The rest of the list is collected into the tail and the tail pattern is
matched against it.

.. syntax:: ListPatt

   Ap('ListPatt',
     Brackets("[", SepBy(NonTerminal('pattern'), ','), ']'),
     Maybe(Sigil("+", NonTerminal('pattern'))))


MapPattern
~~~~~~~~~~

::

  ["k1" => p, (k2) => q]
  ["k1" => p := v1, (k2) => q := v2]
  ["k1" => p, "k2" => q] | rest
  [=> p, => q]

Map patterns match maps. Keys are either literal strings or
expressions in parentheses. The subpatterns are matched against the
values for the keys. ':=' may be used to specify a default value to
match a subpattern against if the key is absent.

.. index:: importer

The 'importer' syntax without keys is a shortcut for binding names
identical to string keys in a map; ``[=> x, => y]`` is equivalent to
``["x" => x, "y" => y]``.

Map
***

::

    def ["first" => second, "third" => fourth] | tail := value

Like a list pattern deconstructing a list, a map pattern deconstructs a ``ConstMap`` and gathers its values.

Keys can be literals (strings, integers, etc.) but cannot be patterns.

The tail of the map will be a map of the key/value pairs which were not
matched in the head. The tail pattern defaults to ``==[].asMap()``.

::

    # def ["first" => first, "second" => second] := value
    def [=> first, => second] := value

This short syntax for map patterns matches values where the keys are the
strings corresponding to the identifiers.

::

    def ["key" => patt := "default value"] := value

Any pair in a map pattern can have a default value using the above syntax.  In
this example, the ``patt`` subpattern will be asked to match against either
the value corresponding to ``"key"``, or ``"default value"``.

.. syntax:: MapPatt

   Ap('MapPatt',
     Brackets("[", SepBy(NonTerminal('mapPattItem'), ','), ']'),
     Maybe(Sigil("|", NonTerminal('pattern'))))

@@at least one item

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


SamePattern
~~~~~~~~~~~

::

  ==val

Same patterns match objects that compare same to their value.

Exactly
*******

::

    def ==specimen := value

Exactly patterns contain a single expression and match if (and only if)
``value == specimen`` according to typical Monte semantics.

While this particular formulation of an exactly pattern might not be very
useful, it can be handy as a pattern in switch expressions.

.. syntax:: SamePatt

   Ap('SamePatt', Sigil("==", NonTerminal('prim')))


NotSamePattern
~~~~~~~~~~~~~~

::

  !=val

Not-same patterns match objects that do not compare same to their value.

Not
***

::

    def !=specimen := value

Exactly patterns contain a single expression and match if (and only if)
``value != specimen`` according to typical Monte semantics.

.. syntax:: NotSamePatt

   Ap('NotSamePatt', Sigil("!=", NonTerminal('prim')))


QuasiliteralPatt
~~~~~~~~~~~~~~~~

::

  foo`some text @p more text @{q :G} ...`

Quasiliteral patterns invoke a quasiparser with text containing
pattern holes. The resulting matcher object is invoked with the object
to be matched, and the patterns in the holes are matched against the
specimens it extracts.

Quasiliteral
************

::

    def `$value holes and @pattern holes` := specimen

Any quasiliteral can be used as a pattern.


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

ViaPattern (kernel)
~~~~~~~~~~~~~~~~~~~

::

  via (a) p

Via
***

::

    def via (view) patt := value

Via patterns contain a **view** (sometimes called a **transformation**) and a
subpattern. The view is an expression which takes a specimen and ejector and
returns a transformed specimen on success or ejects on failure. This is
similar to a guard but permits much richer transformations in addition to
simple tests.

A via pattern matches if its view successfully transforms the specimen and the
subpattern matches the transformed specimen.

.. syntax:: ViaPatt

   Ap('ViaPatt',
     Sigil("via", Brackets("(", NonTerminal('expr'), ')')),
     NonTerminal('pattern'))


SuchThatPattern
~~~~~~~~~~~~~~~

::

  p ? a

Such-That
*********

::

    def patt ? (condition) := value

The such-that pattern contains a subpattern and a **condition**, not unlike
the condition expression in an ``if`` expression. The such-that pattern first
speculatively performs the pattern match in its subpattern, and then succeeds
or fails based on whether the condition evaluates to ``true`` or ``false``.

.. syntax:: SuchThatPatt

   Ap('SuchThatPatt', NonTerminal('pattern'),
      Sigil("?", Brackets("(", NonTerminal('expr'), ")")))
