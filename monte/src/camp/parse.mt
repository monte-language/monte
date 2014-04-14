def [ex, call] := import("camp.expression")

def digit():
    var code := ex('0')
    for digit in "123456789":
        code |= ex(digit)
    return code

def digits := (digit() + digit().repeat()).rule("digits")

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
