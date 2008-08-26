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

void fake_runnable(e_Ref vat, void *data) {
  return;
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

#test enqueue
{
  e_Ref v = e_make_vat(e_null, "bob");
  e_vat_set_active(v);
  e_Ref val = e_make_fixnum(1);
  Vat_data *vat = v.data.other;
  e_Runnable_Item *item;
  e_vat_enqueue(v, fake_runnable, &val);
  fail_unless(g_async_queue_length(vat->messageQueue) == 1);
  item = g_async_queue_pop(vat->messageQueue);
  fail_unless((e_Ref *)(item->data) == &val);
  fail_unless(item->function == &fake_runnable);
  fail_unless(e_same(item->vat, v));
}


#main-pre
{
  tcase_add_checked_fixture(tc1_1, setup, teardown);
}
