#include "elib.h"

static e_Ref make_equalizer() {
  e_Ref result;
  e_Ref *bits = e_malloc(2 * sizeof(e_Ref));
  bits[0] = e_constlist_from_array(0, NULL);
  bits[1] = e_constlist_from_array(0, NULL);
  result.script = &e__equalizer_script;
  result.data.refs = bits;
  return result;
}

static int eq_pushSoFar(e_Ref self, e_Ref left, e_Ref right, int soFar) {
  // XXX selector pooling
  e_Selector push;
  e_make_selector(&push, "push", 1);
  // XXX EoJ uses identityHashCode. do we need a similar mechanism?
  int lhash = left.data.fixnum;
  int rhash = right.data.fixnum;
  if (rhash < lhash) {
    e_Ref t = left;
    left = right;
    right = t;
  }
  e_call_1(self.data.refs[0], &push, left);
  e_call_1(self.data.refs[1], &push, right);
  return soFar + 1;
}


static int eq_findSoFar(e_Ref self, e_Ref left, e_Ref right, int soFar) {
  // XXX selector pooling
  e_Selector get;
  e_make_selector(&get, "get", 1);
  // XXX identityHashCode again
  int lhash = left.data.fixnum;
  int rhash = right.data.fixnum;
  if (rhash < lhash) {
    e_Ref t = left;
    left = right;
    right = t;
  }
  for (int i = 0; i < soFar; i++) {
    e_Ref myLeft = e_call_1(self.data.refs[0], &get, e_make_fixnum(i));
    e_Ref myRight = e_call_1(self.data.refs[1], &get, e_make_fixnum(i));
    if (e_same(left, myLeft) && e_same(right, myRight)) {
      return 1;
    }
  }
  return 0;
}

static e_Ref _eq_optSame(e_Ref self, e_Ref left, e_Ref right, int soFar) {
  // XXX selector pooling
  e_Selector get;
  e_make_selector(&get, "get", 1);
  if (e_same(left, right)) {
    return e_true;
  }
  if (e_is_ref(left) && (e_same(e_ref_isResolved(left), e_false))
      || e_is_ref(right) && (e_same(e_ref_isResolved(right), e_false))) {
    return e_null;
  }
  left = e_ref_target(left);
  right = e_ref_target(right);
  if (e_same(left, right)) {
    return e_true;
  }
  if (eq_findSoFar(self, left, right, soFar)) {
    return e_true;
  }
  // Recurse through ConstLists (EoJ uses arrays instead)
  if (e_is_constlist(left) && e_is_constlist(right)) {
    e_Ref leftlen = flexlist_size(left, NULL);
    if (!e_same(flexlist_size(right, NULL), leftlen)) {
      return e_false;
    }
    int soFarther = eq_pushSoFar(self, left, right, soFar);
    for (int i = 0; i < leftlen.data.fixnum; i++) {
      e_Ref newLeft = e_call_1(left, &get, e_make_fixnum(i));
      E_ERROR_CHECK(newLeft);
      e_Ref newRight = e_call_1(right, &get, e_make_fixnum(i));
      E_ERROR_CHECK(newRight);
      e_Ref optResult = _eq_optSame(self, newLeft, newRight, soFarther);
      E_ERROR_CHECK(optResult);
      if (e_same(optResult, e_null)) {
        return e_null;
      } else if (e_same(optResult, e_false)) {
        return e_false;
      }
    }
    return e_true;
  } else if (e_is_constlist(left) || e_is_constlist(right)) {
    return e_false;
  }
  // XXX put in selfless checks
  return e_false;
}


static e_Ref eq_optSame(e_Ref self, e_Ref left, e_Ref right) {
  e_Ref res = _eq_optSame(self, left, right, 0);
  return res;
}


/// Compare two E objects and return true if they are operationally identical.
e_Ref e_sameEver(e_Ref self, e_Ref *args) {
    if (e_same(args[0], args[1])) {
        return e_true;
    }
    // are we in '__equalizer'?
    if (self.data.refs == NULL) {
      e_Ref eq = make_equalizer();
      e_Ref res = e_sameEver(eq, args);
      return res;
    } else {
      // or in an internal instance?
      e_Ref optResult = eq_optSame(self, args[0], args[1]);
      E_ERROR_CHECK(optResult);
      if (e_eq(optResult, e_null)) {
        return e_throw_cstring("Equality comparison of insufficiently settled objects");
      } else {
        return optResult;
      }
    }
}

e_Script e__equalizer_script;
e_Method equalizer_methods[] = {
  {"sameEver/2", e_sameEver},
  {NULL}
};

e_Ref e_equalizer;
