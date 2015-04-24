======================
Creating Custom Guards
======================

Like many other subsystems in Monte, guards can be made from any ordinary
object which implements the correct methods.

The Basics
==========

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
:doc:`container`, for emptiness and ejects on failure::

    object Empty:
        to coerce(specimen, ej):
            if (specimen.size() != 0):
                throw.eject(ej, `$specimen was not empty`)

The ejector does not need to have a meaningful object (nor even a string) as
its payload, but the payload may be used for diagnostic purposes by the
runtime. For example, a debugger might display them to a developer, or a
debugging feature of the runtime might record them to a log.

Guards and Variable Slots
=========================

.. note::
    There should be a section about ``makeSlot`` and whether it will be part
    of the slot API. Also something about whether ejections can happen in
    varslots.
