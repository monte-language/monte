import ctypes, sys
from monte.nodes import Character
glib = ctypes.CDLL("libglib-2.0.so", mode=ctypes.RTLD_GLOBAL)
gio = ctypes.CDLL("libgio-2.0.so", mode=ctypes.RTLD_GLOBAL)

e = ctypes.CDLL("libecru.so", mode=ctypes.RTLD_GLOBAL)
e.ecru_set_up()


class GString(ctypes.Structure):
    _fields_ = [("str", ctypes.c_char_p),
                ("len", ctypes.c_int),
                ("allocated_len", ctypes.c_int)]
glib.g_string_new_len.restype = ctypes.POINTER(GString)
glib.g_string_new_len.argtypes = (ctypes.c_char_p, ctypes.c_int)
class EScript(ctypes.Structure):
    pass

class ERef(ctypes.Structure):
    pass

class EData(ctypes.Union):
    _fields_ = [("fixnum", ctypes.c_long),
                  ("bignum", ctypes.c_void_p), # mpz_t *
                  ("chr", ctypes.c_ushort),
                  ("gstring", ctypes.POINTER(GString)),
                  ("float64", ctypes.POINTER(ctypes.c_double)),
                  ("refs", ctypes.POINTER(ERef)),
                  ("other", ctypes.c_void_p)]


class ESelector(ctypes.Structure):
    _fields_ = [("verb", ctypes.c_char_p),
                ("arity", ctypes.c_int)]

ECallFunc = ctypes.CFUNCTYPE(ERef, ERef, ESelector, ctypes.POINTER(ERef))
EExecFunc = ctypes.CFUNCTYPE(ERef, ERef, ctypes.POINTER(ERef))

class EMethod(ctypes.Structure):
    _fields_ = [("verb", ctypes.c_char_p),
                ("exec_func", EExecFunc)]

ERef._fields_ = [("script", ctypes.POINTER(EScript)),
                 ("data", EData)]

EScript._fields_ = [("num_methods", ctypes.c_int),
                    ("methods", ctypes.POINTER(EMethod)),
                    ("opt_otherwise", ctypes.POINTER(ECallFunc)),
                    ("typeName", ctypes.POINTER(GString))]

class FlexListData(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int),
                ("capacity", ctypes.c_int),
                ("elements", ctypes.POINTER(ERef))]

class HandlerTableEntry(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ubyte),
                ("stackLevel", ctypes.c_ubyte),
                ("target", ctypes.c_int),
                ("start", ctypes.c_int),
                ("end", ctypes.c_int)]

class Method(ctypes.Structure):
    _fields_ = [("verb", ctypes.c_void_p),
                ("code", ctypes.POINTER(ctypes.c_ubyte)),
                ("length", ctypes.c_int),
                ("num_locals", ctypes.c_ubyte),
                ("handlerTable", ctypes.POINTER(HandlerTableEntry)),
                ("handlerTableLength", ctypes.c_ubyte)]

class Matcher(ctypes.Structure):
    _fields_ = [("pattern", ctypes.POINTER(ctypes.c_ubyte)),
                ("patternLength", ctypes.c_int),
                ("body", ctypes.POINTER(ctypes.c_ubyte)),
                ("bodyLength", ctypes.c_int),
                ("num_locals", ctypes.c_ubyte),
                ("patternHandlerTable", ctypes.POINTER(HandlerTableEntry)),
                ("patternHandlerTableLength", ctypes.c_ubyte),
                ("bodyHandlerTable", ctypes.POINTER(HandlerTableEntry)),
                ("bodyHandlerTableLength", ctypes.c_ubyte)]


class Script(ctypes.Structure):
    _fields_ = [("num_methods", ctypes.c_int),
                ("methods", ctypes.POINTER(Method)),
                ("num_matchers", ctypes.c_int),
                ("matchers", ctypes.POINTER(Matcher)),
                ("num_slots", ctypes.c_int)]

