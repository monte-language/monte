Monte Idioms Quick Reference
============================

This is intended as a compact representation of frequently-used syntax
and frequently-encountered special characteristics of monte. The
beginning monte user may find it a handy reference while experimenting
and reading the documentation; the experienced monte programmer may
find it handy as a refresher if returning to the language after some
time. This reference does not touch pattern matching, parse trees, or
Kernel-E at all.

 - Simple Statements: def, var, assign, print, add, comment
 - Basic Flow: if, while, for, try
 - Modules: Function, Singleton Object, Object Maker, Delegation
 - Text File I/O
 - Windowed Apps
 - Data Structures: Strings, ConstLists, ConstMaps, FlexLists, FlexMaps
 - Java Interface
 - Asynch Sends
 - Remote Comm


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
  ...    traceln("match")
  ... else:
  ...    traceln("no match")
  null

::
  >>> var a := 0; def b := 4
  ... while (a < b):
  ...     a += 1
  null

:
  >>> try:
  ...     3 // 0
  ... catch err:
  ...     traceln(`error: $err`)
  ... finally:
  ...     traceln("always")
  null

::
  >>> for next in (1..3):
  ...     traceln(next)
  null

::
  >>> def map := ['a' => 65, 'b' => 66]
  ... for key => value in (map):
  ...     traceln("got pair")
  null


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

::

  >>> def makeRadio(car):
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
  ... "no usage example"
  "no usage example"
