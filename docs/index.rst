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

See scope.mt for an example.

Debugging Stuff
---------------

Monte strives to provide useful error messages. 

Currently the most convenient way to print out messages from your program is 
with the trace() and traceln() built-in functions. The only difference between
them is that traceln() automatically adds a newline. 

Methods, Objects, Variables
---------------------------

Named values can be either final or variable::
 def aFinal := 42 # aFinal's value cannot be changed
 var aVariable := 6; aVariable *= 7



