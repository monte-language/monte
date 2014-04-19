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

_absent = object()

class OuterScopeLayout(object):
    parent = None
    def __init__(self, gensym, outers):
        self.gensym = gensym
        self.bindings = {}
        for name in outers:
            self.bindings[name] = Binding(
                t.FinalPattern(t.NounExpr(name), None),
                '_m_outerScope["%s"]' % name, OUTER,
                "_monte.deepFrozenGuard",
                None)

    def getBinding(self, n, default=_absent):
        if n in self.bindings:
            return self.bindings[n]
        else:
            if default is _absent:
                raise CompileError("No global named " + repr(n))
            else:
                return default


class FrameScopeLayout(object):
    def __init__(self, fields, verbs, selfName, selfNameNode, fqnPrefix):
        self.selfName = selfName
        self.verbs = verbs
        if selfNameNode and selfNameNode.tag.name != 'IgnorePattern':
            self.selfBinding = Binding(selfNameNode, selfName, FRAME,
                                       '_monte.getObjectGuard(%s)' % selfName,
                                       None)
        else:
            self.selfBinding = None
        self.gensym = SymGenerator().gensym
        self.fields = [f.bindInFrame(self) for f in fields]
        self.fields.sort(key=lambda f: f.name)
        self.fqnPrefix = fqnPrefix

    def getBinding(self, name, default=_absent):
        if self.selfBinding and name == self.selfBinding.name:
            return self.selfBinding
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
        self.metaContextExpr = False
        self.bindings = {}

    def _genPyname(self, name):
        if name in self.bindings:
            raise CompileError("%r already in scope" % (name,))
        if name in self.outer.bindings:
            raise CompileError("Cannot shadow outer-scope name %r" % (name,))
        if self.parent and self.parent.getBinding(name, default=None):
            # a scope outside this one uses the name.  XXX only needs
            #gensym in certain circumstances, such as if the name is a
            #frame var in this context, or
            # "def x := 1; f(x, {def x := 2})"
            pyname = self.gensym(mangleIdent(name))
        else:
            pyname = mangleIdent(name)
        return pyname

    def addCustomBinding(self, name, node):
        pyname = self._genPyname(name)
        self.bindings[name] = CustomBinding(node, pyname, LOCAL, pyname)
        return pyname

    def addFinalBinding(self, name, node, guardExpr="_monte.null"):
        pyname = self._genPyname(name)
        bindingGuardExpr = '_monte.FinalSlot.asType().get(%s)' % (guardExpr,)
        self.bindings[name] = Binding(node, pyname, LOCAL, bindingGuardExpr, guardExpr)
        return pyname

    def addVarBinding(self, name, node, guardExpr="_monte.null"):
        pyname = self._genPyname(name)
        bindingGuardExpr = '_monte.VarSlot.asType().get(%s)' % (guardExpr,)
        self.bindings[name] = Binding(node, pyname, LOCAL, bindingGuardExpr, guardExpr)
        return pyname

    def addSelfBinding(self, name, node, guardname):
        return self.addFinalBinding(name, node, guardname)

    def getBinding(self, n, default=_absent):
        if n in self.bindings:
            return self.bindings[n]
        elif self.parent:
            return self.parent.getBinding(n, default)
        else:
            b = self.frame.getBinding(n, default)
            if b is None:
                b = self.outer.getBinding(n, default)
            return b

    def makeInner(self):
        return ScopeLayout(self, self.frame, self.outer)

class CustomBinding(object):
    def __init__(self, node, pyname, kind, descriptorName):
        self.node = node
        self.pyname = pyname
        self.name = node.args[0].args[0].data
        self.kind = kind
        self.descriptorName = descriptorName

    def getDescriptorName(self):
        return self.descriptorName

    def getValueExpr(self):
        return self.pyname + '.slot.get()'

    def getBindingGuardExpr(self):
        return self.pyname + '.guard'

    def getBindingExpr(self):
        return self.pyname

    def getSlotPairName(self):
        return mangleIdent(self.name) + "_slotPair"

    def getBindingPair(self):
        return (self.pyname + '.slot', self.getBindingGuardExpr())

    def bindInFrame(self, frame):
        if self.name not in frame.verbs:
            pyname = self.pyname
        else:
            pyname = frame.gensym(mangleIdent(self.name))
        if self.kind == FRAME:
            pyname = frame.selfName + '.' + pyname.rpartition('.')[2]
        else:
            pyname = frame.selfName + '.' + pyname
        return CustomBinding(self.node, pyname, FRAME, self.descriptorName)


