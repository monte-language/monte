from monte.runtime.base import MonteObject
from monte.runtime.data import String

class StaticContext(MonteObject):

    def __init__(self, fqn, fields, objectExpr):
        self.fqn = fqn
        self.fields = fields
        self.objectExpr = objectExpr

    def getFQNPrefix(self):
        return String(self.fqn.decode('ascii'))
