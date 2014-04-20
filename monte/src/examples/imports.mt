def [makeFoo, mkB, baz] := import("examples/module")

traceln("Imported some things. Let's make them do stuff.")

def oof := makeFoo("quux")
oof.doSomething()

def bar := mkB()
bar.doSomething()

baz.doSomething()