class Binding(object):
    def __init__(self, node, pyname, kind, bindingGuardExpr, guardExpr, slotname=None):
        self.node = node
        self.pyname = pyname
        self.isFinal = node.tag.name == 'FinalPattern'
        self.bindingGuardExpr = bindingGuardExpr
        self.guardExpr = guardExpr
        self.name = node.args[0].args[0].data
        self.kind = kind
        if slotname is None:
            self.slotname = self.pyname
        else:
            self.slotname = slotname
        self.descriptorName = self.pyname

    def getDescriptorName(self):
        return self.descriptorName

    def generateInitParam(self):
        return self.pyname

    def getValueExpr(self):
        if self.isFinal or self.kind == FRAME:
            return self.pyname
        else:
            return self.pyname + ".get()"

    def getBindingExpr(self):
        if self.isFinal:
            bn = "_monte.FinalSlot(%s)" % (self.pyname,)
        else:
            bn = self.pyname
        return "_monte.Binding(%s, %s)" % (self.bindingGuardExpr, bn)

    def getBindingGuardExpr(self):
        return self.bindingGuardExpr

    def getBindingPair(self):
        if self.isFinal:
            pair = ("_monte.FinalSlot(%s, %s, unsafe=True)" % (self.pyname,
                                                               self.guardExpr),
                    self.bindingGuardExpr)
        else:
            pair = (self.slotname, self.bindingGuardExpr)
        return pair

    def getSlotPairName(self):
        return mangleIdent(self.name) + "_slotPair"

    def bindInFrame(self, frame):
        if self.name not in frame.verbs:
            pyname = self.pyname
            descriptorName = self.descriptorName
        else:
            descriptorName = pyname = frame.gensym(mangleIdent(self.name))

        if self.kind == FRAME:
            pyname = frame.selfName + '.' + pyname.rpartition('.')[2]
        else:
            pyname = frame.selfName + '.' + pyname
        slotname = '%s._m_slots["%s"][0]' % (frame.selfName, self.name)
        guardname = '%s._m_slots["%s"][1]' % (frame.selfName, self.name)
        b = Binding(self.node, pyname, FRAME, guardname, None, slotname)
        b.descriptorName = descriptorName
        return b

    def getAssignStatement(self, temp, frame):
        if self.kind == FRAME:
            if self.pyname == frame.selfName:
                return "%s.%s.put(%s)" % (self.pyname, self.pyname, temp)
            else:
                return "%s = %s" % (self.pyname, temp)
        else:
            return "%s.put(%s)" % (self.pyname, temp)

    def generateSelfVarSlot(self, val, guardname, temp, ej):
        return '\n'.join([
            "%s = _monte.VarSlot(%s)" % (self.pyname, guardname),
            "%s = %s" % (temp, val),
            "%s._m_init(%s, %s)" % (self.pyname, temp, ej)])

    def generateSelfFinalSlot(self, val):
        return '%s = %s' % (self.pyname, val)


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
        self.classNames = getattr(parent, 'classNames', [])


    def with_(self, **kwargs):
        return CompilationContext(self, **kwargs)

    def classWriter(self):
        return self.rootWriter.delay()


