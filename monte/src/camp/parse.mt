def atoi := import("hands.atoi")

def [ex, call] := import("camp.expression")

def unittest := import("unittest")

def digit():
    var code := ex('0')
    for digit in "123456789":
        code |= ex(digit)
    return code

def reduceDigits(["head" => head, "tail" => tail]) :int:
    return atoi([head] + tail)

def digits := (digit().bindTo("head") + digit().repeat().bindTo("tail")).reduce(reduceDigits).rule("digits")

def testDigits(assert):
    def code := digits.head("digits")
    def single():
        assert.equal(code.machine()("7"), [true, 7])
    def multiple():
        assert.equal(code.machine()("42"), [true, 42])
    return [
        single,
        multiple,
    ]

unittest([
    testDigits,
])

def head():
    var code := ex('_')
    for letter in "abcdefhijklmnopqrstuvwxyz":
        code |= ex(letter)
    return code

def heads := (head() + head().repeat())

def comma := ex(',')

def ws := (ex(' ') | ex('\n')).repeat().optional()

def op := ex('(')
def cp := ex(')')

def commaSep := call("term") + (comma + ws + call("term")).repeat()

def term := (heads + (op + commaSep + cp).optional()).rule("term")

def parser := term.head("term").machine()

traceln(parser("test"))
traceln(parser("test(terms)"))
traceln(parser("test(terms, more(terms))"))
traceln(parser("test(terms, more(terms, and, other(deeply, nested), terms))"))
traceln(parser("invalid)"))
traceln(parser("invalid))))))))))))))))))"))
