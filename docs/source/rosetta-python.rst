Python-Monte Idioms
===================

This is a collection of common Python idioms and their equivalent Monte
idioms.

Iteration
---------

Enumeration
~~~~~~~~~~~

Python's ``enumerate`` is usually not necessary in Monte.

Python:

.. code-block:: python

    for i, x in enumerate(xs):
        f(i, x)

Monte::

    for i => x in xs:
        f(i, x)

Objects
-------

Classes
~~~~~~~

Monte does not have classes, but the maker pattern is equivalent.

Python:

.. code-block:: python

    class ClassName(object):
        def __init__(self, param, namedParam=defaultValue):
            self._param = param
            self._namedParam = namedParam

        def meth(self, arg):
            return self._param(self._namedParam, arg)

Monte::

    def makeClassName(param, => namedParam := defaultValue):
        return object objectName:
            to meth(arg):
                return param(namedParam, arg)

Inheritance
~~~~~~~~~~~

Monte doesn't have class-based inheritance; instead, there is
composition-based inheritance.

Python:

.. code-block:: python

    class Parent(object):
        def meth(self, arg):
            return arg * 2

        def overridden(self, arg):
            return arg + 2

    class Child(Parent):
        def overridden(self, arg):
            return arg + 3

Monte::

    object parent:
        to meth(arg):
            return arg * 2

        to overridden(arg):
            return arg + 2

    object child extends parent:
        to overridden(arg):
            return arg + 3

Private Methods
~~~~~~~~~~~~~~~

Neither Python nor Monte have private methods. Python has a naming convention
for methods which should not be called from outside the class. Monte has an
idiom for functions which cannot be called from outside the class.

Python:

.. code-block:: python

    class ClassName(object):

        _state = 42

        def _private(self):
            return self._state

        def public(self):
            return self._private()

Monte::

    def makeClassName():
        var state := 42

        def private():
            return state

        return object objectName:
            to public():
                return private()

Equivalently::

    def makeClassName():
        var state := 42

        return object objectName:
            to public():
                return state
