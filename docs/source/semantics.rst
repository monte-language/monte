==================
Semantics of Monte
==================

This is a brief attempt to detail the evaluation semantics of well-formed
Monte code.

Monte is an object-based expression language which computes by delivering
**messages** to **objects**. During computation, expressions are evaulated,
resulting in either success or failure; successful evaluation yields an
object, while failing evaluation yields an exceptional state.

Kernel-Monte
============

Monte is designed not to be interpreted immediately, but to be reduced
("**expanded**") into a core form called "Kernel-Monte". Kernel-Monte is
smaller than Monte and thus easier to work with, although it lacks most of the
rich expressiveness of Monte.

.. todo::
    Detail semantics of full Monte and not just Kernel-Monte.

Monte as a Tree
===============

Kernel-Monte is specified as an abstract syntax tree. Each node in the tree
represents either an **expression** or a **pattern**. Expressions can be
evaluated to product an object; patterns do not produce values but alter the
current scope.

Along with every node, there is a **static scope**, a compile-time constant
mapping of names to declaration and usage sites. For every expression, it is
known which names are visible and whether they were declared with `def` or
`var`.

Computation proceeds by tree evaluation; the root of the tree is evaluated,
which in turn can provoke evaluation of various branch and leaf nodes as
required.

Scope Introduction & Dismissal
==============================

Many expressions, during evaluation, introduce scopes. When this is done,
names declared after scope introduction are said to be **visible** within the
scope. An expression must pair every scope introduction with a scope
dismissal. After a scope has been dismissed, the names declared within the
scope are no longer visible.

.. note::
    This scoping rule is often called "lexical scoping" and should be familiar
    to users of other lexically-scoped languages.

.. _no_stale_stack_frames:

Monte has a rule known as **"no stale stack frames"**. Inherited from E, the
rule is simple to state: *No Monte expression shall require a scope to be
dismissed by any expression other than itself.* It requires that every
expression bookend its own scope introduction and dismissals.

Names, Nouns, Slots, Bindings
=============================

Monte has a complex system underlying names.

A name is an identifier which refers to a value. Syntactically, there are
three representations of names, and each one refers to a different level of
abstraction.

At the highest level are nouns. Nouns refer directly to values. Nouns in
patterns match values, and nouns in expressions evaluate to the values to
which they refer.

Next are slots. Slots refer to nouns and also the guard which guards the noun.
Slots are also objects which can be accessed and manipulated with slot
patterns and slot expressions. This level of indirection permits access to
guards, and also enables pointer-like reification of nouns.

Finally, at the bottom, Monte has bindings. A binding is a slot for a slot; it
refers to a slot and also the slot guard, which guards that the slot is a
final slot, var slot, etc. Bindings are essential to auditors.

Expressions
===========

Literals
--------

.. _Null:

Null
~~~~

Produces ``null``.

Char
~~~~

Produces an object which passes ``Char``.

Double
~~~~~~

Produces an object which passes ``Double``.

Int
~~~

Produces an object which passes ``Int``.

Str
~~~

Produces an object which passes ``Str``.

Names
-----

Binding
~~~~~~~

Produces the binding for the given name.

Noun
~~~~

Produces the noun for the given name.

Assign
~~~~~~

Assign-exprs have a name and an expression. The expression is evaluated and
the result is both assigned to the name as a noun in the current scope and the
produced value.

If the name's slot is not assignable, an error is thrown.

Def
~~~

Def-exprs have a pattern, an exit expression, and a specimen expression. The
specimen is evaluated, followed by the exit. The specimen is unified with the
pattern, defining names into the surrounding scope. The produced value is the
specimen.

If unification fails, the result of the exit expression is used as an ejector
to escape; if ejecting fails, then an error is thrown.

Hide
~~~~

Hide-exprs have a single subexpression which is evaluated in a fresh scope.
The produced value of the subexpression is used as the produced value.

Message Passing
---------------

Call
~~~~

Call-exprs have a receiver expression, a verb, some argument expressions, and
some named argument expressions. The receiver is evaluated, then each
argument, and then each named argument. Then, the verb, arguments, and named
arguments are packed into a message and passed to the receiver. The value
returned from the receiver is the produced value.

Control Flow
------------

.. _Escape:

Escape
~~~~~~

Escape-exprs have a pattern and inner expression, as well as a catch pattern
and catch expression (not to be confused with :ref:`Try`/catch expressions).
An ejector is created and a scope is introduced. The ejector is unified with
the pattern and then the inner expression is evaluated. The scope is then
dismissed and the produced value from the inner expression is used as the
produced value of the entire escape-expr.

