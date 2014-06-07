module unittest

def makeUnicodeTest(assert):
    def test_unicode_char():
        def snowman := '\u2603'
        # def snowman := '☃'
        traceln(snowman)
        assert.equal(snowman, '\u2603')
    def test_unicode_string():
        def snowman := "\u2603"
        # def snowman := "☃"
        traceln(snowman)
        assert.equal(snowman, "\u2603")
    return [test_unicode_char, test_unicode_string]

unittest([makeUnicodeTest])
