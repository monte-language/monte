from collections import namedtuple
import string
from parsley import ParseError as ParsleyParseError
from terml.nodes import Term, Tag

class ParseError(ParsleyParseError):

    def __init__(self, line, msg, lineNum, colStart, colBound):
        ParsleyParseError.__init__(self, line, None, msg)
        self.line = line
        self.lineNum = lineNum
        self.colStart = colStart
        self.colBound = colBound

    def formatError(self):
        reason = self.formatReason()
        return ('\n' + self.line + '\n' + (' ' * self.colStart + '^' * self.colBound) +
                "\nParse error at line %s, column %s: %s.\n"
                % (self.lineNum, self.colStart, reason))


_SourceSpan = namedtuple("SourceSpan",
                         "uri isOneToOne startLine startCol endLine endCol")
class SourceSpan(_SourceSpan):
    """
Information about the original location of a span of text.
Twines use this to remember where they came from.

uri: Name of document this text came from.

isOneToOne: Whether each character in that Twine maps to the
corresponding source character position.

startLine, endLine: Line numbers for the beginning and end of the
span. Line numbers start at 1.

startCol, endCol: Column numbers for the beginning and end of the
span. Column numbers start at 0.
"""
    def __new__(*args, **kwargs):
        ss = _SourceSpan.__new__(*args, **kwargs)
        if (ss.startLine != ss.endLine and ss.isOneToOne):
            raise ValueError("one-to-one spans must be on a line")
        return ss

    def notOneToOne(self):
        """
        Return a new SourceSpan for the same text that doesn't claim
        one-to-one correspondence.
        """
        return SourceSpan(self.uri, False, self.startLine, self.startCol,
                          self.endLine, self.endCol)

    def __repr__(self):
        return "<%s#:%s::%s>" % (self.uri,
                                 "span" if self.isOneToOne else "blob",
                                 ':'.join(str(x) for x in self[2:]))



def spanCover(a, b):
    """
    Create a new SourceSpan that covers spans `a` and `b`.
    """
    if a is None or b is None or a.uri != b.uri:
        return None
    if (a.isOneToOne and b.isOneToOne
        and a.endLine == b.startLine
        and a.endCol == b.startCol):
        # These spans are adjacent.
        return SourceSpan(a.uri, True,
                          a.startLine, a.startCol,
                          b.endLine, b.endCol)

    # find the earlier start point
    if a.startLine < b.startLine:
        startLine = a.startLine
        startCol = a.startCol
    elif a.startLine == b.startLine:
        startLine = a.startLine
        startCol = min(a.startCol, b.startCol)
    else:
        startLine = b.startLine
        startCol = b.startCol

    #find the later end point
    if b.endLine > a.endLine:
        endLine = b.endLine
        endCol = b.endCol
    elif a.endLine == b.endLine:
        endLine = a.endLine
        endCol = max(a.endCol, b.endCol)
    else:
        endLine = a.endLine
        endCol = a.endCol

    return SourceSpan(a.uri, False, startLine, startCol, endLine, endCol)

def twineAdd(left, right):
    # Poor approximation of the real thing since it doesn't accomodate
    # later slicing.
    leftText, leftSpan = left
    rightText, rightSpan = right

    return leftText + rightText, spanCover(leftSpan, rightSpan)

def twineSlice(twine, start, stop):
    text, span = twine
    if start is None:
        start = 0
    if stop is None:
        stop = len(text)
    if not span.isOneToOne:
        return text[start:stop], span

    startCol = span.startCol + start
    endCol = startCol + (stop - start) - 1
    newspan = SourceSpan(span.uri, True,
                         span.startLine,
                         startCol,
                         span.endLine,
                         endCol)
    return text[start:stop], newspan

