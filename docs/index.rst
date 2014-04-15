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
