# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
import string, sys, linecache
from types import ModuleType as module
from pymeta.runtime import ParseError
from pymeta.grammar import OMetaGrammarMixin, OMeta, OMetaGrammar
from pymeta.builder import TreeBuilder, PythonWriter, GeneratedCodeLoader
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

class PortableTreeBuilder(TreeBuilder):
    def compilePortableAction(self, action):
        return ["PortableAction", action]


class ActionVisitor:
    gensymCounter = 0

    def __init__(self, output):
        self.output = output

    def _gensym(self):
        """
        Produce a unique name for a variable in generated code.
        """
        ActionVisitor.gensymCounter += 1
        return "_A_%s" % (self.gensymCounter)

    def name(self, name):
        result = self._gensym()
        self.output.append('%s = self.lookupActionName(%r, _locals)' % (result, name))
        return result

    def call(self, verb, args):
        result = self._gensym()
        self.output.append('%s = %s(%s)' % (result, verb, ', '.join(args)))
        return result

    def literal(self, value):
        return repr(value)


class PortablePythonWriter(PythonWriter):
    def generate_PortableAction(self, action):
        """
        Generate Python code for an action expression.
        """
        av = ActionVisitor(self.lines)
        return action.visit(av)


def makePortableGrammar(grammar, bits, name):
    g = OMetaGrammar(grammar)
    tree = g.parseGrammar(name, PortableTreeBuilder)
    return moduleFromGrammar(tree, name, OMetaGrammar, bits)

def moduleFromGrammar(tree, className, superclass, globalsDict):
    pw = PortablePythonWriter(tree)
    source = pw.output()

    modname = "pymeta_grammar__" + className
    filename = "/pymeta_generated_code/" + modname + ".py"
    mod = module(modname)
    mod.__dict__.update(globalsDict)
    mod.__name__ = modname
    mod.__dict__[superclass.__name__] = superclass
    mod.__dict__["GrammarBase"] = superclass
    mod.__loader__ = GeneratedCodeLoader(source)
    code = compile(source, filename, "exec")
    eval(code, mod.__dict__)
    fullGlobals = dict(getattr(mod.__dict__[className], "globals", None) or {})
    fullGlobals.update(globalsDict)
    mod.__dict__[className].globals = fullGlobals
    sys.modules[modname] = mod
    linecache.getlines(filename, mod.__dict__)
    return mod.__dict__[className]

_PortableActionGrammar = makePortableGrammar(portableOMetaGrammar,
                                             globals(), "_PortableActionGrammar")

class PortableOMetaGrammar(_PortableActionGrammar):
    """
    An OMeta variant with portable syntax for actions.
    """

    def result(self, action):
        return self.builder.compilePortableAction(action)


    def predicate(self, action):
        return self.builder.pred(self.builder.compilePortableAction(action))


    def action(self, action):
        return self.builder.compilePortableAction(action)



class PortableOMeta(OMeta):
    metagrammarClass = PortableOMetaGrammar

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


    @classmethod
    def makeGrammar(cls, grammar, globals, name="Grammar"):
        g = cls.metagrammarClass(grammar)
        tree = g.parseGrammar(name, PortableTreeBuilder)
        return moduleFromGrammar(tree, name, cls, globals)
