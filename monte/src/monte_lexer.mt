module unittest
export (makeMonteLexer)

object VALUE_HOLE {}
object PATTERN_HOLE {}
object EOF {}
def decimalDigits := '0'..'9'
def hexDigits := decimalDigits | 'a'..'f' | 'A'..'F'

def idStart := 'a'..'z' | 'A'..'Z' | '_'..'_'
def idPart := idStart | '0'..'9'
def closers := ['(' => ')', '[' => ']', '{' => '}']

def isIdentifierPart(c):
    if (c == EOF):
        return false
    return idPart(c)

def MONTE_KEYWORDS := [
    "as", "bind", "break", "catch", "continue", "def", "else", "escape",
    "exit", "extends", "export", "finally", "fn", "for", "guards", "if",
    "implements", "in", "interface", "match", "meta", "method", "module",
    "object", "pass", "pragma", "return", "switch", "to", "try", "var",
    "via", "when", "while"]

def composite(name, data, span):
    return term__quasiParser.makeTerm(term__quasiParser.makeTag(null, name, any),
                                      data, [], span)

def _makeMonteLexer(input, braceStack, var nestLevel):

    # The character under the cursor.
    var currentChar := null
    # Offset of the current character.
    var position := -1
    # Start offset of the text for the token being created.
    var startPos := -1

    # Syntax error produced from most recent tokenization attempt.
    var errorMessage := null

    var count := -1


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
            throw.eject(fail, `Unmatched closing character ${closer.quote()}`)
        else if (braceStack.last()[1] != closer):
            throw.eject(fail, `Mismatch: ${closer.quote()} doesn't close ${braceStack.last()[0]}`)
        def item := braceStack.pop()
        if (item[3]):
            nestLevel -= 1

    def skipWhitespace():
        if (atEnd()):
            return
        while (currentChar == ' '):
            advance()

    def atLogicalEndOfLine():
        if (atEnd()):
            return true
        var i := position + 1
        while ((i < input.size()) && input[i] == ' '):
            i += 1
        return (i == input.size() || [' ', '\n', '#'].contains(input[i]))

    def offsetInLine():
        var i := 0
        while (i < position && input[position - i] != '\n'):
            i += 1
        return i

    def startToken():
        if (startPos >= 0):
            throw("Token already started")
        startPos := position

    def endToken():
        def pos := position
        def tok := input.slice(startPos, pos)
        startPos := -1
        return tok

    def leaf(tok):
        return composite(tok, null, endToken().getSpan())

    def collectDigits(var digitset):
        if (atEnd() || !digitset(currentChar)):
            return false
        digitset |= ('_'..'_')
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
                    throw.eject(fail, "Missing fractional part")
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
                    throw.eject(fail, "Missing exponent")
        def tok := endToken()
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

    def stringLiteral(fail):
        def opener := currentChar
        advance()
        pushBrace(opener, '"', 0, false)
        def buf := [].diverge()
        while (currentChar != '"'):
            if (atEnd()):
                throw.eject(fail, "Input ends inside string literal")
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
        return composite(".char.", c, endToken().getSpan())

    def identifier(fail):
        while (isIdentifierPart(advance())):
            pass
        if (currentChar == '='):
            def c := peekChar()
            if (!['=', '>', '~'].contains(c)):
                advance()
                def chunk := endToken()
                def token := chunk.slice(0, chunk.size() - 1)
                if (MONTE_KEYWORDS.contains(token)):
                    throw.eject(fail, `$token is a keyword`)
                return composite("VERB_ASSIGN", token, chunk.getSpan())
        def token := endToken()
        if (MONTE_KEYWORDS.contains(token.toLowerCase())):
            return composite(token.toLowerCase(), token.toLowerCase(), token.getSpan())
        else:
            return composite("IDENTIFIER", token, token.getSpan())

    def quasiPart(fail):
        def buf := [].diverge()
        while (true):
            while (!['@', '$', '`'].contains(currentChar)):
                # stuff that doesn't start with @ or $ passes through
                if (currentChar == EOF):
                    throw.eject(fail, "File ends inside quasiliteral")
                buf.push(currentChar)
            if (peekChar() == currentChar):
                buf.push(currentChar)
                advance()
                advance()
            else if (currentChar == '`'):
                # close backtick
                advance()
                popBrace('`', fail)
                return composite("QUASI_CLOSE", __makeString.fromChars(buf),
                                 endToken().getSpan())
            else if (currentChar == '$' && peekChar() == '\\'):
                # it's a character constant like $\u2603 or a line continuation like $\
                advance()
                def cc := charConstant()
                if (cc != null):
                    buf.push(cc)
            else:
                def opener := endToken()
                pushBrace(opener, "hole", nestLevel * 4, true)
                if (buf.size() == 0):
                    return null
                return composite("QUASI_OPEN", __makeString.fromChars(buf),
                                 opener.getSpan())


    def openBracket(closer, var opener, fail):
        if (opener == null):
            advance()
            opener := endToken()
        if (atLogicalEndOfLine()):
            pushBrace(opener, closer, nestLevel * 4, true)
        else:
            pushBrace(opener, closer, offsetInLine(), true)
        return composite(opener, null, opener.getSpan())

    def closeBracket(fail):
        advance()
        def closer := endToken()
        popBrace(closer, fail)
        return composite(closer, null, closer.getSpan())

    def getNextToken(fail):
        if (braceStack.last()[1] == '`'):
            startToken()
            return quasiPart()

        skipWhitespace()
        startToken()

        def cur := currentChar
        if (cur == EOF):
            throw.eject(fail, "End of input")
        if (cur == '\n'):
            advance()
            return leaf("EOL")

        if ([';', ',', '~', '?'].contains(cur)):
            advance()
            return leaf(__makeString.fromChars([cur]))

        if (cur == '('):
            return openBracket(")", null, fail)
        if (cur == '['):
            return openBracket("]", null, fail)
        if (cur == '{'):
            return openBracket("}", null, fail)

        if (cur == '}'):
            def result := closeBracket(fail)
            if (braceStack.last()[1] == "hole"):
                popBrace("hole", fail)
            return result
        if (cur == ']'):
            return closeBracket(fail)
        if (cur == ')'):
            return closeBracket(fail)

        if (cur == '$'):
            def nex := advance()
            if (nex == '{'):
                # quasi hole of form ${blah}
                return openBracket("}", null, fail)
            else if (nex != EOF && idStart(nex)):
                # quasi hole of form $blee
                var cc := advance()
                while (isIdentifierPart(cc)):
                    cc := advance()
                def name := endToken()
                def key := name.slice(1)
                if (MONTE_KEYWORDS.contains(key.toLowerCase())):
                    advance()
                    throw.eject(fail, `$key is a keyword`)
                if (braceStack.last()[1] == "hole"):
                    popBrace("hole", fail)
                return composite("DOLLAR_IDENT", key, name.getSpan())
            else if (nex == '$'):
                return leaf("$")
            else:
                throw.eject(fail, `Unrecognized $$-escape "$$$nex"`)

        if (cur == '@'):
            def nex := advance()
            if (nex == '{'):
                # quasi hole of the form @{blee}
                return openBracket("}", null, fail)
            else if (nex != EOF && idStart(nex)):
                # quasi hole of the form @blee
                var cc := advance()
                while (isIdentifierPart(cc)):
                    cc := advance()
                def name := endToken()
                def key := name.slice(1)
                if (MONTE_KEYWORDS.contains(key.toLowerCase())):
                    advance()
                    throw.eject(fail, `$key is a keyword`)
                if (braceStack.last()[1] == "hole"):
                    popBrace("hole", fail)
                return composite("AT_IDENT", key, name.getSpan())
            else if (nex == '@'):
                return leaf("@")
            else:
                throw.eject(fail, `Unrecognized @@-escape "@@$nex"`)

        if (cur == '.'):
            def nex := advance()
            if (nex == '.'):
                def nex2 := advance()
                if (nex2 == '!'):
                    advance()
                    return leaf("..!")
                return leaf("..")
            return leaf(".")

        if (cur == '^'):
            def nex := advance()
            if (nex == '='):
                advance()
                return leaf("^=")
            return leaf("^")

        if (cur == '+'):
            def nex := advance()
            if (nex == '+'):
                advance()
                throw.eject(fail, "++? lol no")
            if (nex == '='):
                advance()
                return leaf("+=")
            return leaf("+")

        if (cur == '-'):
            def nex := advance()
            if (nex == '-'):
                advance()
                throw.eject(fail, "--? lol no")
            if (nex == '='):
                advance()
                return leaf("-=")
            if (nex == '>'):
                advance()
                if (atLogicalEndOfLine()):
                    # this is an arrow ending a line, and should be
                    # followed by an indent
                    pass
                return leaf("->")
            return leaf("-")
        if (cur == ':'):
            def nex := advance()
            if (nex == ':'):
                advance()
                return leaf("::")
            if (nex == '='):
                advance()
                return leaf(":=")
            if (atLogicalEndOfLine()):
                # this is a colon ending a line, and should be
                # followed by an indent
                pass
            return leaf(":")

        if (cur == '<'):
            def nex := advance()
            if (nex == '-'):
                advance()
                return leaf("<-")
            if (nex == '='):
                def nex2 := advance()
                if (nex2 == '>'):
                    advance()
                    return leaf("<=>")
                return leaf("<=")

            if (nex == '<'):
                def nex2 := advance()
                if (nex2 == '='):
                    advance()
                    return leaf("<<=")
                return leaf("<<")
            return leaf("<")

        if (cur == '>'):
            def nex := advance()
            if (nex == '='):
                advance()
                return leaf(">=")
            if (nex == '>'):
                def nex2 := advance()
                if (nex2 == '='):
                    advance()
                    return leaf(">>=")
                return leaf(">>")
            return leaf(">")

        if (cur == '*'):
            def nex := advance()
            if (nex == '*'):
                def nex2 := advance()
                if (nex2 == '='):
                    advance()
                    return leaf("**=")
                return leaf("**")
            if (nex == '='):
                advance()
                return leaf("*=")
            return leaf("*")

        if (cur == '/'):
            def nex := advance()
            if (nex == '/'):
                def nex2 := advance()
                if (nex2 == '='):
                    advance()
                    return leaf("//=")
                return leaf("//")
            if (nex == '='):
                advance()
                return leaf("/=")
            return leaf("/")

        if (cur == '#'):
            while (!['\n', EOF].contains(currentChar)):
                advance()
            def comment := endToken()
            return composite("#", comment.slice(1), comment.getSpan())
        if (cur == '%'):
            def nex := advance()
            if (nex == '='):
                advance()
                return leaf("%=")
            return leaf("%")

        if (cur == '!'):
            def nex := advance()
            if (nex == '='):
                advance()
                return leaf("!=")
            if (nex == '~'):
                advance()
                return leaf("!~")
            return leaf("!")

        if (cur == '='):
            def nex := advance()
            if (nex == '='):
                advance()
                return leaf("==")
            if (nex == '>'):
                advance()
                return leaf("=>")
            if (nex == '~'):
                advance()
                return leaf("=~")
            throw.eject(fail, "Use := for assignment or == for equality")
        if (cur == '&'):
            def nex := advance()
            if (nex == '&'):
                advance()
                return leaf("&&")
            if (nex == '='):
                advance()
                return leaf("&=")
            if (nex == '!'):
                advance()
                return leaf("&!")
            return leaf("&")

        if (cur == '|'):
            def nex := advance()
            if (nex == '='):
                advance()
                return leaf("|=")
            if (nex == '|'):
                return leaf("||")
            return leaf("|")

        if (cur == '"'):
            def s := stringLiteral(fail)
            def closer := endToken()
            popBrace('"', fail)

            return composite(".String.", s, closer.getSpan())

        if (cur == '\''):
            return charLiteral(fail)

        if (cur == '`'):
            advance()
            pushBrace('`', '`', 0, false)
            def part := quasiPart(fail)
            if (part == null):
                def next := getNextToken(fail)
                if (next == EOF):
                    throw.eject(fail, "File ends in quasiliteral")
                return next
            return part

        if (decimalDigits(cur)):
            return numberLiteral(fail)

        if (cur == '_'):
            if (idStart(peekChar())):
                return identifier(fail)
            advance()
            return leaf("_", fail)

        if (cur == '\t'):
            throw.eject(fail, "Tab characters are not permitted in Monte source.")
        if (idStart(cur)):
            return identifier(fail)

        throw.eject(fail, `Unrecognized character ${cur.quote()}`)

    advance()
    return object monteLexer:

        to _makeIterator():
            return monteLexer

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
            return _makeMonteLexer(chunk, braceStack, nestLevel)


