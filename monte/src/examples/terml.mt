def terml := import("terml", import("regions"))
def t := terml["termFactory"]
def x :DeepFrozen := t.Foo(null, t.Baz(1), t.Blee("x"))
traceln(`$x`)
