============
Quasiparsers
============

Quasiparsers ("QP" for short) are part of the **quasiliteral** (QL) subsystem
of Monte. QLs are an essential characteristic of Monte, so the design and
production of QPs should be simple and easy.

Basic Usage
===========

QLs are literal objects that reflect the syntax of some language not native to
Monte. They are formed by an identifier indicating which QP to use and a pair
of backticks::

    def ql := name`and some text`

The exact object created by a QP varies depending on the QP used. One of the
most common QPs used is called ``simple``. ``simple`` formats the QL text and
returns a string::

    def hello :String := simple`Hello world!`

``simple`` is so common that Monte defaults to using it if no QP is
specified::

    def another :String := `is formed from using simple by default`

Another QP provided in the safe scope is ``m``, which parses Monte literal
expressions and returns a code object. ``m`` is useful for code generation::

    def expr := m`2 + 2`

Values
------

Of course, the QL system might not seem very useful if all it can do is turn
literals into objects. We call them *quasi*-literal because we can
syntactically interact with QLs to vary the produced objects.

::

    def name := "Joe"
    def greeting :String := `Hello, $name!`

In this example, ``name`` is interpolated into the QL string to produce
"Hello, Joe!"

Patterns
--------

At this point, QLs seem like a very useful tool for constructing objects. They
can also be used to pull objects apart. Just like many other things in Monte,
QLs can be used as patterns::

    def greeting := "Hello, world!"
    def `Hello, @name!` := greeting

Examine this carefully. This pattern is assigning to ``name``, asserting that
the rest of the pattern (the "Hello, " and "!" fragments) match the specimen.

Quasiliteral Syntax Summary
===========================

*TODO: split quasipattern out of quasiliteral*

.. syntax:: quasiliteral

   Diagram(Sequence(
    Optional(Terminal("IDENTIFIER")),
    '`',
    ZeroOrMore(
        Choice(0, Comment('...text...'),
               Choice(
                   0,
                   Terminal('$IDENT'),
                   Sequence('${', NonTerminal('expr'), '}')),
               Choice(
                   0,
                   Terminal('@IDENT'),
                   Sequence('@{', NonTerminal('pattern'), '}')))),
    '`'))