class Module(ctypes.Structure):
    _fields_ = [("constants", ctypes.POINTER(ERef)),
                ("constantsLength", ctypes.c_ubyte),
                ("selectors", ctypes.POINTER(ESelector)),
                ("selectorsLength", ctypes.c_ubyte),
                ("scope", ctypes.POINTER(ERef)),
                ("scopeLength", ctypes.c_ubyte),
                ("scripts", ctypes.POINTER(ctypes.POINTER(Script))),
                ("scriptsLength", ctypes.c_ubyte),
                ("stackDepth", ctypes.c_ubyte)]

class ScopeData(ctypes.Structure):
    _fields_ = [("names", ctypes.POINTER(ctypes.c_char_p)),
                ("slots", ctypes.POINTER(ERef)),
                ("size", ctypes.c_int)]

class Stackframe(ctypes.Structure):
    pass

Stackframe._fields_ = [("module", ctypes.POINTER(Module)),
                       ("pc", ctypes.c_int),
                       ("scriptNum", ctypes.c_int),
                       ("methodNum", ctypes.c_int),
                       ("codeState", ctypes.c_ubyte),
                       ("patternEjectorNumber", ctypes.c_int),
                       ("ejectorBoxes", ctypes.POINTER(ctypes.POINTER(ERef))),
                       ("stackBottom", ctypes.POINTER(ERef)),
                       ("stackTop", ctypes.POINTER(ERef)),
                       ("locals", ctypes.POINTER(ERef)),
                       ("frame", ctypes.POINTER(ERef)),
                       ("keepLast", ctypes.c_ubyte),
                       ("parent", ctypes.POINTER(Stackframe))]

fixnumScript = ctypes.pointer(EScript.in_dll(e, "e__fixnum_script"))
bignumScript = ctypes.pointer(EScript.in_dll(e, "e__bignum_script"))
float64Script = ctypes.pointer(EScript.in_dll(e, "e__float64_script"))
nullScript = ctypes.pointer(EScript.in_dll(e, "e__null_script"))
booleanScript = ctypes.pointer(EScript.in_dll(e, "e__boolean_script"))
charScript = ctypes.pointer(EScript.in_dll(e, "e__char_script"))
stringScript = ctypes.pointer(EScript.in_dll(e, "e__string_script"))
constlistScript = ctypes.pointer(EScript.in_dll(e, "e__constlist_script"))
readerScript = ctypes.pointer(EScript.in_dll(e, "e__reader_script"))


_e_call_proto = ctypes.PYFUNCTYPE(ERef, ERef, ctypes.POINTER(ESelector), ctypes.POINTER(ERef))
_e_call = _e_call_proto(("e_call", e))

e.ecru_vm_execute.restype = ERef
e.ecru_vm_execute.argtypes = (ctypes.c_char, ctypes.c_char, ctypes.c_char,
                               ctypes.POINTER(ERef), ctypes.POINTER(Module),
                               ctypes.POINTER(ERef), ctypes.c_int,
                               ctypes.c_void_p)

e.ecru_vm_execute_interactive.restype = ERef
e.ecru_vm_execute_interactive.argtypes = (ctypes.POINTER(ERef), ctypes.c_int,
                                           ctypes.c_char, ctypes.c_char, ctypes.c_char,
                                           ctypes.POINTER(ERef), ctypes.POINTER(Module),
                                           ctypes.POINTER(ERef), ctypes.c_int,
                                           ctypes.c_void_p)

e.e_malloc_atomic.restype = ctypes.c_void_p


e.e_make_selector.argtypes = (ctypes.POINTER(ESelector), ctypes.c_char_p,
                              ctypes.c_int)

e.e_constlist_from_array.restype = ERef
e.e_constlist_from_array.argtypes = (ctypes.c_int, ctypes.POINTER(ERef))

e.e_ref_state.argtypes = (ERef,)
e.e_ref_state.restype = ctypes.c_int

e.e_scope_getEvalContext.restype = ctypes.POINTER(ERef)
e.e_scope_getEvalContext.argtypes = (ERef,)

e.ecru_load_bytecode.restype = ctypes.POINTER(Module)

e.e_intern.restype = ctypes.c_void_p
e.e_intern.argtypes = (ctypes.c_char_p,)
import__uriGetter = ERef.in_dll(e, "e_import__uriGetter")
def e_import(modName):
    return e_call(import__uriGetter, "get", modName)

