.. _ordinary-programming:

====================
Ordinary Programming
====================

.. note:: In case you skipped the introduction, this is a last
           reminder that the fireworks start with
           :ref:`distributed-computing`, and you can go there now, or
           continue to read about normal, ordinary computing in E,
           starting with Hello World.

Hello World
===========

We will show Hello World as both a Monte module and at the REPL. REPL
first::

  ▲ traceln("Hello World")
  TRACE: ["Hello World"]
  Result: null

As a Monte module, it looks like::

  def main():
      traceln("Hello World")

.. todo:: document how to compile and run such a hello-world script.


Simple data types, simple control flow
--------------------------------------

Here are some of the basics of the language::

  >>> # Comment on this piece of code
  ...
  ... def a := 3
  ... var b := a + 2
  ... b += 1
  ... if (a < b):
  ...     traceln("a is less than b")
  ... else:
  ...    traceln("Wow, the arithmetic logic unit in this processor is confused")
  null

Variable declarations are made with the ``var`` statement. Variables that are
only assigned a value once at creation (i.e., constants, or variables declared
final) are created with the def statement. In Monte, as in Python, "+=" is
shorthand for adding the righthand value to the lefthand variable.

Single-line comments have a ``#`` at the beginning, and terminate with
the end of line. The ``/**...*/`` comment style is used only for writing
javadoc-style comments, discussed later.

.. todo:: document docstrings

Assignment uses the ``:=`` operator. The single equal sign ``=`` is never
legal in Monte; use ``:=`` for assignment and ``==`` for testing
equality. The function ``traceln`` sends diagnostic output to the
console. The ``if`` statement looks just like its Python equivalent.

.. todo:: Introduce Monte's haskell-style brace-or-indent blocks;
          contrast with Python

.. todo:: "What is the end-of-statement delineator in Monte?"

As with Python, a backslash (``\``) as the final character of a line
escapes the newline and causes that line and its successor to be
interpereted as one::

 ▲ def c := 1 + 2 \
 ...   + 3 + 4
 Result: 10

Indentation
~~~~~~~~~~~

Each form with braces can also be written as an indented block.

Standardize your indentation to use spaces, because tabs are a syntax error in
Monte. Monte core library code uses four-space indentation. However, any
indentation can be used as long as it's consistent throughout the module.


Basic Types and Operators
~~~~~~~~~~~~~~~~~~~~~~~~~

The basic types in Monte are ``Int``, ``Double``, ``Str``, ``Char``, and
``Boolean``. All integer arithmetic is unlimited precision, as if all
integers were longs.

Doubles are represented as 64-bit IEEE floating point numbers. The
operators ``+``, ``-``, ``*`` have their traditional meanings for integers and
floats. The normal division operator ``/`` always gives you a floating
point result. The floor divide operator ``//`` always gives you an
integer, truncated towards negative infinity. So::

  >>> -3.5 // 1
  -4

The Monte modulo operator, ``%``, like the Python modulo operator, returns the
remainder of division that truncates towards zero.

Operator precedence is generally the same as in Java, Python, or C. In
a few cases, Monte will throw a syntax error and require the use of
parentheses.

Monte's quasi-literals enable the easy processing of complex strings
as described in detail later; here is a very simple example::

 >>> def x := 3
 ... `Value of x is: $x`
 "Value of x is: 3"

wherein the back-ticks denote a quasi-literal, and the dollar sign
denotes a variable whose value is to be embedded in the string.

``+`` when used with strings is a concatenation operator as in Python. Unlike
Java, it does *not* automatically coerce other types on the right-hand if the
left-hand operand is a string.

``&&`` and ``||`` and ``!`` have their traditional meanings for booleans;
``true`` and ``false`` are boolean constants.

Strings are enclosed in double quotes. Characters are enclosed in
single quotes, and the backslash acts as an escape character as in
Java, and C: '\n' is the newline character, and '\\' is the backslash
character.

``==`` and ``!=`` are the boolean tests for equality and inequality
respectively. When the equality test is used between appropriately
designated :ref:`transparent immutables<selfless>`, such as
integers, the values are compared to see if the values are equal; for
other objects the references are compared to see if both the left and
right sides of the operator refer to the same object. Chars, booleans,
integers, and floating point numbers are all compared by value, as are
Strings, ConstLists, and ConstMaps.

Additional useful features of transparent immutables are discussed
under :ref:`distributed-computing`.

There are some special rules about the behavior of the basic operators
because of E's distributed security. These rules are described in the
Under the :ref:`Under the Covers<under-cover-objects>` section later
in this chapter.

.. _modules:

Using Monte Modules
-------------------

*TODO: just document using modules here; move other stuff*

A Monte module is a single file. The last statement in the file describes what
it exports. If the last statement in a file defines a method or object, that
method or object is what you get when you import it. If you want to export
several objects from the same file, the last line in the file should simply be
a list of their names.

To import a module, simply use ``def bar = import("foo")`` where the filename of
the module is foo.mt. See the files module.mt and imports.mt for an example of
how to export and import objects.



Ordinary Computing Examples
===========================

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
