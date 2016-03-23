===========================
A Taste of Monte: Hello Web
===========================

Let's see what a simple web server looks like in monte:

.. literalinclude:: tut/web1.mt
    :linenos:
    :language: monte

The ``imports`` line begins a :ref:`module <modules>` and we declare
that this module ``exports`` its ``main`` function, as is conventional
for executable programs.

The :ref:`def expression<def>` for defining the ``helloWeb`` function is
similar to Python and the like.

.. todo:: Forward ref :ref:`auditors` or find a way to elide
          ``DeepFrozen``. (Issue #43).

The ``smallBody`` import works much like Python's ``from
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

The critical distinction between monte and other memory-safe dynamic languages
is that monte is an :ref:`object capability <ocap>` lanugage. Powerful objects
such as ``currentProcess`` and ``makeTCP4ServerEndpoint`` are not in any
global namespace; they cannot be imported. Rather, they are provided
explicitly to the ``main`` function. Except by explicit delegation, no code
can do anything more more than create objects (including functions) in memory.
It cannot read from nor write to files, access the network, clobber global
state, or launch missiles.

By straightforward inspection, we can see that
  - only one TCP port is ever created;
  - its port number is taken from the last command-line argument.


Expressions and Patterns
------------------------

.. todo:: move "expressions and patterns" syntax material here.

Objects and Message Passing
---------------------------

.. todo:: move "objects and message passing" material here.

Indentation and Blocks
----------------------

.. todo:: move "Indentation and Blocks" material here.

Using Library Modules
---------------------

.. todo:: move "Using Library Modules" material here.

DeepFrozen Module Exports
-------------------------

.. todo:: move DeepFrozen blurb here.

