from monte.runtime.base import (MonteObject, ejector, Throw, throw, toQuote,
                                toString)
from monte.runtime.data import (MonteNull, Bool, Bytestring, Character,
                                CompositeTwine, Integer, Float, LocatedTwine,
                                SourceSpan, String, bwrap, makeSourceSpan,
                                theTwineMaker, true, false, null)
from monte.runtime.flow import monteLooper

def tryCoerce(guard, specimen):
    ej = ejector("coercion attempt")
    try:
        return guard.coerce(specimen, ej)
    except ej._m_type:
        return None
    finally:
        ej.disable()

class PrintFQN(object):
    def _printOn(self, out):
        out._m_print(self._m_fqn)

class Guard(MonteObject):
    def coerce(self, specimen, ej):
        from monte.runtime.ref import _resolution
        specimen = _resolution(specimen)
        tryej = ejector("coercion")
        try:
            return self._subCoerce(specimen, tryej)
        except tryej._m_type, p:
            problem = p.args[0]
        finally:
            tryej.disable()
        conform = getattr(specimen, '_conformTo', None)
        if conform is not None:
            newspec = conform(self)
            if newspec is not specimen:
                return self._subCoerce(newspec, ej)
        throw.eject(ej, problem)

    def supersetOf(self, other):
        return false

def deepFrozenFunc(f):
    f._m_auditorStamps = (deepFrozenGuard,)
    return f

def requireDeepFrozen(specimen, sofar, ej, root):
    from monte.runtime.audit import auditedBy
    from monte.runtime.equalizer import equalizer
    from monte.runtime.ref import _isBroken, _optProblem
    from monte.runtime.tables import ConstList
    from monte.runtime.guards.tables import listGuard
    if id(specimen) in sofar:
        return
    sofar.add(id(specimen))
    if auditedBy(deepFrozenGuard, specimen):
        return
    if _isBroken(specimen):
        requireDeepFrozen(_optProblem(specimen), sofar, ej, root)
    if selflessGuard.passes(specimen) is true:
        if transparentGuard.passes(specimen):
            portrayal = specimen._uncall()
            if not isinstance(portrayal, ConstList):
                raise RuntimeError("%s did not uncall to a list" % (toString(specimen),))
            requireDeepFrozen(portrayal.l[0], sofar, ej, root)
            requireDeepFrozen(portrayal.l[1], sofar, ej, root)
            for x in listGuard.coerce(portrayal.l[2], throw):
                requireDeepFrozen(x, sofar, ej, root)
        else:
            throw("Don't know how to deal with Selfless object " + toString(specimen))
    else:
        if equalizer.sameYet(specimen, root) is true:
            throw.eject(ej, toQuote(root) + " is not DeepFrozen")
        else:
            throw.eject(ej, "%s is not DeepFrozen because %s is not" % (toQuote(root), toQuote(specimen)))

def auditForDeepFrozen(audition, ej):
    from monte.expander import scope
    expr = audition.getObjectExpr()
    patternSS = scope(expr.args[1])
    scriptSS = scope(expr.args[3])
    fqn = audition.getFQN()
    names = scriptSS.namesUsed().butNot(patternSS.defNames)
    for name in names:
        if name in patternSS.varNames:
            throw.eject(ej, "%s in the definition of %s is a variable pattern "
                        "and therefore not DeepFrozen" % (toQuote(name), fqn))
        else:
            nameObj = String(name)
            guard = audition.getGuard(nameObj)
            if deepFrozenGuard.supersetOf(guard) is false:
                throw.eject(ej, "%s in the lexical scope of %s does not have "
                            "a guard implying DeepFrozen, but %s" % (
                                toQuote(name), fqn, toQuote(guard)))


class DeepFrozenGuard(MonteObject):
    _m_fqn = "DeepFrozen"
    def coerce(self, specimen, ej):
        requireDeepFrozen(specimen, set(), ej, specimen)
        return specimen

    def supersetOf(self, guard):
        from monte.runtime.bindings import FinalSlotGuard
        from monte.runtime.guards.tables import SpecializedConstListGuard
        if guard is deepFrozenGuard:
            return true
        if subrangeGuardMaker.get(deepFrozenGuard).passes(guard):
            return true
        if isinstance(guard, FinalSlotGuard):
            return self.supersetOf(guard.valueGuard)
        if isinstance(guard, SpecializedConstListGuard):
            return self.supersetOf(guard.elementGuard)
        if _isDataGuard(guard):
            return true
        tryej = ejector("Same guard")
        try:
            value = sameGuardMaker.matchGet(guard, tryej)
            if sameGuardMaker.get(value) == guard:
                requireDeepFrozen(value, set(), tryej, value)
                return true
        except tryej._m_type, p:
            return false
        finally:
            tryej.disable()
        return false

    def audit(self, audition):
        auditForDeepFrozen(audition, throw)
        return true

