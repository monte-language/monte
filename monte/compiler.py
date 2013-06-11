import re, string
from keyword import iskeyword

from StringIO import StringIO
from monte.eparser import parse
from monte.expander import expand, scope

class TextWriter(object):

    stepSize = 4
    midLine = False

    def __init__(self, f, indentSteps=0):
        self.file = f
        self.indentSteps = indentSteps

    def write(self, data):
        if data and not data.isspace():
            if not self.midLine:
                self.file.write(" " * (self.indentSteps * self.stepSize))
            self.file.write(data)

    def writeln(self, data):
        self.write(data)
        self.file.write("\n")
        self.midLine = False

    def indent(self):
        return TextWriter(self.file, self.indentSteps + 1)

mtrans = string.maketrans(string.printable[62:], '_' * 38)

def mangleNoun(n):
    prefix = '_m_'
    if re.match('[a-zA-Z_]\\w*$', n):
        if iskeyword(n) or n.startswith(prefix):
            return prefix + n
        else:
            return n
    return prefix + n.translate(mtrans)

class PythonWriter(object):
    """
    Converts an E syntax tree into Python source.
    """

    def __init__(self, tree):
        self.tree = tree

    def output(self, out):
        return self._generate(out, None, self.tree)

    def _generate(self, out, ctx, node):
        name = node.tag.name
        args = node.args
        if name == 'null':
            return 'None'
        return getattr(self, "generate_"+name)(out, ctx, *args)

    def generate_LiteralExpr(self, out, ctx, litNode):
        if litNode.tag.name == 'Character':
            return "_monte.Character(%r)" % (litNode.args[0].data)
        lit = litNode.data
        if isinstance(lit, basestring):
            #either already unicode, or ascii bytes
            return repr(unicode(lit))
        return repr(lit)

    def generate_NounExpr(self, out, ctx, noun):
        name = noun.data
        if ctx is None:
            # at toplevel.
            return mangleNoun(name)

    def generate_Object(self, out, ctx, doc, name, script):
        #TODO replace this gubbish with proper destructuring
        doc = doc.data
        name = name.args[0].args[0].data
        extends = script.args[0]
        guard = script.args[1]
        implements = script.args[2].args
        methods = script.args[3].args
        matchers = script.args[4].args
        objname = mangleNoun(name)
        scriptname = "_m_%s_Script" % (objname,)
        out.writeln("class %s(_monte.MonteObject):" % (scriptname,))
        classOut = out.indent()
        if doc:
            classOut.writeln('"""')
            for ln in doc.splitlines():
                classOut.writeln(ln)
            classOut.writeln('"""')
        methOut = classOut.indent()
        for meth in methods:
            mdoc = meth.args[0].data
            verb = meth.args[1].data
            params = meth.args[2].args
            methGuard = meth.args[3]
            body = meth.args[4]
            genParams = [self._generate(out, ctx, p) for p in params]
            classOut.writeln("def %s(self, %s):" % (mangleNoun(verb),
                                              ', '.join(genParams)))
            if mdoc:
                methOut.writeln('"""')
                for ln in mdoc.splitlines():
                    methOut.writeln(ln)
                methOut.writeln('"""')
            methOut.writeln("return " + self._generate(methOut, ctx, body))
        out.writeln("%s = %s()" % (objname, scriptname))

    def generate_FinalPattern(self, out, ctx, name, guard):
        if guard.tag.name != 'null':
            raise NotImplementedError()
        return mangleNoun(name.args[0].data)

    def generate_SeqExpr(self, out, ctx, seqs):
        exprs = seqs.args
        if ctx is None:
            # at toplevel.
            for e in exprs:
                # innerctx = ctx.forFxOnly()
                v = self._generate(out, ctx, e)
                if v is not None:
                    out.writeln(v)

def ecompile(source, origin="<string>"):
    ast = expand(parse(source))
    f = StringIO()
    PythonWriter(ast).output(TextWriter(f))
    return f.getvalue().strip()














