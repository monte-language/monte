# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from monte.grammar import ParseError
from monte.expander import StaticScope
from structlike import StructBehavior, record #from epsilon

# XXX should kernel nodes be separate from the non-kernel nodes of the same name?

from pymeta.grammar import OMeta, ParseError



kernelENodeCopyGrammar = """
trans [:t <apply t>:ans] => ans
trans :x ?(x is None) => None
Assign <trans>:left <trans>:right => Assign(left, right)
Def <trans>:pattern <trans>:exit <trans>:expr => Def(pattern, exit, expr)
Escape <trans>:pattern <trans>:block <trans>:catch => Escape(pattern, block, catch)
If <trans>:test <trans>:alt <trans>:consq => If(test, alt, consq)
LiteralExpr :data => LiteralExpr(data)
NounExpr :name => NounExpr(name)
Slot :name => Slot(name)
MethodCallExpr <trans>:receiver :verb [<trans>*:args] => MethodCallExpr(receiver, verb, args)
KernelTry <trans>:tb <trans>:p <trans>:cb => Try(tb, p, cb)
Finally <trans>:tb <trans>:fb => Finally(tb, fb)
HideExpr <trans>:expr => HideExpr(expr)
Meta :name => Meta(name)
Object :doc :name <trans>:script => Object(doc, name, script)
Method :doco :verb [<trans>*:params] <trans>:guard <trans>:block => Method(doco, verb, params, guard, block)
Matcher <trans>:pattern <trans>:block => Matcher(pattern, block)

QuasiLiteralExpr :hole => QuasiLiteralExpr(hole)
QuasiPatternExpr :hole => QuasiPatternExpr(hole)
SeqExpr [<trans>*:items] => SeqExpr(items)

FinalPattern <trans>:name <trans>:guard => FinalPattern(name, guard)
IgnorePattern <trans>:guard => IgnorePattern(guard)
ListPattern [<trans>*:items] :tail ?(tail is None) => ListPattern(items, None)
SlotPattern <trans>:name <trans>:guard => SlotPattern(name, guard)
VarPattern :name <trans>:guard => VarPattern(name, guard)
ViaPattern <trans>:expr <trans>:pattern => ViaPattern(expr, pattern)
"""

try:
    from kernelnodecopier_generated import KernelENodeCopier
except ImportError:
    KernelENodeCopier = OMeta.makeGrammar(kernelENodeCopyGrammar, globals(), name="KernelENodeCopier")
KernelENodeCopier.rule_apply = KernelENodeCopier.apply
renameGrammar = """
NounExpr :name => NounExpr(self.renamings.get(name, name))
FinalPattern <trans>:noun <trans>:guard => (self.renamings.pop(noun.name, None),
                                            FinalPattern(noun, guard))[1]
VarPattern <trans>:noun <trans>:guard => (self.renamings.pop(noun.name, None),
                                          VarPattern(name, guard))[1]
SlotPattern <trans>:noun <trans>:guard => (self.renamings.pop(noun.name, None),
                             SlotPattern(name, guard))[1]
"""

try:
    from baserenamer_generated import BaseRenamer
except ImportError:
    BaseRenamer = KernelENodeCopier.makeGrammar(renameGrammar, globals(), name="BaseRenamer")

class Renamer(BaseRenamer):
    globals = globals()
    def __init__(self, text, renamings):
        BaseRenamer.__init__(self, text)
        self.renamings = renamings

    def rename(cls, ast, renamings):
        return cls([ast], renamings).apply("trans")
    rename = classmethod(rename)

class SubNode(object):
    tempCounter = 1
    scope = None
    def newTemp(self, name):
        """
        Wrong, but acceptable for the moment.
        """
        x = "%s__%s" % (name, SubNode.tempCounter)
        SubNode.tempCounter += 2
        return NounExpr(x)

    def __iter__(self):
        x = [self.__class__.__name__]
        for n in self.__names__:
            x.append(getattr(self, n))
        return iter(x)

    def _serializeList(self, items):
        for i, item in enumerate(items):
            if isinstance(item, StructBehavior):
                items[i] = item.serialize()
            elif isinstance(item, list):
                x = item[:]
                self._serializeList(x)
                items[i] = x

    def serialize(self):
        items = list(self)
        self._serializeList(items)
        return items

    def staticScope(self):
        if self.scope is None:
            self.scope = self.computeStaticScope()
        return self.scope

    def forControl(self, ej, scope):
        return Def(IgnorePattern(NounExpr("__Test")), ej, self.expand())

    def forValue(self, scope):
        return self.expand()

    def forFxOnly(self, scope):
        return self.expand()



class Node(SubNode):
    pass

class Pattern(Node):
    pass

class DelayedNode(Node):

    def expand(self):
        return self.forValue(None)

    def forValue(self, used):
        ej = self.newTemp("ej")
        exports = getExports(self.staticScope(), used)
        if (len(exports) > 0):
            ex = self.newTemp("ex")
            br = self.newTemp("br")
            rs = self.newTemp("rs")
            escExpr = Escape(
                FinalPattern(ej, None),
                SeqExpr([self.forControl(ej, used),
                         makeList([NounExpr("true")] +
                                  [Slot(x) for x in exports])]),
                Catch(
                        FinalPattern(ex, None),
                        SeqExpr([Def(FinalPattern(br, None), None,
                                     MethodCallExpr(NounExpr("Ref"),
                                                    "broken",
                                                    [ex])),
                                 makeList([NounExpr("false")] +
                                          [br] * len(exports))])))
            return SeqExpr([Def(ListPattern([FinalPattern(rs, None)] +
                                            [SlotPattern(NounExpr(x), None)
                                             for x in exports], None),
                                None, escExpr),
                            rs])
        else:
            return Escape(FinalPattern(ej, None),
                             SeqExpr([self.forControl(ej, StaticScope()),
                                      NounExpr("true")]),
                          Catch(IgnorePattern(None),
                                NounExpr("false")))


    def forFxOnly(self, used):
        ej = self.newTemp("ej")
        exports = getExports(self.staticScope(), used)
        if (len(exports) > 0):
            ex = self.newTemp("ex")
            br = self.newTemp("br")
            escExpr = Escape(
                FinalPattern(ej, None),
                SeqExpr([self.forControl(ej, used),
                         makeList([Slot(x) for x in exports])
                         ]),
                Catch(
                        FinalPattern(ex, None),
                        SeqExpr([Def(FinalPattern(br, None), None,
                                     MethodCallExpr(NounExpr("Ref"),
                                                    "broken",
                                                    [ex])),
                                 makeList([br] * len(exports))])))

            return SeqExpr([Def(ListPattern([SlotPattern(NounExpr(x), None)
                                 for x in exports], None),
                                None, escExpr)])
        else:
            return Escape(FinalPattern(ej, None),
                          self.forControl(ej, StaticScope()),
                          None)


