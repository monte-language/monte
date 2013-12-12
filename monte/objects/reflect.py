from zope.interface import Interface
from _monte import MonteObject
class ClassDesc(MonteObject):
    def __new__(cls, wrappedClass):
        if isinstance(wrappedClass, Interface):
            return InterfaceGuardSugar(wrappedClass)
        else:
            return MonteObject.__new__(cls, wrappedClass)

    def __init__(self, cls):
        self.cls = cls

    #XXX read EoCL code to figure out how this looks for GBA
