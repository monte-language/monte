/* -*- mode: c -*- */
#include <check.h>
#include <stdio.h>
#include <string.h>
#include "elib.h"

void setup(void) {
  e_set_up();
}

void teardown(void) {
  if (e_thrown_problem().script != NULL) {
    e_println(e_stdout, e_thrown_problem());
    fail("Unhandled exception");
  } else if (e_ejected_value().script != NULL) {
    e_println(e_stdout, e_ejected_value());
    fail("Unhandled ejection");
  }
}

#test create
{
  e_Ref v = e_make_vat(e_null, "bob");
  Vat_data *vat = v.data.other;
  fail_unless(e_same(vat->label, e_make_string("bob")));
  fail_unless(e_same(vat->runner, e_null));
  fail_unless(vat->turncounter == 0);
  fail_unless(g_async_queue_length(vat->messageQueue) == 0);
}

#test currency
{
  e_Ref v = e_make_vat(e_null, "bob");
  fail_unless(e_same(e_current_vat(), e_null));
  e_vat_set_active(v);
  fail_unless(e_same(e_current_vat(), v));
}

//#test sendonly
//{
//  
//}


#main-pre
{
  tcase_add_checked_fixture(tc1_1, setup, teardown);
}
