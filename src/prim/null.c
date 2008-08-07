#include "elib.h"

static e_Ref null_printOn(e_Ref self, e_Ref *args) {
  E_ERROR_CHECK(e_print(args[0], e_make_string("null")));
  return e_null;
}

e_Method null_methods[] = {
  { "__printOn/1", null_printOn },
  {NULL}
};
e_Script e__null_script;
e_Ref e_null = { &e__null_script, {0}};

