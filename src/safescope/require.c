#include "elib.h"

e_Ref require_run(e_Ref self, e_Ref *args) {
  if (args[0].script != &e__boolean_script) {
    return e_throw_cstring("Argument to 'require' was not a boolean");
  }
  if (e_same(args[0], e_false)) {
    return e_throw(args[1]);
  }
  return e_null;
}

e_Ref require_run1(e_Ref self, e_Ref *args) {
  e_Ref newArgs[] = {args[0], e_make_string("required condition failed")};
  return require_run(self, newArgs);
}

e_Script e__require_script;
e_Method require_methods[] = {
  {"run/1", require_run1},
  {"run/2", require_run},
  {NULL}};

e_Ref e_require;
