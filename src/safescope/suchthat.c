#include "elib.h"

static e_Ref suchThatFuncFalse_run(e_Ref self, e_Ref *args) {
  return e_ejectOrThrow(args[1], "such-that expression was", e_false);
}

e_Script suchThatFuncFalse_script;
e_Method suchThatFuncFalse_methods[] = {
  {"run/2", suchThatFuncFalse_run},
  {NULL}};

static e_Ref suchThatFuncTrue_run(e_Ref self, e_Ref *args) {
  return e_null;
}

e_Script suchThatFuncTrue_script;
e_Method suchThatFuncTrue_methods[] = {
  {"run/2", suchThatFuncTrue_run},
  {NULL}};


static e_Ref suchThat_run2(e_Ref self, e_Ref *args) {
  return e_constlist_from_array(2, args);
}

static e_Ref suchThat_run1(e_Ref self, e_Ref *args) {
  e_Ref func;
  e_Ref boolguard_args[] = {args[0], e_null};
  e_Ref flag = booleanguard_coerce(e_null, boolguard_args);
  E_ERROR_CHECK(flag);
  if (e_same(flag, e_true)) {
    func.script = &suchThatFuncTrue_script;
  } else {
    func.script = &suchThatFuncFalse_script;
  }
  return func;
}

e_Script e__suchThat_script;
e_Method suchThat_methods[] = {
  {"run/2", suchThat_run2},
  {"run/1", suchThat_run1},
  {NULL}};

e_Ref e__suchThat;
