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

The for-loop
------------

The simple structure of the ``for`` loop should be familiar in structure to
Python programmers::

    for value in iterable:
        traceln(value)

A ``for`` loop takes an iterable object and a pattern, and matches each
element in the iterable to the pattern, executing the body of the loop.
``for`` loops permit skipping elements with the ``continue`` keyword::

    for value in iterable:
        if skippable(value):
            continue

They also permit exiting prematurely with the ``break`` keyword::

    for value in iterable:
        if finalValue(value):
            break

All builtin containers are iterable, including lists, maps, and sets. Strings
are also iterable, yielding characters.

For Loop Patterns
~~~~~~~~~~~~~~~~~

``for`` loops are pattern-based, so arbitrary patterns are permitted in
loops::

    for some`$sort of @pattern` in iterable:
        useThat(pattern)

Pair Syntax and Keys
~~~~~~~~~~~~~~~~~~~~

Unlike other languages, Monte iteration always produces a pair of objects at a
time, called the **key** and **value**. A bit of syntax enables
pattern-matching on the key::

    for key => value in iterable:
        traceln(key)
        traceln(value)

As expected, the key for iteration on a map is the key in the map
corresponding to each value. The key for iteration on lists and strings is the
zero-based index of each item or character::

   >>> for i => each in ["a", "b"]:
   ...     traceln(`Index: $i Value: $each`)
   null

It is possible to iterate only over the keys, of course, using an ignore
pattern::

    for key => _ in iterable:
        traceln(key)


Iteration Protocol
~~~~~~~~~~~~~~~~~~

You can create your own data structures over which the for loop can iterate. An example of such a structure, and a brief explanation of the iterate(function) method you need to implement, can be found in the Library Packages: emakers section later in this chapter, where we build a simple queue object.


The Secret Lives of Flow Control Structures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Flow control structures actually return values. For example, the if-else returns the last value in the executed clause:

 # E sample
 def a := 3
 def b := 4
 def max := if (a > b) {a} else {b}

This behavior is most useful when used with the when-catch construct described in the chapter on :ref:`distributed-computing`.
The break statement, when used in a for or a while loop, can be followed by an expression, in which case the loop returns the value of that expression.

.. sidebar:: ternary conditional expression

   While monte does not have the ``c ? x : y`` ternary conditional
   operator, the ``if`` expression works just as well. For example, to
   tests whether ``i`` is even::

     >>> { def i := 3; if (i % 2 == 0) { "yes" } else { "no" } }
     "no"

   Don't forget that Monte requires ``if`` expressions to evaluate
   their condition to a ``Bool``::

     ▲> if (1) { "yes" } else { "no" }
     Parse error: Not a boolean!

.. _loopExpr:

Loops as Expressions
~~~~~~~~~~~~~~~~~~~~

Like all structures in Monte, ``for`` loops are expressions, which means that
they can return values and be used where other expressions are used.

A ``for`` loop usually returns ``null``::

    def result := for value in 0..10 { value }

Here, ``result`` is ``null``.

However, a ``for`` loop can return another value with the ``break`` keyword::

    def result := for value in 0..10 { break value }

Since ``break`` was used, the loop exits on its first iteration, returning
``value``, which was ``0``. So ``result`` is ``0``.

.. note::

    The syntax of ``break`` permits parentheses around the return value, like
    ``break(this)``, and also an empty pair of parentheses to indicate a null
    return value, like so: ``break()``.

.. _comprehension:

Comprehensions
~~~~~~~~~~~~~~

``for`` loops aren't the only way to consume iterable objects. Monte also has
**comprehensions**, which generate new collections from iterables::

    [transform(value) for value in iterable]

This will build and return a list. Maps can also be built with pair syntax::

    [key => makeValue(key) for key in keyList]

And, of course, pair syntax can be used for both the pattern and expression in
a comprehension::

    [value => key for key => value in reverseMap]

Comprehensions also support *filtering* by a condition. The conditional
expression is called a **predicate** and should return ``true`` or ``false``,
depenting on whether the current value should be *skipped*. For example, let's
generate a list of even numbers::

    def evens := [number for number in 0..20 if number % 2 == 0]

Unlike many other languages, the predicate must return a Boolean value; if it
doesn't, then the entire comprehension will fail with an exception.