deepFrozenGuard = DeepFrozenGuard()
DeepFrozenGuard._m_auditorStamps = (deepFrozenGuard,)

#To avoid circular imports
for o in (MonteNull, Bool, Bytestring, Character, Integer, Float, String,
          SourceSpan, Throw, theTwineMaker, makeSourceSpan, monteLooper):
    o._m_auditorStamps = (deepFrozenGuard,)


class PythonTypeGuard(PrintFQN, Guard):
    _m_auditorStamps = (deepFrozenGuard,)
    def __init__(self, typ, name):
        self.typ = typ
        self._m_fqn = name
    def _subCoerce(self, specimen, ej):
        if isinstance(specimen, self.typ):
            return specimen
        else:
            throw.eject(ej, "%r is not a %s" % (specimen, self.typ,))


class AnyGuard(PrintFQN, MonteObject):
    _m_fqn = "any"
    _m_auditorStamps = (deepFrozenGuard,)
    def coerce(self, specimen, ej):
        return specimen

    def get(self, *guards):
        if not guards:
            raise RuntimeError("unneeded any[]")
        return UnionGuard(guards)

    def supersetOf(self, other):
        return true

anyGuard = AnyGuard()


class UnionGuard(MonteObject):
    _m_fqn = "any$UnionGuard"
    _m_auditorStamps = (deepFrozenGuard,)
    def __init__(self, guards):
        self.guards = guards

    def _printOn(self, out):
        #XXX pretty printing would be nice here too
        out.raw_print(u'any[')
        it = iter(self.guards)
        out.quote(next(it))
        for g in it:
            out.raw_print(u', ')
            out.quote(g)
        out.raw_print(u']')

    def coerce(self, specimen, ej):
        for guard in self.guards:
            val = tryCoerce(guard, specimen)
            if val is not None:
                return val
        throw.eject(ej, "doesn't match any of %s" % (self.guards,))

    def supersetOf(self, other):
        for g in self.guards:
            if other == g or (g.supersetOf(other) is true):
                return true
        return false


class SelflessGuard(Guard):
    _m_auditorStamps = (deepFrozenGuard,)
    def passes(self, specimen):
        return bwrap(selflessGuard in getattr(specimen, '_m_auditorStamps', ()))

    def _subCoerce(self, specimen, ej):
        if not selflessGuard in specimen._m_auditorStamps:
            throw.eject(ej, "is not Selfless")

    def __eq__(self, other):
        # to avoid MonteObject.__eq__'s invocation of equalizer
        return self is other

    def audit(self, auditor):
        #XXX Fixme
        return True

selflessGuard = SelflessGuard()

class TransparentStamp(MonteObject):
    _m_fqn = "TransparentStamp"
    _m_auditorStamps = (deepFrozenGuard,)
    def audit(self, audition):
        return true

transparentStamp = TransparentStamp()

for o in CompositeTwine, LocatedTwine, SourceSpan:
    o._m_auditorStamps = (selflessGuard, transparentStamp)

