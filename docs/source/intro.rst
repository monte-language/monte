=========================
Monte is Serious Business
=========================

Introduction
============

What's Monte?
-------------

Monte is a high-level programming language whose design philosophy is
that **secure distributed computing should not be hard**. It provides
much of the expressive convenience of python but also robust
composition using object capabilities in the tradition of E [#]_.

.. note:: While Monte usable and most architectural issues are
	  resolved, it is still undergoing rapid development.
	  See :ref:`roadmap` for details.


Why Monte?
----------

Because `everything is broken`__. Python has great usability, borne
out by a large developer community, but it shares a fundamentally
brittle architecture with much of today's programming languages and
platforms: *insecurity anywhere is a threat to security everywhere*.
While E is comparatively obscure, its object capability discipline
naturally supports the *principle of least authority* so that
malicious or faulty code in one part of a system is straightforwardly
contained. Monte provides the robust composition features of E
in a form that's convenient to the Python developer community.

__ https://medium.com/message/everything-is-broken-81e5f33a24e1

A Taste of Monte
----------------

Let's compose a simple web server from a main program...

.. literalinclude:: tut/web1priv.mt
    :linenos:
    :language: monte

... and an imported `web1` module:

.. literalinclude:: tut/web1.mt
    :linenos:
    :language: monte

The basics of defining functions and calling methods should be
familiar to anyone with exposure to python or even ruby or the C/C++
family (Java, JavaScript, PHP).

.. note:: The import function returns a `ConstMap` (a la python
	  dictionary, but immutable), and `def [=> smallBody] | _ :=
	  import(...)` is a pattern-matching binding, where `[=>
	  smallBody]` is short for `["smallBody" => smallBody]`.  The
	  result is similar to `from lib.http.resource import
	  smallBody`.

We keep the main program to a minimum because it is loaded in the
privileged "unsafe" scope. We can refer to `currentProcess` and
`makeTCP4ServerEndpoint` in this scope.

On the other hand, imported modules such as `web1` (and the various
library modules) are loaded in the safe scope, so that executing them
can do nothing more than create objects (including functions) in
memory and export the value of the last expression (typically, a map
of exported objects). Importing them cannot write to files, access the
network, clobber global state, or launch missiles.

Only when access to make an HTTP endpoint is passed to start() can
this code interact with the network. And by inspection of
`makeWebServer()`, we can see that it can only use the HTTP protocol,
and only on the port given by the last command-line argument.


Where do I start?
-----------------

If you'd like to get involved with developing or using the Monte language,
start by getting acquainted with Python_'s syntax and the computational
concepts of E_. 

Then clone the repo_ and follow the directions below to begin running Monte
code. If you have problems, join us in #monte on irc.freenode.net, ask your
question (use a pastebin_ to share any errors, rather than pasting into the
channel), and wait a few hours if nobody is around. 

If you'd like to contribute to Monte, check out the Monte_ and Typhon_ issue
trackers and the `pipe dreams`_ wiki page. It's also worth grepping for
``TODO`` in the source of both projects. 

.. _Monte: https://github.com/monte-language/monte/issues
.. _Typhon: https://github.com/monte-language/typhon/issues
.. _pipe dreams: https://github.com/monte-language/monte/wiki/Pipe-Dreams
.. _Python: https://docs.python.org/2/tutorial/
.. _E: http://www.skyhunter.com/marcs/ewalnut.html
.. _repo: https://github.com/monte-language/monte
.. _pastebin: http://bpaste.net/

Using Monte
===========

To use the Monte implementation hosted in Python, it's best to set up a
virtualenv:

.. code-block:: console

    $ virtualenv v
    $ source v/bin/activate
    $ pip install -r requirements.txt

To run Monte code (with your virtualenv activated):

.. code-block:: console

    $ bin/monte monte/src/examples/hello.mt

The Repl
--------

Many languages have an interpreter or "Read - Evaluate - Print Loop" for
testing code. Monte's should be documented here if/when it gets one.

Indentation
-----------

Standardize your indentation to use spaces, because tabs are a syntax error in
Monte. Monte core library code uses four-space indentation. However, any
indentation can be used as long as it's consistent throughout the module.

Scoping Rules
-------------

Monte is lexically scoped, with simple scoping rules. In general, names are
only accessible within the scope in which they were defined.

After an object has been created, the names visible to it aren't accessible
from outside the object. This is because Monte objects cannot share their
internal state; they can only respond to messages. For programmers coming from
object-oriented languages with access modifiers, such as ``private`` and
``protected``, this is somewhat like if there were only one access modifier
for variables, ``private``. (And only one access modifier for methods,
``public``.)

Closing Over Bindings
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: monte

    var x := 42
    object obj:
        to run():
            return x += 1

Here, ``obj`` can see ``x``, permitting the usage of ``x`` within ``obj``'s
definition. When ``obj.run()`` is called, ``x`` will be mutated. Monte does
not require any "global" or "nonlocal" keywords to do this.

Capability Model
----------------

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

Debugging Stuff
---------------

Monte strives to provide useful error messages.

Currently the most convenient way to print out messages from your program is
with the ``trace()`` and ``traceln()`` built-in functions. The only difference
between them is that ``traceln()`` automatically adds a newline.

Methods, Objects, Variables
---------------------------

Named values can be either final or variable. A final object cannot be
changed, whereas a variable one can be changed later::

    var myVariableValue := 6

    myVariableValue *= 7

    trace("My variable value: ")
    traceln(`$myVariableValue`)

    def myFinalValue := 42
    # Trying to change a final value will result in a compile-time error. See
    # what happens when this next line is uncommented!
    # myFinalValue /= 6

    trace("My final value: ")
    traceln(`$myFinalValue`)

Everything is an object. New objects are created with a ``object`` keyword::

    object helloThere:
        to greet(whom):
            traceln(`Hello, my dear $whom!`)

    helloThere.greet("Student")

Objects can also be created by functions::

    def makeSalutation(time):
        return object helloThere:
            to greet(whom):
                traceln(`Good $time, my dear $whom!`)

    def hi := makeSalutation("morning")

    hi.greet("Student")

Object Composition
------------------

Monte has a simpler approach to object composition and inheritance than many
other object-based and object-oriented languages. Instead of classes or
prototypes, Monte has a simple single syntax for constructing objects, the
object expression::

    object myObject:
        pass

Unlike Java, Monte objects are not constructed from classes. Unlike JavaScript
or Python, Monte objects are not constructed from prototypes. As a result, it
might not be obvious at first how to build multiple objects which are similar
in behavior. However, Monte has a very simple idiom for class-like constructs.

::

    def makeMyObject():
        return object myObject:
            pass

Methods can be attached to objects with the to keyword::

    object deck:
        to size():
            return 52

Finally, just like with functions, methods can have guards on their parameters
and return value::

    object deck:
        to size(suits :Int, ranks :Int) :Int:
            return suits * ranks

Built-In Types
--------------

Monte provides some classic and common value types directly in the syntax.

Int
~~~

Monte has integer literals. 

.. code-block:: monte

    def x := 5
    def x := 128 ** 128 ** 128

A variety of mathematical methods are available. Integers aren't fixed-width;
they can store arbitrarily large values. 

Char
~~~~

Monte's character type is distinct from the string type. Characters are always
surrounded by apostrophes (``'``) and are always unicode.

.. warning:: 

    In Python, you may be accustomed to 'single' and "double" quotes
    functioning interchangeably. In Monte, double quotes can contain any
    number of letters, but single quotes can only hold a single character. 

.. code-block:: monte

    def u := '☃'

Characters are permitted to be adorable.

String
~~~~~~

Strings are objects with built-in methods and capabilities, rather than
character arrays. Monte's strings are always unicode, like Python 3 (but
unlike Python 2). Strings are always surrounded by double-quotes (``"``).

.. code-block:: monte

    def s := "Hello World!"
    def t := s.replace("World", "Monte hackers") # Hello Monte hackers!
    def u := "¿Dónde aquí habla Monte o español?"

Lists
~~~~~

Among Monte's collection types, the list is a very common type. Lists are
heterogenous ordered unsorted collections with sequencing and indexing, and
have the performance characteristics of arrays in C, vectors in C++, or lists
in Python::

    def l := ['I', "love", "Monte", 42, 0.5]
    def x := l[3] # x == 42

Special Characters
------------------

In lists and strings, special characters and unicode values can be escaped: 

+-----------------+---------------------------------+
| Escape Sequence | Meaning                         |
+=================+=================================+
| ``\\``          | Backslash (``\``)               |
+-----------------+---------------------------------+
| ``\'``          | Single quote (``'``)            |
+-----------------+---------------------------------+
| ``\"``          | Double quote (``"``)            |
+-----------------+---------------------------------+
| ``\b``          | ASCII Backspace (BS)            |
+-----------------+---------------------------------+
| ``\f``          | ASCII Formfeed (FF)             |
+-----------------+---------------------------------+
| ``\n``          | ASCII Linefeed (LF)             |
+-----------------+---------------------------------+
| ``\r``          | ASCII Carriage Return (CR)      |
+-----------------+---------------------------------+
| ``\t``          | ASCII Horizontal Tab (TAB)      |
+-----------------+---------------------------------+
| ``\uxxxx``      | Character with 16-bit hex value |
|                 | *xxxx* (Unicode only)           |
+-----------------+---------------------------------+
| ``\Uxxxxxxxx``  | Character with 32-bit hex value |
|                 | *xxxxxxxx* (Unicode only)       |
+-----------------+---------------------------------+
| ``\xhh``        | Character with hex value *hh*   |
+-----------------+---------------------------------+