object makeMonteLexer:
    to run(input):
        # State for paired delimiters like "", {}, (), []
        def braceStack := [[null, null, 0, true]].diverge()
        return _makeMonteLexer(input, braceStack, 0)

    to holes():
        return [VALUE_HOLE, PATTERN_HOLE]


def lex(s):
    def l := makeMonteLexer(s)
    def toks := [t for t in l]
    if ((def err := l.getSyntaxError()) != null):
        throw(err)
    if (toks.size() > 0 && toks.last().getTag().getName() == "EOL"):
       return toks.slice(0, toks.size() - 1)
    return toks

def tt(tagname, data):
    return term__quasiParser.makeTerm(term__quasiParser.makeTag(null, tagname, any),
                                      data, [], null)

def test_ident(assert):
    assert.equal(lex("foo_bar9"), [tt("IDENTIFIER", "foo_bar9")])
    assert.equal(lex("foo"), [tt("IDENTIFIER", "foo")])

def test_char(assert):
    assert.equal(lex("'z'"), [tt(".char.", 'z')])
    assert.equal(lex("'\\n'"), [tt(".char.", '\n')])
    assert.equal(lex("'\\u0061'"), [tt(".char.", 'a')])
    assert.equal(lex("'\\x61'"), [tt(".char.", 'a')])

