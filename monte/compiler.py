import re, string
from keyword import iskeyword

from StringIO import StringIO
from monte.eparser import parse
from monte.expander import expand, scope

class CompileError(Exception):
    pass

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

    def delay(self):
        return DelayedTextWriter(self)

class DelayedTextWriter(object):
    """
    Sometimes you have to write things out of order.
    """
    def __init__(self, tw, indentSteps=0, lines=()):
        self.parent = tw
        self.lines = lines or []

    def writeln(self, data):
        if data:
            self.lines.append(" " * (self.indentSteps * self.parent.stepSize))
            self.lines.append(data)

    def flush(self):
        for ln in self.lines:
            self.parent.writeln(ln)

    def indent(self):
        """
        Note that this will not have to be flushed independently since it
        shares lines with this.
        """
        return DelayedTextWriter(self.parent, self.indentSteps + 1, self.lines)

    def delay(self):
        """
        Must be flushed independently of this.
        """
        return DelayedTextWriter(self)


mtrans = string.maketrans(string.printable[62:], '_' * 38)
GENSYM_PREFIX = '_g_'
def mangleNoun(n):
    prefix = '_m_'
    if re.match('[a-zA-Z_]\\w*$', n):
        if iskeyword(n) or n.startswith((prefix, GENSYM_PREFIX)):
            return prefix + n
        else:
            return n
    return prefix + n.translate(mtrans)
VALUE, CONTROL, FX_ONLY = range(3)

class SymGenerator(object):
    def __init__(self):
        self.gensymCounter = 0

    def gensym(self, base):
        self.gensymCounter += 1
        return GENSYM_PREFIX + base + str(self.gensymCounter)


class CompilationContext(object):
    def __init__(self, parent, mode=None):
        if mode is None:
            self.mode = getattr(parent, 'mode', VALUE)
        else:
            self.mode = mode
        self.sg = getattr(parent, 'sg', SymGenerator())

    def with_(self, **kwargs):
        return CompilationContext(self, **kwargs)

    def gensym(self, base):
        return self.sg.gensym(base)


