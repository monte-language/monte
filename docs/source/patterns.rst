.. _patterns:

Patterns
========

Monte comes with a powerful and extensible subsystem for destructuring and
viewing objects, called the **pattern subsystem**. A *pattern* is a rule which
conditionally matches objects and binds parts of the matched objects to names.

Pronounciation
--------------

Speak the name of the pattern, followed by "pattern": "This is a via pattern
with a such-that pattern inside."

All Patterns
------------

An exhaustive list of all patterns available in Monte is provided. They are
all shown in the context of the ``def`` expression.

Kernel Patterns
---------------

These patterns are core to the Monte language and are present even in compiled
code. They cannot be reimplemented in terms of other Monte code.

Ignore
~~~~~~

::

    def _ := value

Equivalent to ``value``. Does nothing.

::

    def _ :Guard := value

Performs :ref:`guard <guards>` coercion and discards the result.

Final
~~~~~

::

    def name := value

One of the most ubiquitous patterns. Binds a name unconditionally to a
``FinalSlot`` and prohibits reassignment.

::

    def name :Guard := value

Like above, but coerced by a :ref:`guard <guards>`.

Var
~~~

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

Bind
~~~~

::

    def &&name := binding

A bind pattern does not bind a name, but binds a *binding*.

List
~~~~

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

Via
~~~

::

    def via (view) patt := value

Via patterns contain a **view** (sometimes called a **transformation**) and a
subpattern. The view is an expression which takes a specimen and ejector and
returns a transformed specimen on success or ejects on failure. This is
similar to a guard but permits much richer transformations in addition to
simple tests.

A via pattern matches if its view successfully transforms the specimen and the
subpattern matches the transformed specimen.

Non-Kernel Patterns
-------------------

These richer patterns permit more powerful destructuring and are safe to use
alongside kernel patterns.

Exactly
~~~~~~~

::

    def ==specimen := value

Exactly patterns contain a single expression and match if (and only if)
``value == specimen`` according to typical Monte semantics.

While this particular formulation of an exactly pattern might not be very
useful, it can be handy as a pattern in switch expressions.

Not
~~~

::

    def !=specimen := value

Exactly patterns contain a single expression and match if (and only if)
``value != specimen`` according to typical Monte semantics.

Such-That
~~~~~~~~~

::

    def patt ? (condition) := value

The such-that pattern contains a subpattern and a **condition**, not unlike
the condition expression in an ``if`` expression. The such-that pattern first
speculatively performs the pattern match in its subpattern, and then succeeds
or fails based on whether the condition evaluates to ``true`` or ``false``.

Map
~~~

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

Quasiliteral
~~~~~~~~~~~~

::

    def `$value holes and @pattern holes` := specimen

Any quasiliteral can be used as a pattern.

Slot
~~~~

::

    def &name := slot

The slot pattern, like the bind pattern, allows definition of the slot behind
a name.

Pattern Syntax Reference
------------------------

.. syntax:: pattern

   Diagram(Sequence(
        Choice(0,
               NonTerminal('namePattern'),
               NonTerminal('quasiLiteral'),
               Sequence(Choice(0, "==", "!="), NonTerminal('prim')),
               Sequence("_", Optional(NonTerminal('guard'))),
               Sequence("via", "(", NonTerminal('expr'), ')',
                        NonTerminal('pattern')),
               Sequence("[",
                        ZeroOrMore(NonTerminal('pattern'), ','),
                        ']',
                        Optional(Sequence("+", NonTerminal('pattern')))),
               Sequence("[",
                        OneOrMore(NonTerminal('mapPatternItem'), ','),
                        ']',
                        Optional(Sequence("|", NonTerminal('pattern'))))),
        Optional(Sequence("?", "(", NonTerminal('expr'), ")"))))

.. syntax:: namePattern

   Diagram(
    Choice(0,
           Sequence(Choice(0, "IDENTIFIER", ".String.")),
                    Optional(NonTerminal('guard'))),
           Sequence("var", NonTerminal('noun'),
                    Optional(NonTerminal('guard'))),
           Sequence("&", NonTerminal('noun'),
                    Optional(NonTerminal('guard'))),
           Sequence("bind", NonTerminal('noun'),
                    Optional(NonTerminal('guard'))),
           Sequence("&&", NonTerminal('noun')))

.. syntax:: mapPatternItem

   Diagram(Sequence(
        Choice(0,
               Sequence("=>", NonTerminal('namePattern')),
               Sequence(Choice(0,
                               Sequence("(", NonTerminal('expr'), ")"),
                               ".String.", ".int.", ".float64.", ".char."),
                        "=>", NonTerminal('pattern'))),
        Optional(Sequence(":=", NonTerminal('order')))))

.. syntax:: mapItem

   Diagram(Choice(
        0,
        Sequence("=>", Choice(
            0,
            Sequence("&", NonTerminal('noun')),
            Sequence("&&", NonTerminal('noun')),
            NonTerminal('noun'))),
        Sequence(NonTerminal('expr'), "=>", NonTerminal('expr'))))
