
#include "elib.h"
#include "ecru.h"
#include "vm.h"
#include "ref.h"
#include "scope.h"
#include <Python.h>
#include <string.h>
#include <gc/gc.h>


typedef struct monte_handle {
  PyObject *object;
} monte_handle;

e_Ref monte_wrap(PyObject *obj);
PyObject *monte_unwrap(e_Ref obj);
static PyObject *monte_EObjectWrapper;
static PyObject *monte_PythonCharacter;
static e_Ref compiler, bytecodeDumper, debugDumper;
static e_Selector run, doWrite, get, getToplevelLocals,
  size, withOuterSlots, resolve, fulfillment;

e_Script e__python_object_script;

e_Ref python_vat;

/* XXX these are global variables because boehm GC needs to have a root for
objects only otherwise referenced by Python's ctypes. These won't be necessary
once we stop manipulating C structs from Python. */

e_Ref saveset;

e_Ref throw_python_error() {
  PyObject *ptype, *pvalue, *ptraceback;
  char *typeName, *valueString;
  PyErr_Fetch(&ptype, &pvalue, &ptraceback);
  if (PyExceptionClass_Check(ptype)) {
    typeName = PyExceptionClass_Name(ptype);
  } else if (PyString_Check(ptype)) {
    typeName = PyString_AS_STRING(ptype);
  }
  valueString = PyString_AS_STRING(PyObject_Str(pvalue));
  PyErr_Restore(ptype, pvalue, ptraceback);
  PyErr_Print();
  if (ptype == NULL) {
    return e_throw_cstring("bogus python error");
  } else {
    return e_throw_pair(typeName,
                        e_make_string(valueString));
  }
}

PyObject *e_to_py(e_Ref obj) {
  if (obj.script == NULL) {
    if (obj.data.fixnum != 0) {
      PyErr_SetString(PyExc_SystemError, "wild ejection occurred!");
    } else {
      e_Ref prob = e_thrown_problem();
      e_Ref w = e_make_string_writer();
      e_print(w, prob);
      PyErr_SetString(PyExc_RuntimeError,
                      e_string_writer_get_string(w).data.gstring->str);
    }
    return NULL;
  }
  if (e_is_ref(obj) && e_same(e_true, e_ref_isResolved(obj))) {
    return e_to_py(obj.data.refs[0]);
  } else if (e_is_null(obj)) {
    Py_INCREF(Py_None);
    return Py_None;
  } else if (e_is_fixnum(obj)) {
    return PyInt_FromLong(obj.data.fixnum);
  } else if (e_is_float64(obj)) {
    return PyFloat_FromDouble(*obj.data.float64);
  } else if (e_is_bignum(obj)) {
    // XXX totally cheating here
    char *str = mpz_get_str(NULL, 10, *obj.data.bignum);
    return PyLong_FromString(str, NULL, 10);
  } else if (e_is_string(obj)) {
    return PyString_FromStringAndSize(obj.data.gstring->str,
                                      obj.data.gstring->len);
  } else if (e_is_char(obj)) {
    char x = obj.data.chr;
    PyObject *str = PyString_FromStringAndSize(&x, 1);
    return PyObject_CallFunctionObjArgs(monte_PythonCharacter, str, NULL);
  } else if (e_is_constlist(obj)) {
    Flexlist_data *elist = obj.data.other;
    PyObject *list = PyTuple_New(elist->size);
    for (int i = 0; i < elist->size; i++) {
      PyObject *item = e_to_py(elist->elements[i]);
      Py_INCREF(item);
      PyTuple_SET_ITEM(list, i, item);
    }
    return list;
  } else if (e_is_constmap(obj)) {
    Flexmap_data *emap = obj.data.other;
    PyObject *dict = PyDict_New();
    for (int i = 0; i < emap->occupancy; i++) {
      PyObject *k = e_to_py(emap->keys[i]);
      PyObject *v = e_to_py(emap->values[i]);
      Py_INCREF(k);
      Py_INCREF(v);
      if (PyDict_SetItem(dict, k, v) == -1) {
        return NULL;
      }
    }
    return dict;
  } else if (e_same(obj, e_true)) {
    Py_RETURN_TRUE;
  } else if (e_same(obj, e_false)) {
    Py_RETURN_FALSE;
  } else if (obj.script == &e__python_object_script) {
    return monte_unwrap(obj);
  } else {
    e_Ref putargs[] = {obj, e_null};
    e_flexmap_put(saveset, putargs);
    PyObject *x = PyCObject_FromVoidPtrAndDesc(obj.data.other,
                                               obj.script, NULL);
    return PyObject_CallFunctionObjArgs(monte_EObjectWrapper, x);
  }
}

