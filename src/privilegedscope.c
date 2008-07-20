#include "elib.h"
#include <string.h>
#include <sys/time.h>

e_Ref e_privilegedScope, e_timer, e_println_object, e_print_object;

static e_Ref timer_now(e_Ref self, e_Ref *args) {
  struct timeval t;
  if (gettimeofday(&t, NULL) == 0) {
    e_Selector mult, add;
    e_make_selector(&mult, "multiply", 1);
    e_make_selector(&add, "add", 1);
    e_Ref t1 = e_bignum_from_fixnum(t.tv_sec);
    E_ERROR_CHECK(t1);
    e_Ref onethousand = e_make_fixnum(1000);
    e_Ref t2 = e_call(t1, &mult, &onethousand);
    E_ERROR_CHECK(t2);
    e_Ref usec = e_make_fixnum(t.tv_usec / 10000);
    return e_call(t2, &add, &usec);
  } else {
    return e_throw_cstring("timer.now() problem");
  }
}

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

static e_Script e__timer_script;
static e_Method timer_methods[] = {
  {"now/0", timer_now},
  {NULL}
};


void e__privilegedscope_set_up() {
  e_make_script(&e__timer_script, NULL, timer_methods, "Timer");
  e_make_script(&e__println_script, println_collectArgs, no_methods, "println");
  e_make_script(&e__print_script, print_collectArgs, no_methods, "print");
  e_timer.script = &e__timer_script;
  e_println_object.script = &e__println_script;
  e_print_object.script = &e__print_script;
}
