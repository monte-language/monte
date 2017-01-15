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