e_Ref py_to_e(PyObject *obj) {
  if (obj == Py_None) {
    return e_null;
  } else if (PyInt_Check(obj)) {
    long x = PyInt_AsLong(obj);
    if (PyErr_Occurred()) {
      return throw_python_error();
    }
    return e_make_fixnum(x);
  } else if (PyLong_Check(obj)) {
    // XXX totally cheating here
    mpz_t *bn = e_malloc(sizeof *bn);
    mpz_init_set_str(*bn, PyString_AsString(PyObject_Str(obj)), 10);
    return e_make_bignum(bn);
  } else if (PyFloat_Check(obj)) {
    double x = PyFloat_AsDouble(obj);
    if (PyErr_Occurred()) {
      return throw_python_error();
    }
    return e_make_float64(x);
  } else if (PyString_Check(obj)) {
    int len = PyString_Size(obj);
    char *str = PyString_AsString(obj);
    if (PyErr_Occurred()) {
      return throw_python_error();
    }
    return e_make_gstring(g_string_new_len(str, len));
  } else if (PyTuple_Check(obj) || PyList_Check(obj)) {
    int len = PySequence_Size(obj);
    e_Ref items[len];
    for (int i = 0; i < len; i++) {
      items[i] = py_to_e(PySequence_GetItem(obj, i));
      if (PyErr_Occurred()) {
        return throw_python_error();
      }
    }
    return e_constlist_from_array(len, items);
  } else if (obj == Py_True) {
    return e_true;
  } else if (obj == Py_False) {
    return e_false;
  } else if (PyObject_IsInstance(obj, monte_PythonCharacter)) {
    PyObject *x = PyObject_GetAttrString(obj, "character");
    return e_make_char(PyString_AsString(x)[0]);
  } else if (PyObject_IsInstance(obj, monte_EObjectWrapper)) {
    PyObject *x = PyObject_GetAttrString(obj, "_contents");
    if (!PyCObject_Check(x)) {
      return e_throw_cstring("Wrapped object not an ERef");
    }
    e_Ref res;
    res.script = PyCObject_GetDesc(x);
    res.data.other = PyCObject_AsVoidPtr(x);
    return res;
  } else {
    return monte_wrap(obj);
  }
}

e_Ref invoke_python_object(e_Ref self, e_Selector *sel, e_Ref *args) {
  if (strcmp(sel->verb, "audited-by-magic-verb") == 0) {
    return e_false;
  }
  PyObject *obj = ((monte_handle *)self.data.other)->object;
  PyObject *py_args = PyTuple_New(sel->arity);
  e_Ref res;

  for (int i = 0; i < sel->arity; i++) {
    PyObject *arg = e_to_py(args[i]);
    if (arg == NULL) {
      e_throw_pair("Could not convert argument", e_make_fixnum(i));
    }
    PyTuple_SET_ITEM(py_args, i, arg);
  }
  // liable to break on some weird object, but mostly right
  if (PyCallable_Check(obj) && (strncmp(sel->verb, "run/", 4) == 0)) {
    res = py_to_e(PyObject_Call(obj, py_args, NULL));
  } else {
    int nameLength = strstr(sel->verb, "/") - sel->verb;
    char *verb = malloc(nameLength+1);
    strncpy(verb, sel->verb, nameLength);
    verb[nameLength] = '\0';
    PyObject *meth = PyObject_GetAttrString(obj, verb);
    free(verb);
    if (meth == NULL) {
      return throw_python_error();
    }
    PyObject *pyres = PyObject_Call(meth, py_args, NULL);
    if (pyres == NULL) {
      return throw_python_error();
    }
    res = py_to_e(pyres);
  }
  E_ERROR_CHECK(res);
  return res;
}


