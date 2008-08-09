 /* -*- mode: c -*- */
#include <check.h>
#include <stdio.h>
#include "elib.h"
#include <gmp.h>
#include <string.h>
static e_Selector do_add;
static e_Selector do_wrong;

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

#define HAS_PROBLEM(val) (val.script == NULL && val.data.fixnum == 0)
static void cleanup_exits() {
  e_thrown_problem_set(e_empty_ref);
  e_ejected_value_set(e_empty_ref);
}

#test hello_world
{
  /*
    Basic "hello world" test for the string type and the I/O system.
  */

  e_Ref res = e_print(e_stdout, e_make_string ("Hello, world!\n"));
  if (HAS_PROBLEM(res)) {
    e_println (e_stderr, e_thrown_problem());
    fail("E error raised");
  }
}

#test primitive_same
{
    // e_same should compare primitively-typed E objects with identical values
    // as identical.
    mpz_t bignum, bignum2;
    mpz_init_set_str(bignum, "4000000000", 10);
    mpz_init_set_str(bignum2, "4000000000", 10);
    fail_unless(e_same(e_make_fixnum(17), e_make_fixnum(17)));
    fail_unless(e_same(e_make_bignum(&bignum), e_make_bignum(&bignum2)));
    fail_unless(e_same(e_make_char('q'), e_make_char('q')));
    fail_unless(e_same(e_make_string("foo"), e_make_string("foo")));
    fail_unless(e_same(e_make_float64(3.14159), e_make_float64(3.14159)));
    fail_if(e_same(e_make_fixnum(97), e_make_char('a')));
}

#test equalizer
{
    e_Selector sameEver;
    e_make_selector(&sameEver, "sameEver", 2);
    fail_unless(e_eq(e_call_2(e_equalizer, &sameEver,
                    e_make_string("foo"),
                    e_make_string("foo")), e_true));

}

#test fixnum_add
{
  /*
    Test adding fixnums.
  */
  e_make_selector (&do_add, "add", 1);
  fail_unless(e_call_1(e_make_fixnum(2), &do_add,
                       e_make_fixnum(3)).data.fixnum == 5);
}

#test fixnum_add_overflow
{
  /*
    Test overflowing fixnums into bignums.
   */
  e_make_selector (&do_add, "add", 1);
  e_Ref val = e_call_1 (e_make_fixnum (2000000000),
                        &do_add,
                        e_make_fixnum (2000000000));
  mpz_t val2;
  mpz_init_set_str(val2, "4000000000", 10);
  fail_unless(mpz_cmp(*val.data.bignum, val2) == 0, NULL);
}

#test finalslot
{
  // Test creation and manipulation of finalslots.
  e_Selector do_get, do_put;
  e_make_selector(&do_get, "get", 0);
  e_make_selector(&do_put, "put", 1);
  e_Ref fn = e_make_fixnum(2);
  e_Ref slot = e_make_finalslot(fn);
  fail_unless(e_same(e_call_0(slot, &do_get), fn));
  e_Ref res = e_call_1(slot, &do_put, fn);
  if(!HAS_PROBLEM(res)) {
    fail("Final slot allowed assignment");
  } else {
    fail_unless(strcmp((e_thrown_problem().data.gstring)->str, "Final variables may not be changed.") == 0);
    cleanup_exits();
  }
}


#test varslot
{
  // Test creation and manipulation of varslots.
  e_Selector do_get, do_put;
  e_make_selector(&do_get, "get", 0);
  e_make_selector(&do_put, "put", 1);
  e_Ref fn = e_make_fixnum(2);
  e_Ref fn2 = e_make_fixnum(3);
  e_Ref slot = e_make_varslot(fn);
  fail_unless(e_same(e_call_0(slot, &do_get), fn));
  e_Ref res = e_call_1(slot, &do_put, fn2);
  if (HAS_PROBLEM(res)) {
    fail("varslot assignment failed");
  } else {
    fail_unless(e_same(e_call_0(slot, &do_get), fn2));
  }
}

