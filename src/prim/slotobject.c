#include "elib.h"

/// Retrieve the value from this FinalSlot.
static e_Ref finalslot_get(e_Ref self, e_Ref *args) {
  return self.data.refs[0];
}

/// Update the value in this slot.
static e_Ref slot_put(e_Ref self, e_Ref *args) {
  self.data.refs[0] = args[0];
  return e_null;
}

/// Throw an error when attempting to update an immutable FinalSlot.
static e_Ref finalslot_put(e_Ref self, e_Ref *args) {
  return e_throw_cstring("Final variables may not be changed.");
}

/// Return whether the slot is mutable or not.
static e_Ref finalslot_isFinal(e_Ref self, e_Ref *args) {
  return e_true;
}

/// Produce an immutable version of this slot.
static e_Ref finalslot_readOnly(e_Ref self, e_Ref *args) {
  return self;
}
/// The Miranda method "__printOn".
static e_Ref slot_printOn(e_Ref self, e_Ref *args) {
  e_Ref out = args[0];
  E_ERROR_CHECK(e_print(out, e_make_string("<& ")));
  E_ERROR_CHECK(e_print(out, finalslot_get(self, NULL)));
  E_ERROR_CHECK(e_print(out, e_make_string(">")));
  return e_null;
}

e_Method finalslot_methods[] = {
  {"__printOn/1", slot_printOn},
  {"get/0", finalslot_get},
  {"getValue/0", finalslot_get},
  {"put/1", finalslot_put},
  {"setValue/1", finalslot_put},
  {"readOnly/0", finalslot_readOnly},
  {"isFinal", finalslot_isFinal},
  {NULL}
};
/// The behaviour of a FinalSlot.
e_Script e__finalslot_script;


/// Produce an immutable object containing only a reference to another object.
/// Primarily used in scopes.
e_Ref e_make_finalslot(e_Ref value) {
  // XXX immutable object here, perhaps this should memoize
  e_Ref result;
  e_Ref *spot = e_malloc(sizeof(e_Ref));
  *spot = value;
  result.data.refs = spot;
  result.script = &e__finalslot_script;
  return result;
}

/// Return whether the slot is mutable or not.
static e_Ref varslot_isFinal(e_Ref self, e_Ref *args) {
  return e_true;
}

/// Produce an immutable version of this slot.
static e_Ref varslot_readOnly(e_Ref self, e_Ref *args) {
  e_Ref result = self;
  result.script = &e__finalslot_script;
  return result;
}

/// The Miranda method "__printOn".
static e_Ref varslot_printOn(e_Ref self, e_Ref *args) {
  e_Ref out = args[0];
  E_ERROR_CHECK(e_print(out, e_make_string("<var ")));
  E_ERROR_CHECK(e_print(out, finalslot_get(self, NULL)));
  E_ERROR_CHECK(e_print(out, e_make_string(">")));
  return e_null;
}

e_Method varslot_methods[] = {
  {"__printOn/1", varslot_printOn},
  {"get/0", finalslot_get},
  {"getValue/0", finalslot_get},
  {"put/1", slot_put},
  {"setValue/1", slot_put},
  {"readOnly/0", varslot_readOnly},
  {"isFinal/0", varslot_isFinal},
  {NULL}
};
/// The behaviour of a VarSlot.
e_Script e__varslot_script;


/// Produce an mutable object containing only a reference to another object.
/// Primarily used in scopes.
e_Ref e_make_varslot(e_Ref value) {
  e_Ref result = e_make_finalslot(value);
  result.script = &e__varslot_script;
  return result;
}

e_Ref guardedslot_put(e_Ref self, e_Ref *args) {
  e_Selector do_coerce;
  e_Ref specimen = args[0];
  e_Ref guard = self.data.refs[1];
  e_Ref result;
  e_make_selector(&do_coerce, "coerce", 2);
  result = e_call_2(guard, &do_coerce, specimen, e_null);
  E_ERROR_CHECK(result);
  self.data.refs[0] = result;
  return e_null;
}


e_Method guardedslot_methods[] = {
  {"__printOn/1", varslot_printOn},
  {"get/0", finalslot_get},
  {"getValue/0", finalslot_get},
  {"put/1", guardedslot_put},
  {"setValue/1", guardedslot_put},
  {"readOnly/0", varslot_readOnly},
  {"isFinal/0", varslot_isFinal},
  {NULL}
};

e_Script e__guardedslot_script;

e_Ref e_new_guardedslot(e_Ref value, e_Ref guard, e_Ref optEjector) {
  e_Ref result, coerced_value;
  e_Selector do_coerce;
  e_make_selector(&do_coerce, "coerce", 2);
  coerced_value = e_call_2(guard, &do_coerce, value, optEjector);
  E_ERROR_CHECK(coerced_value);
  e_Ref *spot = e_malloc(2 * sizeof(e_Ref));
  spot[0] = coerced_value;
  spot[1] = guard;
  result.data.refs = spot;
  result.script = &e__guardedslot_script;
  return result;
}

/// Return whether the specimen is one of the base slot types.
_Bool e_is_slot(e_Ref specimen) {
  return (e_is_finalslot(specimen)
       || e_is_guardedslot(specimen)
       || e_is_varslot(specimen));
}
