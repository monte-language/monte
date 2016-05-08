Loops and the Iteration Protocol
================================

Monte has only two kinds of looping constructs: ``for`` loops, which consume
iterators to process a series of elements, and ``while`` loops, which
repeatedly consider a predicate before doing work. Both should be familiar to
any experienced programmer; let's explore them in greater detail.

``for`` loops
-------------

A ``for`` loop is a simple structure that takes an iterable object and loops
over it::

    var x := 0
    for i in (1..10):
        x += i

Here, we can clearly see the three elements of the ``for`` loop, the
*pattern*, ``x``; the *iterable*, ``1..10``, and the loop's *body*,
``x += i``. For each element in the iterable, the iterable is matched against
the pattern, which is available within the body.

Within a ``for`` loop, the ``continue`` keyword will skip the current
iteration of the loop, and ``break`` keyword will exit the loop altogether::

    # Skip the even elements, and give up if we find multiples of three.
    for i in (1..10):
        if (i % 2 == 0):
            continue
        if (i % 3 == 0):
            break
        x -= i

Pair Patterns
~~~~~~~~~~~~~

All iterables yield not just one element, but a *pair* of elements on every
iteration. To access both elements at once, we can use a *pair pattern*::

    def names := ["Scooby", "Shaggy", "Velma"]
    for i => name in (names):
        traceln(`Name $i: $name`)

For a list, like in the previous example, the right-hand side of the pair
matches the current element, and the left-hand side matches that element's
index. When iterating over a map, the pair will match the key and value::

    def animals := [
        "Bagira"     => "panther",
        "Baloo"      => "bear",
        "Shere Khan" => "tiger",
    ]
    for animal => species in (animals):
        traceln(`Animal $animal is a $species`)

``while`` loops
---------------

In addition to the ``for`` loop, Monte provides a ``while`` loop::

    var x := 1
    while (x < 402):
        x *= 2

The ``while`` loop admits ``continue`` and ``break``, just like in ``for``
loops.

Advanced Looping
----------------

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

     >>> { def c := 'c'; if (c < 'e') { "Yay!" } else { "Nope" } }
     "Nope"

.. _loopExpr:

Loops as Expressions
~~~~~~~~~~~~~~~~~~~~

Like all structures in Monte, ``for`` loops are expressions; they return
values::

    def result := for value in (0..10) { value }

Here, ``result`` is ``null``, which is the default return value for ``for``
loops. To override that value, use ``break``::

    def result := for value in (0..10) { break value }

Since ``break`` was used, the loop exits on its first iteration, returning
``value``, which was ``0``. So ``result`` is ``0``.

.. _comprehension:

List & Map Comprehensions
~~~~~~~~~~~~~~~~~~~~~~~~~

``for`` loops aren't the only way to consume iterable objects. Monte also has
**comprehensions**, which generate new collections from iterables::

    [for value in (iterable) transform(value)]

This will build and return a list. Maps can also be built with pair syntax::

    [for key in (keyList) key => makeValue(key)]

And, of course, pair syntax can be used for both the pattern and expression in
a comprehension::

    [for key => value in (reverseMap) value => key]

Additionally, just like in Python and Haskell, comprehensions support
filtering with a predicate; this is called the *for-such* comprehension::

    >>> def evens := [for number in (1..10) ? (number % 2 == 0) number]
    ... evens
    [2, 4, 6, 8, 10]

Just like the `such-that pattern`, this such-that clause is evaluated for
every iteration, and iterations where the clause returns ``false`` are
skipped. Also, just like the such-that pattern, and unlike some other
languages' comprehension syntax, the predicate must return a ``Bool``; if it
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