#test intguard
{
  /// Test that IntGuard accepts ints and ints only, calling an ejector on
  /// coercion failure if specified and throwing a problem if not.
  e_Selector do_coerce;
  e_make_selector(&do_coerce, "coerce", 2);
  e_Ref fn = e_make_fixnum(1);
  e_Ref str = e_make_string("1");
  // coercion should work with a null ejector
  e_Ref res = e_call_2(e_IntGuard, &do_coerce, fn, e_null);
  if (HAS_PROBLEM(res)) {
    fail("IntGuard threw an error when coercing an int");
  }
  fail_unless(e_same(res, fn));
  e_Ref ej = e_make_ejector();
  // coercion should work with a defined ejector
  res = e_call_2(e_IntGuard, &do_coerce, fn, ej);
  fail_unless(e_same(res, fn));
  e_ON_EJECTION(res, ej) {
    fail("IntGuard failed to accept an int");
  }
  e_ejector_disable(ej);
  e_Ref ej2 = e_make_ejector();
  // coercion should eject when it can't succeed
  res = e_call_2(e_IntGuard, &do_coerce, str, ej2);
  e_ON_EJECTION(res, ej2) {
    // XXX assert something about the complaint?
    fail_unless(e_same(e_ejected_value().data.refs[1], str));
  } else {
    fail("IntGuard didn't eject when coercing a string");
  }
  e_ejector_disable(ej2);
  if (HAS_PROBLEM(res)) {
    fail("IntGuard threw an error instead of ejecting on coercion failure");
  }


  res = e_call_2(e_IntGuard, &do_coerce, str, e_null);
  if (!HAS_PROBLEM(res)) {
    fail("IntGuard didn't throw a problem when coercing a string");
  } else {
    fail_unless(e_same(e_thrown_problem().data.refs[1], str));
  }
  cleanup_exits();
}

#test guardedslot
{
  // Test creation and manipulation of guarded slots.
  e_Selector do_get, do_put;
  e_make_selector(&do_get, "get", 0);
  e_make_selector(&do_put, "put", 1);
  e_Ref fn = e_make_fixnum(2);
  e_Ref fn2 = e_make_fixnum(3);
  e_Ref str = e_make_string("foo");
  e_Ref slot, res;
  slot = e_new_guardedslot(fn, e_IntGuard, e_null);
  if (HAS_PROBLEM(slot)) {
    fail("Creating a guarded slot failed");
  }
  res = e_call_0(slot, &do_get);
  if (HAS_PROBLEM(slot)) {
    fail("Fetching from a guarded slot failed");
  }
  fail_unless(e_same(res, fn));
  res = e_call_1(slot, &do_put, fn2);
  if (HAS_PROBLEM(res)) {
    fail("Assigning to a guarded slot failed");
  }
  res = e_call_0(slot, &do_get);
  if (HAS_PROBLEM(slot)) {
    fail("Fetching from a guarded slot failed");
  }
  fail_unless(e_same(res, fn2));


  res = e_call_1(slot, &do_put, str);
  if (!HAS_PROBLEM(res)) {
    fail("Assigning a string to an IntGuard-guarded slot succeeded");
  } else {
    fail_unless(e_same(e_thrown_problem().data.refs[1], str));
  }
  cleanup_exits();
}

#test flexmap_size
{
  e_Selector size, put;
  e_make_selector(&size, "size", 0);
  e_make_selector(&put, "put", 2);
  e_Ref fm = e_make_flexmap(3);
  fail_unless(e_call(fm, &size, 0).data.fixnum == 0);
  e_Ref key = e_make_char('a'), value = e_make_fixnum(1);
  e_call_2(fm, &put, key, value);
  fail_unless(e_call_0(fm, &size).data.fixnum == 1);
}

#test constlist_size
{
  e_Selector size;
  e_make_selector(&size, "size", 0);
  e_Ref contents[3] = { e_make_fixnum(2), e_make_fixnum(4), e_make_fixnum(7) };
  e_Ref aList = e_constlist_from_array(3, contents);
  fail_unless(e_call_0(aList, &size).data.fixnum == 3);
}

#test list_indexing
{
  // Test creation and indexing of lists.
  e_Selector do_get;
  e_Ref contents[3] = { e_make_fixnum(2), e_make_fixnum(4), e_make_fixnum(7) };
  e_make_selector(&do_get, "get", 1);
  e_Ref aList = e_constlist_from_array(3, contents);
  for (int i = 0; i < 3; i++) {
    fail_unless(e_same(e_call_1(aList, &do_get, e_make_fixnum(i)), contents[i]));
  };
}

#test thrower
{
  /// Test that the thrower object actually throws.
  e_Selector do_run;
  e_Ref res;
  e_make_selector(&do_run, "run", 1);

  res = e_call_1(e_thrower, &do_run, e_make_fixnum(1));
  if (!HAS_PROBLEM(res)) {
    fail("thrower didn't throw");
  } else {
    fail_unless(e_same(e_thrown_problem(), e_make_fixnum(1)));
  }
  cleanup_exits();
}

#main-pre
{
  tcase_add_checked_fixture(tc1_1, setup, teardown);
}
