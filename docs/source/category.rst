====================
Categorial Semantics
====================

DF-Mont-Mess
============

Let **DF-Mont-Mess** be the category whose objects are ``DeepFrozen`` messages and
whose arrows are ``DeepFrozen`` Monte objects. For our diagrams, we will
follow the convention that arrows are arrows and objects are encircled.

Since **DF-Mont-Mess** is a category, it must have an identity arrow for all
messages.

.. digraph:: identity

    message [label="[\"run\", [42], [].asMap()]"];

    message -> message [label="id"];

In Monte, this object simply repeats messages delivered to it::

    object id {
        match message {
            message
        }
    }

DF-Mont
=======

Let **DF-Mont** be the category whose objects are ``DeepFrozen`` values, not
just messages, and whose arrows are ``DeepFrozen`` objects, as well as several
primitives. The most important primitive is likely the ability to perform a
call.

.. digraph:: call

    tuple [label="[1, \"add\", [1], [].asMap()]"];

    tuple -> 2 [label="call"];

This is like the Monte expression ``1 + 1``, or ``(1).add(1)``. It is also
like the Monte expression ``2``. In **DF-Mont**, Monte execution is
represented by diagrams which commute, and the direction of computation is
indicated by the direction of arrows.

Initial Object
--------------

We can formalize the statement that every object in **DF-Mont** is
``DeepFrozen`` by showing that there is a unique arrow (up to isomorphism)
``!`` from ``DeepFrozen`` to any other object ``obj`` in the category.

.. digraph:: DeepFrozenInitial

    message [label="[DeepFrozen, \"coerce\", [obj, null], [].asMap()]"];

    DeepFrozen -> message -> obj;

    DeepFrozen -> obj [label="!"];

This diagram commutes. The up-to-isomorphism limitation comes from ``null`` in
``coerce/2``; we may replace it in this diagram with any other object.

Products
--------

Lists act as our products. We can either use calls to do work on lists, or we
can use categorical logic. The arrow ``[[1, 2], [3, 4]]`` → ``[[1, 2], "add",
[[3, 4]], [].asMap()]`` is a member of a family of list-building arrows.

.. digraph:: listAdd

    pair [label="[[1, 2], [3, 4]]"];
    sum [label="[1, 2, 3, 4]"];

    pair -> sum [label="listAdd"];


    pairCall [label="[[1, 2], \"add\", [[3, 4]], [].asMap()]"];
    pair -> pairCall [label="listMake"];
    pairCall -> sum [label="call"];
