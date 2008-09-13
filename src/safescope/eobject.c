#include "elib.h"


static e_Ref e_callWithPair(e_Ref self, e_Ref *args) {
  //XXX selector pooling
  e_Selector get;
  e_make_selector(&get, "get", 1);

  e_Ref receiver = args[0];
  e_Ref argPair = e_coerce(e_ListGuard, args[1], e_null);
  E_ERROR_CHECK(argPair);
  e_Ref verb = e_call_1(argPair, &get, e_make_fixnum(0));
  E_ERROR_CHECK(verb);
  verb = e_coerce(e_StringGuard, verb, e_null);
  E_ERROR_CHECK(verb);
  e_Ref arglist = e_call_1(argPair, &get, e_make_fixnum(1));
  E_ERROR_CHECK(arglist);
  arglist = e_coerce(e_ListGuard, arglist, e_null);
  E_ERROR_CHECK(arglist);
  e_Ref *newArgs = ((Flexlist_data *)arglist.data.other)->elements;
  int arity = ((Flexlist_data *)arglist.data.other)->size;
  e_Selector sel;
  e_make_selector(&sel, (verb.data.gstring)->str, arity);
  return e_call(receiver, &sel, newArgs);

}

static e_Ref e_toString(e_Ref self, e_Ref *args) {
  e_Ref memWriter = e_make_string_writer();
  E_ERROR_CHECK(e_print(memWriter, args[0]));
  return e_string_writer_get_string(memWriter);
}

static e_Ref e_sendOnly(e_Ref self, e_Ref *args) {
  e_Ref receiver = args[0];
  e_Ref verb = e_coerce(e_StringGuard, args[1], e_null);
  E_ERROR_CHECK(verb);
  e_Ref newargs = e_coerce(e_ListGuard, args[2], e_null);
  E_ERROR_CHECK(newargs);
  Flexlist_data *arglist = newargs.data.other;
  e_Selector *sel = e_malloc(sizeof *sel);
  e_make_selector(sel, verb.data.gstring->str, arglist->size);
  sel->eventual = true;
  e_vat_sendOnly(e_current_vat(), receiver, sel, arglist->elements);
  return e_null;
}

static e_Ref e_send(e_Ref self, e_Ref *args) {
  e_Ref receiver = args[0];
  e_Ref verb = e_coerce(e_StringGuard, args[1], e_null);
  E_ERROR_CHECK(verb);
  e_Ref newargs = e_coerce(e_ListGuard, args[2], e_null);
  E_ERROR_CHECK(newargs);
  Flexlist_data *arglist = newargs.data.other;
  e_Selector *sel = e_malloc(sizeof *sel), get;
  e_make_selector(sel, verb.data.gstring->str, arglist->size);
  sel->eventual = true;
  e_make_selector(&get, "get", 1);
  e_Ref ppair = e_make_promise_pair();
  e_Ref result = e_call_1(ppair, &get, e_make_fixnum(0));
  e_Ref resolver = e_call_1(ppair, &get, e_make_fixnum(1));
  e_Ref vat = e_current_vat();
  e_vat_send(vat, receiver, sel, arglist->elements, vat, resolver);
  return result;
}


e_Script THE_E_script;
e_Method THE_E_methods[] = {
  {"callWithPair/2", e_callWithPair},
  {"toString/1", e_toString},
  {"sendOnly/3", e_sendOnly},
  {"send/3", e_send},
  {NULL}
};

e_Ref THE_E;
