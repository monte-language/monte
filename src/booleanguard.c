#include "elib.h"


/// Return the specimen if it's a boolean. Otherwise eject or throw.
e_Ref booleanguard_coerce(e_Ref self, e_Ref *args) {
  e_Ref specimen = e_ref_target(args[0]);
  e_Ref optEjector = args[1];
  if (e_is_boolean(specimen)) {
    return specimen;
  }
  return e_ejectOrThrow(optEjector, "Value doesn't coerce to a Boolean", specimen);
}

e_Method booleanguard_methods[] = {
  {"coerce/2", booleanguard_coerce},
  {NULL}
};

e_Script booleanguard_script;
e_Ref e_BooleanGuard;
