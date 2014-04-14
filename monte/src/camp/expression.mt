def makeCAMP := import("camp.machine")

def makeParser(code):
    return object campCode:
        to getCode():
            return code

        to machine():
            return makeCAMP(code)

        to head(rule):
            def insts := [['L', rule], ['J', code.size() + 1]] + code + ['E']
            return makeParser(insts)

        to add(other):
            return makeParser(code + other.getCode())

        to or(other):
            def otherCode := other.getCode()
            def first := code.size() + 2
            def second := otherCode.size() + 1

            def insts := [['H', first]] + code + [['M', second]] + otherCode
            return makeParser(insts)

        to complement():
            def len := code.size()
            def insts := [['H', len + 3]] + code + [['M', 1], 'F']
            return makeParser(insts)

        to optional():
            # Degenerate ordered choice: (code |)
            def first := code.size() + 2

            def insts := [['H', first]] + code + [['M', 1]]
            return makeParser(insts)

        to repeat():
            def len := code.size()
            def insts := [['H', len + 2]] + code + [['M', -len - 1]]
            return makeParser(insts)

        to rule(name):
            def insts := [['U', name]] + code + ['R']
            return makeParser(insts)

def ex(item):
    return makeParser([['X', item]])

def call(name):
    return makeParser([['L', name]])

def testCampCode(assert):
    def testEx():
        def code := ex('x')
        assert.equal(code.machine()("x"), true)

    def testAdd():
        def code := ex('x') + ex('y')
        assert.equal(code.machine()("xy"), true)

    def testOr():
        def code := ex('x') | ex('y')
        assert.equal(code.machine()("x"), true)
        assert.equal(code.machine()("y"), true)

    def testComplement():
        def code := ~ex('x') + ex('y')
        assert.equal(code.machine()("y"), true)

    def testOptional():
        def code := ex('x').optional() + ex('y')
        assert.equal(code.machine()("y"), true)
        assert.equal(code.machine()("xy"), true)

    def testRepeat():
        def code := ex('x').repeat()
        assert.equal(code.machine()("xxxxx"), true)

    return [
        testEx,
        testAdd,
        testOr,
        testComplement,
        testOptional,
        testRepeat,
    ]

def testRecursion(assert):
    def balancedParens():
        var code := (ex('(') + call("s").optional() + ex(')')).rule("s")
        code head= "s"
        assert.equal(code.machine()("()"), true)
        assert.equal(code.machine()("(())"), true)
        assert.equal(code.machine()("("), false)
        assert.equal(code.machine()(")"), false)
    return [
        balancedParens,
    ]

def unittest := import("unittest")

unittest([
    testCampCode,
    testRecursion,
])

[ex, call]
