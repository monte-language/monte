
#include "elib.h"
#include "ref.h"
///@defgroup guards
//@{

/// Return whether the specimen is of a primitive integral type.
char e_is_integer(e_Ref specimen) {
  return e_is_fixnum(specimen) || e_is_bignum(specimen);
}

/// Return whether the specimen is one of the base slot types.
char e_is_slot(e_Ref specimen) {
  return (e_is_finalslot(specimen)
       || e_is_guardedslot(specimen)
       || e_is_varslot(specimen));
}

/// Return the specimen if it's a fixnum or bignum. Otherwise eject (if ejector present) or throw.
e_Ref intguard_coerce(e_Ref self, e_Ref *args) {
  e_Ref specimen = e_ref_target(args[0]);
  e_Ref optEjector = args[1];
  if (e_is_integer(specimen)) {
    return specimen;
  }
  return e_ejectOrThrow(optEjector, "Value doesn't coerce to an int", specimen);
}

static e_Method intguard_methods[] = {
  {"coerce/2", intguard_coerce},
  {NULL}
};

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

static e_Method float64guard_methods[] = {
  {"coerce/2", float64guard_coerce},
  {NULL}
};

e_Ref e_Float64Guard;


/// Return the specimen if it's a character. Otherwise eject (if ejector present) or throw.
e_Ref charguard_coerce(e_Ref self, e_Ref *args) {
  e_Ref specimen = e_ref_target(args[0]);
  e_Ref optEjector = args[1];
  if (e_is_char(specimen)) {
    return specimen;
  }
  return e_ejectOrThrow(optEjector, "Value doesn't coerce to a char", specimen);
}

static e_Method charguard_methods[] = {
  {"coerce/2", charguard_coerce},
  {NULL}
};

e_Ref e_CharGuard;

/// Return the specimen if it's a string. Otherwise eject (if ejector present) or throw.
e_Ref stringguard_coerce(e_Ref self, e_Ref *args) {
  e_Ref specimen = e_ref_target(args[0]);
  e_Ref optEjector = args[1];
  if (e_is_string(specimen)) {
    return specimen;
  }
  return e_ejectOrThrow(optEjector, "Value doesn't coerce to an string", specimen);
}

static e_Method stringguard_methods[] = {
  {"coerce/2", stringguard_coerce},
  {NULL}
};

e_Ref e_StringGuard;


/// Return the specimen if it's a boolean. Otherwise eject or throw.
e_Ref booleanguard_coerce(e_Ref self, e_Ref *args) {
  e_Ref specimen = e_ref_target(args[0]);
  e_Ref optEjector = args[1];
  if (e_is_boolean(specimen)) {
    return specimen;
  }
  return e_ejectOrThrow(optEjector, "Value doesn't coerce to a Boolean", specimen);
}

static e_Method booleanguard_methods[] = {
  {"coerce/2", booleanguard_coerce},
  {NULL}
};

e_Ref e_BooleanGuard;

e_Ref elistguard_coerce(e_Ref self, e_Ref *args) {
  e_Ref specimen = e_ref_target(args[0]);
  e_Ref optEjector = args[1];
  if (e_is_constlist(specimen)) {
    return specimen;
  } else if (e_is_flexlist(specimen)) {
    return flexlist_snapshot(specimen, NULL);
  }
  return e_ejectOrThrow(optEjector, "Value doesn't coerce to an EList", specimen);
}

e_Ref e_EListGuard;

static e_Script intguard_script;
static e_Script float64guard_script;
static e_Script charguard_script;
static e_Script stringguard_script;
static e_Script booleanguard_script;



void e__guards_set_up() {
  e_make_script(&intguard_script, NULL, intguard_methods, "IntGuard");
  e_IntGuard.data.fixnum = 0;
  e_IntGuard.script = &intguard_script;

  e_make_script(&booleanguard_script, NULL, booleanguard_methods,
                "BooleanGuard");
  e_BooleanGuard.data.fixnum = 0;
  e_BooleanGuard.script = &booleanguard_script;

  e_make_script(&float64guard_script, NULL, float64guard_methods,
                "Float64Guard");
  e_Float64Guard.data.fixnum = 0;
  e_Float64Guard.script = &float64guard_script;

  e_make_script(&charguard_script, NULL, charguard_methods,
                "CharGuard");
  e_CharGuard.data.fixnum = 0;
  e_CharGuard.script = &charguard_script;

  e_make_script(&stringguard_script, NULL, stringguard_methods,
                "StringGuard");
  e_StringGuard.data.fixnum = 0;
  e_StringGuard.script = &stringguard_script;

}
//@}
