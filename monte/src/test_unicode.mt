module unittest
export(foo)     # Until https://github.com/monte-language/monte/issues/23 
def foo := null

def makeUnicodeTest(assert):
    def test_escaped_char():
        def snowman := '\u2603'
        traceln(snowman)
        assert.equal(snowman, '\u2603')

    def test_escaped_string():
        def snowman := "\u2603"
        traceln(snowman)
        assert.equal(snowman, "\u2603")

    def test_raw_char():
        def snowman := '☃'
        traceln(snowman)
        assert.equal(snowman, '☃')

    def test_raw_string():
        def snowman := "☃"
        traceln(snowman)
        assert.equal(snowman, "☃")

    return [test_escaped_char, test_escaped_string,
            test_raw_char, test_raw_string]

unittest([makeUnicodeTest])