(table mostly from `the Python docs <https://docs.python.org/2/_sources/reference/lexical_analysis.txt>`_)

.. note:: 

    Monte intentionally avoids providing escape notation for ASCII vertical
    tabs (``\v``) and octal values (``\o00``) because it is a language of the
    future and in the future, nobody uses those. Hexadecimal escapes are still
    valid for vertical tabs.

.. note::

    As with Python, a backslash (``\``) as the final character of a line
    escapes the newline and causes that line and its successor to be
    interpereted as one.

Data Structures
---------------

Monte has native lists and maps, as well as various other data structures
implemented in the language.

Monte Modules
-------------

A Monte module is a single file. The last statement in the file describes what
it exports. If the last statement in a file defines a method or object, that
method or object is what you get when you import it. If you want to export
several objects from the same file, the last line in the file should simply be
a list of their names.

To import a module, simply use `def bar = import("foo")` where the filename of
the module is foo.mt. See the files module.mt and imports.mt for an example of
how to export and import objects.

Testing
-------

.. note:: Tests are not automatically discovered at present. You need to add
    your test to a package.mt file for it to be run correctly.

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

.. [#] Miller, M.S.: `Robust Composition: Towards a Unified Approach to
       Access Control and Concurrency Control`__. PhD thesis, Johns
       Hopkins University, Baltimore, Maryland, USA (May 2006)

__ http://erights.org/talks/thesis/index.html
