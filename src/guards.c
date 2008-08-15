
#include "elib.h"

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

  e_make_script(&listguard_script, NULL, listguard_methods,
                "ListGuard");
  e_ListGuard.data.fixnum = 0;
  e_ListGuard.script = &listguard_script;
}
//@}
