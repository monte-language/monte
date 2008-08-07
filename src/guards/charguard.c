#include "elib.h"

/// Return the specimen if it's a character. Otherwise eject (if ejector present) or throw.
e_Ref charguard_coerce(e_Ref self, e_Ref *args) {
  e_Ref specimen = e_ref_target(args[0]);
  e_Ref optEjector = args[1];
  if (e_is_char(specimen)) {
    return specimen;
  }
  return e_ejectOrThrow(optEjector, "Value doesn't coerce to a char", specimen);
}

e_Method charguard_methods[] = {
  {"coerce/2", charguard_coerce},
  {NULL}
};

e_Script charguard_script;
e_Ref e_CharGuard;
