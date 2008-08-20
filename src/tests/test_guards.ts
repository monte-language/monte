 /* -*- mode: c -*- */
#include <check.h>
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

#define HAS_PROBLEM(val) (val.script == NULL && val.data.fixnum == 0)
static void cleanup_exits() {
  e_thrown_problem_set(e_empty_ref);
  e_ejected_value_set(e_empty_ref);
}

 /** Test that the type guard accepts only objects of that type, calling an
     ejector on coercion failure if specified and throwing a problem if
     not. */
static void test_type_guard(e_Ref guard, char *typeName, e_Ref specimen,
                            e_Ref badSpecimen) {
  // coercion should work with a null ejector
  e_Ref res = e_coerce(guard, specimen, e_null);
  if (HAS_PROBLEM(res)) {
    fail("`%s' guard threw an error when coercing an instance of `%s'",
         typeName, typeName);
  }
  fail_unless(e_same(res, specimen));
  e_Ref ej = e_make_ejector();
  // coercion should work with a defined ejector
  res = e_coerce(guard, specimen, ej);
  fail_unless(e_same(res, specimen));
  e_ON_EJECTION(res, ej) {
    fail("`%s' guard failed to accept an %s",
         typeName, typeName);
  }
  e_ejector_disable(ej);
  e_Ref ej2 = e_make_ejector();
  // coercion should eject when it can't succeed
  res = e_coerce(guard, badSpecimen, ej2);
  e_ON_EJECTION(res, ej2) {
    // XXX assert something about the complaint?
    fail_unless(e_same(e_ejected_value().data.refs[1], badSpecimen));
  } else {
    fail("`%s' guard didn't eject when coercing a non-`%s'",
         typeName, typeName);
  }
  e_ejector_disable(ej2);
  if (HAS_PROBLEM(res)) {
    fail("`%s' guard threw an error instead of ejecting on coercion failure",
         typeName);
  }


  res = e_coerce(guard, badSpecimen, e_null);
  if (!HAS_PROBLEM(res)) {
    fail("`%s' guard didn't throw a problem when coercing a non-%s",
         typeName, typeName);
  } else {
    fail_unless(e_same(e_thrown_problem().data.refs[1], badSpecimen));
  }
  cleanup_exits();
}

/// The boolean guard only accepts boolean values.
#test booleanguard
{
  test_type_guard(e_BooleanGuard, "boolean", e_true, e_make_fixnum(1));
  test_type_guard(e_BooleanGuard, "boolean", e_false, e_make_fixnum(0));
}

/// The char guard only accepts characters.
#test charguard
{
  test_type_guard(e_CharGuard, "char", e_make_char('a'), e_make_fixnum(97));
}

/// The float64 guard only accepts float64s.
#test float64guard
{
  test_type_guard(e_Float64Guard, "float64", e_make_float64(3.1415),
                  e_make_char('a'));
}

/// The int guard only accepts fixnums and bignums.
#test intguard
{
  mpz_t bignum;
  test_type_guard(e_IntGuard, "int", e_make_fixnum(1), e_make_string("1"));
  mpz_init_set_str(bignum,  "4000000000", 10);
  test_type_guard(e_IntGuard, "int", e_make_bignum(&bignum), e_null);
}

/// The List guard only accepts ConstLists and FlexLists.
#test listguard
{
  e_Ref bits[] = {e_true, e_null, e_make_fixnum(1)};
  e_Ref list = e_constlist_from_array(3, bits);
  e_Ref flexlist = e_flexlist_from_array(3, bits);
  test_type_guard(e_ListGuard, "List", list, e_null);
  test_type_guard(e_ListGuard, "List", flexlist, e_null);
}

/// Objects that can be expressed as literals correctly check as Selfless.
#test selfless_literals
{
  mpz_t bignum;
  mpz_init_set_str(bignum,  "4000000000", 10);
  fail_unless(e_is_selfless(e_make_fixnum(1)));
  fail_unless(e_is_selfless(e_make_boolean(true)));
  fail_unless(e_is_selfless(e_make_bignum(&bignum)));
  fail_unless(e_is_selfless(e_make_string("x")));
  fail_unless(e_is_selfless(e_make_float64(1.5)));
  fail_unless(e_is_selfless(e_constlist_from_array(0, NULL)));
  fail_unless(e_is_selfless(e_make_constmap(0)));
  fail_if(e_is_selfless(e_make_flexmap(0)));
  fail_if(e_is_selfless(e_flexlist_from_array(0, NULL)));

}
/// Guard objects are Selfless.
#test selfless_guards
{
  fail_unless(e_is_selfless(e_IntGuard));
  fail_unless(e_is_selfless(e_StringGuard));
}

#main-pre
{
  tcase_add_checked_fixture(tc1_1, setup, teardown);
}
