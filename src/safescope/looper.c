#include "elib.h"

e_Ref e_loop(e_Ref self, e_Ref *args) {
  //XXX selector pooling
  e_Selector run0;
  e_make_selector(&run0, "run", 0);
  e_Ref val;
  do {
    val = e_call_0(args[0], &run0);
    E_ERROR_CHECK(val);
  } while (e_same(val, e_true));
  return e_null;
}

e_Script e__looper_script;
e_Method looper_methods[] = {
  {"run/1", e_loop},
  {NULL}
};

e_Ref e_looper;
