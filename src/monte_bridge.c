
#include "elib.h"
#include "ecru.h"
#include "vm.h"
#include "ref.h"
#include <scope.h>
#include <Python.h>
#include <string.h>
#include <gc/gc.h>


typedef struct monte_handle {
  PyObject *object;
} monte_handle;

e_Ref monte_wrap(PyObject *obj);
PyObject *monte_unwrap(e_Ref obj);
static PyObject *(*monte_makeEObjectWrapper)(e_Ref);
static PyObject *monte_EObjectWrapper;
static PyObject *monte_PythonCharacter;

/* XXX these are global variables because boehm GC needs to have a root for
objects only otherwise referenced by Python's ctypes. These won't be necessary
once we stop manipulating C structs from Python. */

e_Ref saveset, e_interactiveScope;
ecru_stackframe *lastStackFrame;

e_Script e__python_object_script;


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
    e_flexmap_put(saveset, &obj);
    return monte_makeEObjectWrapper(obj);
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
    // kinda ghetto
    PyObject *x = PyObject_GetAttrString(obj, "_contents");
    e_Ref res;
    const void *refbuf;
    Py_ssize_t bufsize;
    PyObject_AsReadBuffer(x, &refbuf, &bufsize);
    memcpy(&res, refbuf,  sizeof(void *) * 2);
    return res;
  } else {
    return monte_wrap(obj);
  }
}

e_Ref invoke_python_object(e_Ref self, e_Selector *sel, e_Ref *args) {

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

void monte_bridge_set_up(PyObject *wrapper, PyObject *(*wrap)(e_Ref),
                         PyObject *charClass) {
  monte_makeEObjectWrapper = wrap;
  monte_EObjectWrapper = wrapper;
  monte_PythonCharacter = charClass;
  Py_INCREF(wrapper);
  e_make_script(&e__python_object_script, invoke_python_object,
                no_methods, "wrapped Python object");
  saveset = e_make_flexmap(0);

  e_Ref *_interactiveScope = e_make_array(122);
  char **_interactiveScope_names = e_malloc(122 * sizeof(char *));
  e_Ref *oldSlots = ((Scope_data *)e_privilegedScope.data.other)->slots;
  char **oldNames = ((Scope_data *)e_privilegedScope.data.other)->names;
  memcpy(_interactiveScope, oldSlots, 122 * sizeof(e_Ref));
  memcpy(_interactiveScope_names, oldNames, 122 * sizeof(char *));
  e_interactiveScope = e_make_scope(_interactiveScope_names,
                                    _interactiveScope,
                                    122);

}

void monte_handle_finalize(void *hptr, void *cd) {
  monte_handle *handle = hptr;
  Py_DECREF((PyObject *)cd);
  handle->object = NULL;
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

int extendInteractiveScope(PyObject *bindings, e_Ref *locals) {
  if (!PySequence_Check(bindings)) {
    return 0;
  }
  Scope_data *scopeContents = e_interactiveScope.data.other;
  PyObject *bits = PySequence_Fast(bindings, "");
  int len = PySequence_Fast_GET_SIZE(bindings);
  int newSize = scopeContents->size + len;
  char **newNames = e_malloc(newSize * sizeof(char *));
  e_Ref *newSlots = e_malloc(newSize * sizeof(e_Ref));
  memcpy(newNames, scopeContents->names, scopeContents->size * sizeof(char *));
  memcpy(newSlots, scopeContents->slots, scopeContents->size * sizeof(e_Ref));
  for (int i = 0; i < len; i++) {
    PyObject *item = PySequence_Fast_GET_ITEM(bits, i);
    if (!PySequence_Check(item)) {
      return 0;
    }
    PyObject *name = PySequence_GetItem(item, 0);
    PyObject *idx = PySequence_GetItem(item, 1);
    char *n = PyString_AsString(name);
    if (n == NULL) {
      return 0;
    }
    int j = PyInt_AsLong(idx);
    if (j == -1) {
      return 0;
    }
    newNames[scopeContents->size + i] = n;
    newSlots[scopeContents->size + i] = locals[j];
  }
  scopeContents->names = newNames;
  scopeContents->slots = newSlots;
  scopeContents->size = newSize;
  return 1;
}

PyObject *doModuleInteractive(ecru_module *m, PyObject *boundNames,
                              ecru_stackframe **stackp) {
  e_Ref *inits = NULL;
  int numBoundNames = 0;
  e_Ref w = e_make_string_writer();
  if (!PySequence_Check(boundNames)) {
    PyErr_SetString(PyExc_TypeError, "boundNames must be a sequence");
    return NULL;
  }
  numBoundNames = PySequence_Fast_GET_SIZE(boundNames);
  e_Ref initials[numBoundNames];
  if (numBoundNames > 0) {
    for (int i = 0; i < numBoundNames; i++) {
      PyObject *item = PySequence_Fast_GET_ITEM(boundNames, i);
      PyObject *val = PySequence_GetItem(item, 1);
      if (val == NULL) {
        return NULL;
      }
      int idx = PyInt_AsLong(val);
      if (idx == -1) {
        return NULL;
      }
      initials[i] = (*stackp)->locals[idx];
    }
    inits = initials;
  }
  e_Ref res = ecru_vm_execute_interactive(inits, numBoundNames,
                                          0, 0, 0, NULL, m,
                                          NULL, 0, stackp);
  lastStackFrame = *stackp;
  if (res.script != NULL) {
    e_println(w, res);
  } else {
    e_println(w, e_thrown_problem);
  }
  e_Ref str = e_string_writer_get_string(w);
  return e_to_py(str);
}
