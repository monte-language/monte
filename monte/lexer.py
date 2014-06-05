from collections import namedtuple
import string
from ometa.runtime import InputStream, ParseError as ParsleyParseError
from terml.nodes import Term, Tag

class ParseError(ParsleyParseError):
    """
    Represents where and why a parse error happened.
    """
    def __init__(self, line, msg, lineNum, colStart, colBound):
        ParsleyParseError.__init__(self, line, None, msg)
        self.line = line
        self.lineNum = lineNum
        self.colStart = colStart
        self.colBound = colBound

    def formatError(self):
        reason = self.formatReason()
        return ('\n' + self.line + '\n' +
                (' ' * self.colStart + '^' * self.colBound) +
                "\nParse error at line %s, column %s: %s.\n"
                % (self.lineNum, self.colStart, reason))


_SourceSpan = namedtuple("SourceSpan",
                         "uri isOneToOne startLine startCol endLine endCol")
class SourceSpan(_SourceSpan):
    """
    Information about the original location of a span of text. Twines use
    this to remember where they came from.

    (Used in this file as a field on tokens, and as part of a (string,
    span) pair.)

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
    """
    Concatenate strings and combine their spans.
    """
    # Poor approximation of the real thing since it doesn't accomodate
    # later slicing.
    leftText, leftSpan = left
    rightText, rightSpan = right

    return leftText + rightText, spanCover(leftSpan, rightSpan)


def twineSlice(twine, start, stop):
    """
    Slice a string and create an appropriate span for the slice.
    """
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
keywords = set([
    "as", "bind", "break", "catch", "continue", "def", "else", "escape",
    "exit", "extends", "export", "finally", "fn", "for", "guards", "if",
    "implements", "in", "interface", "match", "meta", "method", "module",
    "object", "pass", "pragma", "return", "switch", "to", "try", "var",
    "via", "when", "while"])


def isKeyword(key):
    return key.lower() in keywords


idStart = string.letters + '_'
idPart = string.letters + string.digits + '_'

def isIdentifierPart(c):
    return c in idPart


def isIdentifierStart(c):
    return c in idStart


def leafTag(tagName, span):
    """
    Create a token with no data.
    """
    return Term(Tag(tagName), None, None, span)


def composite(tagName, data, span):
    """
    Create a token with a name and data.
    """
    return Term(Tag(tagName), data, None, span)


class StringFeeder(object):
    """
    Input abstraction for lexer.
    Interactive mode still TODO.
    """
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


class Bracer(object):
    """
    Tracks brace state. Will also be used by interactive mode to
    indent properly at prompt.

    """

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
            lexer.syntaxError("mismatch: %r vs %r" % (self.stack[-1][0],
                                                      closerChar))
        if self.stack.pop()[3]:
            self.nestLevel -= 1

    def popIf(self, closerChar):
        if len(self.stack) <= 1:
            return
        if self.closer() != closerChar:
            return
        if self.stack.pop()[3]:
            self.nestLevel -= 1

    def inStatementPosition(self):
        return self.stack[-1][0] in ('{', 'INDENT', None)


class MonteLexer(object):
    """Tokenizer for Monte language.

    @ivar input: an L{InputFeeder}.
    @ivar currentChar: The last character read.
    @ivar position: The current column. Starts at -1, corresponds to
    index of currentChar.
    @ivar bracer: A L{Bracer}.

    @ivar _delayedNextChar: Whether consuming the previous character
    was delayed or not. Set at the end of lines.

    @ivar _startPos: Beginning column for token currently being lexed.
    @ivar _startText: Text from previous lines for current token, if
    token spans multiple lines.

    @ivar _canStartIndentedBlock: Whether an indent token is expected
    next (i.e., after a colon and newline).
    @ivar _indentPositionStack: Columns indented blocks began at.

    @ivar _currentLine: The line of text currently being tokenized.
    @ivar _currentSpan: The source span for the current line.
    """

    def __init__(self, input):
        self.input = input
        #current column
        self.position = -1
        #last char read
        self.currentChar = None

        self.bracer = Bracer()

        self._delayedNextChar = False
        self._startPos = -1
        self._startText = None

        self._canStartIndentedBlock = False
        self._indentPositionStack = [0]
        self._queuedTokens = []

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
        """
        Advance to the next line, saving text for a partially completed
        token if needed.
        """
        if self.isEndOfFile():
            self.currentChar = EOF
            return
        if self._startPos == -1:
            if self._startText is not None:
                # current token already started
                self._startText = twineAdd(self._startText, (self._currentLine,
                                                             self._currentSpan))
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
        """
        Advance to the next character, loading a new line if needed.
        """
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
        """
        Look at the next character on the current line.
        """
        if self.isEndOfFile() or self.currentChar == '\n':
            raise ValueError()
        return self._currentLine[self.position + 1]

    def getSpan(self, start, bound, err="unexpected end of file"):
        """
        Get a source span for a slice of the current line.
        """
        if self.isEndOfFile():
            raise ValueError(err)
        return twineSlice((self._currentLine, self._currentSpan), start, bound)

    def startToken(self):
        """
        Begin tracking a new token.
        """
        if self._startPos >= 0 or self._startText:
            raise RuntimeError("Token already started")
        self._startPos = self.position

    def endToken(self):
        """
        Create a token from text consumed since L{startToken} was called.
        """
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

    def openBracket(self, closer, opener=None):
        """
        Record an open bracket and the token that will close it.
        """
        c = opener or self.currentChar
        if not opener:
            self.nextChar()
            opener = self.endToken()
        if self._currentLine and self._currentLine[self.position:].isspace():
            self.bracer.nestLevel += 1
            self.bracer.push(opener, closer, self.bracer.nestLevel * 4, True)
        else:
            self.bracer.push(opener, closer, self.position, True)
        return leafTag(c, opener[1])

    def closeBracket(self):
        closerChar = self.currentChar
        self.nextChar()
        closer, span = self.endToken()
        self.bracer.pop(self, closerChar, closer)
        return leafTag(closerChar, span)

    def skipWhiteSpace(self):
        """
        Skip horizontal whitespace.
        """
        if self.isEndOfFile():
            return
        while self.currentChar == ' ':
            self.nextChar()

    def skipLine(self):
        if not self.isEndOfFile():
            self.position = len(self._currentLine) - 1
            self.currentChar = self._currentLine[self.position]
            assert self.currentChar == '\n'

    def leafEOL(self):
        return leafTag('EOL', self.endSpan())

    def syntaxError(self, msg):
        """
        Collect information to indicate where tokenization failure
        happened and why.
        """
        if self._startPos == -1:
            start = self.position - 1
        else:
            start = self._startPos
        start = max(min(start, self.position - 1), 0)
        bound = max(self.position, start + 1)
        raise ParseError(self._currentLine, [('message', msg)],
                         self.input.lineNum, start, bound)

    def next(self):
        """
        Iterator method.
        """
        try:
            result = self.getNextToken()
        finally:
            self._startPos = -1
            self._startText = None
        return result

    def getNextToken(self):
        """
        The main event. Consumes text until a token can be created, then
        returns it.
        """
        if self._queuedTokens:
            return self._queuedTokens.pop()
        if self._delayedNextChar:
            self.nextChar()
            self._delayedNextChar = False
            self.skipWhiteSpace()

        if self.bracer.closer() == '`':
            self.startToken()
            return self.quasiPart()

        self.skipWhiteSpace()
        self.startToken()
        cur = self.currentChar

        if cur is EOF:
            if len(self._indentPositionStack) > 1:
                self._indentPositionStack.pop()
                self.bracer.pop(self, 'DEDENT', '')
                return leafTag('DEDENT', None)
            else:
                raise StopIteration()

        # Updoc.
        if cur in '?>' and (self.position == 0 or self._currentLine[:self.position].isspace()):
            self.skipLine()
            updoc, span = self.endToken()
            return composite('UPDOC', self._currentLine[self.position:], span)


        if cur in ';,~?':
            self.nextChar()
            return leafTag(cur, self.endSpan())

        if cur == '\n':
            if self._canStartIndentedBlock:
                self.nextChar()
                self.skipWhiteSpace()
                while self.currentChar == '\n':
                    self._queuedTokens.insert(0, self.leafEOL())
                    self.startToken()
                    self.nextChar()
                    self.skipWhiteSpace()
                if not self.bracer.inStatementPosition():
                    self.syntaxError("Indented blocks only allowed "
                                     "in statement positions")
                if self.position > self._indentPositionStack[-1]:
                    self._indentPositionStack.append(self.position)
                    self.openBracket('DEDENT', 'INDENT')
                    self._canStartIndentedBlock = False
                    self._queuedTokens.insert(0,
                        leafTag('INDENT', self.getSpan(self._indentPositionStack[-1],
                                                       self.position)[1]))
                    return self.leafEOL()
                else:
                    self.syntaxError("Expected an indented block")

            if not self.bracer.inStatementPosition():
                # no need to account for dedents, bail
                self._delayedNextChar = True
                return self.leafEOL()
            else:
                #look at next line
                tok = self.leafEOL()
                self._queuedTokens.insert(0, tok)
                self.startToken()
                self.nextChar()
                self.skipWhiteSpace()
                while self.currentChar == '\n':
                    self._queuedTokens.insert(0, self.leafEOL())
                    self.startToken()
                    self.nextChar()
                    self.skipWhiteSpace()
                if self.position > self._indentPositionStack[-1]:
                    self.syntaxError("Unexpected indent")
                if self.isEndOfFile():
                    while len(self._indentPositionStack) > 1:
                        self._indentPositionStack.pop()
                        self.bracer.pop(self, 'DEDENT', '')
                        self._queuedTokens.append(leafTag('DEDENT', tok[1]))
                    return self._queuedTokens.pop()

                while self.position < self._indentPositionStack[-1]:
                    if self.position not in self._indentPositionStack:
                        self.syntaxError("unindent does not match any outer indentation level")
                    self._indentPositionStack.pop()
                    self.bracer.pop(self, 'DEDENT', '')
                    self._queuedTokens.append(leafTag('DEDENT',
                                                      self.getSpan(self.position,
                                                                   self.position)))
                return self._queuedTokens.pop()

        if cur == '(':
            return self.openBracket(')')

        if cur == '[':
            return self.openBracket(']')

        if cur == '{':
            return self.openBracket('}')

        if cur == '}':
            result = self.closeBracket()
            self.bracer.popIf('$')
            return result

        if cur == ')':
            return self.closeBracket()

        if cur == ']':
            return self.closeBracket()

        if cur == '$':
            nex = self.nextChar()
            if nex == '{':
                # quasi hole of form ${blah}
                self.nextChar()
                return self.openBracket('}', '${')
            elif isIdentifierStart(nex):
                # quasi hole of form $blee
                nex = self.nextChar()
                while isIdentifierPart(nex):
                    nex = self.nextChar()
                name, span = self.endToken()
                key = name[1:]
                if isKeyword(key):
                    self.nextChar()
                    self.syntaxError(key + "is a keyword")
                self.bracer.popIf('$')
                return composite('DOLLAR_IDENT', key, span)
            else:
                # for $$ or $0
                return leafTag('$', self.endSpan())

        if cur == '@':
            nex = self.nextChar()
            if nex == '{':
                # quasi hole of form @{blah}
                self.nextChar()
                return self.openBracket('}', '@{')
            elif nex == '_' and not isIdentifierPart(self.peekChar()):
                self.nextChar()
                name, span = self.endToken()
                self.bracer.popIf('$')
                return composite('AT_IDENT', '_', span)
            elif isIdentifierStart(nex):
                # quasi hole of form @blee
                nex = self.nextChar()
                while isIdentifierPart(nex):
                    nex = self.nextChar()
                name, span = self.endToken()
                key = name[1:]
                if isKeyword(key):
                    self.nextChar()
                    self.syntaxError(key + "is a keyword")
                self.bracer.popIf('$')
                return composite('AT_IDENT', key, span)
            else:
                # for @@ or @0
                return leafTag('@', self.endSpan())

        if cur == '.':
            nex = self.nextChar()
            if nex == '.':
                nex2 = self.nextChar()
                if nex2 == '!':
                    self.nextChar()
                    return leafTag('..!', self.endSpan())
                return leafTag('..', self.endSpan())
            return leafTag('.', self.endSpan())

        if cur == '^':
            nex = self.nextChar()
            if nex == '=':
                self.nextChar()
                return leafTag('^=', self.endSpan())
            return leafTag('^', self.endSpan())

        if cur == '+':
            nex = self.nextChar()
            if nex == '+':
                self.nextChar()
                self.syntaxError('++? lol no')
            if nex == '=':
                self.nextChar()
                return leafTag('+=', self.endSpan())
            return leafTag('+', self.endSpan())

        if cur == '-':
            nex = self.nextChar()
            if nex == '-':
                self.nextChar()
                self.syntaxError('--? lol no')
            if nex == '=':
                self.nextChar()
                return leafTag('-=', self.endSpan())
            if nex == '>':
                self.nextChar()
                if  all(c in ' \n' for c in self._currentLine[self.position:]):
                    # this is an arrow ending a line, and should be
                    # followed by an indent
                    self._canStartIndentedBlock = True
                return leafTag('->', self.endSpan())
            return leafTag('-', self.endSpan())

        if cur == ':':
            nex = self.nextChar()
            if nex == ':':
                self.nextChar()
                return leafTag('::', self.endSpan())
            if nex == '=':
                self.nextChar()
                return leafTag(':=', self.endSpan())
            if  all(c in ' \n' for c in self._currentLine[self.position:]):
                # this is a colon ending a line, and should be
                # followed by an indent
                self._canStartIndentedBlock = True
            return leafTag(':', self.endSpan())

        if cur == '<':
            nex = self.nextChar()
            if nex == '-':
                nex2 = self.nextChar()
                if nex2 == '*':
                    self.nextChar()
                    self.syntaxError('<-* is reserved')
                return leafTag('<-', self.endSpan())

            elif nex == '=':
                nex2 = self.nextChar()
                if nex2 == '>':
                    self.nextChar()
                    return leafTag('<=>', self.endSpan())
                return leafTag('<=', self.endSpan())
            elif nex == '<':
                nex2 = self.nextChar()
                if nex2 == '=':
                    self.nextChar()
                    return leafTag('<<=', self.endSpan())
                return leafTag('<<', self.endSpan())
            elif isIdentifierStart(nex):
                res = self.uri()
                if res is not None:
                    return res
            return leafTag(cur, self.endSpan())

        if cur == '>':
            nex = self.nextChar()
            if nex == '=':
                self.nextChar()
                return leafTag('>=', self.endSpan())
            if nex == '>':
                nex2 = self.nextChar()
                if nex2 == '=':
                    self.nextChar()
                    return leafTag('>>=', self.endSpan())
                return leafTag('>>', self.endSpan())
            return leafTag('>', self.endSpan())

        if cur == '*':
            nex = self.nextChar()
            if nex == '*':
                nex2 = self.nextChar()
                if nex2 == '=':
                    self.nextChar()
                    return leafTag('**=', self.endSpan())
                return leafTag('**', self.endSpan())
            elif nex == '=':
                self.nextChar()
                return leafTag('*=', self.endSpan())
            elif nex == '-' and self.peekChar() == '>':
                self.nextChar()
                self.nextChar()
                self.syntaxError("*-> is reserved")

            elif nex == '/':
                self.nextChar()
                self.syntaxError("/*..*/ comments are reserved. Use '#' on each line instead")
            return leafTag('*', self.endSpan())

        if cur == '/':
            nex = self.nextChar()
            if nex == '/':
                nex2 = self.nextChar()
                if nex2 == '=':
                    self.nextChar()
                    return leafTag('//=', self.endSpan())
                return leafTag('//', self.endSpan())
            elif nex == '=':
                self.nextChar()
                return leafTag('/=', self.endSpan())
            elif nex == '*':
                nex2 = self.nextChar
                if nex == '*':
                    self.nextChar()
                    self.nextChar()
                    return self.docComment()
                self.syntaxError("/*..*/ comments are reserved. Use '#' on "
                                 "each line instead")
            return leafTag('/', self.endSpan())

        if cur == '#':
            self.skipLine()
            self._delayedNextChar = False
            comment, span = self.endToken()
            return composite('#', comment[1:], span)

        if cur == '%':
            nex = self.nextChar()
            if nex == '=':
                self.nextChar()
                return leafTag('%=', self.endSpan())
            return leafTag('%', self.endSpan())

        if cur == '!':
            nex = self.nextChar()
            if nex == '=':
                self.nextChar()
                return leafTag('!=', self.endSpan())
            elif nex == '~':
                self.nextChar()
                return leafTag('!~', self.endSpan())
            return leafTag('!', self.endSpan())

        if cur == '=':
            nex = self.nextChar()
            if nex == '=':
                self.nextChar()
                return leafTag('==', self.endSpan())
            if nex == '>':
                self.nextChar()
                return leafTag('=>', self.endSpan())
            elif nex == '~':
                self.nextChar()
                return leafTag('=~', self.endSpan())
            self.syntaxError("use := for assignment or == for equality")

        if cur == '!':
            nex = self.nextChar()
            if nex == '=':
                self.nextChar()
                return leafTag('!=', self.endSpan())
            elif nex == '~':
                self.nextChar()
                return leafTag('!~', self.endSpan())
            return leafTag('!', self.endSpan())

        if cur == '&':
            nex = self.nextChar()
            if nex == '&':
                self.nextChar()
                return leafTag('&&', self.endSpan())
            elif nex == '=':
                self.nextChar()
                return leafTag('&=', self.endSpan())
            elif nex == '!':
                self.nextChar()
                return leafTag('&!', self.endSpan())
            return leafTag('&', self.endSpan())

        if cur == '|':
            nex = self.nextChar()
            if nex == '|':
                self.nextChar()
                return leafTag('||', self.endSpan())
            elif nex == '=':
                self.nextChar()
                return leafTag('|=', self.endSpan())
            return leafTag('|', self.endSpan())

        if cur == '\'':
            return self.charLiteral()

        if cur == '"':
            return self.stringLiteral()

        if cur == '`':
            self.nextChar()
            opener = self.getSpan(self._startPos, self.position,
                                  "File ends inside quasiliteral")
            self.bracer.push(opener, '`', 0)
            return self.quasiPart()

        if cur in string.digits:
            return self.numberLiteral()

        if cur == '_':
            if isIdentifierPart(self.peekChar()):
                return self.identifier()
            self.nextChar()
            return leafTag(cur, self.endSpan())

        if cur == '\t':
            self.syntaxError("Tab characters are not permitted in Monte source")

        if isIdentifierStart(cur):
            return self.identifier()
        else:
            self.syntaxError("unrecognized character %r" % (cur,))

    def identifier(self):
        """
        Recognize an identifier and create a token for it.
        """
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
            return composite(token.lower(), token.lower(), span)
        else:
            return composite('IDENTIFIER', token, span)

    def charConstant(self):
        """
        Parse character escape syntax.
        """
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
        elif self.currentChar == '\t':
            self.syntaxError('Quoted tabs must be written as \\t.')
        else:
            c = self.currentChar
            self.nextChar()
            return c

    def charLiteral(self):
        """
        Recognize a character literal and create a token for it.
        """
        self.nextChar()
        c = self.charConstant()
        while c is None:
            c = self.charConstant()
        if self.currentChar != "'":
            self.syntaxError('char constant must end in "\'"')
        self.nextChar()
        return composite('.char.', c, self.endSpan())

    def stringLiteral(self):
        """
        Recognize a string literal and create a token for it.
        """
        self.nextChar()
        self.bracer.push(self.getSpan(self._startPos, self.position,
                                        "file ends inside string literal"),
                         '"', 0)
        buf = []
        while self.currentChar != '"':
            if self.isEndOfFile():
                self.syntaxError("File ends inside string literal")
            cc = self.charConstant()
            if cc is not None:
                buf.append(cc)
        self.nextChar()
        closer = self.endToken()
        self.bracer.pop(self, '"', closer)
        return composite('.String.', ''.join(buf), closer[1])

    def numberLiteral(self):
        """
        Recognize a numeric literal and create a token for it.
        """
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

    def quasiPart(self):
        buf = []
        while True:
            while self.currentChar not in '`@$':
                if self.isEndOfFile():
                    self.syntaxError("File ends inside quasiliteral")
                buf.append(self.currentChar)
                self.nextChar()
            if self.peekChar() == self.currentChar:
                buf.append(self.currentChar)
                if self.currentChar == '$@':
                    buf.append(self.currentChar)
                self.nextChar()
                self.nextChar()
            elif self.currentChar == '`':
                self.nextChar()
                closer = self.endToken()
                self.bracer.pop(self, '`', closer)
                return composite('QUASI_CLOSE', ''.join(buf), closer[1])
            elif self.peekChar() == '`':
                buf.append(self.currentChar())
                self.nextChar()
            elif self.currentChar == '$' and self.peekChar() == '\\':
                self.nextChar()
                cc = self.charConstant()
                if cc is not None:
                    buf.append(cc)
            else:
                opener = self.endToken()
                self.bracer.nestLevel += 1
                self.bracer.push(opener, '$', self.bracer.nestLevel * 4, True)
                if not buf:
                    result = self.getNextToken()
                    if result is EOF:
                        self.syntaxError("file ends in quasiliteral")
                    else:
                        return result
                else:
                    return composite('QUASI_OPEN', ''.join(buf), opener[1])

    def digits(self, radix):
        """
        Get the set of digits valid for the given base.
        """
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
        """
        Recognize a URI literal and create a token for it.
        """
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
            self.syntaxError("Can't use %r in a URI body" %
                             (self.currentChar,))
        self.nextChar()
        source, span = self.endToken()
        return composite('URI', source[1:-1], span)

    def docComment(self):
        """
        Recognize a docstring and create a token for it.
        """
        opener = self.getSpan(self._startPos, self.position,
                              "File ends inside doc-comment")
        self.bracer.push(opener, '*', self.position - 2)
        buf = []
        while '*/' not in self._currentLine:
            buf.append(self._currentLine[self.position:])
            self.skipLine()
            self.nextChar()
            if self.isEndOfFile():
                self.syntaxError("File ends inside doc-comment")
            self.skipWhiteSpace()
            if self.currentChar == '*' and self.peekChar() != '/':
                self.nextChar()
        bound = self._currentLine.find('*/', self.position)
        buf.append(self._currentLine[self.position:bound])
        self.position = bound
        self.nextChar()
        self.nextChar()
        closer = self.endToken()
        self.bracer.pop(self, '*', closer)
        return composite('DOC_COMMENT', ''.join(buf), closer[1])


def makeTokenStream(text, origin="<string>"):
    lexer = MonteLexer(StringFeeder(text, origin))
    toks = [tok for tok in lexer if tok.tag.name != '#'
            and tok.tag.name != 'UPDOC']
    return InputStream.fromIterable(toks)
