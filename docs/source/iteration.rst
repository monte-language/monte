.. _blocks:

Building objects: blocks and scopes
===================================

Indentation
-----------

Each form with braces can also be written as an indented block.

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

Does Monte have functions?
--------------------------

No. Since everything in Monte is an object, you're always calling methods
rather than functions.

Monte does have a convention that objects with a single method with the verb
``run`` are functions. There is no difference, to Monte, between this
function::

    def f():
        pass

And this object::

    object f:
        to run():
            pass

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

Where did ``self`` go?
----------------------

Newcomers to Monte are often surprised to learn that Monte lacks a ``this`` or
``self`` keyword. In fact, Monte does have ways to refer to the current object,
but there's a deeper conceptual difference between Monte and other object-based
languages.

Monte does not have a ``this`` or ``self`` keyword because Monte objects can
refer to their "member" or "private" names without qualification. This is a
consequence of how Monte objects are built. Consider this object maker::

    def makeMyObject():
        return object myObject:
            pass

Let's modify it slightly. We want to give this object a "private" value secret
which cannot be accessed directly, and a method ``getSecret/0`` which will
return it. We put "private" in quotation marks to emphasize that Monte does not
have private names. Instead, all names are private in Monte; if one cannot see
a name, then one cannot access it.

::

    def makeMyObject(secret):
        return object myObject:
            to getSecret():
                return secret

And that's it. No declarations of object contents or special references to ``this``
or ``self``.

We can also simulate "member" names for objects. As before, we can achieve
this effect without ``this``.

::

    def makeMyObject():
        var counter :Int := 0
        return object myObject:
            to getCounter():
                return counter += 1

Here, ``counter`` is not visible outside of ``makeMyObject()``, which means
that no other object can directly modify it. Each time we call
``makeMyObject()``, we get a new object called ``myObject`` with a new counter.

.. note::
    Remember, Monte is an expression language. ``counter += 1`` returns the
    value of ``counter``. That's why ``return counter += 1`` works.

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

What are ejectors?
------------------

An ejector is an object that aborts the current computation and returns to
where it was created. They are created by ``escape`` expressions.

An ejector can be passed as deeply as one wants, but cannot be used outside of
the ``escape`` that created it. This is called the **delimited** property of
ejectors.

Ejectors cannot be used multiple times. The first time an ejector is used, the
``escape`` block aborts computation, resulting in the value of the ejector.
Subsequent clever uses of the ejector will fail. This is called the **single
use** property.

Monte implements the ``return``, ``break``, and ``continue`` expressions with
ejectors.

To be fully technical, ejectors are "single-use delimited continuations".

Block Syntax Summary
--------------------

.. syntax:: FunctionExpr

   Sequence('def', '(', ZeroOrMore(NonTerminal('pattern'), ','), ')',
     NonTerminal('block'))

::

  def fun(p, q) :optionalGuard { body }

.. syntax:: ObjectExpr

   Sequence(
    "object",
    Choice(0, Sequence("bind", NonTerminal('name')),
           "_",
           NonTerminal('name')),
    Optional(NonTerminal('guard')), Comment("objectExpr"))

.. syntax:: objectExpr

   Sequence(
    Optional(Sequence('extends', NonTerminal('order'))),
    NonTerminal('auditors'),
    '{', ZeroOrMore(NonTerminal('objectScript'), ';'), '}')

.. syntax:: objectScript

   Sequence(
    Optional(NonTerminal('doco')),
    Choice(0, "pass", ZeroOrMore("@@meth")),
    Choice(0, "pass", ZeroOrMore(NonTerminal('matchers'))))

.. syntax:: matchers

   OneOrMore(Sequence("match",
             NonTerminal('pattern'),
             NonTerminal('block')))

.. syntax:: doco

   Terminal('.String')

::

  object foo {
      to someMethod(p, q) {
          methBody
      }
  
      method rawMethod(p, q) {
          methBody
      }
       match [verb, arglist] {
           matcherBody
       }
  }
  object foo as someAuditor { ... }
  object foo implements firstAuditor, secondAuditor { ... }
  object foo extends baz { ... }

  /** doc string */
  object foo as someAuditor implements firstAuditor, secondAuditor extends baz { ... }

.. syntax:: InterfaceExpr

   Sequence('@@@@@')

::

  interface Foo { to interfaceMethod(p, q) { ... } }
  interface Foo guards FooStamp { ... }

.. todo:: interface syntax diagram

.. syntax:: IfExpr

   Sequence(
    "if", "(", NonTerminal('expr'), ")", NonTerminal('block'),
    Optional(Sequence("else", Choice(
        0, Sequence("if", Comment('blockExpr@@')),
        NonTerminal('block')))))

::

  if (test) { consq } else if (test2) { consq2 } else { alt }

.. todo:: report bug with else if blockExpr

