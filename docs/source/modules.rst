.. _modules:

================
Modules in Monte
================

Modules are units of compilation. They are single files of Monte source code
which can be compiled on a per-file basis. Modules are relatively
self-contained, declaring both their imported and exported names with special
module syntax.

Module Declaration Syntax
-------------------------

Module files start with a :dfn:`module header`, which is a declaration of the
form::

    import "namespace/module" =~ [=> pa, => re, => ci]
    exports (makeThing, main)

With zero or more ``import`` lines and exactly one ``export`` line.

Each ``import`` line declares that the module depends on an object called a
*dependency*, which is known inside the module by its *pet name*. In this
example, the pet name is "namespace/module". The dependency is matched against
the pattern on the right-hand side of the ``=~`` operator, called the *import
pattern*, and the resulting names are available for use throughout the body of
the module.

A single ``exports`` line follows the import declarations. This line declares a
list of nouns which will be *exported* from the module's scope. Exported names
will be available to other modules which import this module.

All exports must pass ``DeepFrozen``::

    imports
    exports (f)

    def f() as DeepFrozen:
        return 42

Conventions
~~~~~~~~~~~

Each import pattern, by convention, should be a named parameter mapping a
``Str`` key to a noun. This mirrors exported names, so that a name exported
from one module can be imported by another easily.

Imports can have guards on them::

    import "fries/victor" =~ [=> diamonds :DeepFrozen]
    exports (freezeRay, oneLiners)

This is extremely useful for ensuring that imported names are ``DeepFrozen``
and thus usable by exported objects.

Entrypoints
~~~~~~~~~~~

The export name "main", when present, denotes the *entrypoint* of the module.
The entrypoint should take named parameters corresponding to unsafe
capabilities from the unsafe scope, and return an ``Int`` or a promise for an
``Int``.

::

    exports (main)

    def main(=> currentProcess) :Int as DeepFrozen:
        traceln(`Current process: $currentProcess`)
        return 0

Under the Hood
--------------

Under the hood, modules are compiled to be singleton objects which accept
a mapping of imported objects, and return a mapping of exported names.

The Package Loader
------------------

Miranda Imports
~~~~~~~~~~~~~~~

The package loader provides a few Miranda import pet names to all modules.

"unittest"
    A unit test collector. It is not ``DeepFrozen``, so unit tests are
    confined to their module::
    
        import "unittest" =~ [=> unittest]
        exports (adder)

        def adder(x, y) as DeepFrozen:
            return x + y

        def testAdder(assert):
            assert.equal(adder(5, 7), 12)

        unittest([testAdder])

"bench"
    A benchmark collector. It is not ``DeepFrozen``::

        import "bench" =~ [=> bench]

Module Syntax Summary
---------------------

.. syntax:: module

   Sequence(
    ZeroOrMore(Sequence("import", ".String.", "=~", NonTerminal('pattern'))),
    Optional(NonTerminal('exports')),
    NonTerminal('block'))

.. syntax:: exports

   Sequence("exports", "(", ZeroOrMore(NonTerminal('name')), ")")
