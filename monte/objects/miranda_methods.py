from monte.objects.interfaces import ISelfless
from monte.objects.reflect import ClassDesc
def optUncall(self):
    from monte.objects.ref import Ref
    self = Ref.resolution(self)
    if self is not None and ISelfless.providedBy(self):
        spreadUncall = self.getSpreadUncall()
        return [spreadUncall[0], spreadUncall[1], spreadUncall[2:]]
    return None

def getAllegedType(self):
    from monte.objects.ref import Ref
    self = Ref.resolution(self)
    if self is None:
        return ClassDesc(type(None))
    elif isinstance(self, MonteObject):
        return self._m__getAllegedType()
    else:
        # do simplification here to hide class differences between
        # objects that should compare same, if needed
        return ClassDesc(self.__class__)


