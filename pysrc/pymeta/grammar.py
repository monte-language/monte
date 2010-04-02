# -*- test-case-name: pymeta.test.test_pymeta -*-
"""
Public interface to OMeta, as well as the grammars used to compile grammar
definitions.
"""
import string
from builder import TreeBuilder, moduleFromGrammar
from boot import BootOMetaGrammar
from runtime import OMetaBase, ParseError, EOFError, expected

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
        tree = g.parseGrammar(name, TreeBuilder)
        return moduleFromGrammar(tree, name, cls, globals)

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

bareString ::= <token '"'> (<escapedChar> | ~('"') <anything>)*:c <token '"'> => ''.join(c)
string ::= <bareString>:s => self.builder.exactly(s)

name ::= <letter>:x <letterOrDigit>*:xs !(xs.insert(0, x)) => ''.join(xs)

application ::= (<token '<'> <spaces> <name>:name
                  (<applicationArgs>:args
                     => self.builder.apply(name, self.name, *args)
                  |<token '>'>
                     => self.builder.apply(name, self.name)))
applicationArgs ::= <spaces> => self.applicationArgs()

expr1 ::= (<application>
          |<ruleValue>
          |<semanticPredicate>
          |<semanticAction>
          |(<number> | <character>):lit => self.builder.exactly(lit)
          |<string>
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
           => self.builder.bind(self.builder.apply("anything", self.name), n))

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
          (<rulePart n>+:rs => self.builder.rule(n, self.builder._or([r] + rs))
          |                     => self.builder.rule(n, r)))

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
        res, err = self.apply("grammar")
        try:
            x = self.input.head()
        except EOFError:
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
    def applicationArgs(self):
        """
        Collect rule arguments, a list of Python expressions separated by
        spaces.
        """
        args = []
        while True:
            try:
                (arg, endchar), err = self.pythonExpr(" >")
                if not arg:
                    break
                args.append(self.builder.expr(arg))
                if endchar == '>':
                    break
            except ParseError:
                break
        if args:
            return args
        else:
            raise ParseError(self.input.position, expected("Application args"))

    def ruleValueExpr(self):
        """
        Find and generate code for a Python expression terminated by a close
        paren/brace or end of line.
        """
        (expr, endchar), err = self.pythonExpr(endChars="\r\n)]")
        if str(endchar) in ")]":
            self.input = self.input.prev()
        return self.builder.expr(expr)

    def semanticActionExpr(self):
        """
        Find and generate code for a Python expression terminated by a
        close-paren, whose return value is ignored.
        """
        return self.builder.action(self.pythonExpr(')')[0][0])

    def semanticPredicateExpr(self):
        """
        Find and generate code for a Python expression terminated by a
        close-paren, whose return value determines the success of the pattern
        it's in.
        """
        expr = self.builder.expr(self.pythonExpr(')')[0][0])
        return self.builder.pred(expr)

OMeta.metagrammarClass = OMetaGrammar

nullOptimizationGrammar = """

opt ::= ( ["Apply" :ruleName :codeName [<anything>*:exprs]] => self.builder.apply(ruleName, codeName, *exprs)
        | ["Exactly" :expr] => self.builder.exactly(expr)
        | ["Many" <opt>:expr] => self.builder.many(expr)
        | ["Many1" <opt>:expr] => self.builder.many1(expr)
        | ["Optional" <opt>:expr] => self.builder.optional(expr)
        | ["Or" [<opt>*:exprs]] => self.builder._or(exprs)
        | ["And" [<opt>*:exprs]] => self.builder.sequence(exprs)
        | ["Not" <opt>:expr]  => self.builder._not(expr)
        | ["Lookahead" <opt>:expr] => self.builder.lookahead(expr)
        | ["Bind" :name <opt>:expr] => self.builder.bind(expr, name)
        | ["Predicate" <opt>:expr] => self.builder.pred(expr)
        | ["Action" :code] => self.builder.action(code)
        | ["Python" :code] => self.builder.expr(code)
        | ["List" <opt>:exprs] => self.builder.listpattern(exprs)
        )
grammar ::= ["Grammar" :name [<rulePair>*:rs]] => self.builder.makeGrammar(rs)
rulePair ::= ["Rule" :name <opt>:rule] => self.builder.rule(name, rule)

"""

NullOptimizer = OMeta.makeGrammar(nullOptimizationGrammar, {}, name="NullOptimizer")

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
actionLiteral ::=  (<number> | <character> | <bareString>):lit => ActionLiteral(lit)

ruleValue ::= <token "=>"> <action>:a => self.result(a)
semanticPredicate ::= <token "?("> <action>:a <token ")"> => self.predicate(a)
semanticAction ::= <token "!("> <action>:a <token ")"> => self.action(a)
applicationArgs ::= (<spaces> <action>)+:args <token ">"> => [self.result(a) for a in args]
string ::= <bareString>:s => self.builder.apply("tokenBR", self.name, self.action(ActionLiteral(s)))
"""


_PortableActionGrammar = _PythonActionGrammar.makeGrammar(portableOMetaGrammar,
                                                          globals(), "PortableOMeta")

class PortableOMetaGrammar(GrammarInterfaceMixin, _PortableActionGrammar):
    """
    An OMeta variant with portable syntax for actions.
    """

    def result(self, action):
        return self.builder.compilePortableAction(action)


    def predicate(self, action):
        return self.builder.pred(self.builder.compilePortableAction(action))


    def action(self, action):
        return self.builder.compilePortableAction(action)




OMeta.metagrammarClass = OMetaGrammar

class PortableOMeta(OMeta):
    metagrammarClass = PortableOMetaGrammar

    def rule_tokenBR(self):
        """
        Match and return the given string, consuming any preceding or trailing
        whitespace.
        """
        tok = self.input.head()

        m = self.input = self.input.tail()
        try:
            self.eatWhitespace()
            for c in tok:
                self.exactly(c)
            self.apply("br")
            return tok
        except ParseError:
            self.input = m
            raise
