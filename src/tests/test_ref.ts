/* -*- mode: c -*- */
#include <check.h>
#include <stdlib.h>
#include "elib.h"
#include "ref.h"
#include "ref_private.h"

e_Ref sRef, resolver;
e_Selector isResolved, resolve, size, get, fulfillment;
void setup(void) {
  e_set_up();
  e_make_selector(&size, "size", 0);
  e_make_selector(&get, "get", 1);
  e_make_selector(&isResolved, "isResolved", 0);
  e_make_selector(&resolve, "resolve", 1);
  e_make_selector(&fulfillment, "fulfillment", 1);
  e_Ref pair = e_make_promise_pair();
  fail_unless(e_is_constlist(pair));
  fail_unless(e_call_0(pair, &size).data.fixnum == 2);
  sRef = e_call_1(pair, &get, e_make_fixnum(0));
  resolver = e_call_1(pair, &get, e_make_fixnum(1));
}

void teardown(void) {
}

#test existence
{
  // Test that make_promise_pair() at least creates objects of the
  // right type.
  fail_unless(e_is_SwitchableRef(sRef));
  fail_unless(e_is_LocalResolver(resolver));

}

#test resolution
{
  // Ensure that Refs track their resolution state properly.
  fail_if(e_same(e_ref_isResolved(sRef), e_true));
  fail_unless(e_ref_state(sRef) == EVENTUAL);
  fail_unless(e_same(e_call_1(resolver, &resolve, e_make_fixnum(99)), e_null));
  fail_unless(e_same(e_ref_isResolved(sRef), e_true));
  fail_unless(e_ref_state(sRef) == NEAR);
}

#test broken_resolution
{
  // e_ref_state reports references that are broken.
  e_Ref p = e_make_string("bad stuff happened");
  e_resolver_smash(resolver, p);
  fail_unless(e_ref_state(sRef) == BROKEN);
}


#test message
{
  // Messages sent to a SwitchableRef after resolution should forward
  // to its target.
  e_Selector add;
  e_make_selector(&add, "add", 1);
  e_call_1(resolver, &resolve, e_make_fixnum(99));
  fail_unless(e_call_1(sRef, &add, e_make_fixnum(1)).data.fixnum == 100);
}

#test shortening
{
  // Refs to Refs to objects should become Refs to objects when
  // shortened.
  e_Ref sRef2, resolver2;
  e_Ref pair = e_make_promise_pair();
  e_Ref obj = e_make_fixnum(99);
  SwitchableRef_data *ref;
  sRef2 = e_call_1(pair, &get, e_make_fixnum(0));
  resolver2 = e_call_1(pair, &get, e_make_fixnum(1));
  e_call_1(resolver2, &resolve, obj);
  e_call_1(resolver, &resolve, sRef2);
  ref = sRef.data.other;
  fail_unless(e_same(ref->target, obj));
}

#test buffering_sendOnly
{
  // Messages sent to unresolved refs should be buffered.
  e_Selector sendOnly, size, get;
  e_Ref arglist, ref2, target, val;
  e_Ref v = e_make_vat(e_null, "test");
  e_vat_set_active(v);
  e_make_selector(&sendOnly, "sendOnly", 3);
  e_make_selector(&size, "size", 0);
  e_make_selector(&get, "get", 1);
  val = e_make_fixnum(17);
  arglist = e_constlist_from_array(1, &val);
  target = e_flexlist_from_array(0, NULL);
  e_Ref sendOnlyArgs[] = { sRef, e_make_string("push"), arglist};
  ref2 = e_call(THE_E, &sendOnly, sendOnlyArgs);
  fail_unless(e_eq(ref2, e_null));
  e_call_1(resolver, &resolve, target);
  fail_unless(e_eq(e_call_0(target, &size), e_make_fixnum(0)));
  while (e_vat_execute_turn(v)) {};
  fail_unless(e_eq(e_call_0(target, &size), e_make_fixnum(1)));
  e_Ref val2 = e_call_1(arglist, &get, e_make_fixnum(0));
  e_Ref eqargs[] = {val2, val};
  fail_unless(e_eq(e_sameEver(e_equalizer, eqargs), e_true));
}


#test buffering_send
{
  /** Messages sent to unresolved refs should return promises that resolve to
      the result of the send. */
  e_Selector send, size, get;
  e_Ref arglist, ref2, target, val;
  e_Ref v = e_make_vat(e_null, "test");
  e_vat_set_active(v);
  e_make_selector(&send, "send", 3);
  e_make_selector(&size, "size", 0);
  e_make_selector(&get, "get", 1);
  val = e_make_fixnum(17);
  arglist = e_constlist_from_array(1, &val);
  target = e_make_fixnum(21);
  e_Ref sendArgs[] = { sRef, e_make_string("add"), arglist};
  ref2 = e_call(THE_E, &send, sendArgs);
  e_vat_execute_turn(v);
  fail_unless(e_ref_state(ref2) == EVENTUAL);
  e_call_1(resolver, &resolve, e_make_fixnum(4));
  fail_unless(e_ref_state(ref2) == EVENTUAL);
  while (e_vat_execute_turn(v)) {};
  fail_unless(e_ref_state(ref2) == NEAR);
  e_Ref eqargs[] = {ref2, target};
  fail_unless(e_eq(e_sameEver(e_equalizer, eqargs), e_true));
}


#test smash
{
  // e_resolver_smash should convert a resolver's ref to a broken promise.
  e_Ref p = e_make_string("bad stuff happened");
  e_resolver_smash(resolver, p);
  fail_unless(e_is_UnconnectedRef(e_ref_target(sRef)));
}

#test near_fulfillment
{
  // Ref.fulfillment/1 shortens a ref if it is near.
  e_Ref x = e_make_fixnum(99);
  e_call_1(resolver, &resolve, x);
  fail_unless(e_same(e_call_1(THE_REF, &fulfillment, sRef), x));
}

#test unresolved_fulfillment
{
  // Ref.fulfillment/1 throws an error if its arg is unresolved.
  e_Ref p = e_call_1(THE_REF, &fulfillment, sRef);
  fail_unless(p.script == NULL);
  e_Ref prob = e_thrown_problem();
  fail_unless(e_same(prob.data.refs[0],
                     e_make_string("Failed: Not resolved")));
  fail_unless(e_same(prob.data.refs[1],
                     sRef));
}

#test broken_fulfillment
{
  // Ref.fulfillment/1 throws the problem wrapped by a broken reference.
  e_Ref p = e_make_string("bad stuff happened");
  e_resolver_smash(resolver, p);
  e_Ref q = e_call_1(THE_REF, &fulfillment, sRef);
  fail_unless(q.script == NULL);
  e_Ref prob = e_thrown_problem();
  fail_unless(e_same(prob, p));
}

#main-pre
{
  tcase_add_checked_fixture(tc1_1, setup, teardown);
}
