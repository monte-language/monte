def makeCAMP := import("camp.machine")

def makeParser(code):
    return object campCode:
        to getCode():
            return code

        to machine():
            return makeCAMP(code)

        to head(rule):
            def insts := [["call", rule], ["jmp", code.size() + 1]] + code + ["end"]
            return makeParser(insts)

        to add(other):
            return makeParser(code + other.getCode())

        to or(other):
            def otherCode := other.getCode()
            def first := code.size() + 2
            def second := otherCode.size() + 1

            def insts := [["cho", first]] + code + [["com", second]] + otherCode
            return makeParser(insts)

        to complement():
            def len := code.size()
            def insts := [["cho", len + 3]] + code + [["com", 1], 'F']
            return makeParser(insts)

        to optional():
            # Degenerate ordered choice: (code |)
            def first := code.size() + 2

            def insts := [["cho", first]] + code + [["com", 1]]
            return makeParser(insts)

        to repeat():
            def len := code.size()
            def insts := [["cho", len + 2]] + code + [["com", -len - 1]]
            return makeParser(insts)

        to rule(name):
            def insts := [["rule", name]] + code + ["ret"]
            return makeParser(insts)

def ex(item):
    return makeParser([["ex", item]])

def call(name):
    return makeParser([["call", name]])

def testCampCode(assert):
    def testEx():
        def code := ex('x')
        assert.equal(code.machine()("x"), [true, 'x'])

    def testAdd():
        def code := ex('x') + ex('y')
        assert.equal(code.machine()("xy"), [true, 'y'])

    def testOr():
        def code := ex('x') | ex('y')
        assert.equal(code.machine()("x"), [true, 'x'])
        assert.equal(code.machine()("y"), [true, 'y'])

    def testComplement():
        def code := ~ex('x') + ex('y')
        assert.equal(code.machine()("y"), [true, 'y'])

    def testOptional():
        def code := ex('x').optional() + ex('y')
        assert.equal(code.machine()("y"), [true, 'y'])
        assert.equal(code.machine()("xy"), [true, 'y'])

    def testRepeat():
        def code := ex('x').repeat()
        assert.equal(code.machine()("xxxxx"), [true, ['x'] * 5])

    return [
        testEx,
        testAdd,
        testOr,
        testComplement,
        testOptional,
        # XXX broken testRepeat,
    ]

def testRecursion(assert):
    def balancedParens():
        var code := (ex('(') + call("s").optional() + ex(')')).rule("s")
        code head= "s"
        assert.equal(code.machine()("()"), [true, ')'])
        assert.equal(code.machine()("(())"), [true, ')'])
        assert.equal(code.machine()("("), [false, null])
        assert.equal(code.machine()(")"), [false, null])
    return [
        balancedParens,
    ]

def unittest := import("unittest")

unittest([
    testCampCode,
    testRecursion,
])

[ex, call]
