import linecache, sys, uuid, os
from types import ModuleType as module

from monte.compiler import ecompile
from monte.expander import expand, scope
from monte.parser import parse
from monte.runtime.base import MonteObject
from monte.runtime.data import String, Twine, null
from monte.runtime.tables import ConstList, ConstMap, FlexList, FlexMap


# XXX really should be guards -- but all this code is gonna go away, anyhow.
def typecheck(specimen, classes):
    from monte.runtime.ref import _resolution
    specimen = _resolution(specimen)
    if not isinstance(specimen, classes):
        raise RuntimeError("%r is not a %r" % (specimen, classes))
    return specimen

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
    name = uuid.uuid4().hex
    mod = module(name)
    mod.__name__ = name
    mod._m_outerScope = scope
    pysrc, _, lastline = ecompile(source, scope, origin).rpartition('\n')
    pysrc = '\n'.join(["from monte.runtime import compiler_helpers as _monte",
                       pysrc.encode('utf-8'),
                       "_m_evalResult = " + lastline.encode('utf-8')])
    mod.__loader__ = GeneratedCodeLoader(pysrc)
    code = compile(pysrc, name, "exec")
    import __builtin__
    __builtin__.eval(code, mod.__dict__)
    sys.modules[name] = mod
    linecache.getlines(name, mod.__dict__)
    return mod._m_evalResult


class ModuleMap(ConstMap):
    _m_fqn = "ModuleMap"
    def __init__(self, configs, d, keys=None):
        ConstMap.__init__(self, d, keys=None)
        self.configs = configs

    def _m_or(self, behind):
        newconfigs = self.configs + getattr(behind, 'configs', ())
        newmap = ConstMap._m_or(self, behind)
        return ModuleMap(newconfigs, newmap.d, newmap._keys)

    def getConfigs(self):
        return ConstList(tuple(self.configs))

    # XXX add maker and uncall


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

    def _printOn(self, out):
        out.raw_print("<Module %s>" % (self.filename,))


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
        self.requires = set()
        for c in args:
            self.requires.update(c.requires)
        self._inputs = None
        self._contents = None

    def load(self, mapping):
        mapping = typecheck(mapping, (ConstMap, FlexMap))
        # XXX reorganize to be less side-effect-y
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
        return ModuleMap((self,), dict((String(ex), ConfigurationExport(self, ex))
                                       for ex in self.structure.exports))

    def _printOn(self, out):
        out.raw_print(u"<")
        out._m_print(self.structure)
        out.raw_print(u"([")
        if self.structure.imports:
            for name in self.structure.imports[:-1]:
                out.raw_print(u"%s => " % (name,))
                out._m_print(self.args.d[String(name)])
                out.raw_print(u", ")
            out.raw_print(u"%s => " % (self.structure.imports[-1],))
            out._m_print(self.args.d[String(self.structure.imports[-1])])
        out.raw_print(u"])")


class ConfigurationExport(MonteObject):
    _m_fqn = "ConfigurationExport"
    def __init__(self, config, name):
        self.config = config
        self.name = name
        self.requires = self.config.requires

    def load(self, mapping):
        self.config.load(mapping)
        return self.config._contents.get(String(self.name))

    def _printOn(self, out):
        out._m_print(self.config)
        out.raw_print(u"::" + self.name)


def extractArglist(mapping, argnames):
        argnames = set()
        for k in mapping._keys:
            k = typecheck(k, Twine).bare().s
            argnames.add(k)


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
        mapping = typecheck(mapping, (ConstMap, FlexMap))
        # XXX reorganize to be less side-effect-y
        if self._contents is not None:
            if self._inputs is not mapping:
                raise RuntimeError("you are confused somehow")
            return
        package = {}
        for k, v in self.structure.config.d.items():
            package[k] = v.load(mapping)

        for config in getattr(self.structure.config, 'configs', ()):
            config.load(mapping)
        self._inputs = mapping
        self._contents = ConstMap(package)

    def export(self):
        return ModuleMap((self,), dict((String(ex), ConfigurationExport(self, ex))
                                    for ex in self.structure.exports))


