def [=> moduleA, => moduleB] := pkg.readFiles(".")
def n := moduleA()["n"]
def foo := moduleB([
         => n,
     "a" => pkg.require("a"),
     "b" => pkg.require("b")])
pkg.makeModule(["c" => n, "d" => foo["d"]])
