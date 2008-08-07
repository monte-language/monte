#include "elib.h"


/// Return the specimen if it's a string. Otherwise eject (if ejector present) or throw.
e_Ref stringguard_coerce(e_Ref self, e_Ref *args) {
  e_Ref specimen = e_ref_target(args[0]);
  e_Ref optEjector = args[1];
  if (e_is_string(specimen)) {
    return specimen;
  }
  return e_ejectOrThrow(optEjector, "Value doesn't coerce to an string", specimen);
}

e_Method stringguard_methods[] = {
  {"coerce/2", stringguard_coerce},
  {NULL}
};

e_Script stringguard_script;
e_Ref e_StringGuard;
