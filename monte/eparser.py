# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
import string

from parsley import ParseError
from ometa.grammar import loadGrammar
from terml.nodes import termMaker as t

import monte



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
    
    def rule_tokenBR(self):
        """
        Match and return the given string, consuming any preceding or trailing
        whitespace.
        """
        tok, _ = self.input.head()

        m = self.input = self.input.tail()
        try:
            self.eatWhitespace()
            for c  in tok:
                self.exactly(c)
            _, e = self.apply("br")
            return tok, e
        except ParseError:
            self.input = m
            raise


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

    def valueHole(self):
        """
        Look up a value hole in the table and return its position.
        """
        try:
            return self.valueHoles.index(self.input.position - 1)
        except ValueError:
            raise ValueError("A literal $ is not meaningful in E source.")

    def patternHole(self):
        """
        Look up a pattern hole in the table and return its position.
        """
        try:
            return self.patternHoles.index(self.input.position - 1)
        except ValueError:
            raise ValueError("A literal @ is not meaningful in E source.")

EParser.globals = {}
EParser.globals.update(globals())

