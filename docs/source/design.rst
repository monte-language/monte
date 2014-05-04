===============
Design of Monte
===============

This is a gentle overview of the design features of Monte and how it fits into
the larger genealogy of programming languages.

Types
=====

Monte features strong dynamic types. By "strong" we mean that Monte's types
resist automatic coercion; by "dynamic" we mean that objects are not
necessarily specialized to any specific type.

As an example of strong typing in Monte, consider the following statement::

    def x := 42 + true

This statement will result in an error, because ``true`` is a boolean value
and cannot be automatically transformed into an integer, float, or other value
which integers will accept for addition.

Functional Features
===================

Monte has support for the various language features required for programming
in the so-called "functional" style. Monte supports closing over values (by
reference and by binding), and Monte also supports creating new function
objects at runtime. This combination of features enables functional
programming patterns.

Monte also has several features similar to those found in languages in the
Lisp and ML families which are often conflated with the functional style, like
strict lexical scoping, immutable builtin value types, and currying for
message passing.

Object-Based Features
=====================

Monte is descended from the Smalltalk family of languages, and as such,
is an **object-based** language. "Object-oriented" styles of programming are
largely available in Monte.
