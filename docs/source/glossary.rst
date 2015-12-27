========
Glossary
========

Glossary
~~~~~~~~

.. glossary::

    module
        A fundamental unit of compilation for Monte source code. Modules
        consist of a list of imported names, a list of exported objects, and a
        code script which, given the imports, generates the exports.

    retractable
        A :ref:guard that is not :term:`unretractable`.

    unretractable
        An unretractable :ref:guard, informally, cannot be fooled by impostor
        objects that only pretend to be guarded, and it also will not change
        its mind about an object on two different coercions.

        Formally, an :dfn:`unretractable` guard Un is a guard such that for
        all Monte objects, if any given object is successfully coerced by Un,
        then it will always be successfully coerced by Un, regardless of the
        internal state of Un or the object.
