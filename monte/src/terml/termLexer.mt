module makeTag, makeTerm, unittest
export (makeTermLexer)

object EOF {}
def decimalDigits := '0'..'9'
def hexDigits := decimalDigits | 'a'..'f' | 'A'..'F'

def makeTermLexer(input):

    # Does the input string contain a complete expression, such that we can
    # execute it without further user input?
    var inputIsComplete := true

    # The character under the cursor.
    var currentChar := null
    # Offset of the current character.
    var position := -1

    # Start offset of the text for the token being created.
    var startPos := -1

    # Syntax error produced from most recent tokenization attempt.
    var errorMessage := null

    var count := -1

    def composite(name, data, span):
        return makeTerm(makeTag(null, name, any), data, null, span)

    def isEndOfFile():
        return position == input.size()

    def advance():
        position += 1
        if (isEndOfFile()):
            currentChar := EOF
        else:
             currentChar := input[position]

    def peekChar():
        if (isEndOfFile()):
            throw("attempt to read past end of file")
        if (position + 1 == input.size()):
            return EOF
        return input[position + 1]

    def skipWhitespace():
        if (isEndOfFile()):
            return
        while (currentChar == ' '):
            advance()

    def startToken():
        if (startPos >= 0):
            throw("Token already started")
        startPos := position

    def endToken(fail):
        def pos := position
        def tok := input.slice(startPos, pos)
        startPos := -1
        return tok

    def collectDigits(var digitset):
        if (isEndOfFile() || !digitset(currentChar)):
            return false
        digitset |= (char <=> '_')
        while (!isEndOfFile() && digitset(currentChar)):
            advance()
        return true

    def numberLiteral(fail):
        var radix := 10
        var floating := false
        if (currentChar == '0'):
            advance()
            if (currentChar == 'X' || currentChar == 'x'):
                radix := 16
                advance()
        if (radix == 16):
            collectDigits(hexDigits)
        else:
            collectDigits(decimalDigits)
            if (currentChar == '.'):
                def pc := peekChar()
                if (pc == EOF):
                    fail("Missing fractional part")
                if (decimalDigits(pc)):
                    advance()
                    floating := true
                    collectDigits(decimalDigits)
            if (currentChar == 'e' || currentChar == 'E'):
                advance()
                floating := true
                if (currentChar == '-' || currentChar == '+'):
                    advance()
                if (!collectDigits(decimalDigits)):
                    fail("Missing exponent")
        def tok := endToken(fail)
        def s := tok.replace("_", "")
        if (floating):
            return composite(".float64.", __makeFloat(s), tok.getSpan())
        else:
            if (radix == 16):
                return composite(".int.", __makeInt(s.slice(2), 16), tok.getSpan())
            else:
                return composite(".int.", __makeInt(s), tok.getSpan())

    def getNextToken(fail):
        skipWhitespace()
        startToken()
        def cur := currentChar
        if (cur == EOF):
           throw.eject(fail, null)
        if (decimalDigits(cur)):
           return numberLiteral(fail)
        fail(`Unrecognized character ${cur.quote()}`)

    advance()
    return object termLexer:

        to _makeIterator():
            return termLexer

        to getSyntaxError():
            return errorMessage

        to needsMore():
            return inputIsComplete

        to next(ej):
            try:
                if (currentChar == EOF):
                    throw.eject(ej, null)
                def errorStartPos := position
                escape e:
                    return [count += 1, getNextToken(e)]
                catch msg:
                    errorMessage := msg
                    throw.eject(ej, msg)
            finally:
                startPos := -1


def lex(s):
    def l := makeTermLexer(s)
    def toks := [t for t in l]
    if ((def err := l.getSyntaxError()) != null):
        throw(err)
    if (toks.size() > 0 && toks.last().getTag().getName() == "EOL"):
       return toks.slice(0, toks.size() - 1)
    return toks

def test_integer(assert):
    def mkint(n):
        return makeTerm(makeTag(null, ".int.", any), n, null, null)
    assert.equal(lex("0"), [mkint(0)])
    assert.equal(lex("7"), [mkint(7)])
    assert.equal(lex("3_000"), [mkint(3000)])
    assert.equal(lex("0xABad1dea"), [mkint(0xabad1dea)])

def test_float(assert):
    def mkfloat(n):
        return makeTerm(makeTag(null, ".float64.", any), n, null, null)
    assert.equal(lex("1e9"), [mkfloat(1e9)])
    assert.equal(lex("3.1415E17"), [mkfloat(3.1415E17)])
    assert.equal(lex("0.91"), [mkfloat(0.91)])
    assert.equal(lex("3e-2"), [mkfloat(3e-2)])


unittest([test_integer, test_float])
