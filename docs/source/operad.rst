=============================================
Categorial Semantics and the Operads of Monte
=============================================

Drawing Diagrams
================

Monte objects can be viewed as members of a trivial category, **Mont**, whose
objects are some certain Monte objects and whose arrows are zero-arity
messages.

.. digraph:: negate

    42 -> -42 [label="negate/0"];

Identity arrows are added axiomatically. Note that computation in this
category is not like in other computational categories, and a path in **Mont**
is more like a trace of a particular execution than a program. We are working
with values as objects rather than types as objects.

Specifically, we will start with **DF-Mont**, whose objects are
``DeepFrozen``. In order to do this, we will have to immediately introduce the
*operad* **DF-Monts**, whose arrows are messages which can include a list of
other objects. We'll draw this operad's messages as dots which collate
arguments onto them.

.. note::

    Just like in Monte, **Monts** permits passing a map of "keyword"
    arguments. We will omit this from our diagrams for clarity, since keyword
    arguments are not required for the basic features of the operad.

.. digraph:: add

    "add/1" [shape="point"];
    2 -> "add/1" [label="add/1"];
    3:w -> "add/1" [label="arg0"];
    "add/1" -> 5;

With this operad, we can show off some basic coercions.

.. digraph:: dfint

    "coerce/2" [shape="point"];
    DeepFrozen -> "coerce/2" [label="coerce/2"];
    42:w -> "coerce/2" [label="arg0"];
    null:w -> "coerce/2" [label="arg1"];
    "coerce/2" -> 42:n;

This loop on ``42`` indicates that ``DeepFrozen.coerce(42, null) == 42``, or
in other words that ``42`` is its own prize when coerced by ``DeepFrozen``.
This is a sort of idempotence. ``DeepFrozen`` also has this property!

.. digraph:: dfdf

    "coerce/2" [shape="point"];
    DeepFrozen -> "coerce/2" [label="coerce/2"];
    DeepFrozen:w -> "coerce/2" [label="arg0"];
    null:w -> "coerce/2" [label="arg1"];
    "coerce/2" -> DeepFrozen:n;

In fact, every object in **DF-Monts** has this property; the objects of this
operad are precisely the ``DeepFrozen`` Monte objects.

We can also create suspended lists of values; these lists are themselves
values.

.. digraph:: makelist

    "run/2" [shape="point"];
    "_makeList" -> "run/2" [label="run/2"];
    2:w -> "run/2" [label="arg0"];
    3:w -> "run/2" [label="arg1"];
    "run/2" -> "[2,3]";

User-Defined Objects
====================

Suppose that we write ``fn { 42 }``, but as ``DeepFrozen``. We'll call this
"const₀", since it responds to ``run/0``, and in fact there is a family of
constant functions.

.. digraph:: const

    "run/0" [shape="point"];
    "const₀ 42" -> "run/0" [label="run/0"];
    "run/0" -> 42;

Another easy function to write is ``fn x { x }``, and again this can be
``DeepFrozen``. We'll call this "id", for "identity", and it comes with a free
law: in this following diagram, for any object ``x``, the identity arrow on
``x`` is equivalent to this particular composition with "id". The equivalent
statement in Monte is that ``id(x) == x``.

.. digraph:: idlaw

   "run/1" [shape="point"];
   id -> "run/1" [label="run/1"];
   x:w -> "run/1" [label="arg0"];
   "run/1" -> x:n;

   x -> x [label="identity arrow on x"];

.. note::

    Two of the advantages of the operad presentation are manifest:
    Point-freedom and removal of the lists from intermediate messages.
