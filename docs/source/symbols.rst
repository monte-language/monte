What do all the symbols mean?
=============================

`=>`
----

Could be pronounced "rocket" or "fat arrow" if necessary

.. code-block:: monte

    for a => b in c: 

is equivalent to

.. code-block:: python

    for a, b in c.items():

`=>` pattern-matches a pair, like in a map.

`<=>`
-----

"As big as"

Think of it as merging `<=` with `>=`

`:=`
----

Assignment. `a := 42` would be written as `a = 42` in C-flavored syntax.
Comparison in Monte is `==` and the single-equals, `=`, has no meaning. This
all but eliminates the common issue of `if (foo = baz)` suffered by all
languages where you can compile after typo-ing `==`.

`**`
----

Exponentiation. `2 ** 3 == 8`

`*`
---

Multiplication. `2 * 3 == 6`


Boolean Operators
=================

`==`
----

Equality comparison. Can compare references, integers, etc.

`<`, `>`
--------

Less than or greater than. 

.. code-block:: monte

    3 < 2 == False
    3 > 2 == True
    3 < 3 == False

`<=`, `>=`
----------

Less than or equal to, greater than or equal to. 

Same as above, but `3 <= 3 == True`

`&&`
----

And. 

.. code-block:: monte

    True && True == True
    True && False == False
    False && False == False
