===========
Collections
===========

Monte has three builtin types of collections, each of which come in "const"
(immutable) and "flex" (mutable) flavors.

Sets
====

Monte's sets are ordered containers with the standard assortment of
set-theoretic tools, like membership testing, iteration, union, and
intersection. Members are stored based on the sameness test; two members
overlap if, and only if, they are the same.

Sets support syntactic comparison using the `<=>` and related operators. The
comparison takes the form of a subset test. Two sets `s` and `t` are
equivalent, `s <=> t`, if, and only if, they contain the same members and are
the same size.
