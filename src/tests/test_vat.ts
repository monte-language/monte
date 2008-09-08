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
  // Vat creation sets up the initial parameters correctly.
  e_Ref v = e_make_vat(e_null, "bob");
  Vat_data *vat = v.data.other;
  fail_unless(e_same(vat->label, e_make_string("bob")));
  fail_unless(e_same(vat->runner, e_null));
  fail_unless(vat->turncounter == 0);
  fail_unless(g_async_queue_length(vat->messageQueue) == 0);
}

#test currency
{
  // Setting the current vat works.
  e_Ref v = e_make_vat(e_null, "bob");
  fail_unless(e_same(e_current_vat(), e_null));
  e_vat_set_active(v);
  fail_unless(e_same(e_current_vat(), v));
}

#test enqueue
{
  // Enqueuing a runnable function works.
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

#test sendonly
{
  // Enqueuing a message send works.
  e_Ref v = e_make_vat(e_null, "bob");
  e_Ref obj = e_make_fixnum(3);
  e_Ref arg = e_make_fixnum(4);
  Vat_data *vat = v.data.other;
  e_Selector add;
  e_PendingDelivery *msg;
  e_Runnable_Item *item;
  e_vat_set_active(v);
  e_make_selector(&add, "add", 1);
  e_vat_sendOnly(v, obj, &add, &arg);
  fail_unless(g_async_queue_length(vat->messageQueue) == 1);
  item = g_async_queue_pop(vat->messageQueue);
  msg = (e_PendingDelivery *)item->data;
  fail_unless(e_same(msg->object, obj));
  fail_unless(msg->selector == &add);
  fail_unless(e_same(msg->args[0], arg));
  fail_unless(e_same(msg->resolverVat, e_null));
  fail_unless(e_same(msg->resolver, e_null));
}

#test send
{
  // Enqueuing a message send with reply works.
  e_Ref v = e_make_vat(e_null, "bob");
  e_Ref obj = e_make_fixnum(3);
  e_Ref arg = e_make_fixnum(4);
  Vat_data *vat = v.data.other;
  e_Selector add, get;
  e_make_selector(&add, "add", 1);
  e_make_selector(&get, "get", 1);
  e_PendingDelivery *msg;
  e_Runnable_Item *item;
  e_Ref ppair = e_make_promise_pair();
  e_Ref result = e_call_1(ppair, &get, e_make_fixnum(0));
  e_Ref resolver = e_call_1(ppair, &get, e_make_fixnum(1));
  e_vat_set_active(v);
  e_vat_send(v, obj, &add, &arg, v, resolver);
  fail_unless(g_async_queue_length(vat->messageQueue) == 1);
  item = g_async_queue_pop(vat->messageQueue);
  msg = (e_PendingDelivery *)item->data;
  fail_unless(e_same(msg->object, obj));
  fail_unless(msg->selector == &add);
  fail_unless(e_same(msg->args[0], arg));
  fail_unless(e_same(msg->resolverVat, v));
  fail_unless(e_same(msg->resolver, resolver));
}

#test execute_send
{
  /* Executing an enqueued message send runs the call and
     enqueues the send for the reply. */
  e_Ref v = e_make_vat(e_null, "bob");
  e_Ref v2 = e_make_vat(e_null, "bob");
  Vat_data *vat = v.data.other;
  Vat_data *vat2 = v2.data.other;
  e_Ref obj = e_make_fixnum(3);
  e_Ref arg = e_make_fixnum(4);
  e_PendingDelivery *msg;
  e_Runnable_Item *item;
  e_Selector add, get;
  e_make_selector(&add, "add", 1);
  e_make_selector(&get, "get", 1);
  e_Ref ppair = e_make_promise_pair();
  e_Ref result = e_call_1(ppair, &get, e_make_fixnum(0));
  e_Ref resolver = e_call_1(ppair, &get, e_make_fixnum(1));

  e_vat_set_active(v);
  e_PendingDelivery pd = {.object = obj, .selector = &add,
                           .args = &arg, .resolverVat = v2,
                           .resolver = resolver};
  e_vat_execute_send(v, &pd);
  fail_unless(vat->turncounter == 1);
  fail_unless(g_async_queue_length(vat2->messageQueue) == 1);
  item = g_async_queue_pop(vat2->messageQueue);
  msg = (e_PendingDelivery *)item->data;
  fail_unless(e_same(msg->object, resolver));
  fail_unless(strcmp(msg->selector->verb, "resolve/1") == 0);
  fail_unless(e_same(msg->args[0], e_make_fixnum(7)));
  fail_unless(e_same(msg->resolverVat, e_null));
  fail_unless(e_same(msg->resolver, e_null));
}

#test turn_execute
{
  // Executing a turn runs the next enqueued message send.
  e_Ref v = e_make_vat(e_null, "bob");
  e_Ref v2 = e_make_vat(e_null, "bob");
  Vat_data *vat = v.data.other;
  Vat_data *vat2 = v2.data.other;
  e_Ref obj = e_make_fixnum(3);
  e_Ref arg = e_make_fixnum(4);
  e_Selector add, get;
  e_make_selector(&add, "add", 1);
  e_make_selector(&get, "get", 1);
  e_Ref ppair = e_make_promise_pair();
  e_Ref result = e_call_1(ppair, &get, e_make_fixnum(0));
  e_Ref resolver = e_call_1(ppair, &get, e_make_fixnum(1));
  e_vat_set_active(v);
  e_vat_send(v, obj, &add, &arg, v2, resolver);
  fail_unless(g_async_queue_length(vat->messageQueue) == 1);
  fail_if(e_vat_execute_turn(v));
  fail_unless(g_async_queue_length(vat2->messageQueue) == 1);
  fail_if(e_vat_execute_turn(v2));
  fail_unless(e_same(e_ref_target(result), e_make_fixnum(7)));
}

#main-pre
{
  tcase_add_checked_fixture(tc1_1, setup, teardown);
}
