def atoi := import("hands.atoi")

object value:
    pass

object pattern:
    pass

def readHole(s :str) :any:
    var tag := null
    switch (s[0]):
        match =='$':
            tag := value
        match =='@':
            tag := pattern
        match _:
            return null
    def inner := s.slice(2, s.size() - 1)
    def index := atoi(inner)
    return [tag, index]

def testReadHole(assert):
    def testValue():
        assert.equal(readHole("${0}"), [value, 0])
    def testPattern():
        assert.equal(readHole("@{12}"), [pattern, 12])
    return [
        testValue,
        testPattern,
    ]

def unittest := import("unittest")

unittest([
    testReadHole,
])

[readHole, pattern, value]
