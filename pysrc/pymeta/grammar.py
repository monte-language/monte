"""
Public interface to OMeta, as well as the grammars used to compile grammar
definitions.
"""
import sys, string
from builder import PythonBuilder
from boot import BootOMetaGrammar
from runtime import OMetaBase, ParseError

class OMeta(OMetaBase):
    """
    Base class for grammar definitions.
    """
    metagrammarClass = BootOMetaGrammar
    def makeGrammar(cls, grammar, globals, name="Grammar"):
        """
        Define a new subclass with the rules in the given grammar.

        @param grammar: A string containing a PyMeta grammar.
        @param globals: A dict of names that should be accessible by this
        grammar.
        @param name: The name of the class to be generated.
        """
        g = cls.metagrammarClass(grammar)
        return g.parseGrammar(name, PythonBuilder, cls, globals)
    makeGrammar = classmethod(makeGrammar)

ometaGrammar = r"""
number ::= <spaces> ('-' <barenumber>:x => -x
                    |<barenumber>:x => x)
barenumber ::= ('0' (('x'|'X') <hexdigit>*:hs => int(''.join(hs), 16)
                    |<octaldigit>*:ds => int('0'+''.join(ds), 8))
               |<digit>+:ds => int(''.join(ds)))
octaldigit ::= :x ?(x in string.octdigits) => x
hexdigit ::= :x ?(x in string.hexdigits) => x

escapedChar ::= '\\' ('n' => "\n"
                     |'r' => "\r"
                     |'t' => "\t"
                     |'b' => "\b"
                     |'f' => "\f"
                     |'"' => '"'
                     |'\'' => "'"
                     |'\\' => "\\")

character ::= <token "'"> (<escapedChar> | <anything>):c <token "'"> => c

string ::= <token '"'> (<escapedChar> | ~('"') <anything>)*:c <token '"'> => ''.join(c)

name ::= <letter>:x <letterOrDigit>*:xs !(xs.insert(0, x)) => ''.join(xs)

application ::= (<token '<'> <spaces> <name>:name
                  (<applicationArgs>:args
                     => self.builder.apply(name, self.name, args)
                  |<token '>'>
                     => self.builder.apply(name, self.name, [])))
applicationArgs ::= <spaces> => self.applicationArgs(self.name)

expr1 ::= (<application>
          |<ruleValue>
          |<semanticPredicate>
          |<semanticAction>
          |(<number> | <character> | <string>):lit => self.builder.exactly(lit)
          |<token '('> <expr>:e <token ')'> => e
          |<token '['> <expr>:e <token ']'> => self.builder.listpattern(e))

expr2 ::= (<token '~'> (<token '~'> <expr2>:e => self.builder.lookahead(e)
                       |<expr2>:e => self.builder._not(e))
          |<expr1>)

expr3 ::= ((<expr2>:e ('*' => self.builder.many(e)
                      |'+' => self.builder.many1(e)
                      |'?' => self.builder.optional(e)
                      | => e)):r
           (':' <name>:n => self.builder.bind(r, n)
           | => r)
          |<token ':'> <name>:n
           => self.builder.bind(self.builder.apply("anything", self.name, []), n))

expr4 ::= <expr3>*:es => self.builder.sequence(es)

expr ::= <expr4>:e (<token '|'> <expr4>)*:es !(es.insert(0, e))
          => self.builder._or(es)

ruleValue ::= <token "=>"> => self.ruleValueExpr()

semanticPredicate ::= <token "?("> => self.semanticPredicateExpr()

semanticAction ::= <token "!("> => self.semanticActionExpr()

rulePart :requiredName ::= (<spaces> <name>:n ?(n == requiredName)
                            !(setattr(self, "name", n))
                            <expr4>:args
                            (<token "::="> <expr>:e
                               => self.builder.sequence([args, e])
                            |  => args))
rule ::= (<spaces> ~~(<name>:n) <rulePart n>:r
          (<rulePart n>+:rs => (n, self.builder._or([r] + rs))
          |                     => (n, r)))

grammar ::= <rule>*:rs <spaces> => self.builder.makeGrammar(rs)
"""
#don't be confused, emacs

