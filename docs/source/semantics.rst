.. index:: object, semantics, evaluation semantics

==================
Semantics of Monte
==================

This is a brief specification of the evaluation semantics of Monte.

Monte is an object-based expression language which computes by delivering
:ref:`messages<message>` to :dfn:`objects`. During computation, expressions
are evaulated, resulting in either success or failure; successful evaluation
yields an object, while failing evaluation yields an exceptional state.


.. index:: Kernel-Monte, syntactic expansion
.. _kernel:

Kernel-Monte
============

The Monte language as seen by the programmer has the rich set of syntactic
conveniences expected of a modern scripting language. However, to be secure,
Monte must have a simple analyzable semantics. We reconcile these by defining
a subset of the full language called :dfn:`Kernel-Monte`, and only this subset
need be given a rigorous semantics. The rest of Monte is defined by syntactic
expansion to this subset.

Full-Monte
----------

We define :dfn:`Full-Monte` as the complete AST of Monte, and :dfn:`canonical
expansion` as the syntactic expansion which expands Full-Monte to Kernel-Monte
while preserving the intended semantics.

.. note::
    Full-Monte should get its own page and have all of its rich semantics
    spelled out in gory detail.


.. index:: expression, pattern, scope, static scope, abstract syntax

Monte as a Tree
===============

.. _left_to_right:

.. sidebar:: Left-to-Right Rule

    The :dfn:`left-to-right` rule states that *evaluation proceeds lexically
    from left to right.* This rule is violated only rarely:

    * At the kernel level, `DefExpr` evaluates both its RHS and exit before
      any expressions buried in the LHS pattern. Canonical expansion from
      Full-Monte to Kernel-Monte resolves any recursively-defined names in
      order to make this less unintuitive.
    * Object literals have their auditors evaluated before object creation and
      their patterns are unified after object creation.

Kernel-Monte is specified as an abstract syntax tree (AST). Each node in the
tree is either an :dfn:`expression` or a :dfn:`pattern`. Expressions can be
evaluated to product an object; patterns do not produce values but
:dfn:`unify` with values (i.e. objects) to introduce names into scopes.

Along with every node, there is a :dfn:`static scope`, a compile-time constant
mapping of names to declaration and usage sites. For every expression, it is
known which names are visible and whether they were declared with `def` or
`var`.

Computation proceeds by tree evaluation; the root of the tree is evaluated,
which in turn can provoke evaluation of various branch and leaf nodes as
required.

Recursion in a Monte AST is possible via self-reference; all object patterns
are visible within their corresponding script's scope.


.. index:: lexical scoping, stale stack frames

Scope Introduction & Dismissal
==============================

.. _no_stale_stack_frames:

.. sidebar:: No Stale Stack Frames Rule
   
    The :dfn:`no stale stack frames` rule states that *A Monte expression must
    dismiss any scope which it introduces.*

    A stale stack frame is one that isn't currently running; it is neither the
    current stack frame nor below the current stack frame.

    Monte forbids suspending computation mid-frame. There are no coroutines or
    undelimited continuations in Monte. Monte also does not have an
    "async/await" syntax, since there is no way to implement this syntax
    without stale stack frames. As a direct result, no partial execution can
    ever require a Monte implementation to reify stack frames for suspended
    computation.

    The policy is justified by readability concerns. Since Monte permits
    mutable state, one author's code's behavior could be affected by another
    author's code running further up the frame stack. Stale frames make
    comprehension of code much harder as a result.

Many expressions, during evaluation, introduce scopes. When this is done,
names declared after scope introduction are said to be :dfn:`visible` within
the scope. An expression must pair every scope introduction with a scope
dismissal. After a scope has been dismissed, the names declared within the
scope are no longer visible.

.. note::
    This scoping rule is often called "lexical scoping" and should be familiar
    to users of other lexically-scoped languages.

.. index:: name, noun, slot, binding

Names: Nouns, Slots, and References
===================================

Monte has a complex system underlying names.

A :dfn:`noun` is an identifier which refers to a value (an object). There are
three senses of reference from nouns to values, each at a different level of
abstraction.

At the simplest level, nouns refer directly to values. Identifiers in patterns
match values, and nouns in expressions evaluate to the values to which they
were matched.

To represent mutable state, we indirect via slots. :dfn:`Slots` are objects
that contain values and may be updated over time (much like pointers in
C). Slots can be accessed and manipulated with slot patterns and slot
expressions. A final slot acts as though nouns refer directly to values, while
a var slot has a ``put`` operation that updates its value.

