===========
Cheat Sheet
===========

Type Conversions
================

Very often, we programmers know that we have a value of one type, and that we
would like it to be another type; we expect that there is a canonical natural
transformation from what we have to what we want.

Chars
-----

A character might as well be a natural number, with the restriction that it
is also a valid Unicode code point. To get at that number, use
``.asInteger()``::

   'c'.asInteger()

The inverse conversion is arcane::

   '\x00' + 99

Strs
----

A string might as well be a packed list of characters. To build that list::

   _makeList.fromIterable("word")

The inverse, to pack a list of characters into a string::

   _makeStr.fromChars(['w', 'o', 'r', 'd'])
