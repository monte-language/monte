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

    for value in (iterable):
        traceln(value)

A ``for`` loop takes an iterable object and a pattern, and matches each
element in the iterable to the pattern, executing the body of the loop.
``for`` loops permit skipping elements with the ``continue`` keyword::

    for value in (iterable):
        if skippable(value):
            continue

They also permit exiting prematurely with the ``break`` keyword::

    for value in (iterable):
        if finalValue(value):
            break

All builtin containers are iterable, including lists, maps, and sets. Strings
are also iterable, yielding characters.

For Loop Patterns
~~~~~~~~~~~~~~~~~

``for`` loops are pattern-based, so arbitrary patterns are permitted in
loops::

    for some`$sort of @pattern` in (iterable):
        useThat(pattern)

Pair Syntax and Keys
~~~~~~~~~~~~~~~~~~~~

Unlike other languages, Monte iteration always produces a pair of objects at a
time, called the **key** and **value**. A bit of syntax enables
pattern-matching on the key::

    for key => value in (iterable):
        traceln(key)
        traceln(value)

As expected, the key for iteration on a map is the key in the map
corresponding to each value. The key for iteration on lists and strings is the
zero-based index of each item or character::

   >>> for i => each in (["a", "b"]):
   ...     traceln(`Index: $i Value: $each`)
   null

It is possible to iterate only over the keys, of course, using an ignore
pattern::

    for key => _ in (iterable):
        traceln(key)


Iteration Protocol
~~~~~~~~~~~~~~~~~~

You can create your own data structures over which the for loop can iterate. An example of such a structure, and a brief explanation of the iterate(function) method you need to implement, can be found in the Library Packages: emakers section later in this chapter, where we build a simple queue object.


The Secret Lives of Flow Control Structures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Flow control structures actually return values. For example, the if-else returns the last value in the executed clause::

 def a := 3
 def b := 4
 def max := if (a > b) {a} else {b}

This behavior is most useful when used with the when-catch construct described in the :ref:`when-delay` section.
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

    def result := for value in (0..10) { value }

Here, ``result`` is ``null``.

However, a ``for`` loop can return another value with the ``break`` keyword::

    def result := for value in (0..10) { break value }

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

    [for value in (iterable) transform(value)]

This will build and return a list. Maps can also be built with pair syntax::

    [for key in (keyList) key => makeValue(key)]

And, of course, pair syntax can be used for both the pattern and expression in
a comprehension::

    [for key => value in (reverseMap) value => key]

Comprehensions also support *filtering* by a condition. The conditional
expression is called a **predicate** and should return ``true`` or ``false``,
depenting on whether the current value should be *skipped*. For example, let's
generate a list of even numbers::

    >>> def evens := [for number in (1..10) if (number % 2 == 0) number]
    ... evens
    [2, 4, 6, 8, 10]

Unlike many other languages, the predicate must return a Boolean value; if it
doesn't, then the entire comprehension will fail with an exception.


Writing Your Own Iterables
--------------------------

Monte has an iteration protocol which defines iterable and iterator objects.
By implementing this protocol, it is possible for user-created objects to be
used in ``for`` loops and comprehensions.

Iterables need to have ``to _makeIterator()``, which returns an iterator.
Iterators need to have ``to next(ej)``, which takes an ejector and either
returns a list of ``[key, value]`` or fires the ejector with any value to end
iteration. Guards do not matter but can be helpful for clarity.

As an example, let's look at an iterable that counts upward from zero to
infinity::

    object countingIterable:
        to _makeIterator():
            var i := 0
            return object counter:
                to next(_):
                    def rv := [i, i]
                    i += 1
                    return rv

Since the iterators ignore their ejectors, iteration will never terminate.

For another example, let's look at an iterator that wraps another iterator and
only lets even values through::

    def onlyEvens(iterator):
        return object evens:
            to next(ej):
                var rv := iterator.next(ej)
                while (rv[1] % 2 != 0):
                    rv := iterator.next(ej)
                return rv

Note that the ejector is threaded through ``to next(ej)`` into the inner
iterator in order to allow iteration to terminate if/when the inner iterator
becomes exhausted.