PyObject *bridge_set_up(PyObject *self, PyObject *args) {
  PyObject *wrapper, *charClass;
  if (!PyArg_ParseTuple(args, "OO", &wrapper, &charClass)) {
    return NULL;
  }
  ecru_set_up();
  monte_EObjectWrapper = wrapper;
  monte_PythonCharacter = charClass;
  Py_INCREF(wrapper);
  Py_INCREF(charClass);
  e_make_script(&e__python_object_script, invoke_python_object,
                no_methods, NULL, "wrapped Python object");
  saveset = e_make_flexmap(0);
  GString *cName = e_make_string("com.twistedmatrix.ecru.compiler"
                                 ).data.gstring;
  GString *bdName = e_make_string("com.twistedmatrix.ecru.bytecodeDumper"
                               ).data.gstring;
  GString *ddName = e_make_string("com.twistedmatrix.ecru.debugDump"
                               ).data.gstring;
  compiler = e_module_import(cName);
  bytecodeDumper = e_module_import(bdName);
  debugDumper = e_module_import(ddName);
  e_make_selector(&run, "run", 2);
  e_make_selector(&doWrite, "write", 2);
  e_make_selector(&get, "get", 1);
  e_make_selector(&getToplevelLocals, "getToplevelLocals", 0);
  e_make_selector(&size, "size", 0);
  e_make_selector(&resolve, "resolve", 1);
  e_make_selector(&withOuterSlots, "withOuterSlots", 2);
  e_make_selector(&fulfillment, "fulfillment", 1);
  python_vat = e_make_vat(e_null, "python vat");
  e_vat_set_active(python_vat);

  Py_INCREF(Py_None);
  return Py_None;
}

PyObject *bridge_getPrivilegedScope(PyObject *self, PyObject *args) {
  return e_to_py(e_privilegedScope);
}

PyObject *bridge_e_call(PyObject *self, PyObject *args) {
  PyObject *obj, *pyargs;
  char *verb;
  e_Selector sel;
  int siz = PyTuple_Size(args) - 2;
  e_Ref *arglist;
  pyargs = PyTuple_GetSlice(args, 0, 2);
  if(!PyArg_ParseTuple(pyargs, "Os", &obj, &verb)) {
    return NULL;
  }

  if (siz == 0) {
    arglist = NULL;
  } else {
    arglist = e_malloc(siz * sizeof *arglist);
    for (int i = 0; i < siz; i++) {
      arglist[i] = py_to_e(PyTuple_GET_ITEM(args, i+2));
    }
  }
  e_make_selector(&sel, verb, siz);
  return e_to_py(e_call(py_to_e(obj), &sel, arglist));
}

void monte_handle_finalize(void *hptr, void *cd) {
  monte_handle *handle = hptr;
  Py_DECREF((PyObject *)cd);
}

e_Ref monte_wrap(PyObject *obj) {
  e_Ref res;
  res.script = &e__python_object_script;
  monte_handle *handle = e_malloc(sizeof *handle);
  Py_INCREF(obj);
  handle->object = obj;
#ifndef NO_GC
  GC_register_finalizer(handle, monte_handle_finalize, obj, NULL, NULL);
#endif
  res.data.other = handle;
  return res;
}

PyObject *monte_unwrap(e_Ref obj) {
  if (obj.script != &e__python_object_script) {
    return NULL;
  }
  PyObject *x = ((monte_handle *)obj.data.other)->object;
  Py_INCREF(x);
  return x;
}

