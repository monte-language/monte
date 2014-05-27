import linecache, sys, uuid, os
from types import ModuleType as module

from monte.compiler import ecompile
from monte.expander import expand, scope
from monte.parser import parse
from monte.runtime.base import MonteObject
from monte.runtime.data import String, null
from monte.runtime.tables import ConstList, ConstMap, FlexList, FlexMap


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


class FileModuleStructure(MonteObject):
    _m_fqn = "FileModuleStructure"
    def __init__(self, filename, imports, exports, scope):
        self.filename = filename
        self.imports = imports
        self.exports = exports
        self.scope = scope

    def configure(self, params):
        if params is None:
            params = ConstMap({})
        return FileModuleConfiguration(self, params, self.scope)

    def run(self, params=None):
        return self.configure(params).export()


class SyntheticModuleStructure(MonteObject):
    _m_fqn = "SyntheticModuleStructure"
    def __init__(self, config, requires, exports):
        self.config = config
        self.requires = requires
        self.imports = requires
        self.exports = exports

    def configure(self, params):
        if params is None:
            params = ConstMap({})
        return SyntheticModuleConfiguration(self, params)

    def run(self, params=None):
        return self.configure(params).export()


class FileModuleConfiguration(MonteObject):
    _m_fqn = "FileModuleConfiguration"
    def __init__(self, structure, args, scope):
        self.structure = structure
        self.args = args
        self.scope = scope
        self.requires = []
        for c in args:
            self.requires.extend(c.requires)
        self._inputs = None
        self._contents = None

    def load(self, mapping):
        if not isinstance(mapping, (ConstMap, FlexMap)):
            raise RuntimeError("must be a mapping")
        if self._contents is not None:
            if self._inputs is not mapping:
                raise RuntimeError("you are confused somehow")
            return
        args = [self.args.d[String(name)].load(mapping)
                for name in self.structure.imports]
        self._inputs = mapping
        modname = os.path.basename(self.structure.filename)
        if modname.endswith(".mt"):
            modname = modname[:-3]
        d = eval(open(self.structure.filename).read(),
                 self.scope,
                 origin=modname)(*args)
        self._contents = ConstMap(d)


    def export(self):
        return ConstMap(dict((String(ex), ConfigurationExport(self, ex))
                             for ex in self.structure.exports))


class ConfigurationExport(MonteObject):
    _m_fqn = "ConfigurationExport"
    def __init__(self, config, name):
        self.config = config
        self.name = name
        self.requires = self.config.requires

    def load(self, mapping):
        self.config.load(mapping)
        return self.config._contents.get(String(self.name))

def extractArglist(mapping, argnames):
        argnames = set()
        for k in mapping._keys:
            if not isinstance(k, String):
                raise RuntimeError("keys must be strings")
            argnames.add(k.s)


def compareArglists(loadname, provided, required):
        if provided != required:
            missing = required - provided
            extra = provided - required
            err = "Args mismatch when loading %s." % (loadname,)
            if missing:
                err += "Missing: " + ", ".join(missing)
            if extra:
                err += "Extra: " + ", ".join(missing)
            raise RuntimeError(err)


class SyntheticModuleConfiguration(MonteObject):
    _m_fqn = "SyntheticModuleConfiguration"
    def __init__(self, structure, args):
        self.structure = structure
        self.args = args
        self.requires = self.structure.requires
        self._contents = None
        self._inputs = None

    def load(self, mapping):
        if not isinstance(mapping, (ConstMap, FlexMap)):
            raise RuntimeError("must be a mapping")
        if self._contents is not None:
            if self._inputs is not mapping:
                raise RuntimeError("you are confused somehow")
            return
        package = {}
        for k, v in self.structure.config.d.items():
            package[k] = v.load(mapping)
        self._inputs = mapping
        self._contents = ConstMap(package)

    def export(self):
        return ConstMap(dict((String(ex), ConfigurationExport(self, ex))
                             for ex in self.structure.exports))


class RequireConfiguration(MonteObject):
    _m_fqn = "Require"
    def __init__(self, name):
        self.name = name
        self.requires = [name]

    def load(self, mapping):
        if not isinstance(mapping, (ConstMap, FlexMap)):
            raise RuntimeError("must be a mapping")
        return mapping.d[self.name]


def getModuleStructure(name, location, scope, testCollector):
    """
    Search `location` for a readable module with the given name.
    """
    segs = name.split('.')
    # XXX use a file path library or something
    location = os.path.join(location, *segs)
    if os.path.isdir(location):
        return buildPackage(location, name, scope, testCollector)
    fn = location + '.mt'
    if os.path.exists(fn):
        imports, exports = readModuleFile(fn)
        return FileModuleStructure(fn, imports, exports, scope)
    else:
        raise ValueError("No module or package named '%s' in '%s'" % (name, location))


