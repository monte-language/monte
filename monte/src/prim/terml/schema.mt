module unittest, convertToTerm, termFactory
export (baseSchema)
def t := termFactory

object baseSchema:
  to load(data):
      return null

  to dump(data):
      return null

def baseNodeNames := ["null", "true", "false", ".String.", ".float64.",
                      ".char.", ".int.", ".tuple.", ".bag.", ".attr."]

def wrap(f):
    def testf(assert):
        object moreAssert extends assert:
            to check(schema, term):
                return assert.equal(schema.load(schema.dump(term)), term)

        return f(moreAssert)
    return testf

def testNull(assert):
    assert.check(baseSchema, t.null())

def testInt(assert):
    assert.check(baseSchema, convertToTerm(0, null))
    assert.check(baseSchema, convertToTerm(-255, null))
    assert.check(baseSchema, convertToTerm(1048369, null))

def testBigint(assert):
    assert.check(baseSchema, convertToTerm(0x100000001))
    assert.check(baseSchema, convertToTerm(443464870465066586048))
    assert.check(baseSchema, convertToTerm(-443464870465066586048))

def testFloat(assert):
    assert.check(baseSchema, convertToTerm(0.0))
    assert.check(baseSchema, convertToTerm(-1.0))
    assert.check(baseSchema, convertToTerm(3.14))

def testString(assert):
    assert.check(baseSchema, convertToTerm(""))
    assert.check(baseSchema, convertToTerm("yes"))
    assert.check(baseSchema, convertToTerm("\u2603"))

def testTuple(assert):
    assert.check(baseSchema, convertToTerm([0, 1, "", []]))

def testMap(assert):
    assert.check(baseSchema, convertToTerm([1 => "yes", "no" => 0]))

def test_custom(assert):
    def sch := baseSchema.extend(["foo" => 1])
    assert.check(sch, t.foo(0))
    assert.check(sch, t.foo(t.foo(null)))

def tests := [testNull, ]
unittest([wrap(test) for test in tests])
