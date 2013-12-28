import re, string
from keyword import iskeyword

from StringIO import StringIO
from monte.parser import parse
from monte.expander import expand, scope

from terml.nodes import Term, termMaker as t

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

def decimalize(s):
    safe = string.letters  + '_'
    for c in s:
        if c in safe:
            yield c
        else:
            yield str(ord(c))

def mangleIdent(n):
    prefix = '_m_'
    if re.match('[a-zA-Z_]\\w*$', n):
        #mangles: python keywords, clashes with python __foo__ names,
        #and clashes with mangled/generated names
        if (iskeyword(n) or n.startswith((prefix, GENSYM_PREFIX)) or
            (n.startswith('__'))):
            return prefix + ''.join(decimalize(n))
        else:
            return n
    else:
        return prefix + ''.join(decimalize(n))

safeScopeNames = set(["null", "false", "true", "throw", "__loop", "__makeList", "__makeMap", "__makeProtocolDesc", "__makeMessageDesc", "__makeParamDesc", "any", "void", "boolean", "__makeOrderedSpace", "Guard", "require", "__makeVerbFacet", "__MatchContext", "__is", "__splitList", "__suchThat", "__bind", "__extract", "__Empty", "__matchBind", "__Test", "NaN", "Infinity", "__identityFunc", "__makeInt", "escape", "for", "if", "try", "while", "__makeFinalSlot", "__makeTwine", "__makeSourceSpan", "__auditedBy", "near", "pbc", "PassByCopy", "DeepPassByCopy", "Data", "Persistent", "DeepFrozen", "int", "float64", "char", "String", "Twine", "TextWriter", "List", "Map", "Set", "nullOk", "Tuple", "__Portrayal", "notNull", "vow", "rcvr", "ref", "nocall", "SturdyRef", "simple__quasiParser", "twine__quasiParser", "rx__quasiParser", "olde__quasiParser", "e__quasiParser", "epatt__quasiParser", "sml__quasiParser", "term__quasiParser", "__equalizer", "__comparer", "Ref", "E", "promiseAllFulfilled", "EIO", "help", "safeScope", "__eval", "resource__uriGetter", "type__uriGetter", "elib__uriGetter", "elang__uriGetter", "opaque__uriGetter", "__abortIncarnation", "when", "persistenceSealer", "import__uriGetter", "traceln"])

class OuterScopeLayout(object):
    parent = None
    def __init__(self, gensym, outers):
        self.gensym = gensym
        self.outers = outers

    def getBinding(self, n):
        if n in self.outers:
            return Binding(t.FinalPattern(t.NounExpr(n), None),
                           '_monte.' + mangleIdent(n), None, OUTER)


class FrameScopeLayout(object):
    def __init__(self, fields, verbs, selfName, fqnPrefix):
        self.selfName = selfName
        self.verbs = verbs
        self.fields = [self._createBinding(f) for f in fields]
        self.fqnPrefix = fqnPrefix

    def _createBinding(self, f):
        if f.name not in self.verbs:
            pyname = f.pyname
        else:
            pyname =  self.gensym(mangleIdent(f.name))
        return Binding(f.node, self.selfName + '.' + pyname,
                       '_monte.getGuard(%s, "%s")' % (self.selfName, f.name),
                       FRAME)

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
        self.guards = {}
        self.metaContextExpr = False

    def addNoun(self, name, node, guardname=None):
        if name in self.pynames:
            raise CompileError("%r already in scope" % (name,))
        if self.outer.getBinding(name):
            raise CompileError("Cannot shadow outer-scope name %r" % (name,))
        if self.parent and self.parent.getBinding(name):
            # a scope outside this one uses the name.  XXX only needs
            #gensym in certain circumstances, such as if the name is a
            #frame var in this context, or
            # "def x := 1; f(x, {def x := 2})"
            pyname = self.gensym(mangleIdent(name))
        else:
            pyname = mangleIdent(name)
        self.pynames[name] = pyname
        self.nodes[name] = node
        self.guards[name] = guardname
        return pyname

    def addObjectGuard(self, name, guard):
        if name not in self.pynames:
            raise CompileError("internal compiler error")
        self.guards[name] = guard

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
        return Binding(self.nodes[n],  self.pynames[n], self.guards[n], LOCAL)


