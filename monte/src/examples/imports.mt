def [=> makeFoo, "makeBar" => mkB, => Baz] := import("examples/module", ["magicNumber" => 42])

traceln("Imported some things. Let's make them do stuff.")

def oof := makeFoo("quux")
oof.doSomething()

def bar := mkB()
bar.doSomething()

Baz.doSomething()
