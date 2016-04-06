.. _modules:

Modules
=======

Modules are units of compilation. They are single files of Monte source code
which can be compiled on a per-file basis. Modules are relatively
self-contained, declaring both their imported and exported names with special
module syntax.

.. _module-decl:

Module Declaration Syntax
-------------------------

Module files start with a :dfn:`module header`, which is a declaration of the
form::

    import "namespace/module" =~ [=> pa, => re, => ci]
    exports (makeThing, main)

with zero or more ``import`` lines and exactly one ``export`` line.

.. index:: dependency, pet name, import pattern

Each ``import`` line declares that the module depends on an object
called a :dfn:`dependency`, which is known inside the module by its
:dfn:`pet name`. In this example, the pet name is
"namespace/module". The dependency is matched against the pattern on
the right-hand side of the ``=~`` operator, called the :dfn:`import
pattern`, and the resulting names are available for use throughout the
body of the module.

A single ``exports`` line follows the import declarations. This line declares a
list of nouns which will be *exported* from the module's scope. Exported names
will be available to other modules which import this module.

All exports must pass ``DeepFrozen``::

    imports
    exports (f)

    def f() as DeepFrozen:
        return 42

.. syntax:: module_header

   Ap('Module',
    Sigil("imports", P('StrExpr'), Sigil("=~", SepBy(NonTerminal('namePatt')))),
    Maybe(P('exports')),
    NonTerminal('sequence'))

.. syntax:: exports

   Sigil('exports', Brackets("(", SepBy(NonTerminal('name'), ","), ")"))


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

.. _module_expansion:

Module Syntax Expansion
~~~~~~~~~~~~~~~~~~~~~~~

.. sidebar:: Kernel-Monte and Expansion

           .. index: kernel, Kernel Monte, expansion
           .. index:: expansion, syntactic expansion

           The Monte language as seen by the programmer has the rich
           set of syntactic conveniences expected of a modern
           scripting language. However, to avoid complexity that so
           often hampers security, the :doc:`semantics of Monte
           <semantics>` is primarily defined over a smaller language
           called :dfn:`Kernel-Monte`. The rest of E is defined by
           :dfn:`syntactic expansion` to this subset. For example::

              >>> m`1 + 1`.expand()
              m`1.add(1)`

           ``m`` is a :doc:`quasiparser<quasiparsers>` that parses
           Monte source code. It is part of the runtime Monte compiler.

Under the hood, modules are compiled to be singleton objects which accept
a mapping of imported objects, and return a mapping of exported names.

.. index:: entrypoint, main, unsafe capabilities
.. _entrypoints:

Entrypoints
-----------

The export name "main", when present, denotes the :dfn:`entrypoint` of
the module.  The entrypoint should take named parameters corresponding
to unsafe capabilities from the unsafe scope, and return an ``Int`` or
a promise for an ``Int``.

::

    exports (main)

    def main(=> currentProcess) :Int as DeepFrozen:
        traceln(`Current process: $currentProcess`)
        return 0

Unit Testing and Benchmarking
-----------------------------

The package loader provides a few Miranda import pet names to all modules.

"unittest"
    A unit test collector. It is not ``DeepFrozen``, so unit tests are
    confined to their module::

      import "unittest" =~ [=> unittest]

"bench"
    A benchmark collector. It is not ``DeepFrozen``::

        import "bench" =~ [=> bench]
