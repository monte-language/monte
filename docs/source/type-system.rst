===============
The Type System
===============

This is a brief overview of Monte's type system.

Monte does not have a type system, in the type-theoretic sense. Instead, Monte
features :ref:`guards`. However, we cannot deny that guards both syntactically
and semantically resemble types, so we are happy to call our guard system our
"type system" and compare it to other type systems.

We use the Smallshire_ classification of type system features to explain
Monte's typing features in a high-level overview.

.. _Smallshire: https://vimeo.com/74354480

Untyped
=======

A language is :dfn:`untyped` if there is only one type of value in the
language. There are two common definitions here; one is used by Smallshire,
and one is used by Harper_. Both are worth considering, since Monte straddles
the edge.

.. _Harper: https://existentialtype.wordpress.com/2011/03/19/dynamic-languages-are-static-languages/

Smallshire gives Ruby as an example of a typed language.  Ruby is a close
relative of Monte, and by Smallshire's definition, Monte is also a typed
language, in this view, because objects still have innate distinct behaviors.

In constrast, Harper equates untyped and unityped languages. This would mark
Ruby, and Monte too, as untyped.

We say that Monte is untyped, for reasons similar to Harper's. Monte has a
*uniform calling interface*, which means that any message can be sent to any
object, and rejection is always done inside the object's message-receiving
code at runtime.

Dynamic
=======

Monte is :dfn:`dynamic`; it is possible to have a name for a value without
restrictions on the type of the value.

Strong
======

Monte values have :dfn:`strong` types which resist coercion. Indeed, in Monte,
coercion is a reified object protocol. Objects do not have to be coercible,
and most builtin objects cannot be coerced.

Manifest
========

Monte guards are :dfn:`manifest` type annotations, which means that they are
never inferred by canonical expansion.

Optional
========

Guards are :dfn:`optional` and do not have to be specified. Indeed, Monte
boasts :dfn:`gradual` typing, which means that a Monte program can have any
mix of guarded and unguarded names without affecting the correctness of
guards.
