======
Brands
======

The *brand pattern* divides the capability of establishing a secure
communication channel into two facets, called a *sealer* and *unsealer*.

::

    def [ana, cata] := makeBrandPair("finney")
    def box := ana.seal(42)
    cata.unseal(box)

The resulting channel has the following properties:

* **Authentic and Unforgeable**: Boxes created by the sealer cannot be
  unsealed by any object other than the unsealer; to the contrapositive, any
  object that the unsealer unseals must have been sealed with the
  corresponding sealer.
* **Asynchronous**: Boxes created by the sealer can be unwrapped on any
  subsequent turn.
* **Untyped**: Any object can be transmitted along the channel.

Up & Down
=========

To create a new brand, call ``makeBrandPair(nickname :Str)``. The nickname is
purely cosmetic, to aid readability and debugging; it does not have to be
unique.

::

    # Make a sealer named `ana` and an unsealer named `cata`.
    def [ana, cata] := makeBrandPair("finney")

The brand itself is an opaque object which proves that a sealer and unsealer
are paired with each other. It is accessible via the ``.getBrand/0`` method::

    # Hey, these two are a pair!
    ana.getBrand() == cata.getBrand() # should be true

Brands are usable as map keys::

    def brandMap := [ana.getBrand() => [ana, cata]]
    brandMap[cata.getBrand()] # should be `[ana, cata]`

The fundamental operation of a sealer is to ``.seal/1`` an object into a box::

    def box := ana.seal(42)
    box # <box sealed by finney>

The unsealer, unsurprisingly, provides ``.unseal/1``, which opens a box and
returns its contents::

    cata.unseal(box) # should be 42

The box is opaque and yields only one useful method, ``.getBrand/0``, which
can be useful for determining which unsealer might be the correct one to use
for unsealing::

    brandMap[box.getBrand()] # should be `[ana, cata]`

.. note::
    The implementation of ``makeBrandPair`` in the Typhon prelude has other
    methods defined on boxes, but they do not affect the security guarantees
    of the implementation.