def newSelector(verb, arity):
    s = ESelector()
    sel = ctypes.pointer(s)
    e.e_make_selector(sel, verb, arity)
    return sel

def newFixnum(val):
    d = EData()
    d.fixnum = val
    return ERef(fixnumScript, d)

def newChar(val):
    d = EData()
    d.chr = ord(val)
    return ERef(charScript, d)

def newString(val):
    d = EData()
    d.gstring = glib.g_string_new_len(val, len(val))
    return ERef(stringScript, d)

def newFloat(val):
    p = ctypes.cast(e.e_malloc_atomic(ctypes.sizeof(ctypes.c_double)),
                                      ctypes.POINTER(ctypes.c_double))
    p.contents = ctypes.c_double(val)
    d = EData()
    d.float64 = p
    return ERef(float64Script, d)

def newConstList(val):
    convertedVals = [toEObject(x) for x in val]
    a = (ERef * len(val))(*convertedVals)
    return e.e_constlist_from_array(len(val), a)



class EObjectWrapper(object):
    def __init__(self, val):
        self._contents = val

    def __getattr__(self, name):
        def wrapper(*args):
            return e_call(self._contents, name, *args)
        return wrapper

wrapeobject_proto = ctypes.PYFUNCTYPE(ctypes.py_object, ERef)

def _wrapEObject(obj):
    return EObjectWrapper(obj)

wrapEObject = wrapeobject_proto(_wrapEObject)

bridge = ctypes.CDLL("libmonte_bridge.so")

bridge.monte_bridge_set_up.argtypes = (ctypes.py_object, wrapeobject_proto, ctypes.py_object)
bridge.monte_bridge_set_up(EObjectWrapper, wrapEObject, Character)

fromeobject_proto = ctypes.PYFUNCTYPE(ctypes.py_object, ERef)
toeobject_proto = ctypes.PYFUNCTYPE(ERef, ctypes.py_object)
fromEObject = fromeobject_proto(("e_to_py", bridge))
_toEObject = toeobject_proto(("py_to_e", bridge))


def toEObject(obj):
    if isinstance(obj, ERef):
        return obj
    else:
        return _toEObject(obj)


monte_wrap_proto = ctypes.PYFUNCTYPE(ERef, ctypes.py_object)
monte_wrap = monte_wrap_proto(("monte_wrap", bridge))

bridge.monte_unwrap.restype = ctypes.py_object
bridge.monte_unwrap.argtypes = (ERef,)

def openFile(path):
    f = gio.g_file_new_for_path(path)
    ifs = gio.g_file_read(f, 0, 0)
    if ifs == 0:
        raise RuntimeError("couldn't open file")
    d = EData()
    d.other = ifs
    return ERef(readerScript, d)

def loadModule(ef):
    return e.ecru_load_bytecode(ef, e_safeScope)


e_null = ERef(nullScript)
e_true = newFixnum(1)
e_true.script = booleanScript
e_false = newFixnum(0)
e_false.script = booleanScript
e_safeScope = ERef.in_dll(e, "e_safeScope")
e_privilegedScope = ERef.in_dll(e, "e_privilegedScope")
e_thrown_problem = ERef.in_dll(e, "e_thrown_problem")
e_stdin = ERef.in_dll(e, "e_stdin")
e_stdout = ERef.in_dll(e, "e_stdout")
e_do_println = newSelector("println", 1)
e_do_print = newSelector("print", 1)
e_run_1 = newSelector("run", 1)

e.e_make_string_writer.restype = ERef
e.e_string_writer_get_string.restype = ERef
e.e_string_writer_get_string.argtypes = (ERef,)

def e_println(where, what):
    return _e_call(where, e_do_println, ctypes.pointer(what))

def e_print(where, what):
    return _e_call(where, e_do_print, ctypes.pointer(what))

def e_call(receiver, verb, *args):
    sel = newSelector(verb, len(args))
    AA = ERef * len(args)
    argA = AA(*[toEObject(a) for a in args])
    res = _e_call(receiver, sel, argA)
    if res.script:
        return fromEObject(res)
    else:
        e_println(e_stdout, e_thrown_problem)
        raise RuntimeError()