.. syntax:: ForExpr

   Sequence(
    "for",
    NonTerminal('pattern'),
    Optional(Sequence("=>", NonTerminal('pattern'))),
    "in", NonTerminal('comp'),
    NonTerminal('blockCatch'))

.. syntax:: blockCatch

   Sequence(
    NonTerminal('block'),
    Optional(
        Sequence("catch", NonTerminal('pattern'),
                 NonTerminal('block'))))

::

  for valuePatt in iterableExpression { body }
  for keyPatt => valuePatt in iterableExpression { body }
  for valuePatt in iterableExpression { body } catch p { catchblock }

.. syntax:: WhileExpr

   Sequence(
    "while", "(", NonTerminal('expr'), ")", NonTerminal('blockCatch'))

::

  while (test) { body }
  while (test) { body } catch p { catchblock }

.. syntax:: SwitchExpr

   Sequence(
    "switch", "(", NonTerminal('expr'), ")",
    "{", NonTerminal('matchers'), "}")

.. syntax:: matchers

   OneOrMore(Sequence("match",
             NonTerminal('pattern'),
             NonTerminal('block')))

::

  switch (candidate) { match p { body } ... }

.. syntax:: EscapeExpr

   Sequence(
    "escape", NonTerminal('pattern'),
    NonTerminal('blockCatch'))

::

  escape e { body } catch p { catchbody }

.. syntax:: TryExpr

   Sequence(
    "try", NonTerminal('block'), NonTerminal('catchers'))

.. syntax:: catchers

   Sequence(
    ZeroOrMore(Sequence("catch",
                        NonTerminal('pattern'),
                        NonTerminal('block'))),
    Optional(Sequence("finally", NonTerminal('block'))))

::

  try { block } catch p { catchblock1 } catch q { catchblock2 } finally { finblock }

.. syntax:: WhenExpr

   Sequence(
    "when",
    "(", OneOrMore(NonTerminal('expr'), ','), ")",
    "->", NonTerminal('block'),
    NonTerminal('catchers'))

::

  when (x, y) -> { whenblock } catch p { catchblock }

.. syntax:: LambdaExpr

   Sequence(
    "fn",
    ZeroOrMore(NonTerminal('pattern'), ','),
    NonTerminal('block'))

::

  /** docstring */ fn p, q { body }

.. todo:: doctest ``/** docstring */``

.. syntax:: MetaExpr

   Sequence(
    "meta", ".",
    Choice(0,
           Sequence("context", "(", ")"),
           Sequence("getState", "(", ")")))

::

  meta.getState()
  meta.context()

.. syntax:: block

   Sequence(
    "{",
    Choice(
        0,
        ZeroOrMore(
            Choice(
                0,
                NonTerminal('blockExpr'),
                NonTerminal('expr')),
            ";"),
        "pass"),
    "}")

.. syntax:: blockExpr

   Choice(
    0,
    NonTerminal('FunctionExpr'),
    NonTerminal('ObjectExpr'),
    NonTerminal('bind'),
    NonTerminal('def'),
    NonTerminal('InterfaceExpr'),
    NonTerminal('IfExpr'),
    NonTerminal('ForExpr'),
    NonTerminal('WhileExpr'),
    NonTerminal('SwitchExpr'),
    NonTerminal('EscapeExpr'),
    NonTerminal('TryExpr'),
    NonTerminal('WhenExpr'),
    NonTerminal('LambdaExpr'),
    NonTerminal('MetaExpr'))

.. syntax:: expr

   Choice(
    0,
    NonTerminal('assign'),
    Sequence(
        Choice(0, "continue", "break", "return"),
        Choice(0,
               Sequence("(", ")"),
               ";",
               NonTerminal('blockExpr'))))

.. syntax:: bind

   Sequence(
    "bind",
    NonTerminal('name'),
    Optional(NonTerminal('guard')), Comment("objectExpr@@"))

.. syntax:: name

   Choice(0, "IDENTIFIER", Sequence("::", ".String."))

.. syntax:: def

   Sequence(
    "def",
    Choice(
        0,
        Sequence(
            Choice(
                0,
                Sequence("bind", NonTerminal("name"),
                         Optional(NonTerminal('guard'))),
                NonTerminal("name")),
            Choice(0, Comment("objectFunction@@"), NonTerminal('assign'))),
        NonTerminal('assign')))

.. todo:: refactor w.r.t. FunctionExpr

.. syntax:: comprehension

   Choice(
    0,
    Sequence(NonTerminal('pattern'),
             "in", NonTerminal('iter'),
             NonTerminal('expr')),
    Sequence(NonTerminal('pattern'), "=>", NonTerminal('pattern'),
             "in", NonTerminal('iter'),
             NonTerminal('expr'), "=>", NonTerminal('expr')))

.. syntax:: iter

   Sequence(
    NonTerminal('order'),
    Optional(Sequence("if", NonTerminal('comp'))))
