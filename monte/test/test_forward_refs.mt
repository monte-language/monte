# This should make x a forward reference until it is assigned.
# Intead (as of #6f93ab) this fails with
#
#    monte.compiler.CompileError: Can't assign to final variable: 'x'

def x
var y := 1
x := y + 1

traceln(`x: $x, y: $y`)