class TransparentGuard(Guard):
    _m_fqn = "Transparent"
    _m_auditorStamps = (deepFrozenGuard,)
    def passes(self, specimen):
        return transparentStamp in getattr(specimen, '_m_auditorStamps', ())

    def _subCoerce(self, specimen, ej):
        if not transparentStamp in specimen._m_auditorStamps:
            throw.eject(ej, "is not Transparent")

    def audit(self, audition):
        from monte.expander import scope
        expr = audition.getObjectExpr()
        patternSS = scope(expr.args[1])
        scriptSS = scope(expr.args[3])
        fqn = audition.getFQN()
        names = (set(scriptSS.namesUsed().butNot(patternSS.defNames)) -
                 set(audition.outerNames))
        methods = expr.args[3].args[1].args
        for m in methods:
            if m.args[1].data == "_uncall" and m.args[2].args == ():
                break
        else:
            throw("No '_uncall' method in " + fqn)

        uncallExpr = m.args[4]
        if uncallExpr.tag.name == 'Escape':
            uncallExpr = uncallExpr.args[1].args[0].args[0]
            if (uncallExpr.tag.name != 'MethodCallExpr' or
                uncallExpr.args[0].tag.name != 'NounExpr' or
                uncallExpr.args[0].args[0].data != '__return' or
                uncallExpr.args[1].data != 'run'):
                throw("Transparent auditor only smart enough to handle a "
                      "single return expression in _uncall")
            uncallExpr = uncallExpr.args[2].args[0]
        if (uncallExpr.tag.name != 'MethodCallExpr' or
            uncallExpr.args[0].tag.name != 'NounExpr' or
            uncallExpr.args[0].args[0].data != '__makeList' or
            uncallExpr.args[1].data != 'run'):
            throw("Transparent auditor expects a list literal as _uncall return value")

        arglist = uncallExpr.args[2].args[2]
        if (arglist.tag.name != 'MethodCallExpr' or
            arglist.args[0].tag.name != 'NounExpr' or
            arglist.args[0].args[0].data != '__makeList' or
            arglist.args[1].data != 'run'):
            throw("Transparent auditor expects a list literal as third item "
                  "in _uncall return value")
        args = arglist.args[2].args
        uncallNames = set()
        for a in args:
            if a.tag.name != 'NounExpr':
                continue
            uncallNames.add(a.args[0].data)
        uncallTarget = uncallExpr.args[2].args[0]
        if uncallTarget.tag.name == 'NounExpr':
            uncallNames.add(uncallTarget.args[0].data)
        unused = names - uncallNames
        if unused:
            throw("%s is not transparent because its uncall does not include: %s" %
                  (fqn, ', '.join(unused)))
        audition.ask(transparentStamp)
        return true

transparentGuard = TransparentGuard()

class SameGuard(MonteObject):
    _m_fqn = "Same$Same1"
    _m_auditorStamps = (selflessGuard, transparentStamp)
    def __init__(self, obj):
        self.obj = obj

    def _printOn(self, out):
        out.raw_print(u"Same[")
        out.quote(self.obj)
        out.raw_print(u"]")

    def getAllowed(self):
        return self.obj

    def coerce(self, specimen, ej):
        from monte.runtime.equalizer import equalizer
        if equalizer.sameYet(specimen, self.obj):
            return specimen
        else:
            throw.eject(ej, "%s is not %s" % (toQuote(specimen), toQuote(self.obj)))

    def _uncall(self):
        from monte.runtime.data import String
        from monte.runtime.tables import ConstList
        return ConstList((sameGuardMaker, String(u'get'), ConstList((self.obj,))))

sameGuardType = PythonTypeGuard(SameGuard, "SameGuard")

class SameGuardMaker(MonteObject):
    _m_fqn = "Same"
    _m_auditorStamps = (deepFrozenGuard,)
    def asType(self):
        return sameGuardType

    def get(self, obj):
        return SameGuard(obj)

    def matchGet(self, specimen, ejector):
        return sameGuardType.coerce(specimen, ejector).getAllowed()


sameGuardMaker = SameGuardMaker()



class SubrangeGuardMaker(MonteObject):
    _m_fqn = "SubrangeGuardMaker"
    _m_auditorStamps = (deepFrozenGuard,)
    def get(self, superrangeGuard):
        return SubrangeGuard(superrangeGuard)


class SubrangeGuard(MonteObject):
    _m_fqn = "SubrangeGuard"
    _m_auditorStamps = (deepFrozenGuard, transparentStamp, selflessGuard)

    def __init__(self, superrangeGuard):
        self.superrangeGuard = superrangeGuard

    def _uncall(self):
        from monte.runtime.data import String
        from monte.runtime.tables import ConstList
        return ConstList((subrangeGuardMaker, String(u"get"),
                          ConstList((self.superrangeGuard,))))

    def coerce(self, specimen, ejector):
        from monte.runtime.audit import auditedBy
        if auditedBy(self, specimen):
            return specimen
        c = specimen._conformTo(self)
        if auditedBy(self, c):
            return c
        throw.eject(ejector, "%s isn't approved as a SubrangeGuard[%s]" % (
            toQuote(specimen), toQuote(self.superrangeGuard)))

    def passes(self, specimen):
        from monte.runtime.audit import auditedBy
        return auditedBy(self, specimen)

    def _printOn(self, out):
        out.quote(subrangeGuardMaker)
        out.raw_print(u"[")
        out.quote(self.superrangeGuard)
        out.raw_print(u"]")

    def audit(self, audition):
        from monte.runtime.bindings import FinalSlotGuard
        expr = audition.getObjectExpr()
        methods = expr.args[3].args[1].args
        fqn = audition.getFQN()
        for m in methods:
            verb = m.args[1]
            if verb.data == "coerce":
                guardTerm = m.args[3]
                if guardTerm.tag.name == "NounExpr":
                    noun = guardTerm.args[0].data
                    resultGuardSlotGuard = audition.getGuard(String(noun))
                    if isinstance(resultGuardSlotGuard, FinalSlotGuard):
                        guard2 = resultGuardSlotGuard.getValueGuard()
                        if isinstance(guard2, SameGuard):
                            resultGuard = guard2.getAllowed()
                            if resultGuard == self.superrangeGuard:
                                return true
                            m = getattr(self.superrangeGuard, "supersetOf")
                            if m is not None and m(resultGuard):
                                return true
                            else:
                                throw("%s does not have a result guard implying %s, but %s" %(
                                    fqn, toQuote(self.superrangeGuard), toQuote(resultGuard)))
                    throw("%s does not have a determinable result guard, but <& %s> :%s" % (
                        fqn, noun, resultGuardSlotGuard))
                throw("%s does not have a noun as its `coerce` result guard" % (fqn,))
        else:
            throw("%s has no `coerce` method" % (fqn,))

