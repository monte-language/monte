Ordinary Computing
==================

*In case you skipped the introduction, this is a last reminder that
 the fireworks start with @@LINK Distributed Computing, and you can go
 there now, or continue to read about normal, ordinary computing in E,
 starting with Hello World.*

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

Single-line comments have a "#" at the beginning, and terminate with
the end of line. The /**...*/ comment style is used only for writing
javadoc-style E comments, discussed later. @@link here

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


Basic Types and Operators
-------------------------

.. todo:: continue with Walnut outline


Ordinary Computing Examples / A Taste of Monte
----------------------------------------------

Let's see what a simple web server looks like in monte:

.. literalinclude:: tut/web1.mt
    :linenos:
    :language: monte

The ``imports`` line begins a :ref:`module <modules>` and we declare
that this module ``exports`` its ``main`` function, as is conventional
for executable programs.

The :ref:`def expression<def>` for defining the ``helloWeb`` function is
similar to python and the like.

.. todo:: Forward ref :ref:`auditors` or find a way to elide
          ``DeepFrozen``. (Issue #43).

The ``smallBody`` import works much like python's ``from
lib.http.resource import smallBody``, using :ref:`pattern matching
<patterns>` to bind names to objects imported from :ref:`modules
<modules>`.

.. todo:: hoist imports to toplevel once these library modules
          have gone through the module migration.

The ``escape`` expression introduces an :ref:`ejector <ejector>` called
``badRequest``, which we use to deal with ill-formed requests in a
fail-stop manner in case the ``request`` doesn't match the
``[[verb, path], headers]`` pattern.

The ``body`` is defined using :ref:`method calls<message_passing>`
on the imported ``tag`` object.

The critical distinction between monte and other memory-safe dynamic
languages is that monte is an :ref:`object capability <ocap>`
lanugage. Powerful objects such as ``currentProcess`` and
``makeTCP4ServerEndpoint`` are not in any global namespace; they
cannot be imported. Rather, they are provided explicitly to the
``main`` function. Except by explicit delegation, no code can do
anything more more than create objects (including functions) in
memory. It cannot read from nor write to files [#]_, access the
network, clobber global state, or launch missiles.

By straightforward inspection, we can see that
  - only one TCP port is ever created;
  - its port number is taken from the last command-line argument.
