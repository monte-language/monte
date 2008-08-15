 /* -*- mode: c -*- */
#include <check.h>
#include <stdio.h>
#include "elib.h"
#include <gmp.h>
#include <string.h>

e_Selector sameEver, put, push, snapshot;

void setup(void) {
  e_set_up();
  e_make_selector(&sameEver, "sameEver", 2);
  e_make_selector(&put, "put", 2);
  e_make_selector(&push, "push", 1);
  e_make_selector(&snapshot, "snapshot", 0);
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

static void test_equal(e_Ref left, e_Ref right) {
  fail_unless(e_eq(e_call_2(e_equalizer, &sameEver,
                            left, right), e_true));
}

static void test_unequal(e_Ref left, e_Ref right) {

    fail_if(e_eq(e_call_2(e_equalizer, &sameEver,
                          left, right), e_true));

}

#test string
{
  test_equal(e_make_string("foo"),
             e_make_string("foo"));
}


#test booleans
{
  test_equal(e_true, e_true);
  test_unequal(e_true, e_false);
  test_equal(e_true, e_true);
}

#test fixnum
{
  test_equal(e_make_fixnum(17),
             e_make_fixnum(17));
}

#test character
{
  test_equal(e_make_char('q'), e_make_char('q'));
}

#test float64
{
  test_equal(e_make_float64(3.14159), e_make_float64(3.14159));
}

#test bignum
{
    mpz_t bignum, bignum2;
    mpz_init_set_str(bignum,  "4000000000", 10);
    mpz_init_set_str(bignum2, "4000000000", 10);

    test_equal(e_make_bignum(&bignum), e_make_bignum(&bignum2));
}

#test null
{
  test_equal(e_null, e_null);
}

#test mismatch
{
  test_unequal(e_make_fixnum(97), e_make_char('a'));
}

#test constlist
{
  e_Ref bits[] = {e_null, e_true, e_make_fixnum(1)};
  e_Ref left = e_constlist_from_array(3, bits);
  e_Ref right = e_constlist_from_array(3, bits);
  test_equal(left, left);
  test_equal(left, right);
}

#test constmap
{
  e_Ref ks[] = {e_make_fixnum(3), e_make_fixnum(7)};
  e_Ref vs[] = {e_make_string("yes"), e_make_string("hooray")};
  e_Ref left = e_make_flexmap(2);
  e_Ref right = e_make_flexmap(2);
  e_call_2(left, &put, ks[0], vs[0]);
  e_call_2(right, &put, ks[0], vs[0]);
  e_call_2(left, &put, ks[1], vs[1]);
  e_call_2(right, &put, ks[1], vs[1]);
  left = e_call_0(left, &snapshot);
  right = e_call_0(right, &snapshot);
  test_equal(left, left);
  test_equal(right, right);
}

#test simple_circular_constlist
{
  e_Ref bits[] = {e_make_fixnum(1), e_make_fixnum(3), e_null};
  e_Ref left = e_constlist_from_array(3, bits);
  e_Ref right = e_constlist_from_array(3, bits);
  Flexlist_data *leftdata = left.data.other, *rightdata = right.data.other;
  // cheat a bit. normally this would need to be indirected through a promise
  leftdata->elements[2] = left;
  rightdata->elements[2] = right;
  test_equal(left, left);
  test_equal(left, right);
}

#test simple_circular_constmap
{
  e_Ref ks[] = {e_make_fixnum(3), e_make_fixnum(7)};
  e_Ref v = e_make_string("yes");
  e_Ref left = e_make_flexmap(2);
  e_Ref right = e_make_flexmap(2);
  e_call_2(left, &put, ks[0], v);
  e_call_2(right, &put, ks[0], v);
  e_call_2(left, &put, ks[1], left);
  e_call_2(right, &put, ks[1], right);
  left = e_call_0(left, &snapshot);
  right = e_call_0(right, &snapshot);
  // cheat as above
  Flexmap_data *leftdata = left.data.other, *rightdata = right.data.other;
  leftdata->values[1] = left;
  rightdata->values[1] = right;
  test_equal(left, left);
  test_equal(left, right);
}


#main-pre
{
  tcase_add_checked_fixture(tc1_1, setup, teardown);
}
