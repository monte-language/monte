import os.path
from ometa.runtime import TreeTransformerBase
from ometa.grammar import TreeTransformerGrammar
from monte.lexer import isKeyword, isIdentifierPart, isIdentifierStart
from terml.nodes import Term, Tag
def isIdentifier(s):
    return isIdentifierStart(s[0]) and all(isIdentifierPart(c) for c in s[1:])

def concat(left, right):
    return Term(Tag('.tuple.'), None, left.args + right.args, None)

class PrecedenceTemplate(object):
    def __init__(self, prec, contents):
        self.prec = prec or 0
        self.contents = contents

    def __str__(self):
        parts = []
        for item in self.contents:
            if isinstance(item, basestring):
                parts.append(item)
            else:
                prec = getattr(item, 'prec', None) or 0
                if prec > self.prec:
                    parts.append("(%s)" % (item,))
                else:
                    parts.append(str(item))
        return ''.join(parts)

    def __repr__(self):
        return "<PT %s %r>" % (self.prec, self.contents)

class PrecedenceTransformer(TreeTransformerBase):
    nextPrecedence = None

    def rule_prec(self, prec):
        self.nextPrecedence = prec
        return None, self.input.nullError()

    def stringtemplate(self, template, vals):
        if self.nextPrecedence is None:
            for k, v in vals.iteritems():
                if v is None:
                    vals[k]
                if isinstance(v, PrecedenceTemplate):
                    vals[k] = str(v)
                if v and isinstance(v, list) and any(isinstance(x, PrecedenceTemplate) for x in v):
                    vals[k] = [str(x) for x in v]
            return TreeTransformerBase.stringtemplate(self, template, vals)
        output = []
        for chunk in template.args:
            if chunk.tag.name == ".String.":
                output.append(chunk.data)
            elif chunk.tag.name == "QuasiExprHole":
                v = vals[chunk.args[0].data]
                output.append(v)
            else:
                raise TypeError("didn't expect %r in string template" % chunk)

        pt = PrecedenceTemplate(self.nextPrecedence, output)
        self.nextPrecedence = None
        return pt, None


Unparser = TreeTransformerGrammar.makeGrammar(
    open(os.path.join(os.path.dirname(__file__), "unparser.parsley")).read(),
    'Unparser').createParserClass(PrecedenceTransformer, globals())












