#include "elib.h"

e_Ref listguard_coerce(e_Ref self, e_Ref *args) {
  e_Ref specimen = e_ref_target(args[0]);
  e_Ref optEjector = args[1];
  if (e_is_constlist(specimen)) {
    return specimen;
  }
  return e_ejectOrThrow(optEjector, "Value doesn't coerce to a List", specimen);
}

e_Script listguard_script;
e_Method listguard_methods[] = {
  {"coerce/2", listguard_coerce},
  {NULL}
};

e_Ref e_ListGuard;
