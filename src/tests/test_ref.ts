/* -*- mode: c -*- */
#include <check.h>
#include <stdlib.h>
#include "elib.h"
#include "ref.h"
#include "ref_private.h"

e_Ref sRef, resolver;
e_Selector isResolved, resolve, size, get;
void setup(void) {
  e_set_up();
  e_make_selector(&size, "size", 0);
  e_make_selector(&get, "get", 1);
  e_make_selector(&isResolved, "isResolved", 0);
  e_make_selector(&resolve, "resolve", 1);
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
  fail_unless(e_same(ref->myTarget, obj));
}

#test buffering
{
  // Messages sent to unresolved refs should be buffered.
}

#test smash
{
  // e_resolver_smash should convert a resolver's ref to a broken promise.
  e_Ref p = e_make_string("bad stuff happened");
  e_resolver_smash(resolver, p);
  fail_unless(e_is_UnconnectedRef(e_ref_target(sRef)));
}
#main-pre
{
  tcase_add_checked_fixture(tc1_1, setup, teardown);
}
