import re, string
from keyword import iskeyword

from StringIO import StringIO
from monte.eparser import parse
from monte.expander import expand, scope

from terml.nodes import termMaker as t

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
        f = StringIO()
        def flush():
            self.file.write(f.getvalue())
        return TextWriter(f, self.indentSteps), flush


mtrans = string.maketrans(string.printable[62:], '_' * 38)
GENSYM_PREFIX = '_g_'

VALUE, CONTROL, FX_ONLY = range(3)
LOCAL, FRAME, OUTER = range(3)

class SymGenerator(object):
    def __init__(self):
        self.gensymCounter = 0

    def gensym(self, base):
        self.gensymCounter += 1
        return GENSYM_PREFIX + base + str(self.gensymCounter)


def mangleIdent(n):
    prefix = '_m_'
    if re.match('[a-zA-Z_]\\w*$', n):
        #mangles: python keywords, clashes with python __foo__ names,
        #and clashes with mangled/generated names
        if (iskeyword(n) or n.startswith((prefix, GENSYM_PREFIX)) or
            (n.startswith('__') and n.endswith('__'))):
            return prefix + n
        else:
            return n
    else:
        return prefix + n.translate(mtrans)

safeScopeNames = set(["null", "false", "true", "throw", "__loop", "__makeList", "__makeMap", "__makeProtocolDesc", "__makeMessageDesc", "__makeParamDesc", "any", "void", "boolean", "__makeOrderedSpace", "Guard", "require", "__makeVerbFacet", "__MatchContext", "__is", "__splitList", "__suchThat", "__bind", "__extract", "__Empty", "__matchBind", "__Test", "NaN", "Infinity", "__identityFunc", "__makeInt", "escape", "for", "if", "try", "while", "__makeFinalSlot", "__makeTwine", "__makeSourceSpan", "__auditedBy", "near", "pbc", "PassByCopy", "DeepPassByCopy", "Data", "Persistent", "DeepFrozen", "int", "float64", "char", "String", "Twine", "TextWriter", "List", "Map", "Set", "nullOk", "Tuple", "__Portrayal", "notNull", "vow", "rcvr", "ref", "nocall", "SturdyRef", "simple__quasiParser", "twine__quasiParser", "rx__quasiParser", "olde__quasiParser", "e__quasiParser", "epatt__quasiParser", "sml__quasiParser", "term__quasiParser", "__equalizer", "__comparer", "Ref", "E", "promiseAllFulfilled", "EIO", "help", "safeScope", "__eval", "resource__uriGetter", "type__uriGetter", "elib__uriGetter", "elang__uriGetter", "opaque__uriGetter", "__abortIncarnation", "when", "persistenceSealer", "import__uriGetter", "traceln"])

class OuterScopeLayout(object):
    parent = None
    def __init__(self, gensym, outers):
        self.gensym = gensym
        self.outers = outers

    def getNoun(self, n):
        if n in self.outers:
            return '_monte.' + mangleIdent(n)

    def getBinding(self, n):
        if n in self.outers:
            return Binding(t.FinalPattern(t.NounExpr(n), None), OUTER)

class FrameScopeLayout(object):
    def __init__(self, fields, verbs, selfName):
        self.fields = [Binding(f.node, FRAME) for f in fields]
        self.selfName = selfName
        self.verbs = verbs
        self.pynames = {}
        for f in fields:
            if f.name in self.verbs:
                self.pynames[f.name] = self.gensym(mangleIdent(f.name))
            else:
                self.pynames[f.name] = mangleIdent(f.name)

    def getNoun(self, name):
        if name in self.pynames:
            return "%s.%s" % (self.selfName, self.pynames[name])

    def getBinding(self, name):
        for f in self.fields:
            if f.name == name:
                return f


