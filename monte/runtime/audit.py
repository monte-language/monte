from monte.runtime.base import MonteObject, throw
from monte.runtime.data import Twine, bwrap, true
from monte.runtime.guards.base import deepFrozenGuard
from monte.runtime.guards.data import booleanGuard, twineGuard


class Audition(MonteObject):
    _m_fqn = "Audition"

    def __init__(self, fqn, expr, bindings, obj, outerNames, cache):
        self.expr = expr
        self.bindings = bindings
        self.approvers = []
        self.obj = obj
        self.fqn = fqn
        self._active = True
        self.outerNames = outerNames
        self.askedLog = []
        self.guardLog = []
        self.auditorCache = cache


    def ask(self, auditor):
        if not self._active:
            raise RuntimeError("audition is out of scope")
        doCaching = deepFrozenGuard in auditor._m_auditorStamps
        cached = False
        if doCaching:
            if id(auditor) in self.auditorCache:
                answer, asked, guards = self.auditorCache[id(auditor)]

                for name, value in guards:
                    namestr = twineGuard.coerce(name, throw).bare()
                    if not (self.bindings.get(namestr.s) == value):
                        break
                else:
                    cached = True

        if cached:
            for a in asked:
                self.ask(a)
            if answer is true:
                self.approvers.append(auditor)
            return answer
        else:
            prevlogs = self.askedLog, self.guardLog
            self.askedLog = []
            self.guardLog = []
            try:
                #print "%s auditing %s" % (auditor, self.fqn)
                result = booleanGuard.coerce(auditor.audit(self), throw)
                if doCaching and self.guardLog is not None:
                    #print "audit cached:", result
                    self.auditorCache[id(auditor)] = (result, self.askedLog[:], self.guardLog[:])
                if result is true:
                    #print self.fqn, "approved by", auditor
                    self.approvers.append(auditor)
            finally:
                self.askedLog, self.guardLog = prevlogs
            return result

    def getObjectExpr(self):
        return self.expr

    def getGuard(self, name):
        n = twineGuard.coerce(name, throw).bare().s
        if n not in self.bindings:
            self.guardLog = None
            raise RuntimeError('"%s" is not a free variable in %s' %
                               (name, str(self.obj)))
        answer = self.bindings[n]
        if self.guardLog is not None:
            if deepFrozenGuard in answer._m_auditorStamps:
                self.guardLog.append((name, answer))
            else:
                self.guardLog = None
        return answer

    def getFQN(self):
        return self.fqn

    def getOuterNames(self):
        return self.outerNames


class AuditChecker(MonteObject):
    _m_fqn = "__auditedBy"
    _m_auditorStamps = (deepFrozenGuard,)

    def run(self, auditor, specimen):
        return bwrap(auditor in getattr(specimen, "_m_auditorStamps", ()))


auditedBy = AuditChecker()
