Modules in Monte
================

Concepts and Terms
------------------

script
  A source file run as the entry point for a program (such as from the
  command line).

module file
  Source files starting with a ``module`` declaration.

module structure
  An object representing imported  and exported names of a module.

module configuration
  An object representing a the association of a module's import names
  with objects. Created from a module structure.

package
  A module composed from other modules.

package script
  A source file run at link time that produces a module structure for
  its package, possibly by reading module structures from various
  module files.

requirement
  An object given as an argument to a module when creating a package,
  to create an import name for the package.


Mechanics
---------

Scripts are run in a scope with an ``import(name, parameters)``
function, which can be invoked to load modules. The name is used to
locate either a module file or a directory containing a package script
(currently required to be named ``package.mt``). The module is loaded
and its exports are returned as a map.


Package Scripts
---------------

Package scripts are run in the safe scope with the addition of a
package loader object ``pkg``.

The package provides these methods:

``readFiles(relativePath)``
  Creates a map of module names to module structures, for all modules
  found recursively on the given path.

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


Module Structures
-----------------

Module structures' ``run`` methods can be invoked with a mapping of
names to configurations or requirements to create a new module
configuration.
