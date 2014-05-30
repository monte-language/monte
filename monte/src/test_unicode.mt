module unittest
export(foo)     # Until https://github.com/monte-language/monte/issues/23 
def foo := null

def makeUnicodeTest(assert):
   def test_char():
        def snowman := '☃'
        traceln(snowman)
        assert.equal(snowman, '☃')
   def test_string():
        def snowman := "☃"
        traceln(snowman)
        assert.equal(snowman, "☃")
   return [test_char, test_string]

unittest([makeUnicodeTest])