class RequireConfiguration(MonteObject):
    _m_fqn = "Require"
    def __init__(self, name):
        self.name = name
        self.requires = set([name])

    def load(self, mapping):
        mapping = typecheck(mapping, (ConstMap, FlexMap))
        return mapping.d[String(self.name)]


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

    # TODO decide if the boot scope is sufficient for package scripts; it
    # should be, nothing fancy goes on in them currently
    from monte.runtime.scope import bootScope
    pkgfile = os.path.join(packageDirectory, 'package.mt')
    if not os.path.exists(pkgfile):
        raise ValueError("'%s' does not exist" % (pkgfile,))
    packageScriptScope = bootScope.copy()
    packageScriptScope['pkg'] = PackageMangler(name, packageDirectory, scope, testCollector)
    return eval(open(pkgfile).read(), packageScriptScope, "packageLoader")


class TestCollector(MonteObject):
    _m_fqn = "TestCollector"
    requires = set(())
    def __init__(self):
        self.tests = FlexMap({})

    def run(self, prefix, tests):
        tests = typecheck(tests, (ConstList, FlexList))
        for item in tests.l:
            if prefix and not prefix.endswith('.'):
                prefix += '.'
            self.tests.put(String(prefix + item._m_fqn.replace('$', '.')), item)
        return null


class TestStructureFacet(MonteObject):
    _m_fqn = "TestStructureFacet"
    requires = set(())
    def __init__(self, prefix, collector):
        self.prefix = prefix
        self.collector = collector

    def load(self, args):
        return TestConfigFacet(self.prefix, self.collector)

class TestConfigFacet(MonteObject):
    _m_fqn = "TestConfigFacet"
    requires = set(())
    def __init__(self, prefix, collector):
        self.prefix = prefix
        self.collector = collector

    def run(self, tests):
        return self.collector.run(self.prefix, tests)


class NullTestCollector(MonteObject):
    _m_fqn = "NullTestCollector"
    requires = set(())
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
        path = typecheck(pathstr, Twine).bare().s

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
            structures[String(name)] = FileModuleStructure(path, imports,
                                                           exports, self.scope)

        return ConstMap(structures)

    def readFile(self, pathstr):
        path = typecheck(pathstr, Twine).bare().s
        fullpath = os.path.join(self.root, path)
        imports, exports = readModuleFile(fullpath)
        return FileModuleStructure(fullpath, imports, exports, self.scope)

    def readPackage(self, subpkgName):
        subpkgPath = typecheck(subpkgName, Twine).bare().s
        subpkgName = os.path.normpath(subpkgPath)
        if self.name:
            name = u'.'.join([self.name, subpkgName])
        else:
            name = subpkgName
        subpkg = buildPackage(
            os.path.join(self.root, subpkgPath),
            name,
            self.scope,
            self._testCollector)
        return subpkg

    def require(self, name):
        name = typecheck(name, Twine).bare().s
        return RequireConfiguration(name)

    def testCollector(self):
        if self._testCollector is None:
            return NullTestCollector()
        return TestStructureFacet(self.name, self._testCollector)

    def makeModule(self, mapping):
        mapping = typecheck(mapping, (ConstMap, FlexMap))
        requires = set([])
        exports = []
        for k in mapping._keys:
            k = typecheck(k, Twine)
            exports.append(k.bare().s)
            requires.update(mapping.d[k].requires)
        return SyntheticModuleStructure(mapping, requires, exports)


def monteImport(scope):
    def loader(name, mapping=None):
        name = name.s
        if mapping is None:
            mapping = ConstMap({})
        path = os.path.join(os.path.dirname(__file__), '..', 'src')
        s = getModuleStructure(name, os.path.abspath(path), scope, None)
        requires = ConstMap(dict((k, RequireConfiguration(k.bare().s))
                                 for k in mapping.d))
        conf = s.configure(requires)
        conf.load(mapping)
        return conf._contents
    return loader
