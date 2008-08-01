#include "elib.h"

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

e_Script e__timer_script;
e_Method timer_methods[] = {
  {"now/0", timer_now},
  {NULL}
};




e_Ref e_timer;

