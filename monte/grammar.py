# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
from ometa.runtime import ParseError
from ometa.grammar import OMeta


monteOMetaGrammar = r"""
bareString = token('"') (escapedChar | ~('"') anything)*:c token('"') -> ''.join(c)
string =  bareString:s -> t.Apply("tokenBR", self.name, [t.Action(repr(s))])
"""

class MonteOMeta(OMeta.makeGrammar(
        monteOMetaGrammar, globals(),
        name='MonteOMeta',
        superclass=OMeta)):

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