class Character(record("character"), SubNode):
    def __getattr__(self, name):
        if name == "__printOn":
            return lambda f: getattr(f, "print")(self.character)
        else:
            raise AttributeError

class LiteralExpr(record("value"), Node):

    def computeStaticScope(self):
        return StaticScope()

    def expand(self):
        return self

    def welcome(self, visitor):
        return visitor.visitLiteralExpr(self, self.value)

class URIExpr(record("scheme body"), Node):

    def expand(self):
        return MethodCallExpr(NounExpr(self.scheme + "__uriGetter"),
                              "get",
                              [LiteralExpr(self.body)])

class URIGetter(record("scheme"), Node):

    def expand(self):
        return NounExpr(self.scheme + "__uriGetter")

class NounExpr(record("name"), Node):

    def getName(self):
        return self.name


    def asText(self):
        return self.name

    def fromSource(cls, name):
        return cls(hilbertHotelRename(name))
    fromSource = classmethod(fromSource)

    def computeStaticScope(self):
        return StaticScope(namesRead=[self.name])

    def mangle(self, suffix):
        return NounExpr(self.name + suffix)

    def expand(self):
        return self

    def welcome(self, visitor):
        return visitor.visitNounExpr(self, self.name)

class QuasiLiteralExpr(record("value"), Node):

    def computeStaticScope(self):
        return StaticScope()

    def expand(self):
        return self


class QuasiPatternExpr(record("value"), Node):

    def computeStaticScope(self):
        return StaticScope()

    def expand(self):
        return self


class QuasiText(record("pieces"), SubNode):
    pass

class QuasiExprHole(record("expr"), SubNode):
    pass

class QuasiPatternHole(record("pattern"), SubNode):
    pass

class Slot(record("name"), Node):

    def getName(self):
        return "&" + self.name

    def computeStaticScope(self):
        return StaticScope(namesRead=[self.name])

    def expand(self):
        return self

    def welcome(self, visitor):
        return visitor.visitSlotExpr(self, self.name)


class MapExpr(record("assocs"), Node):

    def expand(self):
        return MethodCallExpr(NounExpr("__makeMap"), "fromPairs",
                              [makeList([a.forValue(None)
                                        for a in self.assocs])])

class ListExpr(record("items"), Node):

    def expand(self):
        return MethodCallExpr(NounExpr("__makeList"), "run",
                              [i.forValue(None) for i in self.items])

class MapExprAssoc(record("key value"), SubNode):

    def expand(self):
        return makeList([self.key.expand(), self.value.forValue(None)])
class MapExprExport(record("name"), SubNode):

    def expand(self):
        return makeList([LiteralExpr(self.name.forValue(None).getName()),
                         self.name])

class QuasiExpr(record("name quasis"), Node):

    def expand(self):
        bits = []
        exprs = []
        for q in self.quasis:
            if isinstance(q, QuasiText):
                bits.append(q.pieces)
            elif isinstance(q, QuasiExprHole):
                bits.append("${%s}" % len(exprs))
                exprs.append(q.expr.forValue(None))
            else:
                raise ParseError(None, None)
        if self.name is None:
            name = NounExpr("simple__quasiParser")
        else:
            name = NounExpr(self.name + "__quasiParser")
        return MethodCallExpr(
            MethodCallExpr(name, "valueMaker",
                           [LiteralExpr(''.join(bits))]),
            "substitute",
            [ListExpr(exprs).forValue(None)])


class HideExpr(record("block"), Node):

    def computeStaticScope(self):
        return self.block.staticScope().hide()

    def expand(self):
        return HideExpr(self.block.forValue(None))

    def welcome(self, visitor):
        return visitor.visitHideExpr(self, self.block)

class SeqExpr(record("exprs"), Node):

    def __init__(self, inExprs):
        exprs = []
        for expr in inExprs:
            if isinstance(expr, SeqExpr):
                exprs.extend(expr.exprs)
            else:
                exprs.append(expr)
        self.exprs = exprs

    def computeStaticScope(self):
        r = self.exprs[0].staticScope()
        for e in self.exprs[1:]:
            r = r.add(e.staticScope())
        return r

    def expand(self):
        if len(self.exprs) == 0:
            return SeqExpr([NounExpr("null")])
        exprs = []
        for e in self.exprs[:-1]:
            expr = e.forFxOnly(None)
            exprs.append(expr)
        expr = self.exprs[-1].forValue(None)
        exprs.append(expr)
        return SeqExpr(exprs)

    def welcome(self, visitor):
        return visitor.visitSeqExpr(self, self.exprs)

class MethodCallExpr(record("receiver verb args"), Node):

    def computeStaticScope(self):
        s = self.receiver.staticScope()
        for arg in self.args:
            s = s.add(arg.staticScope())
        return s

    def expand(self):
        return MethodCallExpr(self.receiver.forValue(None), self.verb,
                              [a.forValue(None) for a in self.args])

    def welcome(self, visitor):
        return visitor.visitCallExpr(self, self.receiver,
                                     self.verb,
                                     self.args)

class VerbCurryExpr(record("receiver verb"), Node):

    def expand(self):
        return MethodCallExpr(NounExpr("__makeVerbFacet"), "curryCall",
                              [self.receiver.forValue(None),
                              LiteralExpr(self.verb)])

class GetExpr(record("receiver index"), Node):

    def expand(self):
        return MethodCallExpr(self.receiver, "get", self.index).forValue(None)

class FunctionCallExpr(record("receiver args"), Node):

    def expand(self):
        return MethodCallExpr(self.receiver, "run", self.args).forValue(None)

class FunctionSendExpr(record("receiver args"), Node):

    def expand(self):
        return MethodCallExpr(NounExpr("E"), "send",
                              [self.receiver.forValue(None),
                               LiteralExpr("run"),
                               makeList(self.args)])

class MethodSendExpr(record("receiver verb args"), Node):

    def expand(self):
        return MethodCallExpr(NounExpr("E"), "send",
                              [self.receiver.forValue(None),
                               LiteralExpr(self.verb),
                               makeList(self.args)])

