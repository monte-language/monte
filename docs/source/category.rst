====================
Categorial Semantics
====================

Let **DF-Mont** be the category whose objects are ``DeepFrozen`` messages and
whose arrows are ``DeepFrozen`` Monte objects. For our diagrams, we will
follow the convention that arrows are arrows and objects are encircled.

Since **DF-Mont** is a category, it must have an identity arrow for all
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
