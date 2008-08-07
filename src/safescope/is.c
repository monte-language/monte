#include "elib.h"

static e_Ref isSameFunc_run(e_Ref self, e_Ref *args) {
  if (e_same(self.data.refs[0], args[0])) {
    return args[0];
  } else {
    return e_ejectOrThrow(args[1], "doesn't equal-match", args[0]);
  }
}

e_Script isSameFunc_script;
e_Method isSameFunc_methods[] = {
  {"run/2", isSameFunc_run},
  {NULL}};

static e_Ref is_run(e_Ref self, e_Ref *args) {
  e_Ref isSameFunc;
  isSameFunc.script = &isSameFunc_script;
  isSameFunc.data.refs = e_malloc(sizeof(e_Ref));
  isSameFunc.data.refs[0] = args[0];
  return isSameFunc;
}

e_Script e__is_script;
e_Method is_methods[] = {
  {"run/1", is_run},
  {NULL}};

e_Ref e__is;
