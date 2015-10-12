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

``_getAllegedInterface/0``
    ``_getAllegedInterface`` returns an interface describing this object. If
    not specified, an interface which represents the object faithfully will be
    created and returned.

    The allegedness of the interface hinges on the ability to override this
    method; the returned interface can be just as untrustworthy as the object
    that returns it.

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

``_sealedDispatch/1``
    ``_sealedDispatch`` permits this object to discriminate its responses to
    messages based on the capabilities of the calling object.

    Occasionally, a calling object will wish to prove its capabilities by
    passing some sort of key or token to a receiving object. The receiving
    object may then examine the key, and return an object based on the
    identity or value of the key.

    We provide ``_sealedDispatch/1`` for a specific subset of these cases. The
    caller should pass a brand, and the receiver dispatches on the brand,
    returning either a sealed box guarded by the passed-in brand, or ``null``
    if the brand wasn't recognized.

    By default, ``_sealedDispatch`` returns ``null``. This makes it impossible
    to determine whether an object actually has a customized
    ``_sealedDispatch``.

    A popular analogy for sealed dispatch is the story of the "Red Phone," a
    direct line of communication between certain governments in the past. The
    Red Phone doesn't ring often, but when it does, you generally know who's
    calling. They'll identify themselves, and if you can confirm that it's
    the correct caller, then you can have discussions with them that you
    wouldn't have over an ordinary phone.

``_uncall/0``
    ``_uncall`` undoes the call that created this object. The default
    implementation returns ``null``, because objects are, by default, not
    uncallable. A good implementation of ``_uncall`` will return a list
    containing ``[maker, verb :Str, args :List, namedArgs :Map]`` such that
    ``M.call(maker, verb, args, namedArgs)`` will produce a new object which
    is equal to this object.

    Providing an instance of ``_uncall`` makes an object eligible for
    uncall-based catamorphisms (fold, reduce, ...). In particular, uncallable
    objects are comparable by value.

    .. note::
        In order to be eligible for value comparisons, you'll need to both
        implement ``_uncall`` and also pass an audition proving that your
        uncall is correct. See ``Selfless`` and ``Transparent`` for details.

``_whenBroken/1``
    ``_whenBroken``, by default, does nothing on near objects and sends
    notifications of breakage through references. It is not interesting.

``_whenMoreResolved/1``
    ``_whenMoreResolved``, by default, does nothing on near objects and sends
    notifications of partial fulfillment through references. It is not
    interesting.
