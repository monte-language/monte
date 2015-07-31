Building objects: blocks and scopes
===================================

Comments
--------

This is a single-line comment::

    # Lines starting with a # are single-line comments.
    # They only last until the end of the line.

And this is a multi-line comment::

    /** This comment is multi-line.
        Yes, it starts with two stars,
        but ends with only one.
        These should only be used for docstrings. */


Indentation
-----------

Standardize your indentation to use spaces, because tabs are a syntax error in
Monte. Monte core library code uses four-space indentation. However, any
indentation can be used as long as it's consistent throughout the module.

Everything is an object. New objects are created with a ``object`` keyword::

    object helloThere:
        to greet(whom):
            traceln(`Hello, my dear $whom!`)

    helloThere.greet("Student")

Objects can also be created by functions::

    def makeSalutation(time):
        return object helloThere:
            to greet(whom):
                traceln(`Good $time, my dear $whom!`)

    def hi := makeSalutation("morning")

    hi.greet("Student")

Object Composition
------------------

Monte has a simpler approach to object composition and inheritance than many
other object-based and object-oriented languages. Instead of classes or
prototypes, Monte has a simple single syntax for constructing objects, the
object expression::

    object myObject:
        pass

Unlike Java, Monte objects are not constructed from classes. Unlike JavaScript
or Python, Monte objects are not constructed from prototypes. As a result, it
might not be obvious at first how to build multiple objects which are similar
in behavior. However, Monte has a very simple idiom for class-like constructs.

::

    def makeMyObject():
        return object myObject:
            pass

Methods can be attached to objects with the to keyword::

    object deck:
        to size():
            return 52

Finally, just like with functions, methods can have guards on their parameters
and return value::

    object deck:
        to size(suits :Int, ranks :Int) :Int:
            return suits * ranks

for loops
---------

.. code-block:: monte

    for a => b in c: 

is equivalent to

.. code-block:: python

    for a, b in c.items():


Scoping Rules
-------------

Monte is lexically scoped, with simple scoping rules. In general, names are
only accessible within the scope in which they were defined.

After an object has been created, the names visible to it aren't accessible
from outside the object. This is because Monte objects cannot share their
internal state; they can only respond to messages. For programmers coming from
object-oriented languages with access modifiers, such as ``private`` and
``protected``, this is somewhat like if there were only one access modifier
for variables, ``private``. (And only one access modifier for methods,
``public``.)

Closing Over Bindings
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: monte

    var x := 42
    object obj:
        to run():
            return x += 1

Here, ``obj`` can see ``x``, permitting the usage of ``x`` within ``obj``'s
definition. When ``obj.run()`` is called, ``x`` will be mutated. Monte does
not require any "global" or "nonlocal" keywords to do this.

Using Monte Modules
-------------------

*TODO: just document using modules here; move other stuff*

A Monte module is a single file. The last statement in the file describes what
it exports. If the last statement in a file defines a method or object, that
method or object is what you get when you import it. If you want to export
several objects from the same file, the last line in the file should simply be
a list of their names.

To import a module, simply use `def bar = import("foo")` where the filename of
the module is foo.mt. See the files module.mt and imports.mt for an example of
how to export and import objects.

Iteration Protocol
------------------

Monte comes with a simple and robust iteration protocol.

The for-loop
~~~~~~~~~~~~

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
zero-based index of each item or character.

It is possible to iterate only over the keys, of course, using an ignore
pattern::

    for key => _ in iterable:
        traceln(key)

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

Writing Your Own Iterables
~~~~~~~~~~~~~~~~~~~~~~~~~~

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