class SendCurryExpr(record("receiver verb"), Node):

    def expand(self):
        return MethodCallExpr(NounExpr("__makeVerbFacet"), "currySend",
                              self.receiver.forValue(None),
                              LiteralExpr(self.verb))

class Minus(record("receiver"), Node):

    def expand(self):
        return MethodCallExpr(self.receiver.forValue(None), "negate", [])


class LogicalNot(record("receiver"), Node):

    def expand(self):
        return MethodCallExpr(self.receiver.forValue(None), "not", [])


class BinaryNot(record("receiver"), Node):
    def expand(self):
        return MethodCallExpr(self.receiver.forValue(None), "complement", [])

class OpNode(Node):

    def expand(self):
        opName = binops[self.__class__.__name__]
        return MethodCallExpr(self.receiver.forValue(None), opName,
                          [self.argument.forValue(None)])

class Pow(record("receiver argument"), OpNode):
    pass

class Multiply(record("receiver argument"), OpNode):
    pass

class Divide(record("receiver argument"), OpNode):
    pass

class FloorDivide(record("receiver argument"), OpNode):
    pass

class Remainder(record("receiver argument"), OpNode):
    pass

class Mod(record("receiver argument"), Node):
    def expand(self):
        rec = self.receiver.forValue(None)
        arg = self.argument.forValue(None)
        if (isinstance(rec, MethodCallExpr)
            and rec.verb == "pow"
            and len(rec.args) == 1):
            return MethodCallExpr(rec.receiver, "modPow",
                                  [rec.args[0], arg])
        else:
            return MethodCallExpr(rec, "mod", [arg])


class Add(record("receiver argument"), OpNode):
    pass

class Subtract(record("receiver argument"), OpNode):
    pass

class ShiftLeft(record("receiver argument"), OpNode):
    pass

class ShiftRight(record("receiver argument"), OpNode):
    pass

class Till(record("left right"), Node):
    def expand(self):
        return MethodCallExpr(NounExpr("__makeOrderedSpace"), "op__till",
                          [self.left.forValue(None),
                           self.right.forValue(None)])

class Thru(record("left right"), Node):
    def expand(self):
        return MethodCallExpr(NounExpr("__makeOrderedSpace"), "op__thru",
                          [self.left.forValue(None),
                           self.right.forValue(None)])

class GreaterThan(record("left right"), Node):

    def expand(self):
        return MethodCallExpr(NounExpr("__comparer"),
                          "greaterThan",
                          [self.left.forValue(None),
                           self.right.forValue(None)])


class GreaterThanEqual(record("left right"), Node):
    def expand(self):
        return MethodCallExpr(NounExpr("__comparer"),
                              "geq",
                              [self.left.forValue(None),
                               self.right.forValue(None)])


class AsBigAs(record("left right"), Node):
    def expand(self):
        return MethodCallExpr(NounExpr("__comparer"),
                              "asBigAs",
                              [self.left.forValue(None),
                               self.right.forValue(None)])


class LessThanEqual(record("left right"), Node):
    def expand(self):
        return MethodCallExpr(NounExpr("__comparer"),
                              "leq",
                              [self.left.forValue(None),
                               self.right.forValue(None)])


class LessThan(record("left right"), Node):
    def expand(self):
        return MethodCallExpr(NounExpr("__comparer"),
                              "lessThan",
                              [self.left.forValue(None),
                               self.right.forValue(None)])


class Coerce(record("specimen guard"), Node):

    def expand(self):
        return MethodCallExpr(
            MethodCallExpr(NounExpr("Guard"), "coerce",
                           [self.guard.forValue(None),
                            NounExpr("null")]),
            "coerce",
            [self.specimen.forValue(None),
             NounExpr("null")])


class MatchBind(record("specimen pattern"), DelayedNode):
    _expandedSpecimen = None
    _expandedPattern = None

    def _expandSubnodes(self):
        if self._expandedSpecimen is None:
            self._expandedSpecimen = self.specimen.forValue(None)
        if self._expandedPattern is None:
            self._expandedPattern = self.pattern.expand()
        return self._expandedSpecimen, self._expandedPattern

    def computeStaticScope(self):
        spec, patt = self._expandSubnodes()
        if isinstance(spec, DelayedNode):
            spec = self.specimen
        return spec.staticScope().add(patt.staticScope())


    def forControl(self, ej, scope, selfScope=False):
        spec, patt = self._expandSubnodes()
        return Def(patt, ej, spec)

    def forValue(self, scope):
        spec, patt = self._expandSubnodes()
        exports = getExports(spec.staticScope(), scope)
        if (1 <= len(exports)):
            sp = self.newTemp("sp")
            mbe = MatchBind(sp, patt)
            return SeqExpr([Def(FinalPattern(sp, None), None,
                                spec),
                            mbe.forValue(scope)])
        else:
            return DelayedNode.forValue(self, scope)

    def forFxOnly(self, scope):
        spec, patt = self._expandSubnodes()
        exports = getExports(spec.staticScope(), scope)
        if (len(exports) > 0):
            sp = self.newTemp("sp")
            mbe = MatchBind(sp, patt)
            return SeqExpr([Def(FinalPattern(sp, None), None,
                                spec),
                            mbe.forFxOnly(scope)])
        else:
            return DelayedNode.forFxOnly(self, scope)


class Mismatch(record("specimen pattern"), Node):

    def expand(self):
        return MethodCallExpr(MatchBind(self.specimen,
                                        self.pattern).forValue(None),
                              "not", [])

class Same(record("left right"), Node):

    def expand(self):
        return MethodCallExpr(NounExpr("__equalizer"),
                              "sameEver",
                              [self.left.forValue(None),
                               self.right.forValue(None)])




class NotSame(record("left right"), Node):
    def expand(self):
        return MethodCallExpr(
            MethodCallExpr(NounExpr("__equalizer"),
                           "sameEver",
                           [self.left.forValue(None),
                            self.right.forValue(None)]),
            "not", [])

class ButNot(record("receiver argument"), OpNode):
    pass

class BinaryOr(record("receiver argument"), OpNode):
    pass

class BinaryAnd(record("receiver argument"), OpNode):
    pass

class BinaryXor(record("receiver argument"), OpNode):
    pass

