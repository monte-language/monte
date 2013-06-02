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

OPERATORS = {
    '**': (1, t.Pow),
    '*': (2, t.Multiply),
    '/': (2, t.Divide),
    '//': (2, t.FloorDivide),
    '%': (2, t.Remainder),
    '%%': (2, t.Mod),
    '+': (3, t.Add),
    '-': (3, t.Subtract),
    '<<': (4, t.ShiftLeft),
    '>>': (4, t.ShiftRight),
    '..': (5, t.Thru),
    '..!': (5, t.Till),
    '>': (6, t.GreaterThan),
    '<': (6, t.LessThan),
    '>=': (6, t.GreaterThanEqual),
    '<=': (6, t.LessThanEqual),
    '<=>': (6, t.AsBigAs),
    '=~': (7, t.MatchBind),
    '!~': (7, t.Mismatch),
    '==': (7, t.Same),
    '!=': (7, t.NotSame),
    '&!': (7, t.ButNot),
    '^': (7, t.BinaryXor),
    '&': (8, t.BinaryAnd),
    '|': (8, t.BinaryOr),
    '&&': (9, t.LogicalAnd),
    '||': (10, t.LogicalOr)
}

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

    def rule_infix(self):
        return self.convertInfix(10)

    def rule_logical(self):
        return self.convertInfix(8)

    def rule_order(self):
        return self.convertInfix(6)

    def convertInfix(self, maxPrec):
        leftAssociative = set(['+', '-', '>>', '<<', '/', '*', '//', '%', '%%'])
        selfAssociative = set(['|', '&'])
        lhs, err = self.rule_prefix()
        output = [lhs]
        opstack = []
        while True:
            opTok, _ = self.input.head()
            op = opTok.tag.name
            if op not in OPERATORS:
                break
            nextPrec = OPERATORS[op][0]
            if nextPrec > maxPrec:
                break
            self.input = self.input.tail()
            self.rule_br()
            if opstack and (opstack[-1][0] < nextPrec
                         or op in leftAssociative and
                            opstack[-1][0] <= nextPrec
                         or op in selfAssociative and opstack[-1][2] == op):
                prec, node, opname = opstack.pop()
                rhs = output.pop()
                lhs = output.pop()
                output.append(node(lhs, rhs))
            opstack.append(OPERATORS[op] + (op,))
            if op in ['=~', '!~']:
                nextTok, err = self.rule_pattern()
            else:
                nextTok, err = self.rule_prefix()
            output.append(nextTok)
        while opstack:
            prec, node, opname = opstack.pop()
            rhs = output.pop()
            lhs = output.pop()
            output.append(node(lhs, rhs))
        assert len(output) == 1
        return output[0], err

    def collapseTrailers(self, base, trailers):
        node = base
        for tr in trailers:
            node = tr[0](node, *tr[1:])
        return node

EParser.globals = {}
EParser.globals.update(globals())

def makeParser(source, origin="<string>"):
    stream = makeTokenStream(source, origin)
    return EParser(stream, stream=True)

def parse(source, origin="<string>", tracefunc=None):
    from parsley import _GrammarWrapper
    p = makeParser(source, origin)
    if tracefunc:
        p._trace = tracefunc
    return _GrammarWrapper(p, source).start()
