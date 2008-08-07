#include "elib.h"

e_Ref e_compare(e_Ref self, e_Ref *args) {
  return e_call_1(args[0], &op__cmp, args[1]);
}

e_Ref e_lessThan(e_Ref self, e_Ref *args) {
  e_Ref comp = e_compare(self, args);
  E_ERROR_CHECK(comp);
  return e_call_0(comp, &belowZero);
}

e_Ref e_leq(e_Ref self, e_Ref *args) {
  e_Ref comp = e_compare(self, args);
  E_ERROR_CHECK(comp);
  return e_call_0(comp, &atMostZero);
}
e_Ref e_asBigAs(e_Ref self, e_Ref *args) {
  e_Ref comp = e_compare(self, args);
  E_ERROR_CHECK(comp);
  return e_call_0(comp, &isZero);
}
e_Ref e_geq(e_Ref self, e_Ref *args) {
  e_Ref comp = e_compare(self, args);
  E_ERROR_CHECK(comp);
  return e_call_0(comp, &atLeastZero);
}

e_Ref e_greaterThan(e_Ref self, e_Ref *args) {
  e_Ref comp = e_compare(self, args);
  E_ERROR_CHECK(comp);
  return e_call_0(comp, &aboveZero);
}


e_Script e__comparer_script;
e_Method comparer_methods[] = {
  {"compare/2", e_compare},
  {"lessThan/2", e_lessThan},
  {"leq/2", e_leq},
  {"asBigAs/2", e_asBigAs},
  {"geq/2", e_geq},
  {"greaterThan/2", e_greaterThan}
};

e_Ref e_comparer;
