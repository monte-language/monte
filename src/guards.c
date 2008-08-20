#include "elib.h"
#include "string.h"

e_Ref e_ConstListGuard, e_FlexListGuard, e_BooleanGuard, e_CharGuard,
      e_StringGuard, e_selfless_stamp;

static e_Script e__typeguard_script, e__selfless_auditor_script;

e_Ref e_coerce(e_Ref guard, e_Ref specimen, e_Ref optEjector) {
  // XXX selector pooling
  e_Selector do_coerce;
  e_make_selector(&do_coerce, "coerce", 2);
  return e_call_2(guard, &do_coerce, specimen, optEjector);
}

e_Ref e_make_typeguard(e_Script *script) {
  e_Ref result;
  result.script = &e__typeguard_script;
  result.data.other = (void *)script;
  return result;
}

static e_Ref e_typeguard_coerce(e_Ref self, e_Ref *args) {
  e_Script *typescript = self.data.other;
  e_Ref specimen = e_ref_target(args[0]);
  e_Ref optEjector = args[1];
  if (specimen.script == typescript) {
    return specimen;
  }
  //XXX really need printf-style support for problem creation
  GString *errorMsg = g_string_new("Value doesn't coerce to a ");
  g_string_append_len(errorMsg, typescript->typeName->str,
                      typescript->typeName->len);
  return e_ejectOrThrow(optEjector, errorMsg->str, specimen);
}

static e_Method typeguard_methods[] = {
  {"coerce/2", e_typeguard_coerce},
  {NULL}
};



_Bool e_is_selfless(e_Ref obj) {
  return e_approved_by(obj, e_selfless_stamp);
}

static e_Method selfless_auditor_methods[] = {
  {NULL}
};

void e__guards_set_up() {
  e_make_script(&e__selfless_auditor_script, NULL, selfless_auditor_methods,
                NULL, "SelflessAuditor");
  e_selfless_stamp.script = &e__selfless_auditor_script;
  e_selfless_stamp.data.fixnum = 0;

  e_Ref justSelfless[] = {e_selfless_stamp, {NULL}};
  e_make_script(&e__typeguard_script, NULL, typeguard_methods,
                justSelfless, "Guard");
  e_make_script(&intguard_script, NULL, intguard_methods,
                justSelfless, "IntGuard");
  e_IntGuard.data.fixnum = 0;
  e_IntGuard.script = &intguard_script;

  e_make_script(&listguard_script, NULL, listguard_methods,
                justSelfless, "ListGuard");
  e_ListGuard.data.fixnum = 0;
  e_ListGuard.script = &listguard_script;

  e_BooleanGuard = e_make_typeguard(&e__boolean_script);
  e_Float64Guard = e_make_typeguard(&e__float64_script);
  e_CharGuard = e_make_typeguard(&e__char_script);
  e_StringGuard = e_make_typeguard(&e__string_script);
  e_ConstListGuard = e_make_typeguard(&e__constlist_script);
  e_FlexListGuard = e_make_typeguard(&e__flexlist_script);

}
