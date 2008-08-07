#include "elib.h"

/// Return the specimen if it's a fixnum or bignum. Otherwise eject (if ejector present) or throw.
e_Ref intguard_coerce(e_Ref self, e_Ref *args) {
  e_Ref specimen = e_ref_target(args[0]);
  e_Ref optEjector = args[1];
  if (e_is_integer(specimen)) {
    return specimen;
  }
  return e_ejectOrThrow(optEjector, "Value doesn't coerce to an int", specimen);
}

e_Method intguard_methods[] = {
  {"coerce/2", intguard_coerce},
  {NULL}
};

e_Script intguard_script;
e_Ref e_IntGuard;

/// Return the specimen if it's a float64. Otherwise eject (if ejector present) or throw.
e_Ref float64guard_coerce(e_Ref self, e_Ref *args) {
  e_Ref specimen = e_ref_target(args[0]);
  e_Ref optEjector = args[1];
  if (e_is_float64(specimen)) {
    return specimen;
  } else if (e_is_fixnum(specimen)) {
    return e_make_float64(specimen.data.fixnum);
  } else if (e_is_bignum(specimen)) {
    return e_bignum_as_float64(specimen);
  }
  return e_ejectOrThrow(optEjector, "Value doesn't coerce to a float64", specimen);
}

e_Method float64guard_methods[] = {
  {"coerce/2", float64guard_coerce},
  {NULL}
};
e_Script float64guard_script;
e_Ref e_Float64Guard;

