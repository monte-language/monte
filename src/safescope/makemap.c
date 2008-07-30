#include "elib.h"

e_Ref e_makeMap_fromPairs(e_Ref self, e_Ref *args) {
  //XXX selector pooling
  e_Selector get, put, size;
  e_make_selector(&get, "get", 1);
  e_make_selector(&put, "put", 1);
  e_make_selector(&size, "size", 0);

  e_Ref sizeObj = e_call_0(args[0],  &size);
  E_ERROR_CHECK(sizeObj);
  int length = sizeObj.data.fixnum;
  e_Ref newMap = e_make_flexmap(length);
  //XXX we oughta get an iterate method someday
  for (int i = 0; i < length; i++) {
    e_Ref pairObj = e_call_1(args[0], &get, e_make_fixnum(i));
    E_ERROR_CHECK(pairObj);
    e_Ref keyObj = e_call_1(pairObj, &get, e_make_fixnum(0));
    E_ERROR_CHECK(keyObj);
    e_Ref valueObj = e_call_1(pairObj, &get, e_make_fixnum(1));
    E_ERROR_CHECK(valueObj);
    e_call_2(newMap, &put, keyObj, valueObj);
  }
  newMap.script = &e__constmap_script;
  return newMap;
}

static e_Ref e_makeMap_fromColumns(e_Ref self, e_Ref *args) {
  //XXX selector pooling
  e_Selector coerce, get, size;
  e_make_selector(&coerce, "coerce", 2);
  e_make_selector(&get, "get", 1);
  e_make_selector(&size, "size", 0);

  e_Ref sizeObj = e_call_0(args[0],  &size);
  E_ERROR_CHECK(sizeObj);
  e_Ref vsizeObj = e_call_0(args[1],  &size);
  E_ERROR_CHECK(vsizeObj);
  sizeObj = e_call_2(e_IntGuard, &coerce, sizeObj, e_null);
  vsizeObj = e_call_2(e_IntGuard, &coerce, vsizeObj, e_null);
  int siz = sizeObj.data.fixnum;
  int vsiz = vsizeObj.data.fixnum;

  if (siz != vsiz) {
    return e_throw_cstring("Arity mismatch in __makeMap.fromColumns");
  }
  e_Ref result = e_make_constmap(siz);
  for (int i = 0; i < siz; i++) {
    e_Ref k = e_call_1(args[0], &get, e_make_fixnum(i));
    E_ERROR_CHECK(k);
    e_Ref v = e_call_1(args[1], &get, e_make_fixnum(i));
    E_ERROR_CHECK(v);
    e_Ref args[] = {k, v};
    E_ERROR_CHECK(e_flexmap_put(result, args));
  }
  return result;
}

e_Script e__makeMap_script;
e_Method makeMap_methods[] = {
  {"fromPairs/1", e_makeMap_fromPairs},
  {"fromColumns/2", e_makeMap_fromColumns},
  {NULL}
};


e_Ref e_makeMap;