uriChars = string.letters + string.digits + '_;/?:@&=+$,-.!~*\()%\\#\'|'
EOF = object()
reserved = set(["delegate", "module", "abstract", "an", "as", "assert", "attribute",
           "be", "begin", "behalf", "belief", "believe", "believes", "case",
           "class", "const", "constructor", "declare", "default", "define",
           "defmacro", "delicate", "deprecated", "dispatch", "do", "encapsulate",
           "encapsulated", "encapsulates", "end", "ensure", "enum", "eventual",
           "eventually", "export", "facet", "forall", "function", "given",
           "hidden", "hides", "inline", "is", "know", "knows", "lambda", "let",
           "methods", "namespace", "native", "obeys", "octet", "oneway",
           "operator", "package", "private", "protected", "public",
           "raises", "reliance", "reliant", "relies", "rely", "reveal", "sake",
           "signed", "static", "struct", "suchthat", "supports", "suspect",
           "suspects", "synchronized", "this", "transient", "truncatable",
           "typedef", "unsigned", "unum", "uses", "using", "utf8", "utf16",
           "virtual", "volatile", "wstring"])
basicKeywords = set(["bind", "break", "catch", "continue", "def", "else", "escape", "exit",
           "extends", "finally", "fn", "for", "guards", "if", "implements", "in",
           "interface", "match", "meta", "method", "pragma", "return", "switch",
           "to", "try", "var", "via", "when", "while", "accum", "module", "on",
           "select", "throws", "thunk"])

keywords = reserved | basicKeywords

def isKeyword(key):
    return key.lower() in keywords

idStart = string.letters + '_'
idPart = string.letters + string.digits + '_'

def isIdentifierPart(c):
    return c in idPart

def isIdentifierStart(c):
    return c in idStart

def leafTag(tagName, span):
    return Term(Tag(tagName), None, None, span)

def composite(tagName, data, span):
    return Term(Tag(tagName), data, None, span)

class StringFeeder(object):
    def __init__(self, data, url):
        self.data = data + '\n'
        self.url = url
        self.lineNum = 0
        lines = self.lines()
        self.nextLine = lambda: next(lines)

    def lines(self):
        # TODO: prompt logic
        for line in self.data.splitlines():
            line += '\n'
            self.lineNum += 1
            span = SourceSpan(self.url, True, self.lineNum,
                              0, self.lineNum, len(line) - 1)
            yield (line, span)

        yield (None, None)

class Indenter(object):
    def __init__(self):
        # opener, closer, indent, nested
        self.stack = [(None, None, 0, True)]
        self.nestLevel = 0

    def closer(self):
        return self.stack[-1][1]

    def indent(self):
        return self.stack[-1][2]

    def push(self, opener, closerChar, indent, isNest=False):
        self.stack.append((opener, closerChar, indent, isNest))

    def pop(self, lexer, closerChar, closer):
        if len(self.stack) <= 1:
            lexer.syntaxError("unmatched closing bracket %r" % (closerChar,))
        if self.closer() != closerChar:
            lexer.syntaxError("mismatch: %r vs %r" % (self.stack[-1][0], closerChar))
        if self.stack.pop()[3]:
            self.nestLevel -= 1

    def popIf(self, closerChar):
        if len(self.stack) <= 1:
            return
        if self.closer() != closerChar:
            return
        if self.stack.pop()[3]:
            self.nestLevel -= 1