If the ejector is called within the inner expression, then control immediately
leaves the inner expression and the scope is dismissed. The value passed to
the ejector is used as a specimen and unified with the catch pattern in a
freshly-introduced scope, and then the catch expression is evaluated. Finally,
the catch scope is dismissed and the produced value from the catch expression
is used as the produced value of the escape-expr.

EscapeOnly
~~~~~~~~~~

Escape-only-exprs are just like escape-exprs but only have a single pattern
and expression. A scope is introduced, an ejector is unified with the pattern,
and the expression is evaluated and used as the produced value. If the ejector
is called with a value, then the passed value is immediately used as the
produced value.

.. note::
    EscapeOnly is used to overcome a deficiency in an earlier version of
    Kernel-Monte where :ref:`Escape` could be in an indeterminate state. It is
    functionally identical to Escape with a trivial catch-block.

Finally
~~~~~~~

Finally-exprs contain two expressions. The first expression is evaluated in a
fresh scope. Then, the second expression is evaluated in a fresh scope and its
produced value is the produced value of the entire finally-expr.

The second expression is evaluated even if evaluation is in a failing state
after evaluating the first expression.

If
~~

If-exprs have a test expression, a consequent expression, and an alternative
expression. A scope is introduced, and then the test expression is evaluated,
producing a value which passes ``Bool``. Either the consequent or the
alternative is evaluated and used as the produced value, depending on whether
the test produced ``true`` or ``false``. Finally, the scope is dismissed.

If the test's produced value does not conform to ``Bool``, an error is thrown.

Sequence
~~~~~~~~

Sequence-exprs contain zero or more expressions.

If a sequence-expr contains zero expressions, then it evaluates identically to
:ref:`Null` expressions.

If a sequence-expr contains exactly one expression, it evalutes identically to
that single inner expression.

Otherwise, a sequence-expr evaluates each of its inner expressions in
sequential order, using the final expression's produced value as the produced
value of the entire sequence.

.. _Try:

Try
~~~

Try-exprs have an expression and a catch pattern and expression. The first
expression is evaluated in a fresh scope and used as the produced value.

If an error is thrown in the first expression, then the scope is dismissed, a
new scope is introduced, the error is unified with the catch pattern, and the
catch expression is evaluated and used as the produced value.

Objects
-------

Matcher
~~~~~~~

Matcher-exprs have a pattern and an expression. A scope is introduced and
incoming messages are unified with the pattern. If the unification succeeds,
the expression is evaluated and its produced value is returned to the caller.

Method
~~~~~~

Method-exprs have a verb, a list of argument patterns, a list of named
argument patterns, a guard expression, and a body expression. When a message
matches the verb of the method, a scope is introduced and each pattern is
unified against the message. Each argument pattern is unified against each
argument, and then each named argument pattern is unified against each named
argument.

If unification fails, an error is thrown.

After unification, the guard expression is evaluated and its produced value is
stored for return value guarding. The body expression is evaluated and its
produced value is given as a specimen to the return value guard. The returned
prize from the guard is returned to the caller.

If the return value guard fails, an error is thrown.

.. note::
    The return value guard is evaluated before the body, but called after the
    body.

Object
~~~~~~

Object-exprs have a pattern, a list of auditor expressions, a list of methods,
and a list of matchers. When evaluated, a new object with the methods and
matchers is created. That object is audited by each auditor in sequential
order. The first auditor, if present, is used as the guard for the object.
Finally, the object is unified with its pattern in the surrounding scope.

Objects close over all of the names which are visible in their scope.
Additionally, objects close over the names defined in the object-expr's
pattern.

Patterns
========

Pattern evaluation centers around **unification**. During unification,
patterns are given a specimen and an ejector. Patterns examine the specimens
and create names in the surrounding scope. When patterns fail to unify,
the ejector is fired. If the ejector fails to leave control, then an error is
thrown.

Pattern Nodes
-------------

Ignore
~~~~~~

Ignore-patts coerce their specimen with a guard.

Bind
~~~~

Bind-patts coerce their specimen with a guard and bind the resulting prize as
a binding.

Final
~~~~~

Final-patts coerce their specimen with a guard and bind the resulting prize
into a final slot.

Var
~~~

Var-patts coerce their specimen with a guard and bind the resulting prize into
a var slot.

List
~~~~

List-patts have a list of subpatterns. List-patts coerce their specimen to a
``List`` and match the elements of the specimen to each subpattern, in
sequential order.

If the list-patt and specimen are different lengths, then unification fails.

Via
~~~

Via-patts contain an expression and a subpattern. The specimen and ejector are
passed to the expression's produced value, and the result is unified with the
subpattern.