class LogicalAnd(record("left right"), DelayedNode):
    _expandedLeft = None
    _expandedRight = None

    def _staticScopeLeft(self):
        if isinstance(self.left, DelayedNode):
            return self.left.staticScope()
        else:
            return self._expandLeft().staticScope()

    def _staticScopeRight(self):
        if isinstance(self.right, DelayedNode):
            return self.right.staticScope()
        else:
            return self._expandRight().staticScope()

    def _expandLeft(self):
        if self._expandedLeft is None:
            self._expandedLeft = self.left.forValue(None)
        return self._expandedLeft

    def _expandRight(self):
        if self._expandedRight is None:
            self._expandedRight = self.right.expand()
        return  self._expandedRight

    def computeStaticScope(self):
        return self._staticScopeLeft().add(self._staticScopeRight())

    def forControl(self, ej, scope):
        if scope is None:
            leftUsed = None
        else:
            leftUsed = self._staticScopeRight().add(scope)
        return SeqExpr([self.left.forControl(ej, leftUsed),
                        self.right.forControl(ej, scope)])

class LogicalOr(record("left right"), DelayedNode):
    _expandedLeft = None
    _expandedRight = None

    def _staticScopeLeft(self):
        if isinstance(self.left, DelayedNode):
            return self.left.staticScope()
        else:
            return self._expandLeft().staticScope()

    def _staticScopeRight(self):
        if isinstance(self.right, DelayedNode):
            return self.right.staticScope()
        else:
            return self._expandRight().staticScope()

    def _expandLeft(self):
        if self._expandedLeft is None:
            self._expandedLeft = self.left.forValue(None)
        return self._expandedLeft

    def _expandRight(self):
        if self._expandedRight is None:
            self._expandedRight = self.right.expand()
        return  self._expandedRight

    def computeStaticScope(self):
        leftScope = self._staticScopeLeft()
        rightScope = self._staticScopeRight()
        return StaticScope(leftScope.namesRead | rightScope.namesRead,
                           leftScope.namesSet | rightScope.namesSet,
                           (leftScope.metaStateExprFlag or
                            rightScope.metaStateExprFlag),
                           leftScope.defNames | rightScope.defNames,
                           leftScope.varNames | rightScope.varNames)

    def forControl(self, ej, scope):

        ej2 = self.newTemp("ej")
        exports = list(getExports(self.staticScope(), scope))
        if (len(exports) > 0):
            br = self.newTemp("br")
            ex = self.newTemp("ex")
            br2 = self.newTemp("br")
            leftSlots = [Slot(x, None) for x in
                         exports + list(self._staticScopeLeft().outNames())]
            leftSlots.append(br)
            rightSlots = exports + list(self._staticScopeRight().outNames())
            rightSlots.append(br2)
            return Def(
                ListPattern([SlotPattern(NounExpr(x), None) for x in exports],
                            None),
                None,
                Escape(FinalPattern(ej2, None),
                       SeqExpr([self.left.forControl(ej2, scope),
                                MethodCallExpr(
                                  NounExpr("Ref"),
                                  "broken",
                                  [NounExpr("Right side skipped")]),
                                makeList(leftSlots)]),
                       Catch(FinalPattern(ex),
                             SeqExpr([self.right.forControl(ej, scope),
                                      MethodCallExpr(
                                        NounExpr("Ref"), "broken", [ex]),
                                      makeList(rightSlots)]))))
        else:
            return Escape(FinalPattern(ej2, None),
                         self.left.forControl(ej2, StaticScope()),
                         Catch(IgnorePattern(None),
                               self.right.forControl(ej, StaticScope())))


class Def(record("pattern exit expr"), Node):

    def computeStaticScope(self):
        result = self.pattern.staticScope()
        if self.exit is not None:
            result = result.add(self.exit.staticScope())
        return result.add(self.expr.staticScope())

    def expand(self):
        patt = self.pattern.expand()
        pattScope = patt.staticScope()
        defPatts = pattScope.defNames
        varPatts = pattScope.varNames
        rval = self.expr.forValue(None)
        rvalScope = rval.staticScope()
        if self.exit is not None:
            optEj = self.exit.forValue(None)
            rvalScope = optEj.staticScope().add(rvalScope)
        else:
            optEj = None
        rvalUsed = rvalScope.namesUsed()
        if len(varPatts & rvalUsed) != 0:
            raise ParseError("Circular 'var' definition not allowed", None)
        if len(pattScope.namesUsed() & rvalScope.outNames()) != 0:
            raise ParseError("Pattern may not use var defined on the right", None)
        conflicts = defPatts & rvalUsed
        if (0 >= len(conflicts)):
            return Def(patt, optEj, rval)
        else:
            promises = []
            resolves = []
            renamings = {}
            for oldNameStr in conflicts:
                newName = self.newTemp(oldNameStr)
                newNameR = self.newTemp(oldNameStr + "R")
                renamings[oldNameStr] = newName.name
                 # def [newName, newNameR] := Ref.promise()
                pair = [FinalPattern(newName, None),
                        FinalPattern(newNameR, None)]
                promises.append(Def(ListPattern(pair, None), None,
                                     MethodCallExpr(NounExpr("Ref"),
                                                    "promise", [])))
                resolves.append(MethodCallExpr(newNameR, "resolve",
                                                [NounExpr(oldNameStr)]))
            resName = self.newTemp("res")
            resolves.append(resName)
            if optEj is not None:
                optEj = Renamer.rename(optEj, renamings)
            rval, e = Renamer.rename(rval, renamings)
            resPatt = FinalPattern(resName, None)
            resDef = Def(resPatt, None, Def(patt, optEj, rval))
            return SeqExpr(promises + [resDef] + resolves)

    def welcome(self, visitor):
        return visitor.visitDefineExpr(self, self.pattern, self.exit,
                                       self.expr)

class Forward(record("name"), Node):

    def expand(self):
        name = self.name.expand()
        rname = self.name.mangle("__Resolver")
        return SeqExpr([Def(ListPattern([FinalPattern(name, None),
                                         FinalPattern(rname,
                                                      None)], None),
                            None,
                            MethodCallExpr(NounExpr("Ref"), "promise", [])),
                        rname])


class Assign(record("left right"), Node):

    def computeStaticScope(self):
        ss = StaticScope(namesSet=[self.left.name])
        return ss.add(self.right.staticScope())

    def expand(self):
        left = self.left.expand()
        right = self.right.forValue(None)

        if isinstance(left, NounExpr):
            return Assign(left, right)

        if isinstance(left, MethodCallExpr):
            recip = left.receiver
            setVerb = putVerb(left.verb)
            if setVerb is None:
                raise ParseError("Assignment can only be done"
                                 " to nouns and collection elements", None)
            args = left.args
        else:
            raise ParseError("Assignment can only be done"
                             " to nouns and collection elements", None)
        ares = self.newTemp("ares")
        args.append(Def(FinalPattern(ares, None),
                        None,
                        self.right.forValue(None)))
        return SeqExpr([MethodCallExpr(recip, setVerb, args),
                        ares])

    def welcome(self, visitor):
        return visitor.visitAssignExpr(self, self.left, self.right)


