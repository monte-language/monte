module makeTerm :DeepFrozen, Term :DeepFrozen, makeTag :DeepFrozen, unittest
export (convertToTerm)

def mkt(name, data, args) as DeepFrozen:
    return makeTerm(makeTag(null, name, any), data, args, null)

def convertToTerm(val, ej) as DeepFrozen:
    switch (val):
        match _ :Term:
            return val
        match ==null:
            return mkt("null", null, [])
        match ==true:
            return mkt("true", null, [])
        match ==false:
            return mkt("false", null, [])
        match v :int:
            return mkt(".int.", v, [])
        match v :float:
            return mkt(".float.", v, [])
        match v :str:
            return mkt(".String.", v, [])
        match v :char:
            return mkt(".char.", v, [])
        match v :List:
            def l := [convertToTerm(item, ej) for item in v]
            return mkt(".tuple.", null, l)
        # match v :set:
        #   return mkt(".bag.", null, [convertToTerm(item) for item in v])
        match m :Map:
            return mkt(".bag.", null,
                       [mkt(".attr.", null, [convertToTerm(k, ej),
                       convertToTerm(v, ej)])
                        for k => v in m])
        match _:
            throw.eject(ej, `Could not coerce $val to term`)

def test_convert(assert):
    def t1 := convertToTerm([1, null, 2.5, "yes", 'c', true, [1 => 2]], null)
    assert.equal(t1.getTag().getName(), ".tuple.")
    def a := t1.getArgs()
    def one := a[0]
    assert.equal(one.getTag().getName(), ".int.")
    assert.equal(one.getData(), 1)
    def nul := a[1]
    assert.equal(nul.getTag().getName(), "null")
    def flo := a[2]
    assert.equal(flo.getTag().getName(), ".float.")
    assert.equal(flo.getData(), 2.5)
    def s := a[3]
    assert.equal(s.getTag().getName(), ".String.")
    assert.equal(s.getData(), "yes")
    def c := a[4]
    assert.equal(c.getTag().getName(), ".char.")
    assert.equal(c.getData(), 'c')
    def b := a[5]
    assert.equal(b.getTag().getName(), "true")
    def m := a[6]
    assert.equal(m.getTag().getName(), ".bag.")
    def ma := m.getArgs()
    assert.equal(ma[0].getTag().getName(), ".attr.")
    def k := ma[0].getArgs()[0]
    assert.equal(k.getData(), 1)
    def v := ma[0].getArgs()[1]
    assert.equal(v.getData(), 2)

unittest([test_convert])
