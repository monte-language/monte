================
Miranda Protocol
================

.. epigraph::
    If you cannot afford a method, one will be appointed for you.

Monte objects, left to their own devices, are black boxes; one cannot perform
any sort of introspection on them. However, there are some powers granted to
anybody who can refer to an object. The runtime grants these powers
automatically, and we refer to them as the **Miranda protocol**.

The Miranda protocol grants powers in the form of methods, called **Miranda
methods**, which all objects automatically possess. An object may provide its
own Miranda methods, but does not have to; objects are automatically granted
default Miranda methods with correct behavior. Or, as stated above, "if an
object does not have a Miranda method, one will be provided."

Safety
======

Miranda methods should be safe to call. The default definitions will always
respond without throwing exceptions. It is rude but permissible for an object
to provide a custom Miranda method implementation which can throw or eject, or
return incorrect or misleading information. Therefore, be aware of situations
in which Miranda methods are being used.

.. warning::
    Special mention goes here to the most commonly-called Miranda method,
    ``_printOn/1``. Any time that an object is being turned into a string, it
    almost certainly involves a little bit of ``_printOn/1``, so be careful.

Methods
=======

``_conformTo/1``
    ``_conformTo`` takes a guard and coerces this object to that guard, if
    possible. The default implementation returns ``null`` for all guards.
    Overriding this method lets an object become other objects when under
    scrutiny by guards.

``_getAllegedType/0``
    ``_getAllegedType`` returns an interface describing this object. If not
    specified, an interface which represents the object faithfully will be
    created and returned.

    .. note::
        We're gonna rename this to something that doesn't use the word "type"
        at some point in the near future. Probably "shape" or "interface"?

    .. warning::
        We haven't implemented this one yet.

``_uncall/0``
    ``_uncall`` undoes the call that created this object. The default
    implementation returns ``null``, because objects are, by default, not
    uncallable. A good implementation of ``_uncall`` will return a list
    containing ``[maker, verb, args]`` such that ``M.call(maker, verb, args)``
    will produce a new object which is equal to this object.

    Providing an instance of ``_uncall`` makes an object eligible for
    uncall-based catamorphisms. In particular, uncallable objects are
    comparable by value.

    .. note::
        At some point in the near future, you'll need to both implement
        ``_uncall`` and also pass an audition proving that your uncall is
        correct in order to gain the benefit of uncallability.

``_printOn/1``
    ``_printOn`` writes text representing this object onto the printer passed
    as an argument.

    Customizing ``_printOn`` lets an object change how it is pretty-printed.
    The default pretty-printing algorithm is readable but does not divulge the
    internal state of an object.

``_respondsTo/2``
    ``_respondsTo(verb, arity)`` returns a Boolean value indicating whether
    this object will respond to a message with the given verb and arity. The
    default implementation indicates whether the object's source code listed a
    method with the given verb and arity.

    .. warning::
        Determining whether a given object responds to a given message is
        undecidable. Therefore, there are times when ``_respondsTo/2`` is
        unavoidably wrong, both with false positives and false negatives.

``_whenBroken/1``
    ``_whenBroken``, by default, does nothing on near objects and sends
    notifications of breakage through references. It is not interesting.

``_whenMoreResolved/1``
    ``_whenMoreResolved``, by default, does nothing on near objects and sends
    notifications of partial fulfillment through references. It is not
    interesting.
