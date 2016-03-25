===========================
A Taste of Monte: Hello Web
===========================

Let's see what a simple web server looks like in monte:

.. literalinclude:: tut/web1.mt
    :linenos:
    :language: monte

.. todo:: document how to compile and run such a script.

Indentation and Blocks
----------------------

Monte shares much of its syntax with the C family of languages, but
each form with braces can also be written as an indented block, as in
Python or Haskell::

  >>> def helloWeb(request) { def reply := [200]; return reply }
  ... helloWeb("/")
  [200]

  >>> def helloWeb(request):
  ...     def reply := [200]
  ...     return reply
  ... helloWeb("/page1")
  [200]

Standardize your indentation to use spaces, because tabs are a syntax
error in Monte. Monte core library code uses four-space indentation.


Using Library Modules
---------------------

A :ref:`module declaration <module-decl>` has any number of ``import``
declarations followed by an ``exports`` declaration.

The ``makeHTTPEndpoint`` import reads much like Python's ``from
lib.http.server import makeHTTPEndpoint``, though the mechanics are a
bit different: it uses :ref:`pattern matching <patterns>` to bind
names to objects imported from :ref:`modules <modules>`.


DeepFrozen Module Exports
-------------------------

We declare that this module ``exports`` its ``main`` function, as is
conventional for executable programs.

One of the constraints of :ref:`object capability discipline <ocap>`
is that there is no global mutable state; so exported objects must be
``DeepFrozen``, i.e. transitively immutable. Since ``main`` calls
``helloWeb``, ``helloWeb`` must be ``DeepFrozen`` as well. We'll
discuss this and other static properties of monte code in the
:ref:`auditors` section.


Expressions and Patterns
------------------------

The :ref:`def expression<def>` for defining the ``helloWeb`` function
is similar to Python and the like.  Note that unlike python and C,
which use a mix of statements and expressions, Monte is an expression
language, like Scheme. So ``def body ...`` is an expression with a
value, just like string literals and method calls.

The expression inside the call to ``traceln(...)`` does string
interpolation much like perl or ruby. It's a
:ref:`quasiliteral<quasiliteral>`::

    traceln(`serving on port $portNum`)

Another quasiliteral is b`<p>Hello!</p>`, which denotes a ``Bytes``
object rather than a character string.

This short example includes just a few of Monte's :ref:`patterns
<patterns>`::

    [=> name :Guard]
    name


Objects and Message Passing
---------------------------

Monte is a pure object language.  All operations on objects are done
by :ref:`sending messages<message_passing>`.  This includes ordinary
method calls such as ``argv.last()`` as well as function calls such as
``traceln(portNum)`` and even constructing maps ``["C" => "t"]`` and
lists ``[200, [], body]``.

.. todo:: fwd ref f.run(), _makeList, _makeMap


No Powerful References by Default
---------------------------------

The critical distinction between monte and other memory-safe dynamic languages
is that monte is an :ref:`object capability <ocap>` lanugage. Powerful objects
such as ``makeTCP4ServerEndpoint`` are not in any
global namespace; they cannot be imported. Rather, they are provided
explicitly to the ``main`` function. Except by explicit delegation, no code
can do anything more more than create objects (including functions) in memory.
It cannot read from nor write to files, access the network, clobber global
state, or launch missiles.

By straightforward inspection, we can see that
  - only one TCP port is ever created;
  - its port number is taken from the last command-line argument.
