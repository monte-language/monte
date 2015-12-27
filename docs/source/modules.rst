.. _modules:

Modules in Monte
================

Modules are units of compilation. They are single files of Monte source code
which can be compiled on a per-file basis.

Concepts and Terms
------------------

script
  A source file run as the entry point for a program (such as from the
  command line).

package
  A module structure composed from various module configurations.

package script
  A source file run at link time that produces a module structure for
  its package, possibly by reading module structures from various
  module files.

requirement
  An object given as an argument to a module when creating a package,
  to create an import name for the package.

Module Declaration Syntax
-------------------------

Module files start with a :dfn:`module header`, which is a declaration of the
form::

    imports => dependency1, => dependency2, ...
    exports (name1, name2, ...)

Names specified on the `imports` line are import declarations. Each import
declaration should be a named parameter. Imports can have guards on them::

    imports => preChilled :DeepFrozen
    exports ()

This is extremely useful for ensuring that imported names are ``DeepFrozen``
and thus usable by exported objects.

Export declarations are names defined in the module. Every exported name must
pass audition by ``DeepFrozen``::

    imports
    exports (f)

    def f() as DeepFrozen:
        return 42

.. syntax:: module_

   Ap('Module',
    Sigil("imports", SepBy(NonTerminal('namePatt'))),
    Maybe(
      Sigil('exports', Brackets("(", SepBy(NonTerminal('name'), ","), ")"))),
    NonTerminal('block'))


Mechanics
---------

.. note::
    Packages currently are being reworked. The ``name`` parameter of
    ``import()`` currently selects modules from a single global namespace.

Scripts are run in a scope by ``import(name :Str, parameters :Map[Str,
Any])``, which can be invoked to load modules. The name is used to locate
either a module file or a directory containing a package script (currently
required to be named ``package.mt``). A configuration is created from the
structure read from this, and then loaded with the parameters given, and its
exports are returned as a map.

Package Scripts
---------------

.. note::
    This all is obsolete. Sorry.

Package scripts are run in the safe scope with the addition of a
package loader object ``pkg``.

The package provides these methods:

``readFile(relativePath)``
  Read the module file at the given path and return a module structure.

``readFiles(relativePath)``
  Creates a map of module names to module structures, for all module files
  found recursively on the given path.

``readPackage(relativePath)``
  Creates a module structure by running the package script in the
  given directory.

``require(name)``
  Creates a requirement object with the given name.

``testCollector()``
  Object for collection of unit tests, to be passed to modules
  containing tests that should be discovered by a test
  runner. (Incomplete.)

``makeModule(contents)``
  Creates a module structure from a mapping of names to module
  configurations. Its exports will be the names from the mapping and
  its imports will be the names from the requirement objects contained
  in the configurations.

.. note:: See also `safeScope`__ source.

__ https://github.com/monte-language/typhon/blob/master/typhon/scopes/safe.py#L375


Module Structures
-----------------

Module structures' ``run`` methods can be invoked with a mapping of
names to configurations or requirements to create a new module
configuration.

Testing
-------

When a module is loaded, the name ``unittest`` will be passed. This object can
be used to collect tests. It is not ``DeepFrozen``, so it cannot be captured
by module exports.

::

    imports => unittest
    exports (adder)

    def adder(x, y) as DeepFrozen:
        return x + y

    def testAdder(assert):
        assert.equal(adder(5, 7), 12)

    unittest([testAdder])

Module Syntax Summary
---------------------

.. syntax:: module

   Sequence(
    Optional(Sequence("imports",
                      NonTerminal('imports'),
                      Optional(NonTerminal('exports')))),
    NonTerminal('block'))

.. syntax:: imports

   ZeroOrMore(NonTerminal('namedPattern'))

.. syntax:: exports

   Sequence("exports", "(", ZeroOrMore(NonTerminal('name')), ")")