/*
ecru_module *monte_bridge_pack(e_Ref module, e_Ref scope) {
  // XXX even less error checking than the Python version
  ecru_module *m = e_malloc(sizeof *m);
  e_Ref constants = e_call_0(module, &getConstants);
  e_Ref selectors = e_call_0(module, &getSelectors);
  e_Ref scripts = e_call_0(module, &getScripts);
  int numScripts = ((Flexlist_data *)scripts.data.other)->size + 1;
  e_Ref mainCode = e_call_0(module, &getCode);
  e_Ref htable = e_call(module, &getToplevelHandlerTable);
  ecru_method *mainMethod = e_malloc(sizeof *mainMethod);
  ecru_script *mainScript = e_malloc(sizeof *mainScript);
  ecru_script *scriptsArray = e_malloc(numScripts * sizeof *scriptsArray);

  mainMethod->verb = e_intern("run/0");
  mainMethod->code = ((Flexlist_data *)mainCode.data.other)->elements;
  mainMethod->length = ((Flexlist_data *)mainCode.data.other)->size;
  mainMethod->num_locals = e_call_0(e_call_0(module, &getBindings), &size);
  mainMethod->handlerTable = packHandlerTable(htable);
  mainMethod->handlerTableLength = ((Flexlist_data *)htable.data.other)->size;

  mainScript->num_methods = 1;
  mainScript->methods = mainMethod;
  mainScript->num_matchers = 0;
  mainScript->matchers = NULL;
  mainScript->num_slots = 0;
  scriptsArray[0] = mainScript;
  for (int i = 1; i < numScripts; i++) {
    e_Ref script = e_call_1(scripts, &get, e_make_fixnum(i));
    e_Ref methods = e_call_1(script, &get, e_make_fixnum(0));
    e_Ref matchers = e_call_1(script, &get, e_make_fixnum(1));
    e_Ref numSlots = e_call_1(script, &get, e_make_fixnum(2));
    int numMethods = ((Flexlist_data *)methods.data.other)->size;
    int numMatchers = ((Flexlist_data *)matchers.data.other)->size;
    ecru_method *methodArray = e_malloc(numMethods * sizeof *methodArray);
    ecru_matcher *matcherArray = e_malloc(numMatchers * sizeof *matcherArray);
    ecru_script *s = e_malloc(sizeof *s);
    for (int j = 0; j < numMethods; j++) {
      methodArray[j] = packMethod(e_call_0(methods, &get, e_make_fixnum(j)));
    }
    for (int j = 0; j < numMatchers; j++) {
      matcherArray[j] = packMatcher(e_call_0(matchers, &get, e_make_fixnum(j)));
    }
    s->num_matchers = numMatchers;
    s->num_methods = numMethods;
    s->methods = methodArray;
    s->matchers = matcherArray;
    s->num_slots = numSlots.data.fixnum;
    scriptsArray[i] = s;
  }

  m.constants = ((Flexlist_data *)constants.data.other)->elements;
  m.constantsLength = ((Flexlist_data *)constants.data.other)->size;

  m.selectors = ((Flexlist_data *)selectors.data.other)->elements;
  m.selectorsLength = ((Flexlist_data *)selectors.data.other)->size;

  m.scripts = scriptsArray;
  m.scriptsLength = numScripts;

  m.scope = scope;
  m.stackDepth = 0;
}
*/

ecru_module *monte_bridge_pack(e_Ref module, e_Ref scope) {

}

typedef struct interactive_runnable {
  ecru_module *module;
  e_Ref nameList;
  e_Ref resolverVat;
  e_Ref resolver;
} interactive_runnable;


static void do_interactive_turn(e_Ref vat, void *x) {
  ecru_stackframe *stackp;
  e_Ref newScope;
  interactive_runnable *data = x;
  Vat_data *vatdata = vat.data.other;
  e_Ref res = ecru_vm_execute(0, 0, 0, NULL, data->module,
                                 NULL, 0, &stackp);
  e_Ref result;
  if (e_ref_state(res) == EVENTUAL) {
    result = e_make_string("<Promise>");
  } else {
    e_Ref w = e_make_string_writer();
    e_Ref maybeVal = e_call_1(THE_REF, &fulfillment, res);
    if (maybeVal.script == NULL) {
      e_println(w, e_thrown_problem());
    } else {
      e_println(w, maybeVal);
    }
    result = e_string_writer_get_string(w);
  }
  e_Ref numLocals = e_call_0(data->nameList, &size);
  if (numLocals.script == NULL) {
    result = numLocals;
  } else {
    int siz = numLocals.data.fixnum;
    newScope = data->module->scope;
    if (siz != 0 && res.script != NULL) {
      e_Ref slotsList = e_constlist_from_array(siz, stackp->locals);
      newScope = e_call_2(data->module->scope, &withOuterSlots,
                          data->nameList, slotsList);
    }
  }
  e_Ref out[] = {result, newScope};
  e_Ref resultlist = e_constlist_from_array(2, out);
  e_Ref *arg = e_malloc(sizeof *arg);
  *arg = resultlist;
  e_vat_sendOnly(data->resolverVat, data->resolver, &resolve, arg);
  vatdata->turncounter++;
}

