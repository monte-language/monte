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

module file
  Source files starting with an ``imports`` declaration.

module structure
  An object representing imported and exported names of a module.

module configuration
  An object representing a the association of a module's import names
  with objects. Created from a module structure.

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

Module files start with a **module header**, which is a declaration of the
form::

    imports => dependency1, => dependency2, ...
    exports (name1, name2, ...)

Names specified on the `imports` line are import declarations. Each import
declaration should be a named parameter. Imports can have guards on them::

    imports => preChilled :DeepFrozen
    exports ()

This is extremely useful for ensuring that imported names are ``DeepFrozen``.

Export declarations are names defined in the module. Every exported name must
pass audition by ``DeepFrozen``::

    imports
    exports (f)

    def f() as DeepFrozen:
        return 42

Mechanics
---------

.. note::
    Packages currently are being reworked. The ``name`` parameter of
    ``import()`` currently selects modules from a single global namespace.

Scripts are run in a scope by ``import(name :Str, parameters :Map[Str,
Any])``,
which can be invoked to load modules. The name is used to locate either a
module file or a directory containing a package script (currently required to
be named ``package.mt``). A configuration is created from the structure read
from this, and then loaded with the parameters given, and its exports are
returned as a map.

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

.. note::
    Tests are not automatically discovered at present. You need to add your
    test to a package.mt file for it to be run correctly.

.. note::
    Corbin was too lazy to rewrite this, but it is quite old.

Unit tests are essential to writing good code. Monte's testing framework is
designed to make it simple to write and run good tests. See the testing.mt_
module for a simple example. Note that for more complex objects, you may need
to implement an `_uncall()` method which describes how to recreate the object
out of Monte's built-in primitives. Additionally, such objects will need to
implement the Selfless interface in order to guarantee they won't have mutable
state so that they can be compared.

To test the Python tools surrounding Monte, use Trial. For instance, ``trial
monte.test.test_ast`` (when run from the root of the project) will run the ast
tests.

.. _testing.mt: https://github.com/monte-language/monte/blob/master/monte/src/examples/testing.mt

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


Ordinary Computing Examples / A Taste of Monte
==============================================

Let's see what a simple web server looks like in monte:

.. literalinclude:: tut/web1.mt
    :linenos:
    :language: monte

The ``imports`` line begins a :ref:`module <modules>` and we declare
that this module ``exports`` its ``main`` function, as is conventional
for executable programs.

The :ref:`def expression<def>` for defining the ``helloWeb`` function is
similar to python and the like.

.. todo:: Forward ref :ref:`auditors` or find a way to elide
          ``DeepFrozen``. (Issue #43).

The ``smallBody`` import works much like python's ``from
lib.http.resource import smallBody``, using :ref:`pattern matching
<patterns>` to bind names to objects imported from :ref:`modules
<modules>`.

.. todo:: hoist imports to toplevel once these library modules
          have gone through the module migration.

The ``escape`` expression introduces an :ref:`ejector <ejector>` called
``badRequest``, which we use to deal with ill-formed requests in a
fail-stop manner in case the ``request`` doesn't match the
``[[verb, path], headers]`` pattern.

The ``body`` is defined using :ref:`method calls<message_passing>`
on the imported ``tag`` object.

The critical distinction between monte and other memory-safe dynamic
languages is that monte is an :ref:`object capability <ocap>`
lanugage. Powerful objects such as ``currentProcess`` and
``makeTCP4ServerEndpoint`` are not in any global namespace; they
cannot be imported. Rather, they are provided explicitly to the
``main`` function. Except by explicit delegation, no code can do
anything more more than create objects (including functions) in
memory. It cannot read from nor write to files [#]_, access the
network, clobber global state, or launch missiles.

By straightforward inspection, we can see that
  - only one TCP port is ever created;
  - its port number is taken from the last command-line argument.