def runModule(path):
    ef = openFile(path)
    m = loadModule(ef)
    res = e.ecru_vm_execute('\0', '\0', '\0', None, m, None, 0, None)
    if res.script:
        return res
    else:
        e_println(e_stdout, e_thrown_problem)

_compile = None
_dump = None
_bc = None
def packHandlerTable(ht):
    if (ht is not None and len(ht) > 0):
        AHT = (HandlerTableEntry * len(ht))()
        for (i, table) in enumerate(ht):
            edges = table[3].getEdges()
            AHT[i] = table[:3] + edges
        return AHT
    else:
        return None
methodNames = []

def packMethod(((name, arity), (handlerTable, code, numLocals))):
    m = Method()
    methodName = "%s/%s" % (name, arity)
    methodNames.append(methodName)
    m.verb = e.e_intern(methodName)
    m.code = (ctypes.c_ubyte * len(code))(*code)
    m.length = len(code)
    m.num_locals = numLocals
    m.handlerTable = packHandlerTable(handlerTable)
    m.handlerTableLength = len(handlerTable)
    return m
def packMatcher((pattTable, patt, bodyTable, body, numLocals)):
    m = Matcher()
    m.pattern = (ctypes.c_ubyte * len(patt))(*patt)
    m.patternLength = len(patt)
    m.body = (ctypes.c_ubyte * len(body))(*body)
    m.bodyLength = len(body)
    m.num_locals = numLocals
    m.patternHandlerTable = (HandlerTableEntry * len(pattTable))(*pattTable)
    m.patternHandlerTableLength = len(pattTable)
    m.bodyHandlerTable = (HandlerTableEntry * len(bodyTable))(*bodyTable)
    m.bodyHandlerTableLength = len(bodyTable)
    return m

def parse(source):
    from eparser import EParser
    p = EParser(source.strip())
    tree = p.apply("start")
    x = p.input.data[p.input.position:]
    if len(x) != 0:
        raise ValueError("Syntax error", ''.join(x))
    return tree.forValue(None)

def compile(ktree, scope=e_safeScope, names=()):
    global _compile
    if _compile is None:
        _compile = e_import("com.twistedmatrix.ecru.compiler")
    modw =  _compile.run(ktree, scope, names)
    return modw._contents

def dump(mod, f):
    global _dump
    if _dump is None:
        _dump = e_import("com.twistedmatrix.ecru.bytecodeDumper")
    bits = _dump.run(mod)
    for bit in bits:
        if bit >= 0:
            f.write(chr(bit))
        else:
            f.write(chr(256 + bit))

def batchCompile(source, f):
    kt = parse(source)
    mod = compile(kt)
    dump(mod, f)

def pack(mod, scope):
    m = Module()
    constants = e_call(mod, "getConstants")
    AC = ERef * len(constants)
    m.constants = AC(*[toEObject(a) for a in constants])
    m.constantsLength = len(constants)
    selectors = e_call(mod, "getSelectors")
    AS = ESelector * len(selectors)
    m.selectors = AS(*[newSelector(v, a).contents for (v, a) in selectors])
    m.selectorsLength = len(selectors)
    m.scope = e.e_scope_getEvalContext(scope)
    m.scopeLength = e.e_scope_getSize(scope)
    scripts = e_call(mod, "getScripts")
    ASC = ctypes.POINTER(Script) * (len(scripts) + 1)
    mainCode = e_call(mod, "getCode")
    num_locals = e_call(e_call(mod, "getBindings")._contents, "size")
    ht = e_call(mod, "getToplevelHandlerTable")
    mainHT = packHandlerTable(ht)
    packedMainCode = (ctypes.c_ubyte * len(mainCode))(*mainCode)
    mainMethod = Method(e.e_intern("run/0"), packedMainCode,
                        len(mainCode), num_locals, mainHT, len(ht))
    mainscript = Script(1, ctypes.pointer(mainMethod), 0, None, 0)
    scriptStructs = []
    for script in scripts:
        [methods, matchers, numSlots] = script
        methodStructs = (Method * len(methods))()
        for i, meth in enumerate(methods.iteritems()):
            methodStructs[i] = packMethod(meth)
        matcherStructs = (Matcher * len(matchers))()
        for i, ma in enumerate(matchers):
            matcherStructs[i] = packMatcher(ma)
        s = Script(len(methods), methodStructs, len(matchers), matcherStructs,
                   numSlots)
        scriptStructs.append(ctypes.pointer(s))
    m.scripts = ASC(ctypes.pointer(mainscript), *scriptStructs)
    m.scriptsLength = len(scripts) + 1
    m.stackDepth = 0
    return m

