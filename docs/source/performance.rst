====================
Performance Patterns
====================

Accidentally Quadratic
======================

Lists
-----

The following method of building a list is slow::

    var xs := []
    for x in (iterable):
        xs with= (f(x))

This is due to quadratic amounts of reallocation that must be performed; many
intermediate lists will be built and immediately made inaccessible. Instead,
allocate a mutable list instead of a mutable slot::

    def xs := [].diverge()
    for x in (iterable):
        xs.push(f(x))
    xs.snapshot()

For the specific case of building a list by mapping over an iterable, a list
comprehension is not just concise, but well-optimized. A compiler may be able
to improve the loop further, but if not, then the comprehension will be run
like this latter snippet.

::

    [for x in (iterable) f(x)]

Strings
-------

Similarly, consider building a string by repeated concatenation::

    var s := ""
    for x in (iterable):
        s += x

Once again, this causes quadratic amounts of memory movement. The solution is
to use the String Builder Pattern, storing the partially-built string in a
mutable list::

    def pieces := [].diverge()
    for x in (iterable):
        pieces.push(x)
    "".join(pieces)
