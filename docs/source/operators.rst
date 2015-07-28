==================================
Operators and Augmented Assignment
==================================

.. epigraph::

    Corporate accounts payable, Nina speaking! Just a moment!

    -- Nina, corporate accounts payable, *Office Space*

Monte has a rich set of operators above and beyond those in Kernel-Monte. All
operators are overloadable, but overloading follows a very simple set of
rules: Operators desugar into message passing, and the message is generally
passed to the left-hand operand, except for a few cases where the message is
passed to a *helper object* which implements the operation. In object
capability shorthand, we are asking the object on the left what it thinks of
the object on the right.

Augmented Assignment
====================

All binary operators which pass a message to the left-hand operand can be used
as augmented assignment operators. For example, augmented addition is legal::

    var x := "augmenting "
    x += "addition!"

Behind the scenes, the compiler transforms augmented operators into standard
operator usage, and then into calls::

    var x := "augmenting "
    x := x.add("addition!")

Monte permits this augmented construction for any verb, not just those used by
operators. For example, the ``with`` verb of lists can be used to
incrementally build a list::

    var l := []
    for i in 1..10:
        l with= (i)

And even non-unary messages can get in on the fun, with a properly placed pair
of parentheses::

    var x := 7
    x modPow= (129, 3)