def test_string(assert):
    assert.equal(lex(`"foo\$\nbar"`), [tt(".String.", "foobar")])
    assert.equal(lex(`"foo"`),        [tt(".String.", "foo")])
    assert.equal(lex(`"foo bar 9"`),  [tt(".String.", "foo bar 9")])
    assert.equal(lex(`"foo\nbar"`),  [tt(".String.", "foo\nbar")])

def test_integer(assert):
    assert.equal(lex("0"), [tt(".int.", 0)])
    assert.equal(lex("7"), [tt(".int.", 7)])
    assert.equal(lex("3_000"), [tt(".int.", 3000)])
    assert.equal(lex("0xABad1dea"), [tt(".int.", 2880249322)])

def test_float(assert):
    assert.equal(lex("1e9"), [tt(".float64.", 1e9)])
    assert.equal(lex("3.1415E17"), [tt(".float64.", 3.1415E17)])
    assert.equal(lex("0.91"), [tt(".float64.", 0.91)])
    assert.equal(lex("3e-2"), [tt(".float64.", 3e-2)])

def test_holes(assert):
    assert.equal(lex("${"), [tt("${", null)])
    assert.equal(lex("$blee"), [tt("DOLLAR_IDENT", "blee")])
    assert.equal(lex("@{"), [tt("@{", null)])
    assert.equal(lex("@blee"), [tt("AT_IDENT", "blee")])
    assert.equal(lex("@_fred"), [tt("AT_IDENT", "_fred")])
    assert.equal(lex("@_"), [tt("AT_IDENT", "_")])

