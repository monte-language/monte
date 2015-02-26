=========================
Monte is Serious Business
=========================

Introduction
============

What's Monte?
-------------

Monte is a dynamic language designed to solve the problems of both Python and E.

Why Monte?
----------

Python is great for usability, but has all the security vulnerabilities of its
prececessors. E is a relatively obscure language whose fundamental design
precludes many types of common vulnerability, but its syntax is difficult to
use and its implementations don't perform competitively.

Where do I start?
-----------------

If you'd like to get involved with developing or using the Monte language,
start by getting acquainted with Python_'s syntax and the computational
concepts of E_. 

Then clone the repo_ and follow the directions below to begin running Monte
code. If you have problems, join us in #monte on irc.freenode.net, ask your
question (use a pastebin_ to share any errors, rather than pasting into the
channel), and wait a few hours if nobody is around. 

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
Monte.

* 1 space: How can you read that?
* 2 spaces: *sigh* you must be a Googler.
* 3 spaces: What?
* **4 spaces**: Yes. Good coder. Use 4 spaces.
* 5 spaces: No, five is right out.
* 8 spaces: How can you read that?

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

Everything is an object. Some objects are created automatically, such as
variables and methods. Other objects are created explicitly::

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

    Monte intentionally avoids supporting ASCII vertical tabs (``\v``) and
    octal values (``\o00``) because it is a language of the future and in the
    future, nobody uses those. 

.. note::

    As with Python, a backslash (``\``) as the final character of a line
    escapes the newline and causes that line and its successor to be
    interpereted as one.


Data Structures
---------------

Monte has lists built in natively, and various other data structures
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