class ELexer(object):

    def __init__(self, input):
        self.input = input
        #current column
        self.position = -1
        #last char read
        self.currentChar = None

        self.indenter = Indenter()
        self.continueCount = 0

        self._delayedNextChar = False
        self._startPos = -1
        self._startText = None

        self.inQuasi = False

        self.setLine(self.input.nextLine())
        self.nextChar()

    def __iter__(self):
        return self

    def setLine(self, (line, span)):
        self._currentLine = line
        self._currentSpan = span

    def isEndOfFile(self):
        return self._currentLine is None

    def nextLine(self):
        if self.isEndOfFile():
            self.currentChar = EOF
            return
        if self._startPos == -1:
            if self._startText is not None:
                # current token already started
                self._startText = twineAdd(self._startText, self._currentLine)
            # else no current token, do nothing
        else:
            # current token started on this line
            self._startText = self.getSpan(self._startPos, None)
            self._startPos = -1
        self.position = -1

        #TODO prompt stuff
        self.setLine(self.input.nextLine())
        self.currentChar = '\n'

    def nextChar(self):
        while True:
            if self.isEndOfFile():
                self.currentChar = EOF
                return self.currentChar
            self.position += 1
            if self.position < len(self._currentLine):
                self.currentChar = self._currentLine[self.position]
                return self.currentChar
            else:
                self.nextLine()

    def peekChar(self):
        if self.isEndOfFile() or self.currentChar == '\n':
            raise ValueError()
        return self._currentLine[self.position + 1]

    def getSpan(self, start, bound, err="unexpected end of file"):
        if self.isEndOfFile():
            raise ValueError(err)
        return twineSlice((self._currentLine, self._currentSpan), start, bound)

    def startToken(self):
        if self._startPos >= 0 or self._startText:
            raise RuntimeError("Token already started")
        self._startPos = self.position

    def endToken(self):
        pos = self.position
        if self._delayedNextChar:
            self.position += 1
        if self._startPos == -1:
            # Started on previous line.
            result = self._startText
            if not self.isEndOfFile():
                result = twineAdd(result, self.getSpan(0, pos))
        else:
            # Starts on this line.
            result = self.getSpan(self._startPos, pos)
        self.stopToken()
        return result

    def stopToken(self):
        self._startPos = -1
        self._startText = None

    def endSpan(self):
        return self.endToken()[1]

    def skipWhiteSpace(self):
        """
        Skip horizontal whitespace.
        """
        if self.isEndOfFile():
            return
        while self.currentChar == ' ':
            self.nextChar()

    def leafEOL(self):
        if self.indenter.indent() == 0 and self.continueCount == 0:
            # return leafTag('EOTLU', self.endSpan())
            return leafTag('EOL', self.endSpan())
        else:
            return leafTag('EOL', self.endSpan())

    def syntaxError(self, msg):
        if self._startPos == -1:
            start = self.position - 1
        else:
            start = self._startPos
        start = max(min(start, self.position - 1), 0)
        bound = max(self.position, start + 1)
        raise ParseError(self._currentLine, [('message', msg)],
                         self.input.lineNum, start, bound)

    def next(self):
        try:
            result = self.getNextToken()
        finally:
            self._startPos = -1
            self._startText = None
        return result

    def getNextToken(self):
        if self._delayedNextChar:
            self.nextChar()
            self._delayedNextChar = False
        if self.indenter.closer() == '`':
            self.startToken()
            return self.quasiPart()

        self.skipWhiteSpace()
        self.startToken()
        cur = self.currentChar

        if cur is EOF:
            raise StopIteration()

        if cur in ';,~?':
            self.nextChar()
            return leafTag(cur, self.endSpan())

        if cur == '\n':
            self._delayedNextChar = True
            return self.leafEOL()

        if cur == '(':
            return self.openBracket(')')

        if cur == '[':
            return self.openBracket(']')

        if cur == '{':
            return self.openBracket('}')

        if cur == '}':
            result = self.closeBracket()
            self.indenter.popIf('$')
            return result

        if cur in ')]':
            self.closeBracket()

        if cur == '$':
            nex = self.nextChar()
            if nex == '{':
                # quasi hole of form ${blah}
                self.nextChar()
                return self.openBracket('${', self.endToken(), '}')
            elif isIdentifierStart(nex):
                # quasi hole of form $blee
                nex = self.nextChar()
                while isIdentifierPart(nex):
                    nex = self.nextChar()
                name = self.endToken()
                key = name[0][1:]
                if isKeyword(key):
                    raise self.syntaxError(key + "is a keyword")
                self.indenter.popIf('$')
                return composite('${', key, name[1])
            else:
                # for $$ or $0
                return leafTag('$', self.endSpan())

        if cur == '@':
            raise RuntimeError('todo')

        if cur == '<':
            nex = self.nextChar()
            if nex == '=':
                raise RuntimeError('todo')
            elif nex == '<':
                raise RuntimeError('todo')
            elif isIdentifierStart(nex):
                res = self.uri()
                if res is not None:
                    return res
            return leafTag(cur, self.endSpan())

        if cur == '\'':
            return self.charLiteral()

        if cur == '"':
            return self.stringLiteral()

        if cur in string.digits:
            return self.numberLiteral()

        if cur == '_':
            if isIdentifierPart(self.peekChar()):
                return self.identifier()
            return self.leafTag(cur, self.endSpan())

        if isIdentifierStart(cur):
            return self.identifier()
        else:
            self.syntaxError("unrecognized character %r" % (cur,))

    def identifier(self):
        while isIdentifierPart(self.nextChar()):
            pass

        if self.currentChar == '=':
            c = self.peekChar()
            if c not in '=>~':
                self.nextChar()
                token, span = self.endToken()
                token = token[:-1]
                if isKeyword(token):
                    self.syntaxError(token + "is a keyword")
                return composite("VERB_ASSIGN", token, span)
        token, span = self.endToken()
        if isKeyword(token):
            return leafTag(token.lower(), span)
        else:
            return composite('IDENTIFIER', token, span)

    def charConstant(self):
        if self.currentChar == '\\':
            nex = self.nextChar()
            if nex == 'u':
                hexstr = ""
                for i in range(4):
                    hexstr += self.nextChar()
                try:
                    v = int(hexstr, 16)
                except ValueError:
                    self.syntaxError('\\u escape must be four hex digits')
                else:
                    self.nextChar()
                    return unichr(v)
            if nex == EOF:
                self.syntaxError("end of file in middle of literal")
            c = {
                'b': '\b',
                't': '\t',
                'n': '\n',
                'f': '\f',
                'r': '\r',
                '"': '"',
                '\'': "'",
                '\\': '\\',
                '\n': None
                }.get(nex, -1)
            if c == -1:
                self.syntaxError("Unrecognized escaped character")
            else:
                self.nextChar()
                return c
        if self.currentChar == EOF:
            self.syntaxError("end of file in middle of literal")
        elif self.inQuasi and self.currentChar in '$@':
            c = self.currentChar
            if c != self.nextChar():
                self.syntaxError("When quasi-parsing, %r must be doubled" % (c,))
            self.nextChar()
            return c
        elif self.currentChar == '\t':
            self.syntaxError('Quoted tabs must be written as \\t.')
        else:
            c = self.currentChar
            self.nextChar()
            return c

    def charLiteral(self):
        self.nextChar()
        c = self.charConstant()
        while c is None:
            c = self.charConstant()
        if self.currentChar != "'":
            self.syntaxError('char constant must end in "\'"')
        self.nextChar()
        return composite('.char.', c, self.endSpan())

    def stringLiteral(self):
        self.nextChar()
        self.indenter.push(self.getSpan(self._startPos, self.position,
                                        "file ends inside string literal"), '"', 0)
        buf = []
        while self.currentChar != '"':
            if self.isEndOfFile():
                self.syntaxError("File ends inside string literal")
            cc = self.charConstant()
            if cc is not None:
                buf.append(cc)
        self.nextChar()
        closer = self.endToken()
        self.indenter.pop(self, '"', closer)
        return composite('.String.', ''.join(buf), closer[1])

    def numberLiteral(self):
        radix = 10
        floating = False
        if self.currentChar == '0':
            self.nextChar()
            if self.currentChar.lower() == 'x':
                radix = 16
                self.nextChar()
        if radix == 16:
            self.digits(16)
        else:
            self.digits(10)
            if self.currentChar == '.' and self.peekChar() in string.digits:
                self.nextChar()
                floating = True
                self.digits(10)
            if self.currentChar.lower() == 'e':
                self.nextChar()
                floating = True
                if self.currentChar in '-+':
                    self.nextChar()
                if not self.digits(10):
                    self.syntaxError("Missing exponent")
        tok, span = self.endToken()
        s = tok.replace('_', '')
        if floating:
            return composite('.float64.', float(s), span)
        else:
            if radix == 16:
                return composite('.int.', int(s, 16), span)
            else:
                return composite('.int.', int(s), span)

    def digits(self, radix):
        if radix == 10:
            digs = string.digits
        elif radix == 16:
            digs = string.hexdigits
        if self.currentChar not in digs:
            return False
        digs += '_'
        while self.currentChar in digs:
            self.nextChar()
        return True

    def uri(self):
        length = len(self._currentLine)
        pos = self.position + 1
        while pos < length and isIdentifierPart(self._currentLine[pos]):
            pos += 1
        if pos >= len:
            # something like '... < foo\n', so never mind
            return None
        if '>' == self._currentLine[pos]:
            #success, it was a URI getter
            self.position = pos
            self.nextChar()
            token, span = self.endToken()
            return composite('URI_GETTER', token[1:-1], span)
        elif self._currentLine[pos] != ':':
            # something like '< foo)', never mind again
            return None
        self.position = pos
        self.nextChar()
        while self.currentChar in uriChars:
            self.nextChar()
        if self.currentChar != '>':
            self.syntaxError("Can't use %r in a URI body" % (self.currentChar,))
        self.nextChar()
        source, span = self.endToken()
        return composite('URI', source[1:-1], span)


