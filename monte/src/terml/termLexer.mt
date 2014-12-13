module makeTag, makeTerm, termBuilder, unittest
export (makeTermLexer)

object VALUE_HOLE {}
object PATTERN_HOLE {}
object EOF {}
def decimalDigits := '0'..'9'
def hexDigits := decimalDigits | 'a'..'f' | 'A'..'F'

# huh, maybe regions are dumb for this? guess we need sets
def segStart := 'a'..'z' | 'A'..'Z' | '_'..'_' | '$'..'$' | '.'..'.'
def segPart := segStart | '0'..'9' | '-'..'-'
def closers := ['(' => ')', '[' => ']', '{' => '}']


def _makeTermLexer(input, builder, braceStack, var nestLevel):

    # The character under the cursor.
    var currentChar := null
    # Offset of the current character.
    var position := -1

    # Start offset of the text for the token being created.
    var startPos := -1

    # Syntax error produced from most recent tokenization attempt.
    var errorMessage := null

    var count := -1

    def leafTag(tagname, span):
        return builder.leafInternal(makeTag(null, tagname, any), null, span)


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
            return builder.leafInternal(makeTag(null, ".float64.", any), __makeFloat(s), tok.getSpan())
        else:
            if (radix == 16):
                return builder.leafInternal(makeTag(null, ".int.", any), __makeInt(s.slice(2), 16), tok.getSpan())
            else:
                return builder.leafInternal(makeTag(null, ".int.", any), __makeInt(s), tok.getSpan())

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
                '\n' => null,
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

    def stringLike(fail):
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
        return __makeString.fromChars(buf)

    def charLiteral(fail):
        advance()
        var c := charConstant(fail)
        while (c == null):
           c := charConstant(fail)
        if (currentChar != '\''):
            throw.eject(fail, "Character constant must end in \"'\"")
        advance()
        return builder.leafInternal(makeTag(null, ".char.", any), c, endToken(fail).getSpan())

    def tag(fail, initial):
        var done := false
        def segs := [].diverge()
        if (initial != null):
            segs.push(initial)
        while (currentChar == ':' && peekChar() == ':'):
            advance()
            advance()
            if (currentChar == '"'):
                def s := stringLike(fail)
                segs.push("::\"")
                segs.push(s)
                segs.push("\"")
            else:
                segs.push("::")
                def segStartPos := position
                if (currentChar != EOF && segStart(currentChar)):
                    advance()
                else:
                    throw.eject(fail, "Invalid character starting tag name segment")
                while (currentChar != EOF && segPart(currentChar)):
                    advance()
                segs.push(input.slice(segStartPos, position))
        return leafTag("".join(segs), endToken(fail).getSpan())

    def getNextToken(fail):
        skipWhitespace()
        startToken()
        def cur := currentChar
        if (cur == EOF):
            throw.eject(fail, null)
        if (cur == '"'):
            def s := stringLike(fail)
            def closer := endToken(fail)
            popBrace('"', fail)

            return builder.leafInternal(makeTag(null, ".String.", any), s, closer.getSpan())
        if (cur == '\''):
            return charLiteral(fail)
        if (cur == '-'):
            advance()
            return numberLiteral(fail)
        if (decimalDigits(cur)):
            return numberLiteral(fail)
        if (segStart(cur)):
            def segStartPos := position
            advance()
            while (currentChar != EOF && segPart(currentChar)):
                advance()
            return tag(fail, input.slice(segStartPos, position))
        if (cur == ':' && peekChar() == ':'):
            return tag(fail, null)
        if (['(', '[','{'].contains(cur)):
            pushBrace(cur, closers[cur], 1, true)
            def s := input.slice(position, position + 1)
            def t := leafTag(s, s.getSpan())
            advance()
            return t
        if ([')', ']', '}'].contains(cur)):
            popBrace(cur, fail)
            def s := input.slice(position, position + 1)
            def t := leafTag(s, s.getSpan())
            advance()
            return t
        if ([':', '-', ',', '*', '+', '?'].contains(cur)):
            def s := input.slice(position, position + 1)
            def t := leafTag(s, s.getSpan())
            advance()
            return t
        fail(`Unrecognized character ${cur.quote()}`)

    advance()
    return object termLexer:

        to _makeIterator():
            return termLexer

        to getSyntaxError():
            return errorMessage

        to valueHole():
            return VALUE_HOLE

        to patternHole():
            return PATTERN_HOLE

        to next(ej):
            try:
                if (currentChar == EOF):
                    throw.eject(ej, null)
                def errorStartPos := position
                escape e:
                    def t := getNextToken(e)
                    return [count += 1, t]
                catch msg:
                    errorMessage := msg
                    throw.eject(ej, msg)
            finally:
                startPos := -1

        to lexerForNextChunk(chunk):
            return _makeTermLexer(chunk, builder, braceStack, nestLevel)

