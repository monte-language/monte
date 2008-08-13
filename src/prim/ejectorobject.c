#include "elib.h"

void e_ejector_disable(e_Ref self) {
  self.data.refs[0] = e_empty_ref;
}

/// Perform a non-local exit to the escape block that created this
/// ejector.
e_Ref ejector_run(e_Ref self, e_Ref *args) {
  e_Ref ej;
  if (self.data.refs[0].data.fixnum == 0) {
    return e_throw_cstring("Failed: ejector must be enabled");
  }
  e_ejected_value_set(args[0]);
  ej.script = NULL;
  ej.data.fixnum = self.data.refs[0].data.fixnum;
  return ej;
}

/// Run this ejector with no argument (and thus use 'null' as the ejected value).
static e_Ref ejector_run0(e_Ref self, e_Ref *args) {
  return ejector_run(self, &e_null);
}

/// Test whether this ejector is enabled or not.
static e_Ref ejector_isEnabled(e_Ref self, e_Ref *args) {
  return e_make_boolean(!e_same(self.data.refs[0], e_empty_ref));
}

static e_Ref ejector_disable(e_Ref self, e_Ref *args) {
  self.data.refs[0] = e_empty_ref;
  return e_null;
}

e_Method ejector_methods[] = {
  {"run/0", ejector_run0},
  {"run/1", ejector_run},
  {"disable/0", ejector_disable},
  {"isEnabled/0", ejector_isEnabled},
  {NULL}
};

e_Script e__ejector_script;

/// Create an ejector object.
/** Ejectors are E objects with 'run' methods that unwind the stack to the
    escape expression that creates them. */
e_Ref e_make_ejector() {
  e_Ref ej;
  ej.script = &e__ejector_script;
  ej.data.refs = e_malloc(sizeof(e_Ref));
  ej.data.refs[0].script = NULL;
  ej.data.refs[0].data.fixnum = e_ejector_counter_increment();
  if (e_ejector_counter() <= 0) {
    e_die(e_make_problem("Ejector counter rollover!\n", e_null));
  }
  return ej;
}
