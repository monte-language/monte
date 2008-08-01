#include "elib.h"

static e_Ref e_traceln_run(e_Ref self, e_Ref *args) {
  return e_println(e_stderr, args[0]);
}

e_Script e__traceln_script;
e_Method e__traceln_methods[] = {
  {"run/1", e_traceln_run},
  {NULL},
};

e_Ref e_traceln;
