.. _modules:

Modules
=======

Modules are units of compilation. They are single files of Monte source code
which can be compiled on a per-file basis. Modules are relatively
self-contained, declaring both their imported and exported names with special
module syntax.

Why Modules?
------------

Some languages don't have modules. Instead, they have *inclusion*, where
source code is literally or semantically transposed from one source file into
another. Our primary goal in providing modules is *encapsulation*, allowing
modules to keep some of their design and layout private.

Some other languages have modules that alter global state. These languages
typically *evaluate* when importing, applying each module's code to the global
state. Our module system abstracts this behavior, *parameterizing* inputs to
modules and allowing for isolated modules that can be evaluated multiple times
without side effects.

.. _module-decl:

Module Declaration Syntax
-------------------------

Module files start with a :dfn:`module header`, which is a declaration of the
form::

    import "namespace/name" =~ [=> first, => second]
    exports (maker, main)

with zero or more ``import`` lines and exactly one ``exports`` line.

.. _imports:

Imports
~~~~~~~

.. index:: dependency, pet name, import pattern

Each ``import`` line declares that the module depends on a named
:dfn:`dependency`, which is known inside the module by its :dfn:`pet name`. In
this example, the pet name is "namespace/name". The dependency is matched
against the pattern on the right-hand side of the ``=~`` operator, called the
:dfn:`import pattern`, and the resulting names are available for use
throughout the body of the module.

By convention, pet names have two pieces: The :dfn:`module namespace` and the
module's name.

.. todo::
    When new packaging efforts are ready, update this to mention that module
    namespaces are either the stdlib or a package name.

As a convenience, if the import pattern is a map-pattern, then an automatic
ignore-pattern tail will be attached by the expander. This makes forward
compatibility easier, as unknown names in imported modules will not throw
exceptions.

.. _exports:

Exports
~~~~~~~

A single ``exports`` line follows the import declarations. This line declares a
list of nouns which will be *exported* from the module's scope. Exported names
will be available to other modules which import this module.

All exports must pass ``DeepFrozen``::

    exports (f)

    def f() as DeepFrozen:
        return 42

Which means that exports can only depend on ``DeepFrozen`` imports::

    import "unittest" =~ [=> unittest :Any] # not DeepFrozen!
    exports (f)

    def f() as DeepFrozen: # Exception: `unittest` in the scope of `f` isn't DeepFrozen!
        return unittest

.. syntax:: module_header

   Ap('Module',
    SepBy(Sigil("imports", P('StrExpr'), Sigil("=~", NonTerminal('pattern')))),
    NonTerminal('exports'))

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

In fact, by default, imported names are automatically guarded with
``DeepFrozen``. This allows those imported names to be used in exported
objects.

.. _module_expansion:

Module Syntax Expansion
~~~~~~~~~~~~~~~~~~~~~~~

.. sidebar:: Kernel-Monte and Expansion

      .. index: kernel, Kernel Monte, expansion
      .. index:: expansion, syntactic expansion

      The Monte language as seen by the programmer has the rich set of
      syntactic conveniences expected of a modern scripting language.
      However, to avoid complexity that so often hampers security, the
      :doc:`semantics of Monte <semantics>` is primarily defined over a
      smaller language called :dfn:`Kernel-Monte`. The rest of Monte,
      called :dfn:`Full-Monte`, is defined by :dfn:`syntactic expansion`
      to this subset. For example::

         >>> m`1 + 1`.expand()
         m`1.add(1)`

      ``m`` is a :doc:`quasiparser<quasiparsers>` that parses
      Monte source code. It is part of the runtime Monte compiler.

Under the hood, modules are compiled to be DeepFrozen singleton objects which
accept a mapping of imported objects, and return a mapping of exported names.
The module protocol consists of two methods.

The first method, `.requirements/0`, returns a list of strings. Since modules
are immutable, this list cannot vary. When this list is empty, then the module
is a muffin.

The second method, `.run/1`, does the main work of the module. This method
takes a map as its sole argument, and this map should take every string from
the requirements and provide it as a key which maps to an imported module. We
can think of this map as the imports of the module being evaluated. The method
will return another map of strings, but this map contains the exported values.

Module loaders will check that module exports are immutable by guarding them
with `Map[Str, DeepFrozen]`. This is crucial for enforcing module isolation.

.. index:: entrypoint, main, entrypoint capabilities
.. _entrypoints:

Entrypoints
-----------

The export name "main", when present, denotes the :dfn:`entrypoint` of the
module.  The entrypoint should take named parameters corresponding to
entrypoint capabilities, and return an ``Int`` or a promise for an ``Int``.

::

    exports (main)

    def main(_argv, => currentProcess) :Int as DeepFrozen:
        traceln(`Current process: $currentProcess`)
        return 0

Unit Testing and Benchmarking
-----------------------------

The package loader provides a few Miranda import pet names to all modules.

"unittest"
    A unit test collector. It is not ``DeepFrozen``, so unit tests are
    confined to their module::

      import "unittest" =~ [=> unittest :Any]

"bench"
    A benchmark collector. It is not ``DeepFrozen``::

        import "bench" =~ [=> bench :Any]