class Binding(object):
    def __init__(self, node, pyname, guardname, kind):
        self.node = node
        self.pyname = pyname
        self.isFinal = node.tag.name == 'FinalPattern'
        self.guardExpr = node.args[1]
        self.guardname = guardname
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

    def __init__(self, tree, origin):
        self.tree = tree
        self.origin = origin

    def err(self, msg):
        raise CompileError(msg)

    def output(self, origOut):
        out, flush = origOut.delay()
        ctx = CompilationContext(
            None, rootWriter=origOut,
            layout=ScopeLayout(None, FrameScopeLayout((), None, None, self.origin),
                               OuterScopeLayout(SymGenerator().gensym,
                                                safeScopeNames)))
        val = self._generate(out, ctx, self.tree)
        flush()
        origOut.writeln(val)

    def _generate(self, out, ctx, node):
        name = node.tag.name
        if name == 'null':
            return 'None'
        return getattr(self, "generate_"+name)(out, ctx, node)

    def _generatePattern(self, out, ctx, ej, val, node, objName=False):
        name = node.tag.name
        if objName:
            return getattr(self, "pattern_"+name)(out, ctx, ej, val, node, True)
        else:
            return getattr(self, "pattern_"+name)(out, ctx, ej, val, node)

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

    def generate_LiteralExpr(self, out, ctx, node):
        litNode = node.args[0]
        if ctx.mode == FX_ONLY:
            return
        if litNode.tag.name == 'Character':
            return "_monte.Character(%r)" % (litNode.args[0].data)
        lit = litNode.data
        if isinstance(lit, basestring):
            #either already unicode, or ascii bytes
            lit = unicode(lit)
        return '_monte.wrap(%r)' % (lit,)

    def generate_NounExpr(self, out, ctx, node):
        name = node.args[0].data
        constants = {"null": "None",
                     "true": "True",
                     "false": "False"}
        b = ctx.layout.getBinding(name)
        if b is None:
            self.err("Undefined variable: " + repr(name))
        if b.name in constants:
            return constants[b.name]
        if b.isFinal or b.kind == FRAME:
            return b.pyname
        else:
            return b.pyname + ".get()"

    def generate_BindingExpr(self, out, ctx, node):
        name = node.args[0].data
        if (ctx.layout.frame and
            name in [f.name for f in ctx.layout.frame.fields]):
            return "_monte.getBinding(%s, %r)" % (ctx.layout.frame.selfName,
                                                  mangleIdent(name),)
        else:
            b = ctx.layout.getBinding(name)
            if b.isFinal:
                bn = "_monte.FinalSlot(%s)" % (b.pyname,)
            else:
                bn = b.pyname
            return "_monte.reifyBinding(%s)" % (bn,)

    def generate_SeqExpr(self, out, ctx, node):
        exprs = node.args[0].args
        # at toplevel.
        innerctx = ctx.with_(mode=FX_ONLY)
        for e in exprs[:-1]:
            v = self._generate(out, innerctx, e)
            if v is not None:
                out.writeln(v)

        return self._generate(out, ctx, exprs[-1])

    def generate_MethodCallExpr(self, out, ctx, node):
        rcvr, verb, args = node.args
        rcvrName = self._generate(out, ctx.with_(mode=VALUE), rcvr)
        argNames = [self._generate(out, ctx.with_(mode=VALUE), arg) for arg in args.args]
        if verb.data == "run":
            return "%s(%s)" % (rcvrName, ', '.join(argNames))
        else:
            return "%s.%s(%s)" % (rcvrName, mangleIdent(verb.data), ', '.join(argNames))

    def generate_Def(self, out, ctx, node):
        patt, ej, expr = node.args
        if ej.tag.name != 'null':
            ejName = self._generate(out, ctx.with_(mode=VALUE), ej)
        else:
            ejName = '_monte.throw'
        exprName = self._generate(out, ctx.with_(mode=VALUE), expr)
        n = self._generatePattern(out, ctx, ejName, exprName, patt)
        if ctx.mode != FX_ONLY:
            return n

    def generate_Escape(self, out, ctx, node):
        patt, body, catcher = node.args
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
                sub.writeln("%s = %s.args[0]" % (escapeTemp, ejTemp))
            if ctx.mode != FX_ONLY:
                return escapeTemp
        else:
            return self._generate(out, ctx, body)

    def generate_Object(self, out, ctx, node):
        #XXX replace this gubbish with proper destructuring
        doc, nameNode, script = node.args
        doc = doc.data
        guard = script.args[1]
        if nameNode.tag.name == 'IgnorePattern':
            name = "_"
            nameNode = Term(nameNode.tag, None, (guard,), nameNode.span)
            selfName = ctx.layout.gensym("ignore")
        else:
            name = nameNode.args[0].args[0].data
            nameNode = Term(nameNode.tag, None, (nameNode.args[0], guard), nameNode.span)
            selfName = ctx.layout.addNoun(name, nameNode)

        implements = script.args[2].args
        if guard.tag.name != "null":
            implements = (guard,) + implements
        scriptname = "_m_%s_Script" % (selfName,)
        ss = scope(node)
        used = ss.namesUsed()
        fields = [ctx.layout.getBinding(n) for n in used - ctx.layout.outer.outers]
        selfBinding = ctx.layout.getBinding(name)
        if nameNode.tag.name in ('FinalPattern', 'IgnorePattern'):
            paramNames = self._collectSlots(fields)
        else:
            paramNames = [selfName] + self._collectSlots(fields)
            fields = [selfBinding]
            fields += [ctx.layout.getBinding(n) for n in used - ctx.layout.outer.outers]
        methods = script.args[3].args
        matchers = script.args[4].args
        verbs = [meth.args[1].data for meth in methods]
        methGuards = ["%r: %s" % (meth.args[1].data, self._generate(out, ctx, meth.args[3]))
                      for meth in methods
                      if meth.args[3].tag.name != 'null']
        if methGuards:
            paramNames.insert(0, '{%s}' % ', '.join(methGuards))
        if implements:
            paramNames.insert(0, '[%s]' % ', '.join([self._generate(out, ctx, iface)
                                                     for iface in implements]))
        val = "%s(%s)" % (scriptname, ", ".join(paramNames))
        selfName = self._generatePattern(out, ctx, None, val, nameNode, True)
        frame = FrameScopeLayout(fields, verbs, selfName,
                                 '%s$%s' % (ctx.layout.frame.fqnPrefix, name))
        matcherNames = [ctx.layout.gensym("matcher") for _ in matchers]
        classOut, cflush = ctx.classWriter()
        classOut.writeln("class %s(_monte.MonteObject):" % (scriptname,))
        classBodyOut = classOut.indent()
        if not any([methods, matchers, fields, doc, implements]):
            classBodyOut.writeln("pass")
        if matcherNames:
            classBodyOut.writeln('_m_matcherNames = %r' % (matcherNames,))
        if doc:
            classBodyOut.writeln('"""')
            for ln in doc.splitlines():
                classBodyOut.writeln(ln)
            classBodyOut.writeln('"""')
        fnames = ()
        if any([fields, implements, methGuards]):
            initOut = classBodyOut.indent()
            fnames = sorted([f.name for f in fields])
            pyfnames = [mangleIdent(n) + "_slot" for n in fnames]
            initParams = pyfnames
            if methGuards:
                initParams = ["_m_methodGuards"] + initParams
            if implements:
                initParams = ["_m_auditors"] + initParams
            classBodyOut.writeln("def __init__(%s, %s):" % (selfName,
                                                            ', '.join(initParams)))
            if implements:
                initOut.writeln(selfName + "._m_audit(_m_auditors)")
            if methGuards:
                initOut.writeln(selfName + "._m_guardMethods(_m_methodGuards)")
            for name, pyname  in zip(fnames, pyfnames):
                initOut.writeln("_monte.MonteObject._m_install(%s, '%s', %s)" % (
                    selfName, name, pyname))
            initOut.writeln("")
        metacontext = False
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
            if methGuard.tag.name != 'null':
                rvar = "%s._m_guardForMethod(%r).coerce(%s, _monte.throw)" % (
                    selfName, verb, rvar)
            methOut.writeln("return " + rvar + "\n")
            metacontext = metacontext or methctx.layout.metaContextExpr

        for matcherName, mtch in zip(matcherNames, matchers):
            mtchctx = ctx.with_(layout=ScopeLayout(None, frame, ctx.layout.outer), mode=VALUE)
            patt = mtch.args[0]
            body = mtch.args[1]
            matcherNames.append(matcherName)
            classBodyOut.writeln("def %s(%s, _m_message):" % (matcherName,
                                                              selfName))
            mtchOut = classBodyOut.indent()
            self._generatePattern(mtchOut, mtchctx, '_monte.matcherFail', "_m_message", patt)
            rvar = self._generate(mtchOut, mtchctx, body)
            mtchOut.writeln("return " + rvar + "\n")
            metacontext = metacontext or mtchctx.layout.metaContextExpr

        if implements or metacontext:
            classBodyOut.writeln('_m_objectExpr = "%s"\n' %
                                 node._unparse().encode('zlib')
                                                .encode('base64')
                                                .replace('\n', ''))
        cflush()
        if ctx.mode != FX_ONLY:
            return selfName

    def _collectSlots(self, fields):
        makeSlots = []
        for f in sorted(fields, key=lambda f: f.name):
            if f.isFinal:
                makeSlots.append("_monte.FinalSlot(%s, %s)" % (mangleIdent(f.name),
                                                               f.guardname))
            else:
                makeSlots.append(mangleIdent(f.name))
        return makeSlots

    def generate_Assign(self, out, ctx, node):
        patt, expr = node.args
        name = patt.args[0].data
        v = self._generate(out, ctx.with_(mode=VALUE), expr)
        b = ctx.layout.getBinding(name)
        if not b:
            self.err("Undefined variable:" + repr(name))
        temp = ctx.layout.gensym(mangleIdent(b.name))
        if b.isFinal:
            self.err("Can't assign to final variable: " + repr(name))
        out.writeln("%s = %s" % (temp, v))
        if b.kind == FRAME:
            out.writeln("%s = %s" % (b.pyname, temp))
        else:
            out.writeln("%s.put(%s)" % (b.pyname, temp))
        if ctx.mode != FX_ONLY:
            return temp

    def generate_Finally(self, out, ctx, node):
        block, fin = node.args
        sub = out.indent()
        out.writeln("try:")
        finTemp = ctx.layout.gensym("finally")
        val = self._generate(sub, ctx, block)
        sub.writeln("%s = %s" % (finTemp, val))
        out.writeln("finally:")
        val = self._generate(sub, ctx, fin)
        sub.writeln("%s = %s" % (finTemp, val))
        return finTemp

    def generate_KernelTry(self, out, ctx, node):
        block, patt, catchblock = node.args
        sub = out.indent()
        out.writeln("try:")
        catchTemp = ctx.layout.gensym("catch")
        val = self._generate(sub, ctx, block)
        sub.writeln("%s = %s" % (catchTemp, val))
        excTemp = ctx.layout.gensym("exception")
        out.writeln("except Exception, %s:" % (excTemp,))
        self._generatePattern(sub, ctx, None, excTemp, patt)
        val = self._generate(sub, ctx, catchblock)
        sub.writeln("%s = %s" % (catchTemp, val))
        return catchTemp

    def generate_HideExpr(self, out, ctx, node):
        newctx = ctx.with_(layout=ScopeLayout(ctx.layout, ctx.layout.frame, ctx.layout.outer))
        return self._generate(out, newctx, node.args[0])

    def generate_If(self, out, ctx, node):
        test, consq, alt = node.args
        sub = out.indent()
        tv = self._generate(out, ctx, test)
        ifTemp = ctx.layout.gensym("if")
        out.writeln("if %s:" % (tv,))
        val = self._generate(sub, ctx, consq)
        sub.writeln("%s = %s" % (ifTemp, val))
        if alt.tag.name != 'null':
            out.writeln("else:")
            val = self._generate(sub, ctx, alt)
            sub.writeln("%s = %s" % (ifTemp, val))
        return ifTemp

    def generate_Meta(self, out, ctx, node):
        kind = node.args[0].data
        if kind == 'Context':
            ctx.layout.metaContextExpr = True
            f = ctx.layout.frame
            return "_monte.StaticContext(%r, %r, _m_%s_Script._m_objectExpr)" % (
                f.fqnPrefix, [b.name for b in f.fields], f.selfName)
        elif kind == 'State':
            f = ctx.layout.frame
            return '_monte.Map((%s))' % ', '.join('(%r, _monte.getSlot(%s, %r))' % ('&' + b.name, f.selfName, b.pyname.split('.')[1])
                                      for b in f.fields)

    def pattern_FinalPattern(self, out, ctx, ej, val, node, objname=False):
        name, guard = node.args
        guardname = None
        if guard.tag.name != 'null':
            guardv = self._generate(out, ctx.with_(mode=VALUE), guard)
            guardname = ctx.layout.gensym("guard")
            out.writeln("%s = %s" % (guardname, guardv))
            if ej is None:
                ej = "_monte.throw"
            val = "%s.coerce(%s, %s)" % (guardname, val, ej)
        if objname:
            pyname = ctx.layout.getBinding(name.args[0].data).pyname
            ctx.layout.addObjectGuard(name.args[0].data, guardname)
        else:
            pyname = ctx.layout.addNoun(name.args[0].data, node, guardname)
        out.writeln("%s = %s" % (pyname, val))
        return pyname

    def pattern_IgnorePattern(self, out, ctx, ej, val, node, objname=False):
        guard = node.args[0]
        guardname = None
        if guard.tag.name != 'null':
            guardv = self._generate(out, ctx.with_(mode=VALUE), guard)
            guardname = ctx.layout.gensym("guard")
            out.writeln("%s = %s" % (guardname, guardv))
            if ej is None:
                ej = "_monte.throw"
            val = "%s.coerce(%s, %s)" % (guardname, val, ej)
        pyname = ctx.layout.gensym("ignore")
        out.writeln("%s = %s" % (pyname, val))
        return pyname

    def pattern_VarPattern(self, out, ctx, ej, val, node, objname=False):
        nameExpr, guard = node.args
        name = nameExpr.args[0].data
        if ej is None:
            ej = "_monte.throw"
        if guard.tag.name != 'null':
            guardv = self._generate(out, ctx.with_(mode=VALUE), guard)
            guardname = ctx.layout.gensym("guard")
            out.writeln("%s = %s" % (guardname, guardv))
        else:
            guardname = "None"
        if objname:
            pyname = ctx.layout.getBinding(name).pyname
            ctx.layout.addObjectGuard(name, guardname)
            temp = ctx.layout.gensym(mangleIdent(name))
            out.writeln("%s = _monte.VarSlot(%s)" % (pyname, guardname))
            out.writeln("%s = %s" % (temp, val))
            out.writeln("%s._m_init(%s, %s)" % (pyname, temp, ej))
        else:
            pyname = ctx.layout.addNoun(name, node, guardname)
            temp = ctx.layout.gensym(mangleIdent(name))
            out.writeln("%s = %s" % (temp, val))
            out.writeln("%s = _monte.VarSlot(%s, %s, %s)" % (pyname, guardname, temp, ej))
        return temp

    def pattern_ListPattern(self, out, ctx, ej, val, node):
        pattsTerm, extra = node.args
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
            sub.writeln('raise RuntimeError("Ejector did not exit")')
        for v, patt in zip(vs, patts):
            self._generatePattern(out, ctx, ej, v, patt)
        return listv

    def pattern_ViaPattern(self, out, ctx, ej, val, node):
        lval = self._generate(out, ctx.with_(mode=VALUE), node.args[0])
        newval = "%s(%s, _monte.wrapEjector(%s))" % (lval, val, ej)
        self._generatePattern(out, ctx, ej, newval, node.args[1])
        return val

    def pattern_BindingPattern(self, out, ctx, ej, val, node):
        name = node.args[0].args[0].data
        pyname = ctx.layout.addNoun(name, node)
        out.writeln("%s = _monte.slotFromBinding(%s)" % (pyname, val))
        return pyname

def ecompile(source, origin="__main"):
    ast = expand(parse(source))
    f = StringIO()
    PythonWriter(ast, origin).output(TextWriter(f))
    return f.getvalue().strip()