def test_braces(assert):
    assert.equal(lex("[a, 1]"),
                 [tt("[", null),
                  tt("IDENTIFIER", "a"),
                  tt(",", null),
                  tt(".int", 1),
                  tt("]", null)])
    assert.equal(lex("{1}"),
                 [tt("{", null),
                  tt(".int.", 1),
                  tt("}", null)])
    assert.equal(lex("(a)"),
                 [tt("(", null),
                  tt("IDENTIFIER", "a"),
                  tt(")", null)])

def test_dot(assert):
    assert.equal(lex("."), [tt(".", null)])
    assert.equal(lex(".."), [tt("..", null)])
    assert.equal(lex("..!"), [tt("..!", null)])

def test_caret(assert):
    assert.equal(lex("^"), [tt("^", null)])
    assert.equal(lex("^="), [tt("^=", null)])

def test_plus(assert):
    assert.equal(lex("+"), [tt("+", null)])
    assert.equal(lex("+="), [tt("+=", null)])

def test_minus(assert):
    assert.equal(lex("-"), [tt("-", null)])
    assert.equal(lex("-="), [tt("-=", null)])
    assert.equal(lex("-> {"), [tt("->", null), tt("{", null)])

def test_colon(assert):
    assert.equal(lex(":x"), [tt(":", null), tt("IDENTIFIER", "x")])
    assert.equal(lex(":="), [tt(":=", null)])
    assert.equal(lex("::"), [tt("::", null)])

