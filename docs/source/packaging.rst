Working with Packages
=====================

The source code for the Mafia game and IRC bot are in their own git repository,
https://github.com/monte-language/mt-mafia . Let's download and run it::

  git clone https://github.com/monte-language/mt-mafia
  cd mt-mafia
  mt test mafiabot
  mt run mafiabot chat.freenode.net
This should result in the bot connecting to IRC and being ready to receive commands.

Monte packages are defined by a file in the project root directory named
``mt.json``. This file includes package metadata and a list of dependencies. Previous to the first run, a Nix package is built from the project and its dependencies (currently these can either be from a local directory or a Git repository). The ``mt test`` command collects all unit tests in the project and starts the test runner, whereas ``mt run`` invokes the ``main`` function in mafiabot.mt. (The build step can be invoked directly using ``mt build``.)

The format for ``mt.json`` is a JSON file with the following keys:

name
  A name for the package.

paths
  A list of paths relative to the project root that contain Monte code. "." is acceptable if it's in the root.

entrypoint
  The name of the module with the ``main`` function to invoke. Optional.

dependencies
  An object with package names as keys and dependency descriptions as values. Dependency descriptions are objects with ``url`` keys naming a location to fetch the dependency from, and optionally ``type`` (either "git" or "local" -- defaults to ``git`` if omitted) and ``commit`` (describing the git revision to fetch) keys.


Building the Nix package involves first creating an ``mt-lock.json`` file with a full list of all dependencies and their versions. You may keep this file to pin your builds to specific versions or get rid of it to re-run the dependency discovery process.
