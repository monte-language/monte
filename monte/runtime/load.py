import linecache, sys, uuid, os
from types import ModuleType as module

from monte.compiler import ecompile


class GeneratedCodeLoader(object):
    """
    Object for use as a module's __loader__, to display generated
    source.
    """
    def __init__(self, source):
        self.source = source
    def get_source(self, name):
        return self.source


def eval(source, scope, origin="__main"):
    name = uuid.uuid4().hex
    mod = module(name)
    mod.__name__ = name
    mod._m_outerScope = scope
    pysrc, _, lastline = ecompile(source, scope, origin).rpartition('\n')
    pysrc = '\n'.join(["from monte.runtime import compiler_helpers as _monte",
                       pysrc,
                       "_m_evalResult = " + lastline])
    mod.__loader__ = GeneratedCodeLoader(pysrc)
    code = compile(pysrc, name, "exec")
    import __builtin__
    __builtin__.eval(code, mod.__dict__)
    sys.modules[name] = mod
    linecache.getlines(name, mod.__dict__)
    return mod._m_evalResult


def monteImport(vat):
    monteModules = {}

    def loader(name):
        # The name is a String, so deref it.
        name = name.s
        # XXX hax
        path = os.path.join(os.path.dirname(__file__), '..', 'src',
                            name.replace('.', '/') + '.mt')
        path = os.path.abspath(path)
        if not os.path.exists(path):
            searchPath = [os.path.dirname(path)]
            raise RuntimeError('Could not import "%s".\nSearch path was %s.'
                               % (name, searchPath))
        if not monteModules.get(name):
            monteModules[name] = eval(open(path).read(), vat.scope,
                                      origin=name)
        return monteModules[name]

    return loader
