.. _modules:

Modules
=======

Modules are units of compilation. They are single files of Monte source code
which can be compiled on a per-file basis. Modules are relatively
self-contained, declaring their imported and exported names with special
module syntax.

Why Modules?
------------

Some languages don't have modules. Instead, they have *inclusion*, where
source code is literally or semantically transposed from one source file into
another. Our primary goal in providing modules is *encapsulation*, allowing
modules to keep some of their design and layout private.

Some other languages have modules that alter global state. These languages
typically *evaluate* when importing, applying each module's code to the global
state. Our module system abstracts this behavior, *parameterizing* inputs into
modules and allowing for isolated modules that can be evaluated multiple times
without side effects.

.. _module-decl:

Module Declaration Syntax
-------------------------

Module files start with a :dfn:`module header`, which is a declaration of the
form::

    import "namespace/name" =~ [=> first, => second]
    parameter param :DeepFrozen
    exports (maker, main)

with zero or more ``import`` lines, zero or more ``parameter`` lines, and
exactly one ``exports`` line.

.. syntax:: module_header

   Ap('Module',
    NonTerminal('import'),
    NonTerminal('module_params'),
    NonTerminal('exports'))

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

.. syntax:: import

    SepBy(Sigil("import", P('StrExpr'), Sigil("=~", NonTerminal('pattern'))))

Module Parameters
~~~~~~~~~~~~~~~~~

After the imports come the module parameters. Each ``parameter`` line declares
that the module depends on a varying parameter, bound inside the module by a
pattern. Module parameters will usually be guarded by ``DeepFrozen``, but
unlike with imports, no guards are implied by default.

The difference between imports and parameters is that imports are meant to
compose with exports; when multiple modules are assembled all at once, the
exports of one module will be used directly as the imports of another. In
contrast, module parameters are meant to vary the behavior of many modules
which have already been assembled.

For example, it is possible to compile a given top-level module and a
collection of modules into a muffin; a muffin module no longer requires any
imports, because every necessary module has been rolled into a single
katamari. However, module parameters in the muffin are shared between all
modules and do not need to be ``DeepFrozen``, permitting entire applications
to be parameterized by parameterizing each module independently and then
instantiating the corresponding muffin.

Put another way, module parameters are injected dependencies, in the sense of
`dependency injection`_. Only modules which explicitly request to know about
available parameters will be able to bind them, even though they may be
provided throughout an instantiated module graph.

.. _dependency injection: https://en.wikipedia.org/wiki/Dependency_injection

.. syntax:: module_params

    SepBy(Sigil("parameter", NonTerminal('pattern')))

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

      ``m`` is a quasiparser which parses Monte source code. It is part of the
      runtime Monte compiler.

Under the hood, modules are compiled to be DeepFrozen singleton objects which
accept a mapping of imported objects, and return a mapping of exported names.
The module protocol consists of two methods.

The first method, `.requirements/0`, returns a list of strings. Since modules
are immutable, this list cannot vary. When this list is empty, then the module
is a muffin.

The second method, `.run/1`, does the main work of the module. This method
takes a *package* as its sole positional argument; this package should have a
single `.import/1` method which, like the `.get/1` method of maps, should take
every string from the requirements and provide it as a key which maps to an
imported module. We can think of this map as the imports of the module being
evaluated. The method will return a map of strings, but this map contains the
exported values.

In addition to the package, for each module parameter, `.run/1` will expect a
named argument which matches that parameter.

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
