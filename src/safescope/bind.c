#include "elib.h"

static e_Ref viaFunc1(e_Ref self, e_Ref *args) {
  //XXX selector pooling
  e_Selector resolve;
  e_make_selector(&resolve, "resolve", 1);

  E_ERROR_CHECK(e_call_1(self.data.refs[0], &resolve, args[0]));
  return e_null;
}

e_Script viafunc1_script;
e_Method viafunc1_methods[] = {
  {"run/2", viaFunc1},
  {NULL}};

static e_Ref viaFunc2(e_Ref self, e_Ref *args) {
  //XXX selector pooling
  e_Selector resolve, coerce;
  e_make_selector(&resolve, "resolve", 1);
  e_make_selector(&coerce, "coerce", 2);

  e_Ref obj = e_call(self.data.refs[1], &coerce, args);
  E_ERROR_CHECK(obj);
  E_ERROR_CHECK(e_call_1(self.data.refs[0], &resolve, obj));
  return e_null;
}

e_Script viafunc2_script;
e_Method viafunc2_methods[] = {
  {"run/2", viaFunc2},
  {NULL}};


static e_Ref bind_run1(e_Ref self, e_Ref *args) {
  e_Ref viafunc;
  viafunc.script = &viafunc1_script;
  viafunc.data.refs = e_malloc(sizeof(e_Ref));
  viafunc.data.refs[0] = args[0];
  return viafunc;
}

static e_Ref bind_run2(e_Ref self, e_Ref *args) {
  e_Ref viafunc;
  viafunc.script = &viafunc2_script;
  viafunc.data.refs = e_malloc(sizeof(e_Ref) * 2);
  viafunc.data.refs[0] = args[0];
  viafunc.data.refs[1] = args[1];
  return viafunc;
}

e_Script e__bind_script;
e_Method bind_methods[] = {
  {"run/1", bind_run1},
  {"run/2", bind_run2},
  {NULL}};

e_Ref e__bind;