A :dfn:`binding` is a slot along with a guard that constrains the values in
the slot. Bindings are essential to :ref:`auditors<auditors>`.

To allow references across turns and vats, we indirect via :ref:`references
<references>`.

Exceptions
==========

A Monte expression can yield either a successful result or an exceptional
state. Exceptional states are intentionally vague; they are usually
represented as panics in virtual machines or stack unwinders in interpreters.

While in an exceptional state, most expressions evaluate to that same
exceptional state. A `TryExpr` can replace an exceptional state with a
successful result. A `FinallyExpr` can perform some side computation despite
an exceptional state.

When an error is thrown, the computation switches to an exceptional state and
the thrown error is sealed in an implementation-dependent manner.

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

Produces an object which passes ``Char`` and corresponds to the Unicode
codepoint of the `CharExpr`.

Double
~~~~~~

Produces an object which passes ``Double`` and corresponds to the IEEE 754
double-precision floating-point number of the `DoubleExpr`.

.. note::
    Implementations may, at their discretion, substitute any higher-precision
    IEEE 754 number for the given one.

Int
~~~

Produces an object which passes ``Int`` and corresponds to the integer of the
`IntExpr`.

Str
~~~

Produces an object which passes ``Str`` and corresponds to the sequence of
Unicode codepoints of the `StrExpr`.  .

The string of codepoints is not normalized; it corresponds one-to-one with the
codepoints in the Monte source literal.

Names
-----

Binding
~~~~~~~

Produces the binding for the given noun.

.. todo:: discuss SlotExpr

Noun
~~~~

Produces the value in the slot of the given noun.

Assign
~~~~~~

An `AssignExpr` has a name and an expression. The expression is evaluated and
the result is both assigned to the name as a noun in the current scope and the
produced value.

If the name's slot is not assignable, an error is thrown.

Def
~~~

A `DefExpr` has a pattern, an (optional) exit expression, and a specimen
expression. The specimen is evaluated, followed by the exit (if present). The
specimen is unified with the pattern, defining names into the surrounding
scope. The produced value is the specimen.

If unification fails, the result of the exit expression is used as an ejector
to escape; if ejecting fails, then an error is thrown.

Hide
~~~~

A `HideExpr` has a single subexpression which is evaluated in a fresh scope.
The produced value of the subexpression is used as the produced value.

.. _message:
.. index:: message

Message Passing
---------------

Call
~~~~

A `CallExpr` has a receiver expression, a :dfn:`verb` (string), some argument
expressions, and some named argument expressions. The receiver is evaluated,
then each argument, and then each named argument. Then, a :dfn:`message`
consisting of the verb, arguments, and named arguments is passed to the
receiver. The value returned from the receiver is the produced value.

.. todo:: discuss sameness and doctest `_equalizer`

Control Flow
------------

.. index:: ejector
.. _Escape:

Escape
~~~~~~

.. _ejector:

.. sidebar:: Ejectors

             An ejector is an object whose ``run`` method aborts the current
             computation and returns to where the ejector was created.

             Monte implements the ``return``, ``break``, and ``continue``
             expressions with ejectors.

             Ejectors are so-called `single-use, delimited continuations`:
             their dynamic scope is delimited to downward method calls only,
             and any use after the first will fail.

An `EscapeExpr` has a pattern and inner expression and, optionally, a catch
pattern and catch expression (not to be confused with :ref:`Try`/catch
expressions).

An ejector is created and a scope is introduced. The ejector is unified with
the pattern and then the inner expression is evaluated.

If the ejector was not called during evaluation of the inner expression, the
scope is then dismissed and the produced value from the inner expression is
used as the produced value of the entire `EscapeExpr`.

If the ejector is called within the inner expression, then control immediately
leaves the inner expression and the scope is dismissed; if there is no catch
pattern/expression, then the value passed to the ejector is immediately used
as the produced value. Otherwise, the value passed to the ejector is used as a
specimen and unified with the catch pattern in a freshly-introduced scope, and
then the catch expression is evaluated. Finally, the catch scope is dismissed
and the produced value from the catch expression is used as the produced value
of the escape-expr.

Finally
~~~~~~~

A `FinallyExpr` contain two expressions. The first expression is evaluated in
a fresh scope and its resulting object or failing state is retained. Then, the
second expression is evaluated in a fresh scope. Finally, the retained state
from the first expression, success or failure, is the produced value of the
entire finally-expr.

