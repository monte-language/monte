=====
Slots
=====

Monte's values are stored in **slots**, which are also values. This nested
structure permits some flexibility.

The slot of a value is accessed using the ``&`` unary operator::

    def slot := &value

Final Slots
===========

Final slots are created by final definitions::

    def finalValue := 42
    def finalSlot := &finalValue

Lazy Slots
----------

Lazy slots are a convenient and elegant tool in the safe scope for creating
simple lazy values. A lazy slot is constructed with a thunk which will be
transparently evaluated once (and only once) to compute the slot's value.

::

    def fib(i :Int) :Int:
        return if (i > 1) {fib(i - 1) + fib(i - 2)} else {i}
    def &lazySlot := makeLazySlot(fn {fib(30)}) # or fib(40) for more drama
    traceln(`$lazySlot`) # this will take a few moments
    traceln(`$lazySlot`) # but this will be instantaneous

.. note::
    Lazy slots can be constructed with a var slot, and it can be an
    enlightening exercise. ``makeLazySlot`` is provided as a courtesy since it
    acts like a final slot for auditions with DeepFrozen.

Var Slots
=========

Var slots are created by var definitions::

    var varValue := 7
    def varSlot := &varValue

A var slot's value can be assigned to, and the slot's identity will not
change::

    varValue := 5
    varSlot == &varValue # Still true after assignment
