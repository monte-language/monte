/* -*- mode: c -*- */

#include <string.h>
#include <check.h>
#include "elib.h"

int sentinel;
e_Selector result_selector;
e_Selector do_run;
e_Ref result_object;
e_Script test_script;
e_def_type_predicate(e_is_testobject, test_script);

void setup(void) {
  e_set_up();
  sentinel = 0;
  result_selector.verb = NULL;
  result_selector.arity = -1;
  result_object = e_null;
  e_make_selector(&do_run, "run", 1);
}
#define HAS_PROBLEM(val) (val.script == NULL && val.data.fixnum == 0)

static void cleanup_exits() {
  e_thrown_problem_set(e_empty_ref);
  e_ejected_value_set(e_empty_ref);;
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

e_Ref test_throw_function(int num) {
  e_Ref obj = e_make_fixnum(num);
  return e_throw(obj);
}
e_Ref test_eject_function(int num, e_Ref ejector) {
  return e_call_1(ejector, &do_run, e_make_fixnum(num));
}

e_Ref test_eject_function2(int num, e_Ref ejector) {
  e_Ref numObj = e_make_fixnum(num);
  e_Ref res = e_call_1(ejector, &do_run, numObj);
  if (HAS_PROBLEM(res)) {
    fail("Ejector raised an exception upon invocation");
  }
  return res;
}


e_Ref test_eject_function3(int num, e_Ref ejector) {
  e_Ref numObj = e_make_fixnum(num);
  e_Ref ej2 = e_make_ejector();
  e_Ref res = e_call_1(ejector, &do_run, numObj);
  e_ON_EJECTION(res, ej2) {
    fail("Wrong ejector activated upon invocation");
  }
  e_ejector_disable(ej2);
  return res;
}


e_Ref test_method(e_Ref self, e_Ref *args) {
  sentinel = 1;
  return e_null;
}

e_Ref test_otherwise(e_Ref self, e_Selector *selector, e_Ref *args) {
  result_selector = *selector;
  if (selector->arity == 1) {
    result_object = args[0];
  }
  return e_null;
}


e_Ref test_method_three(e_Ref self, e_Ref *args) {
  return e_make_fixnum(3);
}

#test type_predicate
{
  /// Test that e_def_type_predicate produces a function that correctly identifies objects with the given script.
  e_Method test_methods[] = {{"test/0", test_method}, {NULL}};
  e_Ref test_object;
  e_make_script(&test_script, NULL, test_methods, NULL, "test");
  test_object.script = &test_script;
  fail_unless(e_is_testobject(test_object));
}

#test make_selector
{
  /// Test that e_make_selector creates the selector struct properly and memoizes verbs.
  e_Selector a, b;
  e_make_selector(&a, "foo", 2);
  e_make_selector(&b, "foo", 2);
  fail_unless(strcmp(a.verb, "foo/2") == 0);
  fail_unless(a.arity == 2);
  fail_unless(a.verb == b.verb);
}

#test method_invoke
{
  /// Test that normal method invocation works.
  e_Method test_methods[] = {{"test/0", test_method}, {NULL}};
  e_Selector test_selector;
  e_Ref test_object;
  e_make_script(&test_script, NULL, test_methods, NULL, "test");
  e_make_selector(&test_selector, "test", 0);
  test_object.script = &test_script;
  fail_unless(sentinel == 0);
  e_call_0(test_object, &test_selector);
  fail_unless(sentinel == 1);
}

#test method_invoke_otherwise
{
  /// Test that 'otherwise' invocation works in the situation where there's no
  /// explicit method.
  e_Method test_methods[] = {{NULL}};
  e_Selector test_selector0, test_selector1;
  e_Ref test_object;
  e_make_script(&test_script, test_otherwise, test_methods, NULL, "test");
  test_object.script = &test_script;
  test_object.data.fixnum = 1729;
  e_make_selector(&test_selector0, "hooray", 0);
  e_call_0(test_object, &test_selector0);
  fail_unless(test_selector0.verb == result_selector.verb);
  fail_unless(test_selector0.arity == result_selector.arity);

  e_make_selector(&test_selector1, "yay", 1);
  e_call_1(test_object, &test_selector1, test_object);
  fail_unless(e_same(result_object, test_object));

}

#test wrong_selector
{
  /*
    Test that objects properly throw problems when receiving messages they
    don't understand, i.e., when there's no 'otherwise' function.
  */
  e_Method test_methods[] = {{NULL}};
  e_Selector do_wrong;
  e_Ref test_object, res;
  e_make_selector (&do_wrong, "wrong", 1);
  e_make_script(&test_script, NULL, test_methods, NULL, "test");
  test_object.script = &test_script;
  test_object.data.fixnum = 1729;
  res = e_call_1(test_object, &do_wrong, e_make_string ("Hello, world!\n"));
  if (!HAS_PROBLEM(res)) {
    fail("Wrong-selector error not handled");
  } else {
    fail_unless(strcmp(e_thrown_problem().data.refs[0].data.gstring->str, "Unknown method") == 0);
    fail_unless(strcmp(e_thrown_problem().data.refs[1].data.gstring->str, "<a test>.wrong/1") == 0);
  }
  cleanup_exits();
}


#test throw
{
  /// Test that 'e_throw' correctly indicates an error condition.
  e_Ref obj = e_null, val = test_throw_function(7);
  if (HAS_PROBLEM(val)) {
    obj = e_thrown_problem();
  }
  fail_unless(obj.data.fixnum == 7);
  cleanup_exits();
}


#test throw_pair
{
  /// Test that 'e_throw_pair' constructs a problem and throws it.
  /// A problem is an array containing a string and an object.
  e_Ref obj = e_null;
  e_Ref irr = e_make_fixnum(34);
  const char *txt = "oh no";
  e_Ref res = e_throw_pair(txt, irr);
  if (HAS_PROBLEM(res)) {
    obj = e_thrown_problem();
  }
  fail_if(e_same(obj, e_null));
  fail_unless(e_same(obj.data.refs[0], e_make_string("oh no")));
  fail_unless(e_same(obj.data.refs[1], e_make_fixnum(34)));
  cleanup_exits();
}

#test simple_ejector
{

  /// Test that ejectors return control to the e_CATCH block following an e_ESCAPE.
  e_Ref obj = e_null;
  e_Ref ej = e_make_ejector();
  e_Ref res = test_eject_function(7, ej);
  e_ON_EJECTION(res, ej) {
    obj = e_ejected_value();
    cleanup_exits();
  }
  fail_unless(obj.data.fixnum == 7);
}

#test two_escapes
{
  /// Test that ejectors only trigger the escape that created them.
  e_Ref val = e_make_fixnum(0);
  e_Ref obj = e_null;
  e_Ref ej = e_make_ejector();
  val = test_eject_function3(7, ej);
  e_ON_EJECTION(val, ej) {
    obj = e_ejected_value();
    cleanup_exits();
  }
  fail_unless(obj.data.fixnum == 7);
}

#test ejector_disabling
{
  /// Test that e_EJECTOR_DISABLE disables ejectors.
  e_Selector isEnabled;
  e_make_selector(&isEnabled, "isEnabled", 0);
  e_Ref res;
  e_Ref ej = e_make_ejector();
  res = e_call_0(ej, &isEnabled);
  fail_unless(e_same(res, e_true));
  e_ON_EJECTION(res, ej) {
    fail("Call to ejector.isEnabled ejected");
  }
  e_ejector_disable(ej);
  fail_unless(e_same(e_call_0(ej, &isEnabled), e_false));
  res = e_call_1(ej, &do_run, e_null);
  if (!HAS_PROBLEM(res)) {
    fail("Invocation of disabled ejector didn't throw problem");
  }
  cleanup_exits();
}

#test miranda_methods
{
  // Tests basic methods that all objects respond to.
  e_Method test_methods[] = {{"three/0", test_method_three}, {NULL}};
  e_Selector respondsTo, order, whenBroken, whenMoreResolved, optSealedDispatch,
    conformTo, printOn, optUncall, getAllegedType, reactToLostClient;
  e_make_selector(&respondsTo, "__respondsTo", 2);
  e_make_selector(&order, "__order", 2);
  e_make_selector(&whenBroken, "__whenBroken", 1);
  e_make_selector(&reactToLostClient, "__reactToLostClient", 1);
  e_make_selector(&optSealedDispatch, "__optSealedDispatch", 2);
  e_make_selector(&conformTo, "__conformTo", 1);
  e_make_selector(&printOn, "__printOn", 1);
  e_make_selector(&optUncall, "__optUncall", 0);

  //XXX needs send support
  // e_make_selector(&whenMoreResolved, "__whenMoreResolved", 1);
  //XXX needs type objects
  // e_make_selector(&getAllegedType, "__getAllegedType", 0);

  e_make_script(&test_script, NULL, test_methods, NULL, "testObject");
  e_Ref obj;
  obj.script = &test_script;
  fail_unless(e_same(e_call_2(obj, &respondsTo, e_make_string("three"),
                              e_make_fixnum(0)),
                     e_true));
  fail_unless(e_same(e_call_2(obj, &respondsTo, e_make_string("four"),
                              e_make_fixnum(1)),
                     e_false));
  fail_unless(e_same(e_call_2(obj, &respondsTo, e_make_string("three"),
                              e_make_fixnum(1)),
                     e_false));
  e_Ref target[] = {e_make_fixnum(3), obj};
  e_Ref orderResult =  e_call_2(obj, &order, e_make_string("three"),
                                e_constlist_from_array(0, NULL));
  e_Ref *orderItems = ((Flexlist_data *)orderResult.data.other)->elements;
  fail_unless(e_same(target[0], orderItems[0]));
  fail_unless(e_same(target[1], orderItems[1]));
  fail_unless(e_same(e_call_1(obj, &whenBroken, e_null), e_null));
  fail_unless(e_same(e_call_1(obj, &reactToLostClient, e_null), e_null));
  fail_unless(e_same(e_call_2(obj, &optSealedDispatch, e_null, e_null),
                     e_null));
  fail_unless(e_same(e_call_1(obj, &conformTo, e_null), obj));
  e_Ref writer = e_make_string_writer();
  e_call_1(obj, &printOn, writer);
  fail_unless(e_same(e_string_writer_get_string(writer),
                     e_make_string("<a testObject>")));
  fail_unless(e_same(e_call_0(obj, &optUncall), e_null));
}


#main-pre
{
  tcase_add_checked_fixture(tc1_1, setup, teardown);
}
