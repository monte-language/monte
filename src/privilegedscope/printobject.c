#include "elib.h"
#include <string.h>



e_Ref print_collectArgs(e_Ref self, e_Selector *sel, e_Ref *args) {
  if (strncmp("run", sel->verb, 3) != 0) {
    return otherwise_miranda_methods(self, sel, args);
  } else {
    for (int i = 0; i < sel->arity; i++) {
      E_ERROR_CHECK(e_print(e_stdout, args[i]));
    }
    return e_null;
  }
}

e_Ref println_collectArgs(e_Ref self, e_Selector *sel, e_Ref *args) {
  if (strncmp("run", sel->verb, 3) != 0) {
    return otherwise_miranda_methods(self, sel, args);
  } else {
    for (int i = 0; i < sel->arity; i++) {
      E_ERROR_CHECK(e_print(e_stdout, args[i]));
    }
    return e_print(e_stdout, e_make_string("\n"));
  }

}

e_Script e__println_script,  e__print_script;
e_Ref e_println_object, e_print_object;
