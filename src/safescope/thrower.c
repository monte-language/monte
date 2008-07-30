#include "elib.h"

/// Throw a problem.
static e_Ref thrower_run(e_Ref self, e_Ref *args) {
  return e_throw(args[0]);
}

static e_Ref thrower_eject(e_Ref self, e_Ref *args) {
  return e_ejectOrThrow_problem(args[0], args[1]);
}

e_Script thrower_script;
e_Method thrower_methods[] = {
  {"run/1", thrower_run},
  {"eject/2", thrower_eject},
  {NULL}
};

e_Ref e_thrower;
