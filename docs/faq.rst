Answered Questions
==================

Q) Will the iterable control when the computations are performed? 
-----------------------------------------------------------------

A) That's way outside the scope of an iteration protocol


Q) Parallelism? 
---------------

A) Monte doesn't really say anything about parallelism per se. We *should*
though. If we're going to be agoric, we should say something about CPUs, even
if it's just that people should spin up more vats and make more code use
farrefs.


Q) Let's talk about the _lazy_ iteration protocol
-------------------------------------------------

A)  We can just do like everybody else and have explicit laziness, can't we?
Or do we want language-level extra-lazy stuff?

.. code-block:: monte

 def workItems := [lazyNext(someIter) for _ in 0..!cores]
 # or to be less handwavey
 def workItems := [someIter.lazyNext() for _ in 0..!cores]

lazyNext() is like .next() but it either returns 
    1) a near value if it's immediately available
    2) a promise if it's not
    3) a broken promise if you've iterated off the end
Even this isn't right,  but the idea is that you could use something like
twisted's coiterate to serially compute some items in a iterable, a few at a
time  and as they were made available, the promises in workItems would get 
resolved


Q) How do you send a message to an object?
------------------------------------------

A) In E (and Monte), there are two ways to send a message to an object.

1) Use the method call, foo.baz()
2) Use eventual send, foo <- baz()


Q) Are all messages eligible for both methods of sending?
---------------------------------------------------------

A) A call (#1) is immediate and returns the value of whatever in foo handles that
message, probably a method. 

An eventual send (#2) returns a promise for the result  (in particular, foo does
not receive the messages until the end of the current turn (event loop
iteration), and eventual messages are delivered in order.) Calls are only
allowed for near, resolved objects. Sends can be made to far or unresolved 
objects (promises)
 
All messages are eligible for both kinds of sending, but not all objects can
receive messages in both ways.


Q) What's Monte's comment syntax?
---------------------------------

A) 

.. code-block:: monte

    # This comment goes to the end of the line
    /** This comment is multi-line. 
        Yes, it starts with a two stars
        and ends with only one. 
        These should only be used for docstrings. */


Q) What does "dynamic" mean, when used to describe Monte?
---------------------------------------------------------

A) Dynamic typing, dynamic binding, dynamic compiling. 


Vocabulary
==========

Vat: http://erights.org/elib/concurrency/vat.html might help

farref: references to far objects, namely objects in different vats. Messages
to far objects can only be sent asynchronously.

promise: ES6 promises were derived from E's.