def readModuleFile(moduleFilename):
    ast = parse(open(moduleFilename).read())
    if ast.tag.name != 'Module':
        raise ValueError("'%s' is not a module" % (moduleFilename,))
    imports = []
    exports = []
    for importNode in ast.args[0].args:
        modScope = scope(expand(importNode))
        imports.extend([s.decode('ascii') for s in modScope.outNames()])
    for exportNode in ast.args[1].args:
        modScope = scope(expand(exportNode))
        exports.extend([s.decode('ascii') for s in modScope.namesUsed()])
    return imports, exports


def buildPackage(packageDirectory, name, scope, testCollector):
    from monte.runtime.scope import safeScope
    pkgfile = os.path.join(packageDirectory, 'package.mt')
    if not os.path.exists(pkgfile):
        raise ValueError("'%s' does not exist" % (pkgfile,))
    packageScriptScope = safeScope.copy()
    packageScriptScope['pkg'] = PackageMangler(name, packageDirectory, scope, testCollector)
    return eval(open(pkgfile).read(), packageScriptScope, "packageLoader")


class TestCollector(MonteObject):
    _m_fqn = "TestCollector"
    requires = ()
    def __init__(self):
        self.tests = FlexMap({})

    def run(self, prefix, tests):
        if not isinstance(tests, (ConstList, FlexList)):
            raise RuntimeError("must be a list of test functions")
        for item in tests.l:
            self.tests.put(String(prefix  + '.' + item._m_fqn), item)
        return null


class TestStructureFacet(MonteObject):
    _m_fqn = "TestStructureFacet"
    requires = ()
    def __init__(self, prefix, collector):
        self.prefix = prefix
        self.collector = collector

    def load(self, args):
        return TestConfigFacet(self.prefix, self.collector)

class TestConfigFacet(MonteObject):
    _m_fqn = "TestConfigFacet"
    requires = ()
    def __init__(self, prefix, collector):
        self.prefix = prefix
        self.collector = collector

    def run(self, tests):
        return self.collector.run(self.prefix, tests)


class NullTestCollector(MonteObject):
    _m_fqn = "NullTestCollector"
    requires = ()
    def load(self, tests):
        return self
    def run(self, tests):
        return null


class PackageMangler(MonteObject):
    _m_fqn = "PackageMangler"
    def __init__(self, name, root, scope, testCollector):
        self.name = name
        self.root = root
        self.scope = scope
        self._testCollector = testCollector

    def readFiles(self, pathstr):
        if not isinstance(pathstr, String):
            raise RuntimeError("path must be a string")
        path = pathstr.s

        def collectModules():
            root = os.path.join(self.root, path)
            for p, dirs, fns in os.walk(root):
                for fn in fns:
                    if fn.endswith(".mt") and fn != "package.mt":
                        full = '/'.join([p, fn])
                        modname = full[len(root):-3].strip('/')
                        yield modname.decode('utf-8'), full

        structures = {}
        for name, path in collectModules():
            imports, exports = readModuleFile(path)
            structures[String(name)] = FileModuleStructure(
                path, imports, exports, self.scope)

        return ConstMap(structures)

    def readPackage(self, subpkgName):
        if not isinstance(subpkgName, String):
            raise RuntimeError("expected a string")
        subpkgPath = subpkgName.s
        subpkgName = os.path.normpath(subpkgPath)
        subpkg = buildPackage(
            os.path.join(self.root, subpkgPath),
            u'.'.join([self.name, subpkgName]),
            self.scope,
            self._testCollector)
        return subpkg

    def require(self, name):
        if not isinstance(name, String):
            raise RuntimeError("name must be a string")
        return RequireConfiguration(name.s)

    def testCollector(self):
        if self._testCollector is None:
            return NullTestCollector()
        return TestStructureFacet(self.name, self._testCollector)

    def makeModule(self, mapping):
        if not isinstance(mapping, (ConstMap, FlexMap)):
            raise RuntimeError("must be a mapping")
        requires = []
        exports = []
        for k in mapping._keys:
            if not isinstance(k, String):
                raise RuntimeError("keys must be strings")
            exports.append(k.s)
            requires.extend(mapping.d[k].requires)
        return SyntheticModuleStructure(mapping, requires, exports)


def monteImport():
    def loader(name, mapping=None):
        from monte.runtime.scope import safeScope
        # The name is a String, so deref it.
        name = name.s
        if mapping is None:
            mapping = ConstMap({})
        path = os.path.join(os.path.dirname(__file__), '..', 'src')
        s = getModuleStructure(name, os.path.abspath(path), safeScope, None)
        requires = ConstMap(dict((k, RequireConfiguration(k.s)) for k in mapping.d))
        conf = s.configure(requires)
        conf.load(mapping)
        return conf._contents
    return loader