subrangeGuardMaker = SubrangeGuardMaker()

class NullOkGuard(Guard):
    _m_fqn = "nullOk"
    _m_auditorStamps = (deepFrozenGuard,)
    def coerce(self, specimen, ej):
        if specimen is not null:
            throw.eject(ej, "must be null")
        return null

    def _printOn(self, out):
        out.raw_print(u"nullOk")

    def get(self, subGuard):
        return SpecializedNullOkGuard(subGuard)


class SpecializedNullOkGuard(Guard):
    _m_fqn = "nullOk"
    _m_auditorStamps = (deepFrozenGuard,)
    def __init__(self, subGuard):
        self.subGuard = subGuard

    def coerce(self, specimen, ej):
        if specimen is null:
            return null
        return self.subGuard.coerce(specimen, ej)

    def _printOn(self, out):
        out.raw_print(u"nullOk[")
        out._m_print(self.subGuard)
        out.raw_print(u"]")

nullOkGuard = NullOkGuard()


def _isDataGuard(g):
    from monte.runtime.guards.data import (booleanGuard, voidGuard, intGuard,
                                           floatGuard, charGuard, stringGuard)
    return any(g is dg for dg in  (booleanGuard, voidGuard, intGuard,
                                   floatGuard, charGuard, stringGuard))

class ParamDesc(MonteObject):
    _m_auditorStamps = (deepFrozenGuard,)

    def __init__(self, name, guard):
        self.name = name
        self.guard = guard


class MessageDesc(MonteObject):
    _m_auditorStamps = (deepFrozenGuard,)
    def __init__(self, doc, verb, params, resultGuard):
        self.doc = doc
        self.verb = verb
        self.params = params
        self.resultGuard = resultGuard

class ProtocolDesc(MonteObject):
    _m_auditorStamps = (deepFrozenGuard,)
    def __init__(self, doc, fqn, supers, auditors, msgs):
        self.doc = doc
        self.fqn = self._m_fqn = fqn
        self.supers = supers
        self.auditors = auditors
        self.messages = msgs

    def audit(self, audition):
        return true

    def coerce(self, specimen, ej):
        from monte.runtime.audit import auditedBy
        if auditedBy.run(self, specimen) is true:
            return specimen
        else:
            conformed = specimen._conformTo(self)
            if auditedBy.run(self, conformed):
                return conformed
            else:
                throw.eject(ej, "Not stamped by %s" % (self,))

    @classmethod
    def makePair(cls, doc, fqn, supers, auditors, msgs):
        from monte.runtime.tables import ConstList
        stamp = InterfaceStamp(fqn)
        ig = InterfaceGuard(doc, fqn, supers, auditors, msgs, stamp)
        return ConstList([ig, stamp])


class InterfaceStamp(MonteObject):
    _m_auditorStamps = (deepFrozenGuard,)
    def __init__(self, fqn):
        self._m_fqn = fqn.s

    def audit(self, audition):
        return true


class InterfaceGuard(MonteObject):
    _m_auditorStamps = (deepFrozenGuard,)
    def __init__(self, doc, fqn, supers, auditors, msgs, stamp):
        self.doc = doc
        self.fqn = fqn
        self.supers = supers
        self.auditors = auditors
        self.messages = msgs
        self.stamp = stamp
        self._m_fqn = fqn.s

    def coerce(self, specimen, ej):
        from monte.runtime.audit import auditedBy
        if auditedBy.run(self.stamp, specimen) is true:
            return specimen
        else:
            conformed = specimen._conformTo(self)
            if auditedBy.run(self, conformed):
                return conformed
            else:
                throw.eject(ej, "Not stamped by %s" % (self,))