The second expression is evaluated regardless of whether the first expression
returns an exceptional state; its state is discarded. It is
implementation-dependent whether exceptional states are chained together.

.. sidebar:: Chained Exceptions

    Why doesn't Monte require chained exceptions? In many languages, the
    exception from the first part of a finally-expr would have a chain
    including the exception from the second part of the finally-expr. This
    faciliates debugging.

    Since Monte doesn't offer tools for digging into exceptional states beyond
    catching them as a reified but opaque value, there is little point in
    mandating implementation details for that value. Instead, one might expect
    unsafe names like `unsealException` to have standard behavior, and that
    behavior might include exposing a possibly-empty list of chained
    exceptions. This isn't currently the case, but it might be in the future.

This table shows the possible states:

======= ========= =======
`try`   `finally` result
======= ========= =======
success success   success
error   success   error
success error     error
error   error     error
======= ========= =======

If
~~

An `IfExpr` has a test expression, a consequent expression, and an alternative
expression. A scope is introduced, and then the test expression is evaluated,
producing a value which passes ``Bool``. Either the consequent or the
alternative is evaluated and used as the produced value, depending on whether
the test produced ``true`` or ``false``. Finally, the scope is dismissed.

If the test's produced value does not conform to ``Bool``, an error is thrown.

Sequence
~~~~~~~~

A `SequenceExpr` contains zero or more expressions.

If a `SequenceExpr` contains zero expressions, then it evaluates to `null`.

Otherwise, a `SequenceExpr` evaluates each of its inner expressions in
sequential order, using the final expression's produced value as the produced
value of the entire sequence.

.. _Try:

Try
~~~

A `TryExpr` has an expression and a catch pattern and expression. The first
expression is evaluated in a fresh scope and used as the produced value.

If an error is thrown in the first expression, then the scope is dismissed, a
new scope is introduced, the error is unified with the catch pattern, and the
catch expression is evaluated and used as the produced value.


Objects
-------

Evaluation of a message sent to an object proceeds as follows.

Matcher
~~~~~~~

A matcher has a pattern and an expression. A scope is introduced and incoming
messages are unified with the pattern. If the unification succeeds, the
expression is evaluated and its produced value is returned to the caller.

Method
~~~~~~

A method has a verb, a list of argument patterns, a list of named argument
patterns, a guard expression, and a body expression. When a message matches
the verb of the method, a scope is introduced and each pattern is unified
against the message. Each argument pattern is unified against each argument,
and then each named argument pattern is unified against each named argument.

If the number of arguments in the message differs from the number of argument
patterns in the method, an error is thrown. Informally, the method and message
must have the same arity.

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

An `ObjectExpr` has a pattern, a list of auditor expressions, a list of
methods, and a list of matchers. When evaluated, a new object with the methods
and matchers is created. That object is audited by each auditor in sequential
order. Finally, the object is unified with its pattern in the surrounding
scope, and the first auditor, if present, is used as the guard for the
binding.

Objects close over all of the names which are visible in their scope.
Additionally, objects close over the names defined in the pattern of the
`ObjectExpr`.

.. index:: unification
.. _unification:
   
Patterns
========

Pattern evaluation is a process of :dfn:`unification`. During unification,
patterns are given a specimen and an ejector. Patterns examine the specimens
and create names in the surrounding scope. When patterns fail to unify, the
ejector is fired. If the ejector fails to leave control, then an error is
thrown.

Pattern Nodes
-------------

Ignore
~~~~~~

An `IgnorePatt` coerces its specimen with a guard.

Binding
~~~~~~~

A `BindingPatt` coerces its specimen with the ``Binding`` guard and binds the
resulting prize as a binding.

Final
~~~~~

A `FinalPatt` coerces its specimen with a guard and binds the resulting prize
into a final slot.

Var
~~~

A `VarPatt` coerces its specimen with a guard and binds the resulting prize
into a var slot.

List
~~~~

A `ListPatt` has a list of subpatterns. It coerces its specimen to a ``List``
and matches the elements of the specimen to each subpattern, in sequential
order.

If the `ListPatt` and specimen are different lengths, then unification fails.

Via
~~~

A `ViaPatt` contains an expression and a subpattern. The specimen and ejector
are passed to the expression's produced value, and the result is unified with
the subpattern.