#XXX ignoring REPL case for now
class ScopeLayout(object):
    """
    `outer` is the current outer scope, which is an unalterable set of
    bindings for the normal case and a monotonically growing set for
    the REPL.

    `frame` is the scope of the innermost object expression, which
    contains all of the non-local non-outer names used in that object
    expression.

    `parent` is the most immediately enclosing scope. It may be None,
    if this scope is an immediate child of the outer scope or an
    object expression.
    """
    def __init__(self, parent, frame, outer):
        self.parent = parent
        self.frame = frame
        self.outer = outer
        self.gensym = outer.gensym
        self.nodes = {}
        self.pynames = {}

    def addNoun(self, name, node):
        if name in self.pynames:
            raise CompileError("%r already in scope" % (name,))
        if self.outer.getNoun(name):
            raise CompileError("Cannot shadow outer-scope name %r" % (name,))
        if self.parent and self.parent.getNoun(name):
            # a scope outside this one uses the name.
            #XXX only needs gensym if the name is a frame var in this context.
            pyname = self.gensym(mangleIdent(name))
        pyname = mangleIdent(name)
        self.pynames[name] = pyname
        self.nodes[name] = node
        return pyname

    def _chainGetPyName(self, n):
        p = self.parent
        while p and n not in getattr(p, 'pynames', ()):
            p = p.parent
        if p is not None:
            return p.pynames[n]

    def getNoun(self, n):
        if n in self.pynames:
            return self.pynames[n]
        else:
            for gn in [self._chainGetPyName, self.frame.getNoun,
                       self.outer.getNoun]:
                pyname = gn(n)
                if pyname is not None:
                    return pyname

    def getBinding(self, n):
        if n in self.nodes:
            return self._createBinding(n)
        elif self.parent:
            return self.parent.getBinding(n)
        else:
            b = self.frame.getBinding(n)
            if b is None:
                b = self.outer.getBinding(n)
            return b

    def _createBinding(self, n):
        return Binding(self.nodes[n], LOCAL)

    def fqnPrefix(self):
        pass

    def bindings(self):
        pass

    def isLocal(self, noun):
        pass

    def metaStateBindings(self):
        pass

    def optObjectExpr(self):
        pass


class Binding(object):
    def __init__(self, node, kind):
        self.node = node
        self.isFinal = node.tag.name == 'FinalPattern'
        self.guardExpr = node.args[1]
        self.name = node.args[0].args[0].data
        self.kind = kind

class CompilationContext(object):
    def __init__(self, parent, mode=None, layout=None, rootWriter=None):
        if mode is None:
            self.mode = getattr(parent, 'mode', VALUE)
        else:
            self.mode = mode
        if layout is None:
            self.layout = getattr(parent, 'layout', None)
        else:
            self.layout = layout
        if rootWriter is None:
            self.rootWriter = getattr(parent, 'rootWriter', None)
        else:
            self.rootWriter = rootWriter

    def with_(self, **kwargs):
        return CompilationContext(self, **kwargs)

    def classWriter(self):
        return self.rootWriter.delay()


