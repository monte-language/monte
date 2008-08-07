#include "elib.h"

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
