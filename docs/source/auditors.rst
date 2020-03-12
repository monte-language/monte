.. _auditors:

========
Auditors
========

The auditor subsystem allows objects to certify themselves as having certain
properties. In order to gain certification, specimen objects must pass
**audition**, a process in which the source code of the specimen object is
revealed to an **auditor**, another object which examines the structure of the
specimen and indicates whether it qualifies.

Anatomy of an Audition
======================

We will examine the steps involved in performing an audition. Audition
proceeds by examining objects as expressions, looking at their syntax.

Annotation
----------

In the following trivial object::

   def id(x) as DeepFrozen { return x }

The ``as DeepFrozen`` annotation acts as consent for ``id`` to be audited.

An auditor will be invoked with the ``.audit(audition)`` method, including an
object which tracks the progress of the audition.

Expansion
---------

Auditors do not receive Full-Monte ASTs, but Kernel-Monte. This means that the
auditor sees an expanded expression, like::

   object id as DeepFrozen:
      method run(x):
         escape __return { __return(x) }
         null

The expansion may not be canonical. For example, an optimizing expander may
emit an expression like::

   object id as DeepFrozen { method run(x) { x } }

This expanded AST is available to auditors by calling
``audition.getObjectAST()``.

Framing
-------

Every name in the audited expression is defined somewhere. If a name is not
defined within the object literal, then it is within the object's **frame**.
The frame consists of not only every name which is closed over by the object,
but also the slot and binding information. To auditors, only some of this
information is available; this is due to the fact that the audition is running
on the *syntax* of the object, and not the live values that are in its
closure.

.. sidebar:: When do auditors run?

   At first glance, it may seem strange that auditors cannot see all of the
   values within an object. Why not? The answer lies in when audition can
   happen. An optimizing Monte runtime may try to perform auditions before
   ever running code; the runtime may be able to infer slot guards statically.

Specifically, auditors may retrieve the *slot guards* of names. For example,
the slot guard of ``def x :Int := 42`` is ``FinalSlot[Int]``. Slot guards may
be as generic as ``Any``.

::

   switch (audition.getGuard(name)):
      match via (FinalSlot.extractGuard) g { g }
      match _ { throw(`$name wasn't a final slot`) }

Delegation and Subauditors
--------------------------

There is partial formal support for delegating to other auditors, performing a
sort of subaudition, during one's own audition process. For example, if an
auditor wanted to know whether its specimen were ``DeepFrozen``, it could just
``.ask()``::

   if (!audition.ask(DeepFrozen)):
      throw(`${audition.getFQN()} isn't DeepFrozen`)

Stamps
~~~~~~

Some auditors will admit any object which requests an audition. These auditors
are called **stamps**. An object with a stamp is advertising behavior that is
not necessarily reflected in the object's structure. Stamps can be used to
indicate that an object should be preferentially treated; additionally, a
stamp with limited availability can be used to indicate that an object belongs
to a privileged set of objects.

Delegation and stamps go hand-in-hand; for example, single-inheritance
typechecking can be lifted to the level of auditors by having many "subclass"
auditors delegating to a common "superclass" or "interface" stamp.

Failure and Errors
------------------

Many auditors will ``throw()`` on failure. There is no ejector, nor any place
for an auditor to escape to, but throwing an exception will ensure that the
audition is cancelled and that the specimen is never constructed.

The Results
-----------

Finally, an auditor ought to return a ``Bool`` indicating whether the audition
succeeded. This will be the value passed to any superauditions, if this
auditor was invoked by some ``.ask()``.

The results are cached according to what the auditor asked for during the
audition; depending on which slot guards were examined, the audition may have
to be repeated as the object is constructed with different framing, or the
audition may never need to be repeated.

If the result is ``true``, then the auditor is added to a list which is
attached to the object. There is no direct Miranda method for inspecting this
list, but the safe scope contains ``_auditedBy(auditor, specimen) :Bool``::

   def isDeepFrozen :Bool := _auditedBy(DeepFrozen, 42)

A Showing of Common Auditors
============================

.. _deepfrozen:

DeepFrozen
----------

The ``DeepFrozen`` auditor proves that objects are immutable and that the
objects they refer to are also ``DeepFrozen``.

::

    ▲> DeepFrozen
    DeepFrozen

.. note::
    The specific property proven by ``DeepFrozen``: For any ``DeepFrozen``
    object, all bindings referenced by the object are also ``DeepFrozen``.

.. _selfless:

Selfless
--------

The ``Selfless`` auditor is a stamp. Any object bearing ``Selfless`` can also
bear other stamps to indicate that equality comparisons with that object
should be done in a customized way.

::

    ▲> Selfless
    Selfless

Transparent
-----------

The ``Transparent`` auditor proves that an object implements a custom
``_uncall/0`` Miranda method with certain properties. Any ``Transparent``
object can be compared by comparing the contents of its uncalled
representation.

To prove an object ``Transparent``, a small kit of facet objects must be
obtained and attached to the maker definition::

    def [makerAuditor :DeepFrozen, &&valueAuditor, &&serializer] := Transparent.makeAuditorKit()

Then the maker and object must both submit to audition. The maker must be
``DeepFrozen`` and the inner object ``Selfless``::

    def makeSwatch(color) as DeepFrozen implements makerAuditor:
        return object swatch implements Selfless, valueAuditor:
            to _uncall():
                return serializer(makeSwatch, [color])

The resulting maker will produce objects that can be compared as if by value::

    ▲> def red := makeSwatch("red")
    ▲> def xunre := makeSwatch("red")
    ▲> red == xunre
    Result: true
    ▲> def blue := makeSwatch("blue")
    ▲> red == blue
    Result: false

.. note::
    Using the ``Transparent`` auditor as a guard is legal and works as
    expected, but is not required to obtain correct comparison behavior.

.. note::
    Specifically, the property proven by ``Transparent`` is that uncalling the
    object is the inverse of calling the maker, and vice versa.

.. _bindings:

Bindings
========

What, exactly, are bindings? Bindings are slots of slots. A slot has a value
and a guard, and the value ought to pass coercion by the guard. Similarly, a
binding has a slot and a slot guard, and the slot ought to pass coercion by
the slot guard. For the two common sorts of slots, created by ``def`` and
``var``, there are ``FinalSlot`` and ``VarSlot`` slot guards, respectively.
Subguards may be gotten; ``FinalSlot[Int]`` is a slot guard which admits final
slots which themselves have ``Int`` guarding their (immutable) value.