class PythonWriter(object):
    """
    Converts an E syntax tree into Python source.
    """

    def __init__(self, tree):
        self.tree = tree

    def err(self, msg):
        raise CompileError(msg)

    def output(self, origOut):
        out, flush = origOut.delay()
        ctx = CompilationContext(
            None, rootWriter=origOut,
            layout=ScopeLayout(None, FrameScopeLayout((), None, None),
                               OuterScopeLayout(SymGenerator().gensym,
                                                safeScopeNames)))
        val = self._generate(out, ctx, self.tree)
        flush()
        origOut.writeln(val)

    def _generate(self, out, ctx, node):
        name = node.tag.name
        args = node.args
        if name == 'null':
            return 'None'
        self.currentNode = node
        return getattr(self, "generate_"+name)(out, ctx, *args)

    def _generatePattern(self, out, ctx, ej, val, node):
        name = node.tag.name
        args = node.args
        self.currentNode = node
        return getattr(self, "pattern_"+name)(out, ctx, ej, val, *args)

    def _generatePatternForParam(self, out, ctx, ej, node):
        if node.tag.name in ['FinalPattern', 'VarPattern'] and node.args[1].tag.name == 'null':
            #skip assignment entirely, we'll use the requested name directly in the param list
            return ctx.layout.addNoun(node.args[0].args[0].data, node)
        else:
            pattname = node.tag.name
            if pattname.endswith('Pattern'):
                pattname = pattname[:-7]
            gen = ctx.layout.gensym(pattname)
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
        if ctx.layout.getNoun(name) is None:
            self.err("Undefined variable: " + repr(name))
        return constants.get(name, ctx.layout.getNoun(name))

    def generate_BindingExpr(self, out, ctx, bin):
        name = bin.args[0].data
        if ctx.mode != FX_ONLY:
            return "_monte.getBinding(self, %r)" % (mangleIdent(name),)

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
            return "%s.%s(%s)" % (rcvrName, mangleIdent(verb.data), ', '.join(argNames))

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
            ejTemp = ctx.layout.gensym(name)
            escapeTemp = ctx.layout.gensym("escape")
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

    def generate_Object(self, out, ctx, doc, nameNode, script):
        #TODO replace this gubbish with proper destructuring
        doc = doc.data
        name = nameNode.args[0].args[0].data
        selfName = ctx.layout.addNoun(name, nameNode)
        ss = scope(self.currentNode)
        used = ss.namesUsed()
        fields = [ctx.layout.getBinding(n) for n in used - ctx.layout.outer.outers]
        extends = script.args[0]
        guard = script.args[1]
        implements = script.args[2].args
        methods = script.args[3].args
        matchers = script.args[4].args
        scriptname = "_m_%s_Script" % (selfName,)
        verbs = [meth.args[1].data for meth in methods]
        frame = FrameScopeLayout(fields, verbs, selfName)

        classOut, cflush = ctx.classWriter()
        classOut.writeln("class %s(_monte.MonteObject):" % (scriptname,))
        classBodyOut = classOut.indent()
        if doc:
            classBodyOut.writeln('"""')
            for ln in doc.splitlines():
                classBodyOut.writeln(ln)
            classBodyOut.writeln('"""')
        fnames = ()
        if fields:
            initOut = classBodyOut.indent()
            fnames = sorted([f.name for f in fields])
            classBodyOut.writeln("def __init__(%s, %s):" % (selfName,
                                                            ', '.join(fnames)))
            for n in fnames:
                initOut.writeln("%s.%s = %s" % (selfName, n, n))
            initOut.writeln("")

        for meth in methods:
            methctx = ctx.with_(layout=ScopeLayout(None, frame, ctx.layout.outer), mode=VALUE)
            mdoc = meth.args[0].data
            verb = meth.args[1].data
            params = meth.args[2].args
            methGuard = meth.args[3]
            body = meth.args[4]
            methOut = classBodyOut.indent()
            paramOut, flush = methOut.delay()
            paramNames = [self._generatePatternForParam(paramOut, methctx, None, p)
                          for p in params]
            classBodyOut.writeln("def %s(%s):" % (
                mangleIdent(verb),
                ', '.join([selfName] + paramNames)))
            if mdoc:
                methOut.writeln('"""')
                for ln in mdoc.splitlines():
                    methOut.writeln(ln)
                methOut.writeln('"""')
            flush()
            rvar = self._generate(methOut, methctx, body)
            methOut.writeln("return " + rvar + "\n")

        cflush()
        out.writeln("%s = %s(%s)" % (selfName, scriptname, ", ".join(fnames)))
        if ctx.mode != FX_ONLY:
            return selfName


    def generate_Assign(self, out, ctx, patt, expr):
        name = patt.args[0].data
        v = self._generate(out, ctx.with_(mode=VALUE), expr)
        pyname = ctx.layout.getNoun(name)
        out.writeln("%s = %s" % (pyname, v))
        b = ctx.layout.getBinding(name)
        if not b:
            self.err("Undefined variable:" + repr(name))
        if b.isFinal:
            self.err("Can't assign to final variable: " + repr(name))
        if ctx.mode != FX_ONLY:
            return pyname

    def pattern_FinalPattern(self, out, ctx, ej, val, name, guard):
        if guard.tag.name != 'null':
            guardv = self._generate(out, ctx.with_(mode=VALUE), guard)
            if ej is None:
                ej = "_monte.throw"
            val = "%s.coerce(%s, %s)" % (guardv, val, ej)
        pyname = ctx.layout.addNoun(name.args[0].data, self.currentNode)
        out.writeln("%s = %s" % (pyname, val))
        return pyname

    pattern_VarPattern = pattern_FinalPattern

    def pattern_ListPattern(self, out, ctx, ej, val, pattsTerm, extra):
        #XXX extra
        patts = pattsTerm.args
        listv = ctx.layout.gensym("total_list")
        vs = [ctx.layout.gensym("list") for _ in patts]
        errv = ctx.layout.gensym("e")
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
