.. _quasiliteral:

=============
Quasiliterals
=============

Quasiliterals, or QLs, are an important part of Monte syntax which allows us
to embed arbitrary DSLs into Monte. With the power of QLs, Monte can be
extended into new territory in a very neat way.

What's a Quasiliteral?
======================

This is a quasiliteral::

    `Backticks start and end quasiliterals`

A quasiliteral can have values mixed into it with ``$``. A value can be a
name::

    def name :Str := "Todd"
    `Hello, $name!`

A value can also be an expression, using brackets::

    `2 + 2 = ${2 + 2}`

Quasiliterals can be used as patterns::

    # Equivalent to: def =="self" := "self"
    def `self` := "self"

Quasiliteral patterns also permit pattern-matching with ``@`` to retrieve
single names::

    def `(@first, @second)` := "(42, 5)"

And any pattern can be used with brackets::

    def `x := @{var x}` := "x := 7"
    x += "-11" # What? I like slushies!

Finally, there are different *quasiparsers*, or QPs, which each have different
behavior::

    # `` makes strings
    `def x := 42` :Str
    # b`` makes bytestrings
    b`def x := 42` :Bytes
    # m`` makes Monte AST objects
    m`def x := 42` :(astBuilder.getAstGuard())

How to Use QLs
==============

A quasiliteral expression starts with the name of a quasiparser (which can be
empty) followed by a backtick. Then, a mixture of strings and holes are
allowed, followed by a final backtick. The holes can either be
expression-holes, with ``$``, or pattern-holes, with ``@``.

.. warning::

    Pattern-holes cannot be used in QL expressions, only in QL patterns. Using
    a pattern-hole in a QL expression is a syntax error!

Builtin Quasiparsers
====================

There are three common QPs included in Monte's safe scope.

Simple
------

.. sidebar:: Did You Know?

    Monte originally used the same name as E for ::"``":
    ``simple__quasiParser``. That's why we call ::"``" the
    "simple" quasiparser.

The simple or empty QP builds strings::

    `string` == "string" # true

It can mix any value into a string, even values that don't pass ``Str``::

    `${7}` == "7" # true

The simple QP does this by calling ``M.toString/1`` on the values.
Correspondingly, the value's ``_printOn/1`` is called, and can be customized::

    object shirt { to _printOn(out) { out.print("tye-dye shirt") } }
    def description :Str := `I am wearing a $shirt.`

When used as a pattern, the simple QP performs very simple but straightforward
and powerful string parsing::

    def container := "glass"
    def `a $container of @drink` := "a glass of lemonade"

Bytes
-----

The bytes QP builds bytestrings::

    b`asdf`

The encoding of characters is unconditionally Latin-1. Non-Latin-1 characters
cause errors to be thrown at runtime::

    b`ErrorRaiser™`

Other than that quirk, the bytes QP behaves much like the simple QP, including
parsing::

    def b`@header:@value` := b`x:12`

Monte
-----

Finally, the Monte QP builds Monte ASTs from literal Monte source::

    m`def x := 42`

The Monte QP can be used for code generation, since it evaluates to objects
usable with ``eval/2``::

    eval(m`2 + 2`, [].asMap())

Custom Quasiparsers
===================

Anybody can write their own quasiparser.

Parsing with Values
-------------------

The first half of the QP API deals with building the initial structure and
including values.

``.valueHole(index :Int)`` should create a value marker which can be used in
place of some value which will be included later. ``.valueMaker(pieces
:List)`` will be called with a list of pieces, which can be either strings or
value markers, and it should return a partial structure. That structure can be
completed with its ``.substitute(values :List)``, which provides a list of
values that can be swapped with the value markers.

To see how this API all comes together, let's look at the kernel expansion of
a simple QP call::

    `Just another $day for this humble $string.`

What Monte actually does is call ``.valueMaker/1``, like so::

    ::"``".valueMaker(["Just another ", ::"``".valueHole(0),
                       " for this humble ", ::"``".valueHole(1),
                       "."]).substitute([day, string])

Parsing Patterns
----------------

The pattern API is similar and builds upon the expression API.

First, the ``.patternHole/1`` method allows pattern hole markers to be built,
just like with value holes. Then, the structure is built with
``.matchMaker/1`` instead of ``.valueMaker/1``. This structure should have a
completion method, ``.matchBind(values :List, specimen, ej)`` which attempts
to unify the specimen with the structure completed by the values or eject on
failure.

Here's a simple pattern::

    def `how ${hard} could it be to match @this?` := "not hard, just complex"

And its expansion::

    def via (_quasiMatcher.run(::"``".matchMaker(["how ", ::"``".valueHole(0),
                                                  " could it be to match ",
                                                  ::"``".patternHole(0),
                                                  "?"]),
                               [hard])) [this] := "not hard, just complex"

Note how the ``_quasiMatcher`` helper in the safe scope takes care of the
extra runtime plumbing.
