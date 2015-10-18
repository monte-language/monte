.. _patterns:

Pattern matching
================

Patterns attempt to match objects and either succeed or fail.

.. todo:: blend wizards text with doc text

.. todo:: change pseudocode into real code (updoc/doctest style)

.. todo:: document expansion of non-kernel patterns

Monte comes with a powerful and extensible subsystem for destructuring and
viewing objects, called the **pattern subsystem**. A *pattern* is a rule which
conditionally matches objects and binds parts of the matched objects to names.

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
          NonTerminal('namePattern'),
	  Choice(0,
	    NonTerminal('SamePattern'),
	    NonTerminal('NotSamePattern')),
          NonTerminal('QuasiLiteralPattern'),
          NonTerminal('ViaPattern'),
          NonTerminal('IgnorePattern'),
          NonTerminal('ListPattern'),
          NonTerminal('MapPattern'),
          NonTerminal('SuchThatPattern'))

.. syntax:: namePattern

   Choice(0,
           NonTerminal('FinalPattern'),
           NonTerminal('VarPattern'),
           NonTerminal('BindPattern'),
           NonTerminal('SlotPattern'),
           NonTerminal('BindingPattern'))


FinalPattern (kernel)
~~~~~~~~~~~~~~~~~~~~~

::

  x
  ::"hello, world"
  x :G

.. syntax:: FinalPattern

   Sequence(Choice(0, "IDENTIFIER", ".String."),
                    Optional(NonTerminal('guard')))

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


VarPattern (kernel)
~~~~~~~~~~~~~~~~~~~

.. syntax:: VarPattern

   Sequence("var", NonTerminal('name'),
            Optional(NonTerminal('guard')))

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

BindPattern
~~~~~~~~~~~

.. syntax:: BindPattern

   Sequence("bind", NonTerminal('name'),
       Optional(NonTerminal('guard')))

::

  bind x
  bind x ::"hello, world"
  bind x :G

Bind patterns match an object and bind it to a forward-declared name,
optionally testing for guard conformance.

Expansion
*********

::

  >>> m`def bind x := 2`.expand()
  m`def via (_bind.run(x_Resolver, null)) _ := 2`


SlotPattern
~~~~~~~~~~~

.. syntax:: SlotPattern

   Sequence("&", NonTerminal('name'),
       Optional(NonTerminal('guard')))

::

    def &name := slot

Slot patterns match an object and bind them to the slot of the
pattern's name, optionally testing the object for guard conformance.

Expansion
*********

::

  >>> m`def &x := 1`.expand()
  m`def via (__slotToBinding) &&x := 1`

BindingPattern (kernel)
~~~~~~~~~~~~~~~~~~~~~~~

.. syntax:: BindingPattern

   Sequence("&&", NonTerminal('name'))

::

  &&x
  &&::"hello, world"

Binding patterns match an object and use it as the binding for the
given name.

::

    def &&name := binding

A bind pattern does not bind a name, but binds a *binding*.



IgnorePattern (kernel)
~~~~~~~~~~~~~~~~~~~~~~

.. syntax:: IgnorePattern

   Sequence("_", Optional(NonTerminal('guard')))

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


ListPattern (kernel)
~~~~~~~~~~~~~~~~~~~~

.. syntax:: ListPattern

   Sequence("[",
            ZeroOrMore(NonTerminal('pattern'), ','),
            ']',
            Optional(Sequence("+", NonTerminal('pattern'))))

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

MapPattern
~~~~~~~~~~

.. syntax:: MapPattern

   Sequence("[",
            OneOrMore(NonTerminal('mapPatternItem'), ','),
            ']',
            Optional(Sequence("|", NonTerminal('pattern'))))

.. syntax:: mapPatternItem

   Sequence(
        Choice(0,
               Sequence("=>", NonTerminal('namePattern')),
               Sequence(
                 Choice(0,
		   Choice(0, ".String.", ".int.", ".float64.", ".char."),
                   Sequence("(", NonTerminal('expr'), ")")),
                 "=>", NonTerminal('pattern'))),
        Optional(Sequence(":=", NonTerminal('order'))))

.. syntax:: mapItem

   Choice(
        0,
        Sequence("=>", Choice(
            0,
            Sequence("&", NonTerminal('name')),
            Sequence("&&", NonTerminal('name')),
            NonTerminal('name'))),
        Sequence(NonTerminal('expr'), "=>", NonTerminal('expr')))

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

SamePattern
~~~~~~~~~~~

.. syntax:: SamePattern

   Sequence("==", NonTerminal('prim'))

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

NotSamePattern
~~~~~~~~~~~~~~

.. syntax:: NotSamePattern

   Sequence("!=", NonTerminal('prim'))

::

  !=val

Not-same patterns match objects that do not compare same to their value.

Not
***

::

    def !=specimen := value

Exactly patterns contain a single expression and match if (and only if)
``value != specimen`` according to typical Monte semantics.

QuasiliteralPattern
~~~~~~~~~~~~~~~~~~~

.. syntax:: QuasiliteralPattern

   Sequence(
    Optional(Terminal("IDENTIFIER")),
    '`',
    ZeroOrMore(
        Choice(0, Comment('...text...'),
               Choice(
                   0,
                   Terminal('@IDENT'),
                   Sequence('@{', NonTerminal('pattern'), '}')))),
    '`')

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


ViaPattern (kernel)
~~~~~~~~~~~~~~~~~~~

.. syntax:: ViaPattern

   Sequence("via", "(", NonTerminal('expr'), ')',
            NonTerminal('pattern'))

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


SuchThatPattern
~~~~~~~~~~~~~~~

.. syntax:: SuchThatPattern

   Sequence(NonTerminal('pattern'), "?", "(", NonTerminal('expr'), ")")

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

CallPattern
~~~~~~~~~~~

a(p, q)

.. todo:: check whether this is implemented.
