.. _taste:

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

Monte shares much of its syntax with the C family of languages::

  >>> def helloWeb(request) { return [200, "hello"]; }
  ... helloWeb("/")
  [200, "hello"]

But as in Haskell, each form with braces can also be written as an indented
block, so that idiomatic Monte as looks much like Python.

Standardize your indentation to use spaces, because tabs are a syntax
error in Monte. Monte core library code uses four-space indentation.


Using Library Modules
---------------------

A :ref:`module declaration <module-decl>` has any number of ``import``
declarations followed by an ``exports`` declaration.

The ``makeHTTPEndpoint`` import reads much like Python's ``from
lib.http.server import makeHTTPEndpoint``, though the mechanics are a bit
different: it uses :ref:`pattern matching <patterns>` to bind names to objects
imported from modules.


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

Monte is a pure object language.  All operations on objects are done by
:ref:`sending messages<message_passing>`.  This includes ordinary method calls
such as ``argv.last()`` as well as :ref:`function calls<def-fun>` such as
``traceln(portNum)`` and even constructing :ref:`lists<ListExpr>` ``[200, [],
body]`` and :ref:`maps<MapExpr>` ``["C" => "t"]``.


Cooperation Without Vulerability
--------------------------------

Suppose our server takes an arbitrary expression from the web client and
evaluates it:

.. literalinclude:: tut/web2.mt
    :linenos:
    :language: monte

With conventional languages and frameworks, this would be `injection`__, #1 on
the list of top 10 web application security flaws:

  Injection can result in data loss or corruption, lack of accountability, or
  denial of access. Injection can sometimes lead to complete host takeover.

But using object capability discipline, untrusted code has only the authority
that we explicitly give it.  This rich form of cooperation comes with
dramatically less vulerability [#dos]_.  The environment in this example is
empty.  In particular, ``makeTCP4ServerEndpoint`` is not in scope when the
remote code is executed, so the code cannot use it to access the network.
Neither does the code have any access to read from nor write to files, clobber
global state, nor launch missiles.

__ https://www.owasp.org/index.php/Top_10_2013-A1-Injection

.. rubric:: Notes

.. [#dos] We implicitly grant authority to compute indefinitely. Object
          capability discipline does not address denial of service. Monte's
          vats include a conventional mechanism to put a finite limit on
          computation.
