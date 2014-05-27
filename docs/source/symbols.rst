What do all the symbols mean?
=============================

=>
--

Could be pronounced "rocket" or "fat arrow" if necessary

.. code-block:: monte
    for a => b in c: 

is equivalent to

.. code-block:: python
    for a, b in c.items():

`=>` pattern-matches a pair, like in a map.

<=>
---

"As big as"

Think of it as merging `<=` with `>=`

:=
--

Assignment. `a := 42` would be written as `a = 42` in C-flavored syntax.
Comparison in Monte is `==` and the single-equals, `=`, has no meaning. This
all but eliminates the common issue of `if (foo = baz)` suffered by all
languages where you can compile after typo-ing `==`. 
