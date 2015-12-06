.. _ordinary-programming:

.. note:: In case you skipped the introduction, this is a last
           reminder that the fireworks start with
           :ref:`distributed-computing`, and you can go there now, or
           continue to read about normal, ordinary computing in E,
           starting with Hello World.

Hello World
-----------

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

  >>> # E sample
  ... # Comment on this piece of code
  ...
  ... def a := 3
  ... var b := a + 2
  ... b += 1
  ... if (a < b):
  ...     traceln("a is less than b")
  ... else:
  ...    traceln("Wow, the arithmetic logic unit in this processor is confused")

Variable declarations are made with the `var` statement. Variables
that are only assigned a value once at creation (i.e., constants, or
variables declared final) are created with the def statement. In Monte as
in python, "+=" is shorthand for adding the righthand value to the
lefthand variable.

Single-line comments have a `#` at the beginning, and terminate with
the end of line. The `/**...*/` comment style is used only for writing
javadoc-style comments, discussed later.

.. todo:: document docstrings

Assignment uses the `:=` operator. The single equal sign `=` is never
legal in Monte; use `:=` for assignment and `==` for testing
equality. The function `traceln` sends diagnostic output to the
console. The `if` statement looks just like its python equivalent.

.. todo:: Introduce Monte's haskell-style brace-or-indent blocks;
          contrast with python

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

The basic types in Monte are `Int`, `Double`, `Str`, `Char`, and
`Boolean`. All integer arithmetic is unlimited precision, as if all
integers were longs.

Doubles are represented as 64-bit IEEE floating point numbers. The
operators `+`, `-`, `*` have their traditional meanings for integers and
floats. The normal division operator `/` always gives you a floating
point result. The floor divide operator `//` always gives you an
integer, truncated towards negative infinity. So::

  >>> -3.5 // 1
  -4

The Monte modulo operator, `%`, like the python modulo operator,
returns the remainder of division that truncates towards zero.

Operator precedence is generally the same as in Java, Python, or C. In
a few cases, Monte will throw a syntax error and require the use of
parentheses.

Monte's quasi-literals enable the easy processing of complex strings
as described in detail later; here is a very simple example::

 >>> def x := 3
 >>> def printString := `Value of x is: $x`

wherein the back-ticks denote a quasi-literal, and the dollar sign
denotes a variable whose value is to be embedded in the string.

`+` when used with strings is a concatenation operator as in
python. Unlike Java, it does *not* automatically coerce other types on
the right-hand if the left-hand operand is a string.

`&&` and `||` and `!` have their traditional meanings for booleans;
`true` and `false` are boolean constants.

Strings are enclosed in double quotes. Characters are enclosed in
single quotes, and the backslash acts as an escape character as in
Java, and C: '\n' is the newline character, and '\\' is the backslash
character.

`==` and `!=` are the boolean tests for equality and inequality
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

Additional flow of control
--------------------------

We have already seen the if/then/else structure. Other traditional
structures include:

 - `while (booleanExpression) {...}`
 - `try{...} catch errorVariable {...} finally{...}`
 - `throw (ExceptionExpressionThatCanBeAString)`
 - `break` (which jumps out of a while or for loop; if the break
   keyword is followed by an expression, that expression is returned
   as the value of the loop)
 - `continue` (which jumps to the end of a while or for, and starts
   the next cycle)
 - `switch (expression) {match==v1{...} match==v2{...}
   ... match _{defaultAction}}`

One structure that is more powerful
   than its Java counterpart is the for loop.

 # E sample
 for i in 1..3 {
    println(i)
 }
 for j in ["a", 1, true] {println(j)}


In this simple example, i becomes 1, 2, 3 in succession. In the
second, j becomes each of the elements of the list.

The for loop operates not only with number ranges, but also with
lists, maps (i.e. hashtables), text files, directories, and other
structures discussed later in this book. The expanded version of the
for loop that is needed to get both keys and values out of maps is:

 # E syntax
 for key => value in theMap {
     println(`Key: $key Value: $value`)
 }
 # You can get the index and the value from a list at the same time the same way
 for i => each in ["a", "b"] {
     println(`Index: $i Value: $each`)
 }


You can create your own data structures over which the for loop can iterate. An example of such a structure, and a brief explanation of the iterate(function) method you need to implement, can be found in the Library Packages: emakers section later in this chapter, where we build a simple queue object.
The Secret Lives of Flow Control Structures
Flow control structures actually return values. For example, the if-else returns the last value in the executed clause:

 # E sample
 def a := 3
 def b := 4
 def max := if (a > b) {a} else {b}

This behavior is most useful when used with the when-catch construct described in the chapter on Distributed Computing.
The break statement, when used in a for or a while loop, can be followed by an expression, in which case the loop returns the value of that expression.
(Note: the following patch of code is used by updoc.e, the E testing tool, to enable execution of all the upcoming code that depends on Swing)

 ?? in new vat awtVat.e-awt
 ? pragma.syntax("0.9")


Do I have to specify a default matcher for a switch expression?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The short answer: No. You might want to read on for the consequences of
omitting it, though.

Switch expressions expand to a tree of possibilities, with each matcher being
tried in turn until one matches. If none of them match, then an exception is
thrown with a short description of the failing specimen.

To override this behavior, specify a matcher that cannot fail. Examples of
patterns that cannot fail include final and var patterns without guards, and
ignore patterns::

    switch (specimen):
        match ==x:
            traceln(`$specimen was just like $x`)
        match i :Int:
            traceln(`$i is an Int`)
        match _:
            traceln(`Default matcher!`)

In this example, since the final matcher always succeeds, the default behavior
of throwing an exception is effectively overridden.

The long answer: When Monte expands ``switch`` expressions into Kernel-Monte, the
entire expression becomes a long series of ``if`` expressions. The final
``else`` throws an exception using the ``_switchFailed`` helper object. If the
penultimate ``if`` test cannot fail, then the final ``else`` is unreachable,
and it will be pruned by the optimizer during compilation.

The Secret Lives of Flow Control Structures
-------------------------------------------

Flow control structures actually return values. For example, the if-else returns the last value in the executed clause:

 # E sample
 def a := 3
 def b := 4
 def max := if (a > b) {a} else {b}

This behavior is most useful when used with the when-catch construct described in the chapter on Distributed Computing.
The break statement, when used in a for or a while loop, can be followed by an expression, in which case the loop returns the value of that expression.
(Note: the following patch of code is used by updoc.e, the E testing tool, to enable execution of all the upcoming code that depends on Swing)

 ?? in new vat awtVat.e-awt
 ? pragma.syntax("0.9")


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
