#include "elib.h"

static e_Ref constset_with(e_Ref self, e_Ref *args) {
  if (e_same(flexlist_contains(self, args), e_true)) {
    return self;
  } else {
    e_Ref res = flexlist_with_1(self, args);
    res.script = &e__constset_script;
    return res;
  }
}

static e_Ref constset_printOn(e_Ref self, e_Ref *args) {
  e_Ref out = args[0];
  E_ERROR_CHECK(constlist_printOn(self, args));
  E_ERROR_CHECK(e_print(out, e_make_string(".asSet()")));
  return e_null;
}


static e_Ref flexset_printOn(e_Ref self, e_Ref *args) {
  e_Ref out = args[0];
  E_ERROR_CHECK(constlist_printOn(self, args));
  E_ERROR_CHECK(e_print(out, e_make_string(".asSet().diverge()")));
  return e_null;
}

static e_Ref flexset_diverge(e_Ref self, e_Ref *args) {
  e_Ref res = flexlist_diverge(self, args);
  res.script = &e__flexset_script;
  return res;
}

static e_Ref flexset_addElement(e_Ref self, e_Ref *args) {
  if (e_same(flexlist_contains(self, args), e_false)) {
    E_ERROR_CHECK(flexlist_push(self, args));
  }
  return e_null;
}

static e_Ref flexset_snapshot(e_Ref self, e_Ref *args) {
  e_Ref result = flexlist_diverge(self, NULL);
  result.script = &e__constset_script;
  return result;
}

e_Script e__constset_script;
e_Method constset_methods[] = {
  {"__printOn/1", constset_printOn},
  {"size/0", flexlist_size},
  {"getElements/0", flexlist_snapshot},
  {"with/1", constset_with},
  {"iterate/1", flexlist_iterate},
  {"diverge/0", flexset_diverge},
  {NULL}};

e_Script e__flexset_script;
e_Method flexset_methods[] = {
  {"__printOn/1", flexset_printOn},
  {"size/0", flexlist_size},
  {"getElements/0", flexlist_snapshot},
  {"with/1", constset_with},
  {"iterate/1", flexlist_iterate},
  {"addElement/1", flexset_addElement},
  {"snapshot/0", flexset_snapshot},
  {NULL}};

