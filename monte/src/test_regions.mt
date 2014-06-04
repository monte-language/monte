module unittest
export (foo)
def foo := null

def testIterable(assert):
    assert.equal([x for x in 0..!5], [0, 1, 2, 3, 4])

def testContainment(assert):
    def reg := 0..!5
    assert.equal(reg(3), true)
    assert.equal(reg(5), false)
    assert.raises(fn fail {reg(1.0)})

def testGuard(assert):
    assert.equal(def x :(0..!5) := 3, 3)
    assert.ejects(fn ej, fail {def x :(0..!5) exit ej := 7})

def testDeepFrozen(assert):
    def x :(0..!5) := 2
    object y implements DeepFrozen:
        to add(a):
            return a + x
    assert.equal(y =~ _ :DeepFrozen, true)

unittest([testIterable, testContainment, testGuard, testDeepFrozen])

