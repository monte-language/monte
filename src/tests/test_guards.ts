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
e_Ref e_coerce(e_Ref guard, e_Ref specimen, e_Ref optEjector) {
  e_Selector do_coerce;
  e_make_selector(&do_coerce, "coerce", 2);
  return e_call_2(guard, &do_coerce, specimen, optEjector);
}

#define HAS_PROBLEM(val) (val.script == NULL && val.data.fixnum == 0)
static void cleanup_exits() {
  e_thrown_problem_set(e_empty_ref);
  e_ejected_value_set(e_empty_ref);
}


static void test_type_guard(e_Ref guard, char *typeName, e_Ref specimen,
                            e_Ref badSpecimen) {
  /** Test that the type guard accepts only objects of that type, calling an
      ejector on coercion failure if specified and throwing a problem if
      not. */

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

#test booleanguard
{
  test_type_guard(e_BooleanGuard, "boolean", e_true, e_make_fixnum(1));
  test_type_guard(e_BooleanGuard, "boolean", e_false, e_make_fixnum(0));
}

#test charguard
{
  test_type_guard(e_CharGuard, "char", e_make_char('a'), e_make_fixnum(97));
}

#test float64guard
{
  test_type_guard(e_Float64Guard, "float64", e_make_float64(3.1415),
                  e_make_char('a'));
}

#test intguard
{
  test_type_guard(e_IntGuard, "int", e_make_fixnum(1), e_make_string("1"));
}

#test listguard
{
  e_Ref bits[] = {e_true, e_null, e_make_fixnum(1)};
  e_Ref list = e_constlist_from_array(3, bits);
  e_Ref flexlist = e_flexlist_from_array(3, bits);
  test_type_guard(e_ListGuard, "List", list, flexlist);
}


#main-pre
{
  tcase_add_checked_fixture(tc1_1, setup, teardown);
}
