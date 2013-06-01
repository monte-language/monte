# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
import string

from parsley import ParseError
from ometa.grammar import loadGrammar
from ometa.runtime import expected
from terml.nodes import termMaker as t

import monte
from monte.lexer import reserved, basicKeywords, keywords, makeTokenStream


def quasiHoleKeywordCheck(n):
    if n in keywords:
        raise ValueError("Unexpected keyword %r in quasi hole" % (n,))
    else:
        return None

def exprHoleKeywordCheck(n):
    if n in keywords:
        raise ValueError("Unexpected keyword %r in quasi hole" % (n,))
    else:
        return None

def throwSemanticHere(arg):
    """
    Raise an error when invalid source is parsed.
    """
    raise ValueError(arg)

def noIgnorePatternHole():
    raise RuntimeError()

def noIgnoreExpressionHole():
    raise RuntimeError()


BaseEParser = loadGrammar(monte, "eparser", globals())

class EParser(BaseEParser):
    """
    A parser for E.
    """

    def rule_tok(self, tok):
        """
        Match a single token from the token stream.
        """
        candidate, e = self.input.head()
        if candidate.tag.name != tok:
            raise self.input.nullError(expected("token", tok))
        self.input = self.input.tail()
        return candidate.data, e

    def rule_ws(self):
        #lexer already did it
        return None, None

    def rule_token(self):
        """
        Handle double-quoted tokens, matching 'br' after then the token.
        """
        token, _ = self.input.head()
        self.input = self.input.tail()
        x = self.rule_tok(token)
        self.apply('br')
        return x

    rule_exactly = rule_tok
    exactly = rule_tok

    def keywordCheck(self, ident):
        """
        Ensure an identifier isn't a keyword or reserved word.
        """
        if ident in reserved:
            raise ParseError(self.input, self.input.position, ident + " is a reserved word")
        elif ident in basicKeywords:
            raise ParseError(self.input, self.input.position, ident + " is a keyword")
        else:
            return ident

    def valueHole(self, d):
        """
        Look up a value hole in the table and return its position.
        """
        try:
            return self.valueHoles[d]
        except ValueError:
            raise ValueError("A literal $ is not meaningful in E source.")

    def patternHole(self, a):
        """
        Look up a pattern hole in the table and return its position.
        """
        try:
            return self.patternHoles[a]
        except ValueError:
            raise ValueError("A literal @ is not meaningful in E source.")

EParser.globals = {}
EParser.globals.update(globals())

def makeParser(source, origin="<string>"):
    stream = makeTokenStream(source, origin)
    return EParser(stream, stream=True)

def parse(source, origin="<string>"):
    from parsley import _GrammarWrapper
    return _GrammarWrapper(makeParser(source, origin), source).start()