def test_crunch(assert):
    assert.equal(lex("<"), [tt("<", null)])
    assert.equal(lex("<-"), [tt("<-", null)])
    assert.equal(lex("<="), [tt("<=", null)])
    assert.equal(lex("<<="), [tt("<<=", null)])
    assert.equal(lex("<=>"), [tt("<=>", null)])

def test_zap(assert):
    assert.equal(lex(">"), [tt(">", null)])
    assert.equal(lex(">="), [tt(">=", null)])
    assert.equal(lex(">>="), [tt(">>=", null)])

def test_star(assert):
    assert.equal(lex("*"), [tt("*", null)])
    assert.equal(lex("*="), [tt("*=", null)])
    assert.equal(lex("**"), [tt("**", null)])
    assert.equal(lex("**="), [tt("**=", null)])

def test_slash(assert):
    assert.equal(lex("/"), [tt("/", null)])
    assert.equal(lex("/="), [tt("/=", null)])
    assert.equal(lex("//"), [tt("//", null)])
    assert.equal(lex("//="), [tt("//=", null)])

def test_mod(assert):
    assert.equal(lex("%"), [tt("%", null)])
    assert.equal(lex("%="), [tt("%=", null)])

def test_comment(assert):
    assert.equal(lex("# yes\n1"), [tt("#", " yes"), tt("EOL", null),
                                   tt(".int.", 1)])

def test_bang(assert):
    assert.equal(lex("!"), [tt("!", null)])
    assert.equal(lex("!="), [tt("!=", null)])
    assert.equal(lex("!~"), [tt("!~", null)])

def test_eq(assert):
    assert.equal(lex("=="), [tt("==", null)])
    assert.equal(lex("=~"), [tt("=~", null)])
    assert.equal(lex("=>"), [tt("=>", null)])

def test_and(assert):
    assert.equal(lex("&"), [tt("&", null)])
    assert.equal(lex("&="), [tt("&=", null)])
    assert.equal(lex("&!"), [tt("&!", null)])
    assert.equal(lex("&&"), [tt("&&", null)])

def test_or(assert):
    assert.equal(lex("|"), [tt("|", null)])
    assert.equal(lex("|="), [tt("|=", null)])


unittest([test_ident, test_char, test_string, test_integer, test_float,
          test_holes, test_braces, test_dot, test_caret, test_plus, test_minus,
          test_colon, test_crunch, test_zap, test_star, test_slash, test_mod,
          test_comment, test_bang, test_eq, test_and, test_or])
