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

    # State for paired delimiters like "", {}, (), []
    def braceStack := [[null, null, 0, true]].diverge()
    var nestLevel := 0

    # Syntax error produced from most recent tokenization attempt.
    var errorMessage := null

    var count := -1

    def composite(name, data, span):
        return makeTerm(makeTag(null, name, any), data, null, span)

    def atEnd():
        return position == input.size()

    def advance():
        position += 1
        if (atEnd()):
            currentChar := EOF
        else:
             currentChar := input[position]
        return currentChar

    def peekChar():
        if (atEnd()):
            throw("attempt to read past end of input")
        if (position + 1 == input.size()):
            return EOF
        return input[position + 1]

    def pushBrace(opener, closer, indent, canNest):
        if (canNest):
            nestLevel += 1
        braceStack.push([opener, closer, indent, canNest])

    def popBrace(closer, fail):
        if (braceStack.size() <= 1):
            fail(`Unmatched closing character ${closer.quote()}`)
        else if (braceStack.last()[1] != closer):
            fail(`Mismatch: ${closer.quote()} doesn't close ${braceStack.last()[0]}`)
        def item := braceStack.pop()
        if (item[3]):
            nestLevel -= 1

    def skipWhitespace():
        if (atEnd()):
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
        if (atEnd() || !digitset(currentChar)):
            return false
        digitset |= (char <=> '_')
        while (!atEnd() && digitset(currentChar)):
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

    def charConstant(fail):
        if (currentChar == '\\'):
            def nex := advance()
            if (nex == 'u'):
                def hexstr := __makeString.fromChars([advance() for _ in 0..!4])
                def v
                try:
                    bind v := __makeInt(hexstr, 16)
                catch _:
                    throw.eject(fail, "\\u escape must be four hex digits")
                advance()
                return __makeCharacter(v)
            else if (nex == 'x'):
                def v
                try:
                    bind v := __makeInt(__makeString.fromChars([advance(), advance()]), 16)
                catch _:
                    throw.eject(fail, "\\x escape must be two hex digits")
                advance()
                return __makeCharacter(v)
            else if (nex == EOF):
                throw.eject(fail, "End of input in middle of literal")
            def c := [
                'b' => '\b',
                't' => '\t',
                'n' => '\n',
                'f' => '\f',
                'r' => '\r',
                '"' => '"',
                '\'' => '\'',
                '\\' => '\\',
                "\n" => null,
                ].fetch(nex, fn{-1})
            if (c == -1):
                throw.eject(fail, `Unrecognized escape character ${nex.quote()}`)
            else:
                advance()
                return c
        if (currentChar == EOF):
            throw.eject(fail, "End of input in middle of literal")
        else if (currentChar == '\t'):
            throw.eject(fail, "Quoted tabs must be written as \\t")
        else:
            def c := currentChar
            advance()
            return c

    def stringLiteral(fail):
        def opener := currentChar
        advance()
        pushBrace(opener, '"', 0, false)
        def buf := [].diverge()
        while (currentChar != '"'):
            if (atEnd()):
                fail("Input ends inside string literal")
            def cc := charConstant(fail)
            if (cc != null):
               buf.push(cc)
        advance()
        def closer := endToken(fail)
        popBrace('"', fail)
        return composite(".String.", __makeString.fromChars(buf), closer.getSpan())

    def charLiteral(fail):
        advance()
        var c := charConstant(fail)
        while (c == null):
           c := charConstant(fail)
        if (currentChar != '\''):
            throw.eject(fail, "Character constant must end in \"'\"")
        advance()
        return composite(".char.", c, endToken(fail).getSpan())

    def getNextToken(fail):
        skipWhitespace()
        startToken()
        def cur := currentChar
        if (cur == EOF):
            throw.eject(fail, null)
        if (cur == '"'):
            return stringLiteral(fail)
        if (cur == '\''):
            return charLiteral(fail)
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

def test_string(assert):
    def mkstr(s):
        return makeTerm(makeTag(null, ".String.", any), s, null, null)
    assert.equal(lex("\"foo bar\""), [mkstr("foo bar")])
    # assert.equal(lex("\"foo\\nbar\""), [mkstr("foo\nbar")])
    # assert.equal(lex("\"foo\\\\nbar\""), [mkstr("foobar")])
    # assert.equal(lex("\"z\\u0061p\""), [mkstr("zap")])
    # assert.equal(lex("\"z\\x61p\""), [mkstr("zap")])

def test_char(assert):
    def mkchar(c):
        return makeTerm(makeTag(null, ".char.", any), c, null, null)
    assert.equal(lex("'z'"), [mkchar('z')])
    assert.equal(lex("'\\n'"), [mkchar('\n')])
    assert.equal(lex("'\\u0061'"), [mkchar('a')])
    assert.equal(lex("'\\x61'"), [mkchar('a')])


unittest([test_integer, test_float, test_string, test_char])