object makeTermLexer:
    to run(input, builder):
        # State for paired delimiters like "", {}, (), []
        def braceStack := [[null, null, 0, true]].diverge()
        return _makeTermLexer(input, builder, braceStack, 0)

    to holes():
        return [VALUE_HOLE, PATTERN_HOLE]

def lex(s):
    def l := makeTermLexer(s, termBuilder)
    def toks := [t for t in l]
    if ((def err := l.getSyntaxError()) != null):
        throw(err)
    if (toks.size() > 0 && toks.last().getTag().getName() == "EOL"):
       return toks.slice(0, toks.size() - 1)
    return toks

def test_integer(assert):
    def mkint(n):
        return makeTerm(makeTag(null, ".int.", any), n, [], null)
    assert.equal(lex("0"), [mkint(0)])
    assert.equal(lex("-1"), [mkint(-1)])
    assert.equal(lex("7"), [mkint(7)])
    assert.equal(lex("3_000"), [mkint(3000)])
    assert.equal(lex("0xABad1dea"), [mkint(0xabad1dea)])

def test_float(assert):
    def mkfloat(n):
        return makeTerm(makeTag(null, ".float64.", any), n, [], null)
    assert.equal(lex("1e9"), [mkfloat(1e9)])
    assert.equal(lex("3.1415E17"), [mkfloat(3.1415E17)])
    assert.equal(lex("0.91"), [mkfloat(0.91)])
    assert.equal(lex("-0.91"), [mkfloat(-0.91)])
    assert.equal(lex("3e-2"), [mkfloat(3e-2)])

def test_string(assert):
    def mkstr(s):
        return makeTerm(makeTag(null, ".String.", any), s, [], null)
    assert.equal(lex("\"foo bar\""), [mkstr("foo bar")])
    assert.equal(lex("\"foo\\nbar\""), [mkstr("foo\nbar")])
    assert.equal(lex("\"foo\\\nbar\""), [mkstr("foobar")])
    assert.equal(lex("\"z\\u0061p\""), [mkstr("zap")])
    assert.equal(lex("\"z\\x61p\""), [mkstr("zap")])

def test_char(assert):
    def mkchar(c):
        return makeTerm(makeTag(null, ".char.", any), c, [], null)
    assert.equal(lex("'z'"), [mkchar('z')])
    assert.equal(lex("'\\n'"), [mkchar('\n')])
    assert.equal(lex("'\\u0061'"), [mkchar('a')])
    assert.equal(lex("'\\x61'"), [mkchar('a')])

def test_tag(assert):
    def mkTag(n):
        return makeTerm(makeTag(null, n, any), null, [], null)
    assert.equal(lex("foo"), [mkTag("foo")])
    assert.equal(lex("::\"foo\""), [mkTag("::\"foo\"")])
    assert.equal(lex("::foo"), [mkTag("::foo")])
    assert.equal(lex("foo::baz"), [mkTag("foo::baz")])
    assert.equal(lex("foo::\"baz\""), [mkTag("foo::\"baz\"")])
    assert.equal(lex("biz::baz::foo"), [mkTag("biz::baz::foo")])
    assert.equal(lex("foo_yay"), [mkTag("foo_yay")])
    assert.equal(lex("foo$baz32"), [mkTag("foo$baz32")])
    assert.equal(lex("foo-baz.19"), [mkTag("foo-baz.19")])

def test_quant(assert):
    def mkTag(n):
        return makeTerm(makeTag(null, n, any), null, [], null)
    assert.equal(lex("*"), [mkTag("*")])
    assert.equal(lex("+"), [mkTag("+")])
    assert.equal(lex("?"), [mkTag("?")])


unittest([test_integer, test_float, test_string, test_char, test_tag, test_quant])