class VerbAssign(record("verb left args"), Node):
    def expand(self):
        updateVerb = self.verb
        return self.verbAssignExpand(updateVerb, self.args)

    def verbAssignExpand(self, updateVerb, args):
        left = self.left.expand()

        if isinstance(left, NounExpr):
            return Assign(left, MethodCallExpr(left, updateVerb,
                                               [a.forValue(None)
                                                for a in args]))
        elif isinstance(left, MethodCallExpr):
            r = self.newTemp("recip")
            prelude = Def(FinalPattern(r, None), None, left.receiver)
            seq = [prelude]
            setArgs = []
            args = [a.forValue(None) for a in args]
            for arg in left.args:
                a = self.newTemp("arg")
                seq.append(Def(FinalPattern(a, None), None, arg))
                setArgs.append(a)
            seq.extend(Assign(MethodCallExpr(r,
                                             left.verb,
                                             setArgs),
                              MethodCallExpr(MethodCallExpr(r,
                                                            left.verb,
                                                            setArgs),
                                             updateVerb,
                                             args)).forValue(None).exprs)
            return SeqExpr(seq)
        elif isinstance(left, QuasiLiteralExpr):
            raise ParseError("Can't use update-assign syntax on a \"$\"-hole. "
                             "Use explicit \":=\" syntax instead", None);
        elif isinstance(left, QuasiPatternExpr):
            raise ParseError("Can't use update-assign syntax on a \"@\"-hole. "
                             "Use explicit \":=\" syntax instead", None)
        else:
            raise ParseError("Can only update-assign nouns and calls", None)


class AugAssign(record("op left right"), VerbAssign):

    def expand(self):
        updateVerb = binops[self.op]
        return self.verbAssignExpand(updateVerb, [self.right])

class Break(record("expr"), Node):

    def expand(self):
        if self.expr is not None:
            args = [self.expr.forValue(None)]
        else:
            args = []
        return MethodCallExpr(NounExpr("__break"), "run", args)

class Continue(record("expr"), Node):

    def expand(self):
        if self.expr is not None:
            args = [self.expr.forValue(None)]
        else:
            args = []
        return MethodCallExpr(NounExpr("__continue"), "run", args)

class Return(record("expr"), Node):

    def expand(self):
        if self.expr is not None:
            args = [self.expr.forValue(None)]
        else:
            args = []
        return MethodCallExpr(NounExpr("__return"), "run", args)


class Guard(record("expr subscripts"), SubNode):

    def expand(self):
        expr = self.expr
        for sub in self.subscripts:
            expr = GetExpr(expr, sub)
        return expr.forValue(None)


class IgnorePattern(record("guard"), Pattern):

    def asText(self):
        return "_"

    def expand(self):
        if self.guard is None:
            return self
        else:
            return IgnorePattern(self.guard.forValue(None))


    def computeStaticScope(self):
        if self.guard is None:
            return StaticScope()
        else:
            return self.guard.staticScope()


    def welcome(self, visitor):
        return visitor.visitIgnorePattern(self, self.guard)

class QuasiPattern(record("name quasis"), Pattern):
    pass

class SamePattern(record("value"), Pattern):

    def expand(self):
        return ViaPattern(MethodCallExpr(NounExpr("__is"), "run",
                                         [self.value.forValue(None)]),
                          IgnorePattern(None))

class VarPattern(record("name guard"), Pattern):

    def getName(self):
        return self.name.name

    def getNoun(self):
        return self.name

    def asText(self):
        return "var " + self.getName()

    def computeStaticScope(self):
        r = StaticScope(varNames=[self.name.name])
        if self.guard is not None:
            r = r.add(self.guard.staticScope())
        return r

    def expand(self):
        if self.guard is None:
            g = None
        else:
            g = self.guard.forValue(None)
        return VarPattern(self.name.expand(), g)

    def welcome(self, visitor):
        return visitor.visitVarPattern(self, self.name, self.guard)

class BindPattern(record("name guard"), Pattern):

    def getName(self):
        return self.name.getName()

    def expand(self):
        name = self.name.expand()
        args = [name.mangle("__Resolver")]
        if self.guard is not None:
            args.append(self.guard.forValue(None))
        return ViaPattern(MethodCallExpr(NounExpr("__bind"), "run",
                                         args),
                          IgnorePattern(None))


class FinalPattern(record("name guard"), Pattern):

    def getName(self):
        return self.name.name

    def getNoun(self):
        return self.name

    def asText(self):
        return self.getName()

    def computeStaticScope(self):
        r = StaticScope(defNames=[self.name.name])
        if self.guard is not None:
            r = r.add(self.guard.staticScope())
        return r

    def expand(self):
        if self.guard is not None:
            return FinalPattern(self.name.expand(), self.guard.forValue(None))
        else:
            return FinalPattern(self.name.expand(), None)

    def welcome(self, visitor):
        return visitor.visitFinalPattern(self, self.name, self.guard)


class SlotPattern(record("name guard"), Pattern):

    def getName(self):
        return "&" + self.name.name

    def asText(self):
        return self.getName()

    def getNoun(self):
        return self.name

    def expand(self):
        if self.guard is None:
            guard = None
        else:
            guard = self.guard.forValue(None)
        return SlotPattern(self.name.forValue(None),
                           guard)

    def computeStaticScope(self):
        r = StaticScope(varNames=[self.name.name])
        if self.guard is not None:
            r = r.add(self.guard.staticScope())
        return r

    def welcome(self, visitor):
        return visitor.visitSlotPattern(self, self.name, self.guard)


class MapPatternAssoc(record("key value"), SubNode):

    def getPair(self):
        return [self.key.forValue(None),
                self.value.expand()]

class MapPatternImport(record("name"), SubNode):

    def getPair(self):
        n = self.name.forValue(None)
        return [LiteralExpr(n.getName()), n]

class MapPatternOptional(record("assoc default"), SubNode):

    def expandAssoc(self):
        k, v = self.assoc.getPair()
        return (MethodCallExpr(NounExpr("__extract"), "depr",
                               [k, self.default.forValue(None)]),
                v)


