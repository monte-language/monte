.. _auditors:

========
Auditors
========

The auditor subsystem allows objects to certify themselves as having certain
properties. In order to gain certification, specimen objects must pass
**audition**, a process in which the source code of the specimen object is
revealed to an **auditor**, another object which examines the structure of the
specimen and indicates whether it qualifies.

Stamps
------

Some auditors will admit any object which requests an audition. These auditors
are called **stamps**. An object with a stamp is advertising behavior that is
not necessarily reflected in the object's structure. Stamps can be used to
indicate that an object should be preferentially treated; additionally, a
stamp with limited availability can be used to indicate that an object belongs
to a privileged set of objects.

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
bare other stamps to indicate that equality comparisons with that object
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

Bindings (WIP)
--------------

.. todo:: discuss bindings. Expand this section to "slots and
          bindings"? or discuss bindings under auditors?