debugDump = e_import("com.twistedmatrix.ecru.debugDump")

def show(source, out=e_stdout):
    ktree = parse(source)
    mod = compile(ktree)
    debugDump.run(mod, out)

def doModule(m, doPrint=False, stackframeHolder=None):
    res = e.ecru_vm_execute('\0', '\0', '\0', None, ctypes.pointer(m),
                             None, 0, stackframeHolder)
    if res.script:
        if doPrint:
            e_println(e_stdout, res)
        else:
            return fromEObject(res)
    else:
        e_println(e_stdout, e_thrown_problem)

def doModuleInteractive(m, out, boundNames, stackframe):
    if len(boundNames) > 0:
        initials = []
        bits = stackframe.contents.locals
        for n, i in boundNames:
            initials.append(bits[i])
            #to get it in the saved set:
            fromEObject(bits[i])
        LA = ERef * len(initials)
        inits = LA(*initials)
        initsSize = len(initials)
    else:
        inits = None
        initsSize = 0
    res = e.ecru_vm_execute_interactive(inits, initsSize,
                                         '\0', '\0', '\0', None,
                                         ctypes.pointer(m),
                                         None, 0, ctypes.pointer(stackframe))
    if res.script:
        if out is not None:
            e_println(out, res)
        else:
            return fromEObject(res)
    else:
        e_println(out, e_thrown_problem)


modules = []

def do(source, doPrint=False, scope=e_safeScope):
    ktree = parse(source)
    mod = compile(ktree, scope)
    m = pack(mod, scope)
    modules.append(m)
    return doModule(m, doPrint)

def interactiveEval(expr, scope, boundNames, stackp):
    w = e.e_make_string_writer()
    try:
        ktree = parse(expr)
        mod = compile(ktree, scope, [x for (x, i) in boundNames])
        m = pack(mod, scope)
        localscopenames = ktree.staticScope().outNames()
        names = list(e_call(mod, "getToplevelLocals"))
        modules.append(m)
        doModuleInteractive(m, w, boundNames, stackp)
        res = fromEObject(e.e_string_writer_get_string(w))
        if len(names) > 0:
            for i in range(len(names)):
                if names[i] not in localscopenames:
                    continue
                for n, j in boundNames[:]:
                    if names[i] == n:
                        boundNames.remove((n, j))
                boundNames.append((names[i], i))
        return res
    except Exception, ex:
        return repr(ex)


def repl():
    import readline
    scope = e_privilegedScope
    ps1 = "? "
    ps2 = "> "

    delimiters = { "(": ")", "[": "]", "{": "}"}
    quotes = '"\''
    stack = []
    quoted = False

    prompt = ps1
    expr = ""
    boundNames = []
    stackp = ctypes.POINTER(Stackframe)()
    while True:
        try:
            line = raw_input(prompt)
        except EOFError:
            return
        for i, c in enumerate(line):
            if c in quotes:
                if quoted:
                    if line[i-1] != "\\" and c == stack[-1]:
                        stack.pop()
                        quoted = False
                else:
                    stack.append(c)
                    quoted = True
            elif not quoted:
                if c in delimiters:
                    stack.append(c)
                elif len(stack) > 0 and c == delimiters[stack[-1]]:
                    stack.pop()
        expr += line + '\n'
        if len(stack) == 0:
            prompt = ps1
            print interactiveEval(expr, scope, boundNames, stackp)
            expr = ""
        else:
            prompt = ps2


if __name__ == "__main__":
    repl()