class MapPatternRequired(record("assoc"), SubNode):

    def expandAssoc(self):
        k, v = self.assoc.getPair()
        return (MethodCallExpr(NounExpr("__extract"), "run", [k]), v)

class MapPattern(record("assocs tail"), Pattern):
    def expand(self):
        if self.tail is None:
            result = IgnorePattern(NounExpr("__Empty"))
        else:
            result = self.tail.forValue(None)
        for assoc in reversed(self.assocs):
            left, right = assoc.expandAssoc()
            result = ViaPattern(left, ListPattern([right, result], None))
        return result

class ListPattern(record("patterns tail"), Pattern):

    def computeStaticScope(self):
        r = StaticScope()
        for patt in self.patterns:
            r = r.add(patt.staticScope())
        return r

    def expand(self):
        patts = [p.expand() for p in self.patterns]
        if self.tail is None:
            return ListPattern(patts,
                               None)
        else:
            patts.append(self.tail.expand())
            return ViaPattern(MethodCallExpr(NounExpr("__splitList"), "run",
                                             [LiteralExpr(len(self.patterns))]),
                              patts)

    def welcome(self, visitor):
        return visitor.visitListPattern(self, self.patterns)


class ViaPattern(record("expr pattern"), Pattern):

    def staticScope(self):
        return self.expr.staticScope().add(self.pattern.staticScope())

    def expand(self):
        return ViaPattern(self.expr.forValue(None), self.pattern.expand())

    def welcome(self, visitor):
        return visitor.visitViaPattern(self, self.expr, self.pattern)

class SuchThatPattern(record("pattern expr"), Pattern):

    def expand(self):
        inner = ViaPattern(MethodCallExpr(NounExpr("__suchThat"),
                                          "run",
                                          [self.expr.forValue(None)]),
                           IgnorePattern(None))
        return ViaPattern(NounExpr("__suchThat"),
                          ListPattern([self.pattern.expand(),
                                       inner], None))


class Interface(record("doco name guard extends implements script"), SubNode):

    def expand(self):
        name = self.name.getName()
        meta = MethodCallExpr(
            MethodCallExpr(
                    Meta("context"),
                    "getFQNPrefix",
                    []),
            "add",
            [LiteralExpr(name+"__T")])
        if self.extends is None:
            extends = []
        else:
            extends = [e.forValue(None) for e in self.extends]
        if self.implements is None:
            implements = []
        else:
            implements = [i.forValue(None) for i in self.implements]
        if isinstance(self.script, InterfaceFunction):
            script = [MessageDesc("", "to", self.script.params,
                                  self.script.guard)]
        else:
            script = self.script
        doco = LiteralExpr(self.doco or "")
        return Def(self.name.expand(),
                   None,
                   HideExpr(MethodCallExpr(NounExpr("__makeProtocolDesc"),
                                           "run",
                                           [doco, meta,
                                            ListExpr(extends).forValue(None),
                                            ListExpr(implements).forValue(None),
                                              ListExpr(script).forValue(None)
                                              ])))


class InterfaceFunction(record("params guard"), SubNode):
    pass

class MessageDesc(record("doco type verb paramDescs guard"), SubNode):

    def expand(self):
        doco = self.doco or ""
        if self.guard is None:
            guard = NounExpr("void")
        else:
            guard = self.guard.forValue(None)
        return HideExpr(MethodCallExpr(NounExpr("__makeMessageDesc"), "run",
                              [LiteralExpr(doco), LiteralExpr(self.verb),
                               ListExpr(self.paramDescs).forValue(None),
                               guard]))

class ParamDesc(record("noun guard"), SubNode):

    def expand(self):
        if self.guard is None:
            guard = NounExpr("any")
        else:
            guard = self.guard.forValue(None)
        return MethodCallExpr(NounExpr("__makeParamDesc"), "run",
                              [LiteralExpr(self.noun.getName()),
                               guard])


class Object(record("doco name script"), Node):

    def computeStaticScope(self):
        r = self.name.staticScope()
        for a in self.script.implements:
            r = r.add(a)
        r = r.add(self.script.staticScope())
        return r

    def expand(self):
        if not isinstance(self.script, Script):
            script = self.script.getScript()
        else:
            script = self.script
        return self.kernelObject(self.name, script)

    def kernelObject(self, name, script):
        if isinstance(name, BindPattern):
            unmangledName = FinalPattern(
                NounExpr(name.getName()), None)
            return Def(name.expand(), None,
                       HideExpr(self.kernelObject(unmangledName, script)))
        if script.extends is None:
            return Object(self.doco, name, script.expandScript())
        else:
            name = name.expand()
            ext = script.extends.forValue(None)
            bits = [Def(FinalPattern(NounExpr("super"), None),
                        None, ext),
                    Object(self.doco, name,
                           script.expandWithDelegate())]
            if isinstance(name, VarPattern):

                bits.append(Slot(name.getName()))
                return SeqExpr([Def(SlotPattern(name.name, None),
                                    None,
                                   HideExpr(SeqExpr(bits))),
                                name.name])
            else:
                return Def(name.expand(), None,
                           HideExpr(SeqExpr(bits)))


    def welcome(self, visitor):
        return visitor.visitObjectExpr(self, self.doco, self.name,
                                       self.script.implements, self.script)


class Script(record("extends implements methods matchers"), SubNode):

    def computeStaticScope(self):
        r = StaticScope()
        for meth in self.methods:
            r = r.add(meth.staticScope().hide())
        for matcher in self.matchers:
            r = r.add(matcher.staticScope().hide())
        return r

    def getMatchers(self):
        return self.matchers

    def getOptMethods(self):
        return self.methods

    def expandScript(self):
        return Script(None,  [i.forValue(None) for i in self.implements],
                      [m.expand() for m in self.methods],
                      [m.expand() for m in self.matchers])

    def expandWithDelegate(self):
        s = self.expandScript()
        p = self.newTemp("pair")
        s.matchers.append(Matcher(FinalPattern(p, None),
                                  MethodCallExpr(NounExpr("E"),
                                                 "callWithPair",
                                                 [NounExpr("super"), p])))
        return s

class Function(record("params guard implements block"), SubNode):

    def getScript(self):
        return Script(None, self.implements,
                      [To(None, "run", self.params, self.guard, self.block)],
                      [])


