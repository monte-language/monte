Answered Questions
==================

Will the iterable control when the computations are performed? 
-----------------------------------------------------------------

That's way outside the scope of an iteration protocol


Parallelism? 
---------------

Monte doesn't really say anything about parallelism per se. We *should*
though. If we're going to be agoric, we should say something about CPUs, even
if it's just that people should spin up more vats and make more code use
farrefs.


Let's talk about the _lazy_ iteration protocol
-------------------------------------------------

 We can just do like everybody else and have explicit laziness, can't we?
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


How do you send a message to an object?
------------------------------------------

In E (and Monte), there are two ways to send a message to an object.

1) Use the method call, foo.baz()
2) Use eventual send, foo <- baz()


Are all messages eligible for both methods of sending?
---------------------------------------------------------

A call (#1) is immediate and returns the value of whatever in foo handles that
message, probably a method. 

An eventual send (#2) returns a promise for the result  (in particular, foo does
not receive the messages until the end of the current turn (event loop
iteration), and eventual messages are delivered in order.) Calls are only
allowed for near, resolved objects. Sends can be made to far or unresolved 
objects (promises)
 
All messages are eligible for both kinds of sending, but not all objects can
receive messages in both ways.


What's Monte's comment syntax?
---------------------------------



.. code-block:: monte

    # This comment goes to the end of the line
    /** This comment is multi-line. 
        Yes, it starts with a two stars
        and ends with only one. 
        These should only be used for docstrings. */


What does "dynamic" mean, when used to describe Monte?
---------------------------------------------------------

Dynamic typing, dynamic binding, dynamic compiling. 

What are ejectors?
------------------

so... named breaks?                                       
14:22 <     simpson>| Sure. You can break out of any expression with them,
though. For example, early returns are implemented with them.
14:23 <        dash>| sort of, but it's of indefinite scope, you can pass it
to methods etc and invoking it unwinds the stack
14:23 <        dash>| yes, return/break/continue are all implemented as
ejectors
If you're familiar with call/cc shenanigans, it's like that, but delimited so
that it can't be called outside the scope that created it.

Blocking operators?
-------------------

Not available in Monte. so, because of the no-stale-stack-frames policy, monte
has neither generators nor threads nor C#-style async/await

Stale stack frames?
-------------------

stack frames that aren't running? 
at any point in time your code's behavior, since it is exposed to mutable
state, is affected by the stack frames above it
if you violate strict stack ordering (as generators do), then you violate the
obvious assumptions people make when reading and writing such code
14:59 <     mythmon>| ok. you don't want your scopes changing around you.       
14:59 <        dash>| mythmon: changing in a hard-to-comprehend way, yes :)     
14:59 <     mythmon>| which, of course, makes something like the 'await'
keyword I asked about totally impossible.
at a function's call site, you know what code you have to read to figure out
what it does to your execution state
15:00 <        dash>| at an 'await' or 'yield' point, you don't know what code
you have to read
15:01 <     mythmon>| sure I do.                                                
15:01 <     mythmon>| all of it.                                                
15:01 <     mythmon>| :)                                                        
15:01 <        dash>| right! and monte is a language intended to be useful in
an environment with an unbounded amount of code ;)


psuedomonadic joining on promises
---------------------------------

15:10 <     simpson>| The other thing, IIRC, is that we have what I'm going to
call pseudomonadic joining on promises.
15:11 <     mythmon>| simpson: is that the thing where promises become the
values for the promise?
15:11 <     simpson>| def p := foo<-bar(); def p2 := p<-baz()                   
15:11 <     simpson>| Yeah.                                                     
15:12 <     simpson>| Also IIRC when-exprs evaluate to a promise as well, so
you can have something like...
15:12 <     simpson>| def p := foo<-bar(); def p2 := when (p) -> { p.doStuff()
}; p2<-baz()


Why the name?
-------------

It's like Monty Python, but with E.

Vats?
-----
 http://erights.org/elib/concurrency/vat.html might help

farrefs?
--------

 references to far objects, namely objects in different vats. Messages
to far objects can only be sent asynchronously.

everything's an object here, so you aren't calling functions, but methods.
15:20 <     simpson>| It's surprisingly opinionated, I'm finding; there's
really only one concurrency pattern.
15:21 <     simpson>| If you *insist* on doing near-ref operations on a
far-ref, then you *must* make a when-expr. (And the compiler will transform
that into far-ref operations!)


promises?
---------

ES6 promises were derived from E's.
    the crucial part is, when promises are resolved they become forwarders to
their values


Everything's a method?
----------------------

 Well, everything's a message pass, rather.                
15:24 <        dash>| there are three words about references                    
15:24 <     simpson>| Function objects are desugared to objects with a single
run() method.
15:24 <     mythmon>| ok.                                                       
15:24 <        dash>| near/far, settled/unsettled, resolved/unresolved      
http://www.erights.org/elib/concurrency/refmech.html
15:27 <        dash>| a near reference is to an object in the same vat          
15:27 <        dash>| a far reference is to an object elsewhere                 
15:28 <        dash>| references are settled if they won't change to a
different reference state. they can be compared with == and used as hashtable
keys.
15:29 <        dash>| hmmm okay that's actually about the same as 'resolved'    
15:30 <        dash>| there's some edge cases around that, or were once         
15:30 <        dash>| anyway yes, a reference is either a promise or resolved   
15:30 <        dash>| a resolved reference is either near, far, or broken       
15:30 <        dash>| near references can have synchronous calls made on them   
15:31 <        dash>| promises, far references, or broken references will
raise an exception if synchronous calls are made

