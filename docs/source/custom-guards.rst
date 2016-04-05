Guard Protocol
==============

Like many other subsystems in Monte, guards can be made from any ordinary
object which implements the correct methods.

.. sidebar:: Are Guards Slow?

   Since guards are Monte objects and can be user-defined, concerns about
   performance are reasonable.

   According to :doc:`semantics`, every assignment acts *as if* its
   guard were executed; that is: once for every ``def``, at
   definition, and for ``var``, once at definition and once for every
   re-assignment.

   But if an implementation can determine statically that the specimen
   will always pass (e.g. ``def x :Int := 1``) then the check can be
   optimized away. An ahead-of-time compiler might use type inference
   to prove that all specimens at a definition site might be of a
   certain type. A just-in-time compiler might recognize at runtime
   that a guard's code is redundant with unboxing, and elide both the
   unboxing and the guard.

   The Typhon virtual machine almost always can skip typical basic
   guards like ``Int`` and ``Bool``.


The Basics
----------

The main method for a guard is ``coerce/2``, which takes an object to examine,
called the **specimen**, and an ejector. If the specimen conforms to the
guard, then the guard returns the conformed value; otherwise, the ejector is
used to abort the computation.

::

    object Any:
        to coerce(specimen, _):
            return specimen


    object Void:
        to coerce(_, _):
            return null

Here are two example guards, ``Any`` and ``Void``. ``Any`` passes all
specimens through as-is, and ``Void`` ignores the specimen entirely, always
returning ``null``.

Here's an actual test. The ``Empty`` guard checks its specimen, which is a
container, for emptiness and ejects on failure::

    object Empty:
        to coerce(specimen, ej):
            if (specimen.size() != 0):
                throw.eject(ej, `$specimen was not empty`)

The ejector does not need to have a meaningful object (nor even a string) as
its payload, but the payload may be used for diagnostic purposes by the
runtime. For example, a debugger might display them to a developer, or a
debugging feature of the runtime might record them to a log.
