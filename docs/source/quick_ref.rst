.. _quick-ref:

Monte Idioms Quick Reference
============================

This is intended as a compact representation of frequently-used syntax
and frequently-encountered special characteristics of monte. The
beginning monte user may find it a handy reference while experimenting
and reading the documentation; the experienced monte programmer may
find it handy as a refresher if returning to the language after some
time. This reference does not touch pattern matching, parse trees, or
Kernel-E at all.


Simple Statements
-----------------

::

  >>> def a := 2 + 3
  ... var a2 := 4
  ... a2 += 1
  ... def b := `answer: $a`
  ... traceln(b)
  ... b
  "answer: 5"


Basic Flow
----------

::

   >>> if ('a' == 'b'):
   ...    "match"
   ... else:
   ...    "no match"
   "no match"

::

   >>> var a := 0; def b := 4
   ... while (a < b):
   ...     a += 1
   ... a
   4

::

   >>> var resource := "reserved"
   ... try:
   ...     3 // 0
   ... catch err:
   ...     `error!`
   ... finally:
   ...     resource := "released"
   ... resource
   "released"

::

   >>> def x := [].diverge()
   ... for next in (1..3):
   ...     x.push([next, next])
   ... x.snapshot()
   [[1, 1], [2, 2], [3, 3]]

::

   >>> def map := ['a' => 65, 'b' => 66]
   ... var sum := 0
   ... for key => value in (map):
   ...     sum += value
   ... sum
   131


Modules
-------

Function
~~~~~~~~

::

   >>> def addTwoPrint(number):
   ...     traceln(number + 2)
   ...     return number + 2
   ...
   ... def twoPlusThree := addTwoPrint(3)
   ... twoPlusThree
   5

Singleton Object (stateless)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   >>> object adder:
   ...     to add1(number):
   ...         return number + 1
   ...     to add2(number):
   ...         return number + 2
   ... def result := adder.add1(3)
   ... result
   4


Objects with state
~~~~~~~~~~~~~~~~~~

::

   >>> def makeOperator(baseNum):
   ...     def instanceValue := 3
   ...     object operator:
   ...         to addBase(number):
   ...             return baseNum + number
   ...         to multiplyBase(number):
   ...             return baseNum * number
   ...     return operator
   ... def threeHandler := makeOperator(3)
   ... def threeTimes2 := threeHandler.multiplyBase(2)
   ... threeTimes2
   6


Objects self-referencing during construction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: find out why this test goes wonky

::

   .>> def makeRadio(car):
   ...     # define radios
   ... def makeCar(name):
   ...     var x := 0
   ...     var y := 0
   ...     def car # using def with no assignment
   ...     def myWeatherRadio := makeRadio(car)
   ...     bind car:
   ...         to receiveWeatherAlert():
   ...             # ....process the weather report....
   ...             # myWeatherRadio.foo(...)
   ...         to getX():
   ...             return x
   ...         to getY():
   ...             return y
   ...         # ....list the rest of the car methods....
   ...     return car
   ... makeCar("ferrari").getX()
   0


Delegation
~~~~~~~~~~

::

   >>> def makeExtendedFile(myFile):
   ...     return object extendedFile extends myFile:
   ...         to append(text):
   ...             var current := myFile.getText()
   ...             current := current + text
   ...             myFile.setText(current)
   ...
   ... makeExtendedFile(object _ {})._respondsTo("append", 1)
   true


File I/O
--------

Access to files is given to the `main` entry point::

    >>> def main(argv, => makeFileResource):
    ...     def fileA := makeFileResource("fileA")
    ...     fileA <- setContents(b`abc\ndef`)
    ...     def contents := fileA <- getContents()
    ...     when (contents) ->
    ...         for line in (contents.split("\n")):
    ...             traceln(line)
    ...
    ... main._respondsTo("run", 1)
    true


Web Applications
----------------

Access to TCP/IP networking is also given to the `main` entry
point. The ``lib/http/server`` module builds an HTTP server from a
TCP/IP listener::

    import "lib/http/server" =~ [=> makeHTTPEndpoint :DeepFrozen]
    exports (main)

    def hello(request) as DeepFrozen:
        return [200, ["Content-Type" => "text/plain"], b`hello`]

    def main(argv, => makeTCP4ServerEndpoint) as DeepFrozen:
        def tcpListener := makeTCP4ServerEndpoint(8080)
        def httpServer := makeHTTPEndpoint(tcpListener)
        httpServer.listen(hello)

Data Structures
---------------

ConstList
~~~~~~~~~

::

   >>> var a := [8, 6, "a"]
   ... a[2]
   "a"

   >>> var a := [8, 6, "a"]
   ... a.size()
   3

   >>> var a := [8, 6, "a"]
   ... for i in (a):
   ...     traceln(i)
   ... a := a + ["b"]
   ... a.slice(0, 2)
   [8, 6]


ConstMap
~~~~~~~~

::

   >>> def m := ["c" => 5]
   ... m["c"]
   5

   >>> ["c" => 5].size()
   1

   >>> def m := ["c" => 5]
   ... for key => value in (m):
   ...     traceln(value)
   ... def flexM := m.diverge()
   ... flexM["d"] := 6
   ... flexM.size()
   2


FlexList
~~~~~~~~

::

   >>> def flexA := [8, 6, "a", "b"].diverge()
   ... flexA.extend(["b"])
   ... flexA.push("b")
   ... def constA := flexA.snapshot()
   [8, 6, "a", "b", "b", "b"]


FlexMap
~~~~~~~

::

   >>> def m := ["c" => 5]
   ... def flexM := m.diverge()
   ... flexM["b"] := 2
   ... flexM.removeKey("b")
   ... def constM := flexM.snapshot()
   ["c" => 5]


Eventual Sends
--------------

::

   >>> def abacus := object mock { to add(x, y) { return x + y } }
   ... var out := null
   ...
   ... def answer := abacus <- add(1, 2)
   ... when (answer) ->
   ...     out := `computation complete: $answer`
   ... catch problem:
   ...     traceln(`promise broken $problem `)
   3

::

   >>> def makeCarRcvr := fn autoMake { `shiny $autoMake` }
   ...
   ... def carRcvr := makeCarRcvr <- ("Mercedes")
   ... Ref.whenBroken(carRcvr, def lost(brokenRef) {
   ...     traceln("Lost connection to carRcvr")
   ... })
   ... carRcvr
   "shiny Mercedes"

   >>> def [resultVow, resolver] := Ref.promise()
   ...
   ... when (resultVow) ->
   ...     traceln(resultVow)
   ... catch prob:
   ...     traceln(`oops: $prob`)
   ...
   ... resolver.resolve("this text is the answer")
   ... resultVow
   "this text is the answer"
