module unittest
export(foo)     # Until https://github.com/monte-language/monte/issues/23 
def foo := null

def makeUnicodeTest(assert):
    def test_snowman():
        def snowman := '☃'
        traceln(snowman)
        assert.equal(snowman, '☃')
    return [test_snowman]

unittest([makeUnicodeTest])