# ['!', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '!=', '!~', '%%', '%=', '&!', '&&', '&=', '**', '*=', '+=', '-=', '->', '..', '//', '/=', '::', ':=', '<-', '<<', '<=', '==', '=>', '=~', '>=', '>>', '^=', 'as', 'fn', 'if', 'in', 'to', '|=', '||', '%%=', '**=', '..!', '/**', '//=', '<<=', '<=>', '>>=', 'def', 'for', 'try', 'var', 'via', 'bind', 'else', 'exit', 'meta', 'when', 'accum', 'break', 'catch', 'match', 'scope', 'while', 'escape', 'guards', 'method', 'pragma', 'return', 'switch', 'context', 'extends', 'finally', 'continue', 'getState', 'interface', 'implements']

"""
hspace = (' '|'\t'|'\f'|('#' (~eol anything)*))
ws = ('\r' '\n'|'\r' | '\n' | hspace)*

number = ws barenumber
barenumber = '-'?:sign ('0' (('x'|'X') <hexdigit*>:hs
                                        -> int((sign or '') + hs, 16)
                        |floatPart(sign '0')
                        |<octaldigit*>:ds -> int((sign or '') + '0' + ds, 8))
               |decdigits:ds floatPart(sign ds)
               |decdigits:ds -> int((sign or '') + ds))

exponent = <('e' | 'E') ('+' | '-')? decdigits>
floatPart :sign :ds = <('.' decdigits exponent?) | exponent>:tail
                    -> float((sign or '') + ds + tail)
decdigits = digit:d ((:x ?(x.isdigit()) -> x) | '_' -> "")*:ds
          -> d + ''.join(ds)
octaldigit = :x ?(x in string.octdigits) -> x
hexdigit = :x ?(x in string.hexdigits) -> x

string = ws '"' (escapedChar | ~('"') anything)*:c '"' -> ''.join(c)
character = ws '\'' (escapedChar | ~('\''|'\n'|'\r'|'\\') anything):c '\''
          -> t.Character(c)
escapedUnicode = ('u' <hexdigit hexdigit hexdigit hexdigit>:hs
                -> unichr(int(hs, 16))
               |'U' <hexdigit hexdigit hexdigit hexdigit
                     hexdigit hexdigit hexdigit hexdigit>:hs
                -> unichr(int(hs, 16)))

escapedOctal = ( <:a ?(a in "0123") octdigit? octdigit?>
                 | <:a ?(a in "4567") octdigit?>):os -> int(os, 8)

escapedChar = '\\' ('n' -> '\n'
                     |'r' -> '\r'
                     |'t' -> '\t'
                     |'b' -> '\b'
                     |'f' -> '\f'
                     |'"' -> '"'
                     |'\'' -> '\''
                     |'?' -> '?'
                     |'\\' -> '\\'
                     | escapedUnicode
                     | escapedOctal
                     | eol -> "")

eol = hspace* ('\r' '\n'|'\r' | '\n')

uriBody = <(letterOrDigit|'_'|';'|'/'|'?'|':'|'@'|'&'|'='|'+'|'$'|','|'-'|'.'
            |'!'|'~'|'*'|'\''|'('|')'|'%'|'\\'|'|'|'#')+>


updocLine = <('?'|'#'|'>') (~('\n' | '\r') anything)*>:txt eol -> txt
updoc = ('?' (~('\n' | '\r') anything)*
             ((eol (eol | updocLine)*) (spaces | updocLine))?
        )

eolplus = eol updoc?
linesep = eolplus+

br = (spaces eolplus | eolplus)*


uriScheme = <letter (letterOrDigit | '_' | '+' | '-' | '.')*>
uriGetter = "<" uriScheme:s '>'
identifier = spaces <(letter | '_') (letterOrDigit | '_')*>

"""
