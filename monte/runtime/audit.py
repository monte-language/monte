from monte.runtime.base import MonteObject, throw
from monte.runtime.data import String, bwrap, null, true
from monte.runtime.guards.data import booleanGuard

class Audition(MonteObject):
    _m_fqn = "Audition"
    def __init__(self, expr, bindings, obj):
        self.expr = expr
        self.bindings = bindings
        self.approvers = []
        self.obj = obj

    def ask(self, auditor):
        #XXX caching of audit results
        result = booleanGuard.coerce(auditor.audit(self), throw)
        if result is true:
            self.approvers.append(auditor)

    def getGuard(self, name):
        if not isinstance(name, String):
            raise RuntimeError("%r is not a string" % (name,))
        if name.s not in self.bindings:
            raise RuntimeError('"%s" is not a free variable in %s' %
                               (name.s, self.obj))
        return self.bindings[name.s]


class AuditChecker(MonteObject):
    _m_fqn = "__auditedBy"

    def run(self, auditor, specimen):
        return bwrap(auditor in specimen._m_auditorStamps)

theAuditor = AuditChecker()
