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

def eval(source, scope=None, origin="__main"):
    if scope is None:
        from monte.runtime.scope import safeScope as scope
    name = uuid.uuid4().hex + '.py'
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

monteModules = {}
def monteImport(name):
    # The name is a String, so deref it.
    name = name.s
    # XXX hax
    path = os.path.join(os.path.dirname(__file__), '..', 'src',
                        name.replace('.', '/') + '.mt')
    if not os.path.exists(path):
        raise RuntimeError("%s does not exist" % path)
    if not monteModules.get(name):
        monteModules[name] = eval(open(path).read(), origin=name)
    return monteModules[name]