class GrammarInterfaceMixin(object):
    """
    Interface bits common to various OMeta permutations.
    """
    def parseGrammar(self, name, builder, *args):
        """
        Entry point for converting a grammar to code (of some variety).

        @param name: The name for this grammar.

        @param builder: A class that implements the grammar-building interface
        (interface to be explicitly defined later)
        """
        self.builder = builder(name, self, *args)
        res = self.apply("grammar")
        try:
            x = self.input.head()
        except IndexError:
            pass
        else:
            x = repr(''.join(self.input.data[self.input.position:]))
            raise ParseError("Grammar parse failed. Leftover bits: %s" % (x,))
        return res



_PythonActionGrammar = OMeta.makeGrammar(ometaGrammar, globals())

class OMetaGrammar(GrammarInterfaceMixin,
                   _PythonActionGrammar):
    """
    The base grammar for parsing grammar definitions.
    """

    def applicationArgs(self, codeName):
        """
        Collect rule arguments, a list of Python expressions separated by
        spaces.
        """
        args = []
        while True:
            try:
                arg, endchar = self.pythonExpr(" >")
                if not arg:
                    break
                args.append(arg)
                if endchar == '>':
                    break
            except ParseError:
                break
        if args:
            return [[self.builder.compilePythonExpr(self.name, arg)] for arg in args]
        else:
            raise ParseError()

    def ruleValueExpr(self):
        """
        Find and generate code for a Python expression terminated by a close
        paren/brace or end of line.
        """
        expr, endchar = self.pythonExpr(endChars="\r\n)]")
        if str(endchar) in ")]":
            self.input = self.input.prev()
        return self.builder.action(self.builder.compilePythonExpr(self.name, expr))

    def semanticActionExpr(self):
        """
        Find and generate code for a Python expression terminated by a
        close-paren, whose return value is ignored.
        """
        expr = self.builder.compilePythonExpr(self.name, self.pythonExpr(')')[0])
        return self.builder.action(expr)

    def semanticPredicateExpr(self):
        """
        Find and generate code for a Python expression terminated by a
        close-paren, whose return value determines the success of the pattern
        it's in.
        """
        expr = self.builder.compilePythonExpr(self.name, self.pythonExpr(')')[0])
        return self.builder.pred(self.builder.action(expr))

class ActionNoun(object):
    """
    A noun in a portable OMeta grammar action.
    """
    def __init__(self, name):
        self.name = name


    def visit(self, visitor):
        return visitor.name(self.name)

class ActionCall(object):
    """
    A call action in a portable OMeta grammar.
    """
    def __init__(self, verb, args):
        self.verb = verb
        self.args = args or []


    def visit(self, visitor):
        return visitor.call(self.verb.visit(visitor),
                            [arg.visit(visitor) for arg in self.args])


class ActionLiteral(object):
    """
    A literal value in a portable OMeta action.
    """
    def __init__(self, value):
        self.value = value

    def visit(self, visitor):
        return visitor.literal(self.value)



portableOMetaGrammar = """
action ::= <spaces> (<actionCall> | <actionNoun> | <actionLiteral>)
actionCall ::= <actionNoun>:verb <token "("> <actionArgs>?:args <token ")"> => ActionCall(verb, args)
actionArgs ::= <action>:a (<token ','> <action>)*:b => [a] + b
actionNoun ::= <name>:n => ActionNoun(n)
actionLiteral ::=  (<number> | <character> | <string>):lit => ActionLiteral(lit)

ruleValue ::= <token "=>"> <action>:a => self.result(a)
semanticPredicate ::= <token "?("> <action>:a <token ")"> => self.predicate(a)
semanticAction ::= <token "!("> <action>:a <token ")"> => self.action(a)
applicationArgs ::= (<spaces> <action>)+:args <token ">"> => [self.result(a) for a in args]
"""


_PortableActionGrammar = _PythonActionGrammar.makeGrammar(portableOMetaGrammar,
                                                          globals(), "PortableOMeta")

class PortableOMeta(GrammarInterfaceMixin, _PortableActionGrammar):
    """
    An OMeta variant with portable syntax for actions.
    """

    def result(self, action):
        return self.builder.compilePortableAction(action)


    def predicate(self, action):
        return self.builder.pred(self.builder.compilePortableAction(action))


    def action(self, action):
        return self.builder.compilePortableAction(action)[:-1] + ["None"]


OMeta.metagrammarClass = OMetaGrammar