class PythonWriter(object):
    """
    Converts an E syntax tree into Python source.
    """

    def __init__(self, tree):
        self.tree = tree

    def output(self, out):
        val = self._generate(out, CompilationContext(None), self.tree)
        out.writeln(val)

    def _generate(self, out, ctx, node):
        name = node.tag.name
        args = node.args
        if name == 'null':
            return 'None'
        return getattr(self, "generate_"+name)(out, ctx, *args)

    def _generatePattern(self, out, ctx, ej, val, node):
        name = node.tag.name
        args = node.args
        return getattr(self, "pattern_"+name)(out, ctx, ej, val, *args)

    def _generatePatternForParam(self, out, ctx, ej, node):
        if node.tag.name in ['FinalPattern', 'VarPattern'] and node.args[1].tag.name == 'null':
            #skip assignment entirely, we'll use the requested name directly in the param list
            return mangleNoun(node.args[0].args[0].data)
        else:
            pattname = node.tag.name
            if pattname.endswith('Pattern'):
                pattname = pattname[:-7]
            gen = ctx.gensym(pattname)
            self._generatePattern(out, ctx, ej, gen, node)
            return gen

    #The convention is: return an expression, directly write out
    #statements it depends on.

    def generate_LiteralExpr(self, out, ctx, litNode):
        if ctx.mode == FX_ONLY:
            return
        if litNode.tag.name == 'Character':
            return "_monte.Character(%r)" % (litNode.args[0].data)
        lit = litNode.data
        if isinstance(lit, basestring):
            #either already unicode, or ascii bytes
            return repr(unicode(lit))
        return repr(lit)

    def generate_NounExpr(self, out, ctx, noun):
        name = noun.data
        constants = {"null": "None",
                     "true": "True",
                     "false": "False"}
        return constants.get(name, mangleNoun(name))

    def generate_BindingExpr(self, out, ctx, bin):
        name = bin.args[0].data
        if ctx.mode != FX_ONLY:
            return "_monte.getBinding(self, %r)" % (mangleNoun(name),)

    def generate_SeqExpr(self, out, ctx, seqs):
        exprs = seqs.args
        # at toplevel.
        innerctx = ctx.with_(mode=FX_ONLY)
        for e in exprs[:-1]:
            v = self._generate(out, innerctx, e)
            if v is not None:
                out.writeln(v)

        return self._generate(out, ctx, exprs[-1])

    def generate_MethodCallExpr(self, out, ctx, rcvr, verb, args):
        rcvrName = self._generate(out, ctx.with_(mode=VALUE), rcvr)
        argNames = [self._generate(out, ctx.with_(mode=VALUE), arg) for arg in args.args]
        if verb.data == "run":
            return "%s(%s)" % (rcvrName, ', '.join(argNames))
        else:
            return "%s.%s(%s)" % (rcvrName, mangleNoun(verb.data), ', '.join(argNames))

    def generate_Def(self, out, ctx, patt, ej, expr):
        if ej.tag.name != 'null':
            ejName = self._generate(out, ctx.with_(mode=VALUE), ej)
        else:
            ejName = '_monte.throw'
        exprName = self._generate(out, ctx.with_(mode=VALUE), expr)
        n = self._generatePattern(out, ctx, ejName, exprName, patt)
        if ctx.mode != FX_ONLY:
            return n

    def generate_Escape(self, out, ctx, patt, body, catcher):
        bodyScope = scope(body)
        pattScope = scope(patt)
        # only generate ejector code if it's mentioned in the body
        if bodyScope.namesUsed() & pattScope.outNames():
            name = next(iter(pattScope.outNames()))
            ej = self._generatePattern(out, ctx, None,
                                       '_monte.ejector("%s")' % (name,),
                                       patt)
            out.writeln("try:")
            sub = out.indent()
            ejTemp = ctx.gensym(name)
            escapeTemp = ctx.gensym("escape")
            val = self._generate(sub, ctx, body)
            sub.writeln("%s = %s" % (escapeTemp, val))
            out.writeln("except %s._m_type, %s:" % (ej, ejTemp))
            if catcher.tag.name != 'null':
                self._generatePattern(sub, ctx, None,
                                      ejTemp, catcher.args[0])
                val = self._generate(sub, ctx, catcher.args[1])
                sub.writeln("%s = %s" % (escapeTemp, val))
            else:
                sub.writeln("%s = %s" % (escapeTemp, ejTemp))
            if ctx.mode != FX_ONLY:
                return escapeTemp
        else:
            return self._generate(out, ctx, body)

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
            paramOut = methOut.delay()
            paramNames = [self._generatePatternForParam(paramOut, ctx, None, p)
                          for p in params]
            classOut.writeln("def %s(%s):" % (mangleNoun(verb),
                                              ', '.join(['self'] + paramNames)))
            if mdoc:
                methOut.writeln('"""')
                for ln in mdoc.splitlines():
                    methOut.writeln(ln)
                methOut.writeln('"""')
            paramOut.flush()
            methOut.writeln("return " + self._generate(methOut, ctx.with_(mode=VALUE), body))
        out.writeln("%s = %s()" % (objname, scriptname))
        if ctx.mode != FX_ONLY:
            return objname


    def generate_Assign(self, out, ctx, patt, expr):
        name = patt.args[0].data
        v = self._generate(out, ctx.with_(mode=VALUE), expr)
        out.writeln("%s = %s" % (mangleNoun(name), v))
        if ctx.mode != FX_ONLY:
            return name

    def pattern_FinalPattern(self, out, ctx, ej, val, name, guard):
        if guard.tag.name != 'null':
            guardv = self._generate(out, ctx.with_(mode=VALUE), guard)
            if ej is None:
                ej = "_monte.throw"
            val = "%s.coerce(%s, %s)" % (guardv, val, ej)
        n = mangleNoun(name.args[0].data)
        out.writeln("%s = %s" % (n, val))
        return n

    pattern_VarPattern = pattern_FinalPattern

    def pattern_ListPattern(self, out, ctx, ej, val, pattsTerm, extra):
        #XXX extra
        patts = pattsTerm.args
        listv = ctx.gensym("total_list")
        vs = [ctx.gensym("list") for _ in patts]
        errv = ctx.gensym("e")
        sub = out.indent()
        out.writeln("%s = %s" % (listv, val))
        out.writeln("try:")
        if patts:
            sub.writeln("%s, = %s" % (', '.join(vs), listv))
        else:
            sub.writeln("if len(%s):" % listv)
            subsub = sub.indent()
            subsub.writeln("raise ValueError('Failed to match empty list')")
        out.writeln("except ValueError, %s:" % (errv,))
        if ej is None:
            sub.writeln("_monte.throw(%s)" % (errv,))
        else:
            sub.writeln("%s(%s)" % (ej, errv))
        for v, patt in zip(vs, patts):
            self._generatePattern(out, ctx, ej, v, patt)
        return listv

def ecompile(source, origin="<string>"):
    ast = expand(parse(source))
    f = StringIO()
    PythonWriter(ast).output(TextWriter(f))
    return f.getvalue().strip()
