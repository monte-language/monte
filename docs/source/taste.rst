.. _taste:

===========================
A Taste of Monte: Hello Web
===========================

Let's see what a simple web server looks like in Monte:

.. literalinclude:: tut/web1.mt
    :linenos:
    :language: monte

The ``makeHTTPEndpoint`` import reads much like Python's ``from
lib.http.server import makeHTTPEndpoint``, though the mechanics of a
:ref:`module declaration <module-decl>` in monte are a bit different:
it uses :ref:`pattern matching <patterns>` to bind names to objects
imported from modules.


.. sidebar:: DeepFrozen Module Exports

   One of the constraints of :ref:`object capability discipline
   <ocap>` is that there is no global mutable state; so exported
   objects must be ``DeepFrozen``, i.e. transitively immutable. Since
   ``main`` calls ``helloWeb``, ``helloWeb`` must be ``DeepFrozen`` as
   well. We'll discuss this and other static properties of Monte code
   in the :ref:`auditors` section.


We declare that this module ``exports`` its ``main`` function, as is
conventional for executable programs.

.. todo:: Document how to compile and run such a script.

Blocks in Monte are typically written with indentation, like Python,
though :ref:`blocks in general <indent_blocks>` may be written with
curly-braces as well.

.. note:: Tabs are a syntax error in Monte.


Expressions
-----------

The :ref:`def-expr<def>` for defining the ``helloWeb`` function is similar to
Python's syntax for defining functions.

.. sidebar:: Expression Languages

    Unlike Python, Haskell, and C, which use a mix of statements and
    expressions, Monte is an expression language, like Scheme. So ``def
    body…`` is an expression with a value, just like string literals and
    method calls.

The expression inside the call to ``traceln(…)`` does string interpolation,
similar to Perl, Ruby, and bash. It is a :ref:`quasiliteral<quasiliteral>`
expression::

    ▲> def portNum := 8080
    ▲> `serving on port $portNum`
    "serving on port 8080"

Another quasiliteral is ``b`<p>Hello!</p>```, which denotes a ``Bytes`` object
rather than a character string.


Objects and Message Passing
---------------------------

Monte is a pure object language, which means that all values in Monte are
objects. All operations on objects are done by :ref:`passing
messages<message_passing>`. This includes ordinary method calls like
``argv.last()`` as well as :ref:`function calls<def-fun>` such as
``traceln(portNum)`` and even syntax for constructing :ref:`lists<ListExpr>`
like ``[200, [], body]`` and :ref:`maps<MapExpr>` like ``["C" => "t"]``.


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
dramatically less vulnerability [#dos]_.  The environment in this example is
:ref:`safeScope`, which is the same environment modules are evaluated in -- it
provides basic runtime services such as constructors for lists, maps, and
other structures, but no "powerful" objects.  In particular,
``makeTCP4ServerEndpoint`` is not in scope when the remote code is executed,
so the code cannot use it to access the network.  Neither does the code have
any access to read from nor write to files, clobber global state, nor launch
missiles.

__ https://www.owasp.org/index.php/Top_10_2013-A1-Injection

.. rubric:: Notes

.. [#dos] We implicitly grant authority to compute indefinitely. Object
          capability discipline does not address denial of service. Monte's
          vats include a conventional mechanism to put a finite limit on
          computation.