class Matcher(record("pattern block"), SubNode):

    def staticScope(self):
        r = self.pattern.staticScope()
        return r.add(self.block.staticScope()).hide()

    def expand(self):
        return Matcher(self.pattern.expand(), self.block.forValue(None))

    def getPattern(self):
        return self.pattern

    def getBody(self):
        return self.block


class To(record("doco verb params guard block"), SubNode):

    def expand(self):
        if self.guard is None:
            g = None
        else:
            g = self.guard.forValue(None)
        return Method(self.doco, self.verb,
                      [p.expand() for p in self.params], g,
                      Escape(FinalPattern(NounExpr("__return"), None),
                             SeqExpr([self.block.forValue(None),
                                      NounExpr("null")]),
                             None))


class Method(record("doco verb params guard block"), SubNode):

    def computeStaticScope(self):
        r = StaticScope()
        for param in self.params:
            r = r.add(param.staticScope())
        if self.guard is not None:
            r = r.add(self.guard.staticScope())
        return r.add(self.block.staticScope()).hide()

    def expand(self):
        if self.guard is None:
            g = None
        else:
            g = self.guard.forValue(None)
        return Method(self.doco, self.verb,
                      [p.expand() for p in self.params], g,
                      self.block.forValue(None))

    def getVerb(self):
        return self.verb

    def getPatterns(self):
        return self.params

    def getBody(self):
        return self.block



class Catch(record("pattern block"), SubNode):
    pass
class Accum(record("base accumulator"), Node):

    def expand(self):
        base = self.base.forValue(None)
        tempName = self.newTemp("accum")
        return SeqExpr([Def(VarPattern(tempName, None), None, base),
                        self.accumulator.expand(tempName),
                        tempName])

class AccumFor(record("left right expr body catcher"), SubNode):

    def expand(self, temp):
        body = self.body.expand(temp)
        return For(self.left, self.right, self.expr, body,
                   self.catcher).forValue(None)

class AccumIf(record("expr body"), SubNode):
    def expand(self, tempName):
        body = self.body.expand(tempName)
        return If(self.expr, body, NounExpr("null")).forValue(None)

class AccumWhile(record("test body catcher"), SubNode):
    def expand(self, tempName):
        body = self.body.expand(tempName)
        return While(self.test, body,
                     self.catcher).forValue(None)


class AccumOp(record("op expr"), SubNode):

    def expand(self, tempName):
        return Assign(tempName,
                      MethodCallExpr(tempName,
                                     binops[self.op],
                                     [self.expr.forValue(None)]))

class AccumCall(record("verb args"), SubNode):
    def expand(self, tempName):
        return Assign(tempName,
                      MethodCallExpr(tempName,
                                     self.verb,
                                     [a.forValue(None)
                                      for a in self.args]))


class Escape(record("pattern block catcher"), Node):

    def staticScope(self):
        ejScope = self.pattern.staticScope()
        bodyScope = self.block.staticScope()
        r = ejScope.add(bodyScope).hide()
        if self.catcher is None:
            return r
        else:
            argScope = self.catcher.pattern.staticScope()
            catcherScope = self.catcher.block.staticScope()
            return r.add(argScope.add(catcherScope)).hide()

    def expand(self):
        if self.catcher is not None:
            catcher = Catch(self.catcher.pattern.expand(),
                            self.catcher.block.forValue(None))
        else:
            catcher = None

        return Escape(self.pattern.expand(),
                      self.block.forValue(None),
                      catcher)

    def welcome(self, visitor):
        if self.catcher is not None:
            return visitor.visitEscapeExpr(self, self.pattern,
                                           self.block,
                                           self.catcher.pattern,
                                           self.catcher.block)
        else:
            return visitor.visitEscapeExpr(self, self.pattern,
                                           self.block,
                                           None, None)


class For(record("key value expr block catcher"), Node):

    def expand(self):
        block = self.block.forValue(StaticScope())
        fTemp = self.newTemp("validFlag")
        kTemp = self.newTemp("key")
        vTemp = self.newTemp("value")
        if self.key is not None:
            key = self.key.expand()
        else:
            key = IgnorePattern(None)
        value = self.value.expand()
        coll = self.expr.forValue(block.staticScope())
        if key.staticScope().add(value.staticScope()).outNames() & coll.staticScope().namesUsed():
            raise ParseError("Use on right isn't really in scope of definition", None)
        if coll.staticScope().outNames() & key.staticScope().add(value.staticScope()).namesUsed():
            raise ParseError("Use on left would get captured by definition on right", None)
        if self.catcher is not None:
            catcher = Catch(self.catcher.pattern.expand(),
                            self.catcher.block.forValue(None))
        else:
            catcher = None

        body = SeqExpr([MethodCallExpr(NounExpr("require"),
                                       "run",
                                       [fTemp,
                                        LiteralExpr("For-loop body isn't valid"
                                                    " after for-loop exits.")]),
                        If(LogicalAnd(MatchBind(kTemp, key),
                                      MatchBind(vTemp, value)),
                           Escape(FinalPattern(NounExpr("__continue"), None),
                                  SeqExpr([block, NounExpr("null")]),
                                  None),
                           None).forValue(None)])

        closure = Object("For-loop body", IgnorePattern(None),
                         Script(None, [],
                                [Method(None, "run",
                                        [FinalPattern(kTemp, None),
                                         FinalPattern(vTemp, None)],
                                        None,
                                        body)],
                                []))

        return Escape(FinalPattern(NounExpr("__break"), None),
                      SeqExpr([Def(VarPattern(fTemp, None), None,
                                   NounExpr("true")),
                               Finally(MethodCallExpr(coll,
                                                      "iterate",
                                                      [closure]),
                                         Assign(fTemp, NounExpr("false"))),
                               NounExpr("null")]),
                      catcher)

class If(record("test consq alt"), Node):

    def computeStaticScope(self):
        t = self.test.staticScope()
        c = self.consq.staticScope()
        if self.alt is None:
            e = StaticScope()
        else:
            e = self.alt.staticScope()
        return t.add(c).hide().add(e).hide()

    def expand(self):
        if isinstance(self.test, DelayedNode):
            then = self.consq.forValue(StaticScope())
            ej = self.newTemp("ej")
            if self.alt is not None:
                els = self.alt.forValue(None)
            else:
                els = NounExpr("null")
            return Escape(FinalPattern(ej, None),
                          SeqExpr([self.test.forControl(ej,
                                          self.test.staticScope()),
                                   then]),
                          Catch(IgnorePattern(None), els))
        else:
            if self.alt is not None:
                alt = self.alt.forValue(None)
            else:
                alt = NounExpr("null")
            return If(self.test.forValue(None), self.consq.forValue(None),
                      alt)


    def welcome(self, visitor):
        return visitor.visitIfExpr(self, self.test,
                                   self.consq, self.alt)