e_Ref doModuleInteractive(ecru_module *m,  e_Ref compiledModule) {
  e_Ref nameList = e_call_0(compiledModule, &getToplevelLocals);
  e_Ref obj = e_make_vmobject(m, 0, NULL);
  e_Ref ppair = e_make_promise_pair();
  e_Ref result = e_call_1(ppair, &get, e_make_fixnum(0));
  e_Ref resolver = e_call_1(ppair, &get, e_make_fixnum(1));
  interactive_runnable data = {.module = m, .nameList = nameList, .resolverVat = python_vat, .resolver = resolver};
  interactive_runnable *queueItem = e_malloc(sizeof *queueItem);
  *queueItem = data;
  e_vat_enqueue(python_vat, do_interactive_turn, queueItem);
  return result;
}

static e_Ref dump_module(e_Ref module) {
  e_Ref w = e_make_string_writer();
  E_ERROR_CHECK(w);
  e_Ref x = e_call_2(bytecodeDumper, &doWrite, module, w);
  E_ERROR_CHECK(x);
  return e_string_writer_get_string(w);
}

static e_Ref debug_dump(e_Ref module) {
  e_Ref w = e_make_string_writer();
  E_ERROR_CHECK(w);
  e_Ref x = e_call_2(debugDumper, &run, module, w);
  E_ERROR_CHECK(x);
  return e_string_writer_get_string(w);
}
static e_Ref synchronous_interactive_eval(e_Ref ktree, e_Ref scope) {
  e_Ref module = e_call_2(compiler, &run, ktree, scope);
  E_ERROR_CHECK(module);
  e_Ref str = dump_module(module);
  E_ERROR_CHECK(str);
  e_Ref r = e_make_string_reader(str);
  E_ERROR_CHECK(r);
  ecru_module *m = ecru_load_bytecode(r, scope);
  e_Ref out = doModuleInteractive(m, module);
  e_vat_set_active(python_vat);
  while (e_vat_execute_turn(python_vat)) {};
  return out;
}

static PyObject *bridge_dump_module(PyObject *self, PyObject *args) {
  PyObject *ktree, *scope;
  if (!PyArg_ParseTuple(args, "OO", &ktree, &scope)) {
    return NULL;
  }
  e_Ref module = e_call_2(compiler, &run, py_to_e(ktree), py_to_e(scope));
  if (module.script == NULL) {
    return e_to_py(module);
  }
  return e_to_py(dump_module(module));
}

static PyObject *bridge_debug_dump(PyObject *self, PyObject *args) {
  PyObject *ktree, *scope;
  if (!PyArg_ParseTuple(args, "OO", &ktree, &scope)) {
    return NULL;
  }
  e_Ref module = e_call_2(compiler, &run, py_to_e(ktree), py_to_e(scope));
  if (module.script == NULL) {
    return e_to_py(module);
  }
  return e_to_py(debug_dump(module));
}


static PyObject *bridge_interactive_eval(PyObject *self, PyObject *args) {
  PyObject *ktree, *scope;
  if (!PyArg_ParseTuple(args, "OO", &ktree, &scope)) {
    return NULL;
  }
  return e_to_py(synchronous_interactive_eval(py_to_e(ktree), py_to_e(scope)));
}

static PyMethodDef bridge_methods[] = {
  {"setup", bridge_set_up, METH_VARARGS,
   "Call this before using any other bridge functions. Takes the classes 'EObjectWrapper' and 'Character' as args."},
  {"getPrivilegedScope", bridge_getPrivilegedScope, METH_VARARGS,
   //   "Fetch a single E object by name from the privileged scope."},
   "Fetch the E object representing the unsafe scope."},
  {"e_call", bridge_e_call, METH_VARARGS,
   "Call a method on an E object."},
  {"dumpModule", bridge_dump_module, METH_VARARGS,
   "Return a compiled emaker, serialized to a string."},
  {"debugDump", bridge_debug_dump, METH_VARARGS,
   "Print out a debug dump of compilation results."},
  {"interactiveEval", bridge_interactive_eval, METH_VARARGS,
   "Evaluate a Kernel-E tree in a given scope. Return the result and a new scope."},
  {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initbridge() {
  Py_InitModule("bridge", bridge_methods);
}