class PythonWriter(object):
    """
    Converts an E syntax tree into Python source.
    """

    def __init__(self, tree, origin, outerScope):
        self.tree = tree
        self.origin = origin
        self.outerScope = outerScope

    def err(self, msg):
        raise CompileError(msg)

    def output(self, origOut):
        out, flush = origOut.delay()
        ctx = CompilationContext(
            None, rootWriter=origOut,
            layout=ScopeLayout(None, FrameScopeLayout((), None, None, None, self.origin),
                               OuterScopeLayout(SymGenerator().gensym,
                                                self.outerScope.keys())))
        val = self._generate(out, ctx, self.tree)
        flush()
        origOut.writeln(val)

    def _generate(self, out, ctx, node):
        name = node.tag.name
        if name == 'null':
            return '_monte.null'
        return getattr(self, "generate_"+name)(out, ctx, node)

    def _generatePattern(self, out, ctx, ej, val, node, objName=False):
        name = node.tag.name
        if objName:
            return getattr(self, "pattern_"+name)(out, ctx, ej, val, node, True)
        else:
            return getattr(self, "pattern_"+name)(out, ctx, ej, val, node)

    def _generatePatternForParam(self, out, ctx, ej, node):
        if node.tag.name == 'FinalPattern' and node.args[1].tag.name == 'null':
            #skip assignment entirely, we'll use the requested name directly in the param list
            return ctx.layout.addFinalBinding(node.args[0].args[0].data, node)
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
            return "_monte.makeCharacter(%r)" % (litNode.args[0].data)
        lit = litNode.data
        if isinstance(lit, basestring):
            #either already unicode, or ascii bytes
            lit = unicode(lit)
        return '_monte.wrap(%r)' % (lit,)

    def generate_NounExpr(self, out, ctx, node):
        name = node.args[0].data
        constants = {"null": "_monte.null",
                     "true": "_monte.true",
                     "false": "_monte.false"}
        b = ctx.layout.getBinding(name)
        if b.name in constants:
            return constants[b.name]
        return b.getValueExpr()

    def generate_BindingExpr(self, out, ctx, node):
        name = node.args[0].args[0].data
        if (ctx.layout.frame and
            name in [f.name for f in ctx.layout.frame.fields]):
            return "_monte.getBinding(%s, %r)" % (ctx.layout.frame.selfName,
                                                  mangleIdent(name),)
        else:
            b = ctx.layout.getBinding(name)
            return b.getBindingExpr()

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
            newctx = ctx.with_(layout=ctx.layout.makeInner())
            val = self._generate(sub, newctx, body)
            sub.writeln("%s = %s" % (escapeTemp, val))
            out.writeln("except %s._m_type, %s:" % (ej, ejTemp))
            if catcher.tag.name != 'null':
                self._generatePattern(sub, ctx, None,
                                      ejTemp + '.args[0]', catcher.args[0])
                val = self._generate(sub, ctx, catcher.args[1])
                sub.writeln("%s = %s" % (escapeTemp, val))
            else:
                sub.writeln("%s = %s.args[0]" % (escapeTemp, ejTemp))
            out.writeln("finally:")
            sub.writeln("%s.disable()" % ej)
            if ctx.mode != FX_ONLY:
                return escapeTemp
        else:
            return self._generate(out, ctx, body)

    def generate_Object(self, out, ctx, node):
        doc, nameNode, auditorExprs, script = node.args
        doc = doc.data
        guard = auditorExprs.args[0]
        auditors = [self._generate(out, ctx, iface) for iface in auditorExprs.args]
        if guard.tag.name == "null":
            guard = None
            guardPyname = None
            auditors = auditors[1:]
        else:
            guardPyname = auditors[0]

        if nameNode.tag.name == 'IgnorePattern':
            name = "_"
            selfName = ctx.layout.gensym("ignore")
        else:
            name = nameNode.args[0].args[0].data
            if nameNode.tag.name == 'FinalPattern':
                selfName = ctx.layout.addFinalBinding(name, nameNode,
                                                      guardPyname or "_monte.null")
            elif nameNode.tag.name == 'VarPattern':
                selfName = ctx.layout.addVarBinding(name, nameNode,
                                                      guardPyname or "_monte.null")
            else:
                raise RuntimeError("internal compiler error")
        scriptname = "_m_%s_Script" % (selfName,)
        if scriptname in ctx.classNames:
            scriptname = "%s_Script" % (ctx.layout.gensym(selfName),)
        ctx.classNames.append(scriptname)
        ss = scope(node)
        used = ss.namesUsed()
        outerSet = set(ctx.layout.outer.bindings.keys())
        fieldNames = used - outerSet
        usedOuters = used & outerSet
        fields = [ctx.layout.getBinding(n) for n in fieldNames]
        if nameNode.tag.name != 'IgnorePattern':
            selfBinding = ctx.layout.getBinding(name)
        if nameNode.tag.name in ('FinalPattern', 'IgnorePattern'):
            paramNames = self._collectSlots(fields)
        else:
            paramNames = [
                "(%s, %s)" % (selfName, selfBinding.getBindingGuardExpr())
            ] + self._collectSlots(fields)
            fields = [selfBinding]
            fields += [ctx.layout.getBinding(n) for n in fieldNames]
        methods = script.args[1].args
        matchers = script.args[2].args
        verbs = [meth.args[1].data for meth in methods]
        methGuards = ["%r: %s" % (meth.args[1].data, self._generate(out, ctx, meth.args[3]))
                      for meth in methods
                      if meth.args[3].tag.name != 'null']
        if methGuards:
            paramNames.insert(0, '{%s}' % ', '.join(methGuards))
        if auditors:
            paramNames.insert(0, '[%s]' % ', '.join(auditors))
        val = "%s(%s)" % (scriptname, ", ".join(paramNames))

        selfSlotName = self._generatePattern(out, ctx, None, val, nameNode, True)
        frame = FrameScopeLayout(fields, verbs, selfName, nameNode,
                                 '%s$%s' % (ctx.layout.frame.fqnPrefix, name))
        matcherNames = [ctx.layout.gensym("matcher") for _ in matchers]
        classOut, cflush = ctx.classWriter()
        classOut.writeln("class %s(_monte.MonteObject):" % (scriptname,))
        classBodyOut = classOut.indent()
        classBodyOut.writeln("_m_fqn = '%s$%s'" % (
            ctx.layout.frame.fqnPrefix,
            name.encode('string-escape')))
        if matcherNames:
            classBodyOut.writeln('_m_matcherNames = %r' % (matcherNames,))
        if doc:
            classBodyOut.writeln('"""')
            for ln in doc.splitlines():
                classBodyOut.writeln(ln)
            classBodyOut.writeln('"""')
        fnames = ()
        if any([frame.fields, auditors, methGuards]):
            initOut = classBodyOut.indent()
            pyfnames = [f.getSlotPairName() for f in frame.fields]
            initParams = pyfnames
            if methGuards:
                initParams = ["_m_methodGuards"] + initParams
            if auditors:
                initParams = ["_m_auditors"] + initParams
            for b in frame.fields:
                classBodyOut.writeln("%s = _monte._SlotDescriptor(%r)" % (b.getDescriptorName(),
                                                                          b.name))
            classBodyOut.writeln("def __init__(%s, %s):" % (selfName,
                                                            ', '.join(initParams)))
            if methGuards:
                initOut.writeln(selfName + "._m_guardMethods(_m_methodGuards)")
            if frame.fields:
                initOut.writeln(selfName + "._m_slots = {")
                dictOut = initOut.indent()
                for b, pyname in zip(frame.fields, pyfnames):
                    dictOut.writeln("%r: %s," % (b.name, pyname))
                initOut.writeln("}")
            else:
                initOut.writeln(selfName + "._m_slots = {}")
            if auditors:
                initOut.writeln(selfName + "._m_outers = {")
                dictOut = initOut.indent()
                for name in usedOuters:
                    b = ctx.layout.outer.bindings[name]
                    dictOut.writeln('%r: %s,' % (name, b.getBindingGuardExpr()))
                initOut.writeln("}")
                # XXX pass actual outers somehow
                initOut.writeln(selfName + "._m_audit(_m_auditors, _monte.safeScope)")

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

        if auditors or metacontext:
            classBodyOut.writeln('_m_objectExpr = "%s"\n' %
                                 node._unparse().encode('zlib')
                                                .encode('base64')
                                                .replace('\n', ''))
        cflush()
        if ctx.mode != FX_ONLY:
            return selfSlotName

    def _collectSlots(self, fields):
        makeSlots = []
        for f in sorted(fields, key=lambda f: f.name):
            pair = f.getBindingPair()
            makeSlots.append("(%s, %s)" % pair)
        return makeSlots

    def generate_Assign(self, out, ctx, node):
        patt, expr = node.args
        name = patt.args[0].data
        v = self._generate(out, ctx.with_(mode=VALUE), expr)
        b = ctx.layout.getBinding(name)
        temp = ctx.layout.gensym(mangleIdent(name))
        if b.isFinal:
            self.err("Can't assign to final variable: " + repr(name))
        out.writeln("%s = %s" % (temp, v))
        out.writeln(b.getAssignStatement(temp, ctx.layout.frame))
        if ctx.mode != FX_ONLY:
            return temp

    def generate_Finally(self, out, ctx, node):
        block, fin = node.args
        sub = out.indent()
        out.writeln("try:")
        finTemp = ctx.layout.gensym("finally")
        newctx = ctx.with_(layout=ctx.layout.makeInner())
        val = self._generate(sub, newctx, block)
        sub.writeln("%s = %s" % (finTemp, val))
        out.writeln("finally:")
        newctx = ctx.with_(layout=ctx.layout.makeInner())
        val = self._generate(sub, newctx, fin)
        sub.writeln(val)
        return finTemp

    def generate_KernelTry(self, out, ctx, node):
        block, patt, catchblock = node.args
        sub = out.indent()
        out.writeln("try:")
        catchTemp = ctx.layout.gensym("catch")
        newctx = ctx.with_(layout=ctx.layout.makeInner())
        val = self._generate(sub, newctx, block)
        sub.writeln("%s = %s" % (catchTemp, val))
        out.writeln("except _monte.MonteEjection:")
        sub.writeln("raise")
        excTemp = ctx.layout.gensym("exception")
        out.writeln("except BaseException, %s:" % (excTemp,))
        self._generatePattern(sub, ctx, None, excTemp, patt)
        newctx = ctx.with_(layout=ctx.layout.makeInner())
        val = self._generate(sub, newctx, catchblock)
        sub.writeln("%s = %s" % (catchTemp, val))
        return catchTemp

    def generate_HideExpr(self, out, ctx, node):
        newctx = ctx.with_(layout=ctx.layout.makeInner())
        return self._generate(out, newctx, node.args[0])

    def generate_If(self, out, ctx, node):
        test, consq, alt = node.args
        sub = out.indent()
        ifctx = ctx.with_(layout=ctx.layout.makeInner())
        tv = self._generate(out, ifctx, test)
        ifTemp = ctx.layout.gensym("if")
        out.writeln("if _monte.booleanGuard.coerce(%s, _monte.null):" % (tv,))
        newctx = ifctx.with_(layout=ifctx.layout.makeInner())
        val = self._generate(sub, newctx, consq)
        sub.writeln("%s = %s" % (ifTemp, val))
        out.writeln("else:")
        if alt.tag.name != 'null':
            newctx = ifctx.with_(layout=ifctx.layout.makeInner())
            val = self._generate(sub, newctx, alt)
        else:
            val = '_monte.null'
        sub.writeln("%s = %s" % (ifTemp, val))
        return ifTemp

    def generate_Meta(self, out, ctx, node):
        kind = node.args[0].data
        if kind == 'Context':
            ctx.layout.metaContextExpr = True
            f = ctx.layout.frame
            if f.selfName:
                objExpr = "_m_%s_Script._m_objectExpr" % f.selfName
            else:
                objExpr = "None"
            return "_monte.StaticContext(%r, %r, %s)" % (
                f.fqnPrefix, [b.name for b in f.fields], objExpr)
        elif kind == 'State':
            f = ctx.layout.frame
            return '_monte.Map((%s))' % ', '.join('(%r, _monte.getSlot(%s, %r))' % ('&' + b.name, f.selfName, b.pyname.split('.')[1])
                                      for b in f.fields)

    def pattern_FinalPattern(self, out, ctx, ej, val, node, objname=False):
        name, guard = node.args
        guardname = "_monte.null"
        if guard.tag.name != 'null':
            guardv = self._generate(out, ctx.with_(mode=VALUE), guard)
            guardname = ctx.layout.gensym("guard")
            out.writeln("%s = %s" % (guardname, guardv))
            if ej is None:
                ej = "_monte.throw"
            val = "%s.coerce(%s, %s)" % (guardname, val, ej)
        if objname:
            b = ctx.layout.getBinding(name.args[0].data)
            out.writeln(b.generateSelfFinalSlot(val))
            return b.getValueExpr()
        else:
            pyname = ctx.layout.addFinalBinding(name.args[0].data, node, guardname)
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
            guardname = "_monte.null"
        if objname:
            b =  ctx.layout.getBinding(name)
            temp = ctx.layout.gensym(mangleIdent(name))
            out.writeln(b.generateSelfVarSlot(val, guardname, temp, ej))
        else:
            pyname = ctx.layout.addVarBinding(name, node, guardname)
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
        guardname = ctx.layout.gensym("guard")
        pyname = ctx.layout.addCustomBinding(name, node)
        out.writeln("%s = %s" % (pyname, val))
        return pyname

def ecompile(source, scope, origin="__main"):
    ast = expand(parse(source))
    f = StringIO()
    PythonWriter(ast, origin, scope).output(TextWriter(f))
    return f.getvalue().strip()