class Lambda(record("doco patterns block"), Node):

    def expand(self):
        return Object(self.doco, IgnorePattern(None), self).forValue(None)

    def getScript(self):
        return Script(None, [],
                      [Method(None, "run", self.patterns, None,
                              self.block)],
                      [])

class Meta(record("type"), Node):

    def expand(self):
        return self

class Switch(record("expr matchers"), Node):

    def expand(self):
        sp = self.newTemp("specimen")
        return HideExpr(SeqExpr([
                    Def(FinalPattern(sp, None),
                        None, self.expr),
                    matchExpr(self.matchers, sp)])).forValue(None)

class Try(record("tryblock catchers finallyblock"), Node):

    def expand(self):
        tryblock = self.tryblock.forValue(None)
        if not self.catchers:
            if not self.finallyblock:
                return HideExpr(tryblock)
            else:
                expr = self.tryblock
        elif len(self.catchers) == 1:
            expr = KernelTry(tryblock,
                             self.catchers[0].pattern.expand(),
                             self.catchers[0].block.forValue(None))
        else:
            sp = self.newTemp("specimen")
            catchers = matchExpr(self.catchers, sp).forValue(None)
            expr = KernelTry(tryblock, FinalPattern(sp, None), catchers)

        if self.finallyblock is not None:
            return Finally(expr, self.finallyblock.forValue(None))
        else:
            return expr

class KernelTry(record("tryblock pattern catchblock"), Node):

    def computeStaticScope(self):
        s = self.tryblock.staticScope()
        p = self.pattern.staticScope()
        c = self.catchblock.staticScope()
        return s.hide().add(p.add(c)).hide()

    def expand(self):
        return KernelTry(self.tryblock.forValue(None),
                         self.pattern.expand(),
                         self.catchblock.forValue(None))

    def welcome(self, visitor):
        return visitor.visitCatchExpr(self,
                                      self.tryblock,
                                      self.pattern,
                                      self.catchblock)


class Finally(record("tryblock finallyblock"), Node):

    def computeStaticScope(self):
        a = self.tryblock.staticScope()
        f = self.finallyblock.staticScope()
        return a.hide().add(f).hide()

    def expand(self):
        return Finally(self.tryblock.forValue(None),
                       self.finallyblock.forValue(None))

    def welcome(self, visitor):
        return visitor.visitFinallyExpr(self,
                                        self.tryblock,
                                        self.finallyblock)


class While(record("test block catcher"), Node):

    def expand(self):
        body = If(self.test, SeqExpr([Escape(FinalPattern(NounExpr("__continue"), None),
                                             self.block, None),
                                      NounExpr("true")]),
                  NounExpr("false")).forValue(None)
        obj = Object("While loop body", IgnorePattern(None),
                     Script(None, [],
                            [Method(None, "run", [],
                                    NounExpr("boolean"),
                                    body)], []))
        if self.catcher is None:
            catcher = None
        else:
            catcher = Catch(self.catcher.pattern.expand(),
                            self.catcher.block.forValue(None))
        return Escape(FinalPattern(NounExpr("__break"), None),
                      MethodCallExpr(NounExpr("__loop"), "run",
                                     [obj]),
                      catcher)



class When(record("args block catchers finallyblock"), Node):

    def expand(self):
        if len(self.args) > 1:
            arg = MethodCallExpr(NounExpr("promiseAllFulfilled"), "run",
                                 [ListExpr(self.args).forValue(None)])
        else:
            arg = self.args[0].forValue(None)


        if not self.catchers:
            ex = self.newTemp("ex")
            catcher = Catch(FinalPattern(ex, None),
                            MethodCallExpr(NounExpr("throw"),
                                           "run", [ex]))
            resolution = self.newTemp("resolution")
        else:
            if len(self.catchers) == 1:
                catcher = self.catchers[0]
            elif len(self.catchers) > 1:
                specimen = self.newTemp("specimen")
                catcher = Catch(FinalPattern("specimen", None),
                                matchExpr(self.catchers, specimen))
            resolution = self.newTemp("resolution")
        body = SeqExpr([Def(IgnorePattern(None),
                            None,
                            MethodCallExpr(NounExpr("Ref"), "fulfillment",
                                           [resolution])),
                        self.block])
        obj = Object("when-catch 'done' function", IgnorePattern(None),
                     Script(None, [],
                            [Method(None, "run",
                                    [FinalPattern(resolution, None)],
                                    None,
                                    Try(body, [catcher],
                                        self.finallyblock).forValue(None))],
                            []))
        return HideExpr(
            MethodCallExpr(NounExpr("Ref"), "whenResolved",
                           [arg, obj]))

class Pragma(record("verb arg"), Node):

    def expand(self):
        return NounExpr("null");

def putVerb(verb):
    if verb == "get":
        return "put"
    elif verb == "run":
        return "setRun"
    elif verb.startswith("get"):
        return "set"+verb[3:]
    elif verb.startswith("__get"):
        return "__set"+verb[5:]

binops =  {"Add": "add",
           "Subtract": "subtract",
           "Multiply": "multiply",
           "Divide": "approxDivide",
           "Remainder": "remainder",
           "Mod": "mod",
           "Pow": "pow",
           "FloorDivide": "floorDivide",
           "ShiftRight": "shiftRight",
           "ShiftLeft": "shiftLeft",
           "BinaryAnd": "and",
           "BinaryOr": "or",
           "BinaryXor": "xor",
           "ButNot": "butNot",
           }

def makeList(items):
    return MethodCallExpr(NounExpr("__makeList"), "run", items)

def hilbertHotelRename(name):
    if "__" in name:
        base, x = name.rsplit("__", 1)
        if x.isdigit():
            i = int(x)
            return "%s__%s" % (base, i*2)
    return name

def getExports(scope, used):
    outs = scope.outNames()
    if used is not None and not used.metaStateExprFlag:
        outs = outs & used.namesUsed()
    return outs

def matchExpr(matchers, var):
    result = MethodCallExpr(NounExpr("throw"), "run",
                            [MethodCallExpr(LiteralExpr("no match: "),
                                            "add", [var])])
    for m in reversed(matchers):
        result = If(MatchBind(var, m.pattern), m.block, result).expand()
    return result
