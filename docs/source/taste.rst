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
empty.  In particular, ``makeTCP4ServerEndpoint`` is not in scope, so the code
cannot use it to access the network.  Neither does the code have any access to
read from nor write to files, clobber global state, nor launch missiles.


__ https://www.owasp.org/index.php/Top_10_2013-A1-Injection

More on ocap (WIP)
~~~~~~~~~~~~~~~~~~

A capability is a reference to an object and represents authority to invoke
methods on the object.

   Monte inherits from E a specific flavor of capability-based security known
   as object capabilities. With object capabilities, capability-oriented
   programming has the same flavor as object-oriented programming, except that
   capability-oriented programming takes the usual object-oriented constraints
   more seriously. Often when using object capabilities for security, one
   finds that a more secure program is simply a program that follows
   object-oriented principles of modularization more closely.

   - The fractal nature of POLA encourages short and readable modules, leading
     to applications having relatively low amounts of code. As a consequence,
     the attack surface of an application is decreased and code review is
     easier. The implementors of E and CapDesk boast of implementing
     peer-to-peer chat systems and digital-money bank servers in hundreds,
     *not* tens of thousands, of lines of code.

     When the time comes for a security inspection, capability security allows
     simple reachability analysis to exclude huge swaths of code because they
     cannot embody a threat. As a consequence, auditing a system for security
     becomes cost-effective to an extent that is simply unimaginable with
     other approaches [#darpa]_.

   - With Monte, it is straightforward to create systems that run across the
     Internet that are as secure and safe as if the entire system were running
     on a single computer in your basement. As one of the original developers
     of Smalltalk observed, upon learning about the object-capability paradigm
     from E, capability security is "natural security": if you shouldn't use
     it, you just can't see it.


Capability Model (WIP)
~~~~~~~~~~~~~~~~~~~~~~

.. note:: Not sure whether this should be here, or in a separate page.

No object created within a scope will be accessible outside of that scope,
unless a message about it is passed out. In Monte, the only way for object A
to know that B exists is:

* If B created A or A was created with knowledge of B
* If A created B
* If any object that A knows about passed A a message about B

For example::

    def scope():
        def a := 1
        def innerScope():
            def b := 2
            traceln(`a is $a and b is $b`)

        # This line would cause a compile-time error, since the name `b` isn't
        # accessible in this scope!
        # traceln(`I cannot access $b here`)

        return innerScope

    scope()()

.. rubric:: Notes

.. [#darpa] As documented in `the DarpaBrowser report
            <http://www.combex.com/papers/darpa-report/index.html>`_

.. [#dos] We implicitly grant authority to compute indefinitely. Object
          capability discipline does not address denial of service. Monte's
          vats include a conventional mechanism to put a finite limit on
          computation.
