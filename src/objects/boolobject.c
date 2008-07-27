#include "elib.h"


static e_Ref boolean_printOn(e_Ref self, e_Ref *args) {
  e_Ref string = e_make_string(self.data.fixnum ? "true" : "false");
  E_ERROR_CHECK(e_print(args[0], string));
  return e_null;
}

static inline e_Ref boolean_value(e_Ref ref) {
  ref = e_ref_target(ref);
  if (!e_is_boolean (ref)) {
    return e_throw_pair("Not a boolean", ref);
  }
  return ref;
}

static e_Ref boolean_not(e_Ref self, e_Ref *args) {
  return e_make_boolean(1 - self.data.fixnum);
}

static e_Ref boolean_or(e_Ref self, e_Ref *args) {
  e_Ref bval = boolean_value (args[0]);
  E_ERROR_CHECK(bval);
  return e_make_boolean(self.data.fixnum | bval.data.fixnum);
}

static e_Ref boolean_xor(e_Ref self, e_Ref *args) {
  e_Ref bval = boolean_value (args[0]);
  E_ERROR_CHECK(bval);
  return e_make_boolean (self.data.fixnum ^ bval.data.fixnum);
}

static e_Ref boolean_and(e_Ref self, e_Ref *args) {
  e_Ref bval = boolean_value (args[0]);
  E_ERROR_CHECK(bval);
  return e_make_boolean (self.data.fixnum & bval.data.fixnum);
}

static e_Ref boolean_pick(e_Ref self, e_Ref *args) {
  return args[1 - self.data.fixnum];
}

e_Method boolean_methods[] = {
  { "__printOn/1", boolean_printOn },
  { "not/0", boolean_not },
  { "and/1", boolean_and },
  { "or/1", boolean_or },
  { "xor/1", boolean_xor },
  { "pick/2", boolean_pick },
  {NULL}
};
e_Script e__boolean_script;

e_Ref e_true, e_false;


