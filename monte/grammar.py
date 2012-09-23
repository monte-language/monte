# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
from ometa.runtime import ParseError
from ometa.builder import TermActionPythonWriter, _Term2PythonAction
from ometa.grammar import TermOMeta, OMeta
from terml.nodes import termMaker as t


class _Term2Action(_Term2PythonAction):

    def leafTag(bldr, tag, span):
        if tag.name[0].isupper():
            return "self.termMaker." + tag.name
        elif tag.name.startswith('.'):
            return tag.name
        else:
            return "self.lookupActionName(%r, _locals)" % (tag.name,)

_builder = _Term2Action()

class PortableActionPythonWriter(TermActionPythonWriter):
    def generate_Action(self, out, term):
        return self._expr(out, "action", term.build(_builder) + ", None")


portableOMetaGrammar = r"""
bareString = token('"') (escapedChar | ~('"') anything)*:c token('"') -> ''.join(c)
string =  bareString:s -> t.Apply("tokenBR", self.name, [s])
"""

class PortableOMeta(OMeta.makeGrammar(
        portableOMetaGrammar, globals(),
        name='PortableOMeta', superclass=TermOMeta)):
    _writer = PortableActionPythonWriter

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
