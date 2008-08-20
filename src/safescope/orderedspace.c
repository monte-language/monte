#include "elib.h"



e_Ref descender_iterate(e_Ref self, e_Ref *args) {
  //XXX selector pooling
  e_Selector run2;
  e_make_selector(&run2, "run", 2);

  int left = self.data.refs[0].data.fixnum;
  int right = self.data.refs[1].data.fixnum;
  for (int i = 0, j = right; j >= left; i++, j--) {
    e_Ref res = e_call_2(args[0], &run2, e_make_fixnum(i), e_make_fixnum(j));
    E_ERROR_CHECK(res);
  }
  return e_null;
}

e_Script e__descender_script;
e_Method descender_methods[] = {
  {"iterate/1", descender_iterate},
  {NULL}};


e_Ref orderedSpace_iterate(e_Ref self, e_Ref *args) {
  //XXX selector pooling
  e_Selector run2;
  e_make_selector(&run2, "run", 2);

  int left = self.data.refs[0].data.fixnum;
  int right = self.data.refs[1].data.fixnum;
  for (int i = 0, j = left; j <= right; i++, j++) {
    e_Ref res = e_call_2(args[0], &run2, e_make_fixnum(i), e_make_fixnum(j));
    E_ERROR_CHECK(res);
  }
  return e_null;
}

e_Ref orderedSpace_compare(e_Ref self, e_Ref *args) {
  int selfLeft = self.data.refs[0].data.fixnum;
  int selfRight = self.data.refs[1].data.fixnum;
  int otherLeft = args[0].data.refs[0].data.fixnum;
  int otherRight = args[0].data.refs[1].data.fixnum;
  _Bool selfExtra = selfLeft < otherLeft || selfRight > otherRight;
  _Bool otherExtra = selfLeft > otherLeft || selfRight < otherRight;
  if (selfExtra) {
    if (otherExtra) {
      return e_make_float64(0.0/0.0);
    } else {
      return e_make_float64(1);
    }
  } else {
    if (otherExtra) {
      return e_make_float64(-1);
    } else {
      return e_make_float64(0);
    }
  }
}

e_Ref orderedSpace_descending(e_Ref self, e_Ref *args) {
  self.script = &e__descender_script;
  return self;
}

e_Ref orderedSpace_getEdges(e_Ref self, e_Ref *args) {
  return e_constlist_from_array(2, self.data.refs);
}

e_Ref orderedSpace_coerce(e_Ref self, e_Ref *args) {
  e_Ref specimen = args[0];
  e_Ref optEjector = args[1];
  e_Ref left = self.data.refs[0];
  e_Ref right = self.data.refs[1];
  e_Ref intres = e_coerce(e_IntGuard, args[0], args[1]);
  E_ERROR_CHECK(intres);
  if (intres.data.fixnum >= left.data.fixnum &&
      intres.data.fixnum <= right.data.fixnum) {
    return specimen;
  }
  return e_ejectOrThrow(optEjector, "Value not in region", specimen);
}

static e_Ref orderedSpace_printOn(e_Ref self, e_Ref *args) {
  e_Ref left = self.data.refs[0];
  e_Ref right = e_make_fixnum(self.data.refs[1].data.fixnum + 1);
    E_ERROR_CHECK(e_print(args[0], left));
    E_ERROR_CHECK(e_print(args[0], e_make_string("..!")));
    E_ERROR_CHECK(e_print(args[0], right));
    return e_null;
}

e_Script e__orderedSpace_script;
e_Method orderedSpace_methods[] = {
  {"iterate/1", orderedSpace_iterate},
  {"op__cmp/1", orderedSpace_compare},
  {"descending/0", orderedSpace_descending},
  {"getEdges/0", orderedSpace_getEdges},
  {"coerce/2", orderedSpace_coerce},
  {"__printOn/1", orderedSpace_printOn},
  {NULL}};



e_Ref e_make_orderedSpace(e_Ref left, e_Ref right) {
  e_Ref os;
  os.script = &e__orderedSpace_script;
  os.data.refs = e_malloc(sizeof(e_Ref) * 2);
  os.data.refs[0] = left;
  os.data.refs[1] = right;
  return os;
}

e_Ref makeOrderedSpace_till(e_Ref self, e_Ref *args) {
  e_Ref left = args[0];
  e_Ref right = args[1];
  if (left.script != &e__fixnum_script &&
      right.script != &e__fixnum_script) {
    return e_throw_cstring("Only ints supported in __OrderedSpaceMaker for now");
  }
  right.data.fixnum--;
  return e_make_orderedSpace(left, right);
}

e_Ref makeOrderedSpace_thru(e_Ref self, e_Ref *args) {
  e_Ref left = args[0];
  e_Ref right = args[1];
  if (left.script != &e__fixnum_script &&
      right.script != &e__fixnum_script) {
    return e_throw_cstring("Only ints supported in __OrderedSpaceMaker for now");
  }
  return e_make_orderedSpace(left, right);
}

e_Script e__makeOrderedSpace_script;
e_Method makeOrderedSpace_methods[] = {
  {"op__till/2", makeOrderedSpace_till},
  {"op__thru/2", makeOrderedSpace_thru},
  {NULL}};

e_Ref e_makeOrderedSpace;
