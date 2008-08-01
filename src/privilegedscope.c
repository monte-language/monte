#include "elib.h"
#include <string.h>
#include <sys/time.h>

e_Ref e_privilegedScope;
e_Ref e_timer, e_println_object, e_print_object;

static e_Script e__println_script;
static e_Script e__print_script;
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

void e__privilegedscope_set_up() {
  e_make_script(&e__timer_script, NULL, timer_methods, "Timer");
  e_make_script(&e__println_script, println_collectArgs, no_methods, "println");
  e_make_script(&e__print_script, print_collectArgs, no_methods, "print");
  e_timer.script = &e__timer_script;
  e_println_object.script = &e__println_script;
  e_print_object.script = &e__print_script;
}
