from monte.runtime.base import MonteObject, throw
from monte.runtime.data import bwrap, null, true
from monte.runtime.guards.data import booleanGuard

class Audition(MonteObject):
    def __init__(self, expr, bindings):
        self.expr = expr
        self.bindings = bindings
        self.approvers = []

    def ask(self, auditor):
        #XXX caching of audit results
        result = booleanGuard.coerce(auditor.audit(self), throw)
        if result is true:
            self.approvers.append(auditor)


def collectBindings(obj):
    return null

class AuditChecker(MonteObject):
    _m_fqn = "__auditedBy"

    def run(self, auditor, specimen):
        return bwrap(auditor in specimen._m_auditorStamps)

theAuditor = AuditChecker()
