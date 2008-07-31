#include "elib.h"

static e_Ref test_coerce(e_Ref self, e_Ref *args) {
  if (e_same(args[0], e_true)) {
    return e_true;
  } else {
    return e_ejectOrThrow(args[1], "condition was false", e_false);
  }
}

e_Script e__test_script;
e_Method test_methods[] = {
  {"coerce/2", test_coerce},
  {NULL}};

e_Ref e__Test;
