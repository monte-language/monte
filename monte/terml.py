# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from pymeta.runtime import character
from monte.grammar import PortableOMeta
from monte.baseparser import CommonParser
termLGrammar = r"""
literal ::= (<string>:x => TermLiteral(".String.", x)
            | <character>:x => TermLiteral(".char.", x)
            | <number>:x => TermLiteral(numberType(x), x))

tag ::= (<segment>:seg1 (':' ':' <sos>)*:segs => Tag(cons(seg1, segs))
        | (':' ':' <sos>)+:segs => prefixedTag(segs))

sos ::= <segment> | (<string>:s => tagString(s))

segment ::= <ident> | <special> | <uri>

ident ::= <segStart>:i1 <segPart>*:ibits => join(cons(i1, ibits))

segStart ::= <letter> | '_' | '$'

segPart ::= <letterOrDigit> | '_' | '.' | '-' | '$'

special ::= '.':a <ident>:b => concat(a, b)

uri ::= '<' <uriBody>*:uriChars '>' => concat(b, uriChars, e)

functor ::= <spaces> (<literal> | <tag>:t <functorHole>:h => taggedHole(t, h) | <tag> | <functorHole>)

functorHole ::= ((<token "${"> <decdigits>:n '}' => ValueHole(n))
                |(<token "$"> <decdigits>:n  => ValueHole(n))
                |(<token "$"> <tag>:t => NamedValueHole(t))
                |(<token "@{"> <decdigits>:n '}' => PatternHole(n))
                |(<token "@"> <decdigits>:n  => PatternHole(n))
                |(<token "@"> <tag>:t => NamedPatternHole(t)))

baseTerm ::= <functor>:f ('(' <argList>:a ')' => Term(f, a)
                     | => Term(f, emptyList()))

argList ::= ((<term>:t (',' <term>)*:ts ) => cons(t, ts)
            | => emptyList())

tupleTerm ::= <token '['> <argList>:a <token ']'> => Tuple(a)

bagTerm ::= <token '{'> <argList>:a <token '}'> => Bag(a)

labelledBagTerm ::= <functor>:f <bagTerm>:b => LabelledBag(f, b)

extraTerm ::= <tupleTerm> | <labelledBagTerm>  | <bagTerm> | <baseTerm>

attrTerm ::= <extraTerm>:k <token ':'> <extraTerm>:v => Attr(k, v)

term ::=  <attrTerm> | <extraTerm>

"""

class _Term(object):

    def __init__(self, functor, arglist):
        self.functor = functor
        self.arglist = arglist
        assert len(arglist) >= 0


    def __eq__(self, other):
        return (self.functor, self.arglist) == (other.functor, other.arglist)


    def __repr__(self):
        return "Term(%r)" % (self._unparse())


    def _unparse(self):
        if len(self.arglist) == 0:
            return self.functor._unparse()
        args = ', '.join([a._unparse() for a in self.arglist])
        if self.functor.name == '.tuple.':
            return "[%s]" % (args,)
        elif self.functor.name == '.attr.':
            return "%s: %s" % (self.arglist[0]._unparse(), self.arglist[1]._unparse())
        elif self.functor.name == '.bag.':
            return "{%s}" % (args,)
        elif len(self.arglist) == 1 and self.arglist[0].functor.name == '.bag.':
            return "%s%s" % (self.functor._unparse(), args)
        else:
            return "%s(%s)" % (self.functor._unparse(), args)



class TermLiteral(object):

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __eq__(self, other):
        return other.__class__ == self.__class__ and self.data == other.data

    def __repr__(self):
        return "TermLiteral(%r)" % (self.data,)

    def _unparse(self):
        if self.name == '.String.':
            return '"%s"' % self.data
        elif self.name == '.char.':
            return "'%s'" % self.data
        else:
            return str(self.data)



class Tag(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return other.__class__ == self.__class__ and self.name == other.name

    def __repr__(self):
        return "Tag(%r)" % (self.name,)

    def _unparse(self):
        return self.name



BaseTermLParser = PortableOMeta.makeGrammar(termLGrammar,  globals(), "TermLParser")


class TermLParser(CommonParser, BaseTermLParser):

    def action_TermLiteral(self, name, data):
        return TermLiteral(name, data)

    def action_Character(self, char):
        return character(char)

    def action_Tag(self, nameSegs):
        return Tag('::'.join(nameSegs))

    def action_prefixedTag(self, tagnameSegs):
        return self.action_Tag([''] + tagnameSegs)

    def action_tagString(self, string):
        return '"' + string + '"'

    def action_emptyList(self):
        return []

    def action_Term(self, functor, argList):
        if isinstance(functor, TermLiteral) and len(argList) > 0:
            raise ValueError("Term %s can't have both data and children" % (functor.name,))
        return _Term(functor, argList)

    def action_numberType(self, n):
        if isinstance(n, float):
            return ".float64."
        elif isinstance(n, (long, int)):
            return ".int."
        raise ValueError("wtf")


    def action_Tuple(self, args):
        return _Term(Tag(".tuple."), args)

    def action_Bag(self, args):
        return _Term(Tag(".bag."), args)

    def action_LabelledBag(self, f, arg):
        return _Term(f, [arg])

    def action_Attr(self, k, v):
        return _Term(Tag(".attr."), [k, v])



def Term(termString):
    """
    Parser frontend for term strings.
    """
    p = TermLParser(termString)
    return p.apply("term")[0]
