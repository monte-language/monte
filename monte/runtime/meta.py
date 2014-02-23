from monte.runtime.base import MonteObject

class StaticContext(MonteObject):

    def __init__(self, fqn, fields, objectExpr):
        self.fqn = fqn
        self.fields = fields
        self.objectExpr = objectExpr
