#include "elib.h"
#include <string.h>


e_Ref e_privilegedScope;

void e__privilegedscope_set_up() {
  e_make_script(&e__timer_script, NULL, timer_methods, "Timer");
  e_make_script(&e__println_script, println_collectArgs, no_methods, "println");
  e_make_script(&e__print_script, print_collectArgs, no_methods, "print");
  e_timer.script = &e__timer_script;
  e_println_object.script = &e__println_script;
  e_print_object.script = &e__print_script;
}
