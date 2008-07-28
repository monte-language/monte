#include <ctype.h>
#include <limits.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

#include "elib.h"
#include "ref.h"
#include "elib_private.h"

#if OLD_GIO
#include <gio/gsocketoutputstream.h>
#include <gio/gsocketinputstream.h>
#else
#include <gio/gunixoutputstream.h>
#include <gio/gunixinputstream.h>
#endif



e_Selector e_do_print, e_do_println, e_do_printOn, e_do_quote_print;
static e_Selector run2;

e_Method no_methods[] = {{NULL, NULL}};

/// Comparisons of primitive types, without recursion or ref shortening.
_Bool e_same(e_Ref ref1, e_Ref ref2) {
    if (e_eq(ref1, ref2)) {
        return true;
    } else if (ref1.script != ref2.script) {
        return false;
    } else if (ref1.script == &e__string_script) {
      return g_string_equal(ref1.data.gstring, ref2.data.gstring);
    } else if (ref1.script == &e__bignum_script) {
      return mpz_cmp(*ref2.data.bignum, *ref1.data.bignum) == 0;
    } else if (ref1.script == &e__float64_script) {
      return *ref1.data.float64 == *ref2.data.float64;
    }
    return false;
}


e_Ref e_empty_ref = {NULL, {0}};

//@}

/// @ingroup misc
//@{
/* An array of refs is not itself an E object; we use it to implement
   collections. */

e_Ref *e_make_array(int size) {
  e_Ref *result = e_malloc(size * sizeof result[0]);
  int i;
  for (i = 0; i < size; ++i)
    result[i] = e_null;
  return result;
}

//@}

/// @ingroup flexmap
//@{

//@}

/// @ingroup list
//@{

/// Overwrite this run with nulls.
static void flexlist_zero(e_Ref self, int start, int bound) {
  Flexlist_data *list = self.data.other;
  for (int i = start; i < bound; i++) {
    list->elements[i] = e_null;
  }
}

/// Reset this list's size, allocating more memory if needed.
void flexlist_setSize(e_Ref self, int newSize) {
  Flexlist_data *list = self.data.other;
  if (newSize == list->size) {
    return;
  } else if (newSize < list->size) {
    flexlist_zero(self, newSize, list->size);
  } else if (newSize > list->capacity) {
    // over-allocate proportional to the list size
    int newCapacity = (newSize >> 3) + (newSize < 9 ? 3 : 6) + newSize;
    e_Ref *newVals = e_make_array(newCapacity);
    memcpy(newVals, list->elements, list->size * sizeof *list->elements);
    list->elements = newVals;
    list->capacity = newCapacity;
  }
  list->size = newSize;
}

static e_Ref flexlist_put(e_Ref self, int index, e_Ref value) {
  Flexlist_data *list = self.data.other;
  if (index == list->size) {
    flexlist_setSize(self, list->size + 1);
  } else if (index > list->size) {
    return e_throw_pair("Index out of bounds", e_make_fixnum(index));
  }
  list->elements[index] = value;
  return e_null;
}

static e_Ref flexlist_put_2(e_Ref self, e_Ref *args) {
  e_Ref intguard_args[] = {args[0], e_null};
  e_Ref index = intguard_coerce(e_null, intguard_args);
  E_ERROR_CHECK(index);
  return flexlist_put(self, index.data.fixnum, args[1]);
}

static e_Ref flexlist_push(e_Ref self, e_Ref *args) {
  Flexlist_data *list = self.data.other;
  E_ERROR_CHECK(flexlist_put(self, list->size, args[0]));
  return e_null;
}


static e_Ref constlist_printOn(e_Ref self, e_Ref *args) {
  Flexlist_data *list = self.data.other;
  e_Ref out = args[0];
  E_ERROR_CHECK(e_print(out, e_make_string("[")));
  for (int i = 0; i < list->size; i++) {
    E_ERROR_CHECK(e_quote_print(out, list->elements[i]));
    if (i+1 != list->size) {
      E_ERROR_CHECK(e_print(out, e_make_string(", ")));
    }
  }
  E_ERROR_CHECK(e_print(out, e_make_string("]")));
  return e_null;
}

static e_Ref flexlist_printOn(e_Ref self, e_Ref *args) {
  E_ERROR_CHECK(constlist_printOn(self, args));
  E_ERROR_CHECK(e_print(args[0], e_make_string(".diverge()")));
  return e_null;
}

static e_Ref flexlist_get_1(e_Ref self, e_Ref *args) {
  Flexlist_data *info = self.data.other;
  e_Ref intguard_args[] = {args[0], e_null};
  e_Ref index = intguard_coerce(e_null, intguard_args);
  E_ERROR_CHECK(index);
  int i = index.data.fixnum;
  if (i >= info->size) {
    return e_throw_pair("Index out of bounds", index);
  }
  return info->elements[i];
}

static e_Ref flexlist_pop(e_Ref self, e_Ref *args) {
  Flexlist_data *list = self.data.other;
  e_Ref result = list->elements[list->size - 1];
  flexlist_setSize(self, list->size - 1);
  return result;
}

e_Ref flexlist_size(e_Ref self, e_Ref *args) {
  return e_make_fixnum(((Flexlist_data *)(self.data.other))->size);
}

static e_Ref flexlist_diverge(e_Ref self, e_Ref *args) {
  e_Ref result;
  Flexlist_data *list = e_malloc(sizeof *list);
  memcpy(list, self.data.other, sizeof *list);
  e_Ref *newList = e_malloc(list->capacity * sizeof *list->elements);
  memcpy(newList, list->elements, list->size * sizeof *list->elements);
  list->elements = newList;
  result.data.other = list;
  result.script = &e__flexlist_script;
  return result;
}

static e_Ref flexlist_diverge_1(e_Ref self, e_Ref *args) {
  Flexlist_data *list;
  e_Ref res = flexlist_diverge(self, args);
  list = self.data.other;
  list->elementGuard = args[0];
  return res;
}

e_Ref flexlist_snapshot(e_Ref self, e_Ref *args) {
  e_Ref result = flexlist_diverge(self, NULL);
  result.script = &e__constlist_script;
  return result;
}

static e_Ref flexlist_asMap(e_Ref self, e_Ref *args) {
  Flexlist_data *list = self.data.other;
  e_Ref map = e_make_flexmap(list->size);
  for (int i = 0; i < list->size; i++) {
    e_Ref putArgs[] = {e_make_fixnum(i), list->elements[i]};
    e_flexmap_put(map, putArgs);
  }
    map.script = &e__constmap_script;
  return map;
}

static e_Ref flexlist_contains(e_Ref self, e_Ref *args) {
  Flexlist_data *list = self.data.other;
  for (int i = 0; i < list->size; i++) {
    if (e_same(args[0], list->elements[i])) {
      return e_true;
    }
  }
    return e_false;
}

static e_Ref flexlist_lastIndexOf1_2(e_Ref self, e_Ref *args) {
  Flexlist_data *list = self.data.other;
  e_Ref intarg[] = {args[1], e_null};
  e_Ref start = intguard_coerce(e_null, intarg);
  E_ERROR_CHECK(start);
  if (start.data.fixnum >= list->size) {
    return e_throw_pair("Index out of bounds", start);
  }
  for (int i = start.data.fixnum; 0 <= i; i--) {
    if (e_same(args[0], list->elements[i])) {
      return e_make_fixnum(i);
    }
  }
  return e_make_fixnum(-1);
}

static e_Ref flexlist_lastIndexOf1(e_Ref self, e_Ref *args) {
  Flexlist_data *list = self.data.other;
  e_Ref idxArg[] = {args[0], e_make_fixnum(list->size-1)};
  return flexlist_lastIndexOf1_2(self, idxArg);
}

static e_Ref flexlist_with_1(e_Ref self, e_Ref *args) {
  e_Ref newList = flexlist_snapshot(self, NULL);
  Flexlist_data *list = newList.data.other;
  flexlist_put(newList, list->size, args[0]);
  return newList;
}

static e_Ref flexlist_with_2(e_Ref self, e_Ref *args) {
  e_Ref newList = flexlist_snapshot(self, NULL);
  e_Ref intguard_args[] = {args[0], e_null};
  e_Ref idx = intguard_coerce(e_null, intguard_args);
  E_ERROR_CHECK(idx);
  flexlist_put(newList, idx.data.fixnum, args[1]);
  return newList;
}

static e_Ref flexlist_as_set(e_Ref self, e_Ref *args) {
  e_Ref newSet = flexlist_diverge(self, NULL);
  newSet.script = &e__constset_script;
  return newSet;
}

static e_Ref flexlist_iterate(e_Ref self, e_Ref *args) {
    Flexlist_data *list = self.data.other;
    for (int i = 0; i < list->size; i++) {
      e_Ref res = e_call_2(args[0], &run2, e_make_fixnum(i), list->elements[i]);
      E_ERROR_CHECK(res);
    }
    return e_null;
}

static e_Ref flexlist_last(e_Ref self, e_Ref *args) {
  Flexlist_data *list = self.data.other;
  if (list->size == 0) {
    return e_throw_cstring("Empty list");
  }
  return list->elements[list->size-1];
}

static e_Ref flexlist_add(e_Ref self, e_Ref *args) {
  e_Ref result;
  e_Ref listguardargs[] = {args[0], e_null};
  e_Ref arg = elistguard_coerce(e_null, listguardargs);
  E_ERROR_CHECK(arg);
  Flexlist_data *resData = e_malloc(sizeof *resData);
  Flexlist_data *selfData = self.data.other;
  Flexlist_data *otherData = arg.data.other;
  int size = selfData->size + otherData->size;
  result.script = &e__constlist_script;
  result.data.other = resData;
  resData->size = size;
  resData->capacity = size;
  if (resData->capacity > 0) {
    resData->elements = e_malloc(sizeof(e_Ref) * resData->capacity);
  }
  if (selfData->size > 0) {
    memcpy(resData->elements, selfData->elements,
           sizeof(e_Ref) * selfData->size);
  }
  if (otherData->size > 0) {
    memcpy(resData->elements + selfData->size, otherData->elements,
           sizeof(e_Ref) * otherData->size);
  }
  return result;
}

static e_Ref flexlist_append(e_Ref self, e_Ref *args) {
  e_Ref listguardargs[] = {args[0], e_null};
  e_Ref arg = elistguard_coerce(e_null, listguardargs);
  E_ERROR_CHECK(arg);
  Flexlist_data *selfData = self.data.other;
  Flexlist_data *otherData = arg.data.other;
  int size = selfData->size + otherData->size;
  int oldSize = selfData->size;
  flexlist_setSize(self, size);
  if (otherData->size > 0) {
    memcpy(selfData->elements + oldSize, otherData->elements,
           sizeof(e_Ref) * otherData->size);
  }
  return e_null;
}

e_Ref flexlist_insert(e_Ref self, e_Ref *args) {
  e_Ref intguard_args[] = {args[0], e_null};
  e_Ref idx = intguard_coerce(e_null, intguard_args);
  E_ERROR_CHECK(idx);
  Flexlist_data *data = self.data.other;
  int originalSize = data->size;
  flexlist_setSize(self, originalSize+1);
  for (int i = originalSize; i > idx.data.fixnum; i--) {
    data->elements[i] = data->elements[i-1];
  }
  data->elements[idx.data.fixnum] = args[1];
  return e_null;
}

static e_Ref flexlist_run_2(e_Ref self, e_Ref *args) {
  Flexlist_data *selfData = self.data.other;
  e_Ref start_args[] = {args[0], e_null};
  e_Ref bound_args[] = {args[1], e_null};
  e_Ref start = intguard_coerce(e_null, start_args);
  E_ERROR_CHECK(start);
  int startIdx = start.data.fixnum;
  e_Ref bound = intguard_coerce(e_null, bound_args);
  E_ERROR_CHECK(bound);
  int boundIdx = bound.data.fixnum;
  if (boundIdx > selfData->size || startIdx > selfData->size) {
    return e_throw_cstring("Index out of bounds");
  }
  if (boundIdx < startIdx) {
    return e_throw_cstring("Negative list run size");
  }
  return e_constlist_from_array(boundIdx - startIdx,
                                selfData->elements + startIdx);
}

static e_Ref flexlist_run_1(e_Ref self, e_Ref *args) {
  Flexlist_data *list = self.data.other;
  e_Ref newargs[] = {args[0], e_make_fixnum(list->size)};
  return flexlist_run_2(self, newargs);
}

static e_Ref flexlist_multiply(e_Ref self, e_Ref *args) {
  e_Ref times_args[] = {args[0], e_null};
  e_Ref times = intguard_coerce(e_null, times_args);
  E_ERROR_CHECK(times);
  if (times.data.fixnum == 0) {
    return e_constlist_from_array(0, NULL);
  }
  e_Ref newlist = flexlist_diverge(self, NULL);
  for (int i = 0; i < times.data.fixnum; i++) {
    flexlist_append(newlist, &self);
  }
  newlist.script = &e__constlist_script;
  return newlist;
}

e_Script e__constlist_script;
static e_Method constlist_methods[] = {
  {"__printOn/1", constlist_printOn},
  {"get/1", flexlist_get_1},
  {"size/0", flexlist_size},
  {"diverge/0", flexlist_diverge},
  // disabled until guard checks actually done
  //{"diverge/1", flexlist_diverge_1},
  {"asMap/0", flexlist_asMap},
  {"contains/1", flexlist_contains},
  {"snapshot/0", flexlist_snapshot},
  {"lastIndexOf1/1", flexlist_lastIndexOf1},
  {"lastIndexOf1/2", flexlist_lastIndexOf1_2},
  {"with/1", flexlist_with_1},
  {"with/2", flexlist_with_2},
  {"asSet/0", flexlist_as_set},
  {"iterate/1", flexlist_iterate},
  {"last/0", flexlist_last},
  {"add/1", flexlist_add},
  {"multiply/1", flexlist_multiply},
  {"run/1", flexlist_run_1},
  {"run/2", flexlist_run_2},
  {NULL}
};

e_Ref e_constlist_from_array(int size, e_Ref* contents) {
  e_Ref result;
  Flexlist_data *info = e_malloc(sizeof *info);
  result.script = &e__constlist_script;
  result.data.other = info;
  info->size = size;
  info->capacity = size;
  info->elementGuard = e_null;
  if (info->capacity > 0) {
    info->elements = e_malloc(sizeof(e_Ref) * info->capacity);
    memcpy(info->elements, contents, sizeof(e_Ref) * info->size);
  }
  return result;
}

e_Script e__flexlist_script;
static e_Method flexlist_methods[] = {
  {"__printOn/1", flexlist_printOn},
  {"get/1", flexlist_get_1},
  {"size/0", flexlist_size},
  {"diverge/0", flexlist_diverge},
  // disabled until guard checks actually done
  //{"diverge/1", flexlist_diverge_1},
  {"push/1", flexlist_push},
  {"pop/0", flexlist_pop},
  {"snapshot/0", flexlist_snapshot},
  {"asMap/0", flexlist_asMap},
  {"contains/1", flexlist_contains},
  {"lastIndexOf1/1", flexlist_lastIndexOf1},
  {"lastIndexOf1/2", flexlist_lastIndexOf1_2},
  {"with/1", flexlist_with_1},
  {"with/2", flexlist_with_2},
  {"asSet/0", flexlist_as_set},
  {"iterate/1", flexlist_iterate},
  {"last/0", flexlist_last},
  {"add/1", flexlist_add},
  {"multiply/1", flexlist_multiply},
  {"append/1", flexlist_append},
  {"run/2", flexlist_run_2},
  {"put/2", flexlist_put_2},
  {"insert/2", flexlist_insert},
  {NULL}
};


e_Ref e_flexlist_from_array(int size, e_Ref* contents) {
  e_Ref list = e_constlist_from_array(size, contents);
  list.script = &e__flexlist_script;
  return list;
}


//@}
/// @ingroup set
//@{


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
static e_Method constset_methods[] = {
  {"__printOn/1", constset_printOn},
  {"size/0", flexlist_size},
  {"getElements/0", flexlist_snapshot},
  {"with/1", constset_with},
  {"iterate/1", flexlist_iterate},
  {"diverge/0", flexset_diverge},
  {NULL}};

e_Script e__flexset_script;
static e_Method flexset_methods[] = {
  {"__printOn/1", flexset_printOn},
  {"size/0", flexlist_size},
  {"getElements/0", flexlist_snapshot},
  {"with/1", constset_with},
  {"iterate/1", flexlist_iterate},
  {"addElement/1", flexset_addElement},
  {"snapshot/0", flexset_snapshot},
  {NULL}};


//@}

/// @ingroup slot
//@{

/// Retrieve the value from this FinalSlot.
static e_Ref finalslot_get(e_Ref self, e_Ref *args) {
  return self.data.refs[0];
}

/// Update the value in this slot.
static e_Ref slot_put(e_Ref self, e_Ref *args) {
  self.data.refs[0] = args[0];
  return e_null;
}

/// Throw an error when attempting to update an immutable FinalSlot.
static e_Ref finalslot_put(e_Ref self, e_Ref *args) {
  return e_throw_cstring("Final variables may not be changed.");
}

/// Return whether the slot is mutable or not.
static e_Ref finalslot_isFinal(e_Ref self, e_Ref *args) {
  return e_true;
}

/// Produce an immutable version of this slot.
static e_Ref finalslot_readOnly(e_Ref self, e_Ref *args) {
  return self;
}
/// The Miranda method "__printOn".
static e_Ref slot_printOn(e_Ref self, e_Ref *args) {
  e_Ref out = args[0];
  E_ERROR_CHECK(e_print(out, e_make_string("<& ")));
  E_ERROR_CHECK(e_print(out, finalslot_get(self, NULL)));
  E_ERROR_CHECK(e_print(out, e_make_string(">")));
  return e_null;
}

static e_Method finalslot_methods[] = {
  {"__printOn/1", slot_printOn},
  {"get/0", finalslot_get},
  {"getValue/0", finalslot_get},
  {"put/1", finalslot_put},
  {"setValue/1", finalslot_put},
  {"readOnly/0", finalslot_readOnly},
  {"isFinal", finalslot_isFinal},
  {NULL}
};
/// The behaviour of a FinalSlot.
e_Script e__finalslot_script;


/// Produce an immutable object containing only a reference to another object.
/// Primarily used in scopes.
e_Ref e_make_finalslot(e_Ref value) {
  // XXX immutable object here, perhaps this should memoize
  e_Ref result;
  e_Ref *spot = e_malloc(sizeof(e_Ref));
  *spot = value;
  result.data.refs = spot;
  result.script = &e__finalslot_script;
  return result;
}

/// Return whether the slot is mutable or not.
static e_Ref varslot_isFinal(e_Ref self, e_Ref *args) {
  return e_true;
}

/// Produce an immutable version of this slot.
static e_Ref varslot_readOnly(e_Ref self, e_Ref *args) {
  e_Ref result = self;
  result.script = &e__finalslot_script;
  return result;
}

/// The Miranda method "__printOn".
static e_Ref varslot_printOn(e_Ref self, e_Ref *args) {
  e_Ref out = args[0];
  E_ERROR_CHECK(e_print(out, e_make_string("<var ")));
  E_ERROR_CHECK(e_print(out, finalslot_get(self, NULL)));
  E_ERROR_CHECK(e_print(out, e_make_string(">")));
  return e_null;
}

static e_Method varslot_methods[] = {
  {"__printOn/1", varslot_printOn},
  {"get/0", finalslot_get},
  {"getValue/0", finalslot_get},
  {"put/1", slot_put},
  {"setValue/1", slot_put},
  {"readOnly/0", varslot_readOnly},
  {"isFinal/0", varslot_isFinal},
  {NULL}
};
/// The behaviour of a VarSlot.
e_Script e__varslot_script;


/// Produce an mutable object containing only a reference to another object.
/// Primarily used in scopes.
e_Ref e_make_varslot(e_Ref value) {
  e_Ref result = e_make_finalslot(value);
  result.script = &e__varslot_script;
  return result;
}

e_Ref guardedslot_put(e_Ref self, e_Ref *args) {
  e_Selector do_coerce;
  e_Ref specimen = args[0];
  e_Ref guard = self.data.refs[1];
  e_Ref result;
  e_make_selector(&do_coerce, "coerce", 2);
  result = e_call_2(guard, &do_coerce, specimen, e_null);
  E_ERROR_CHECK(result);
  self.data.refs[0] = result;
  return e_null;
}


static e_Method guardedslot_methods[] = {
  {"__printOn/1", varslot_printOn},
  {"get/0", finalslot_get},
  {"getValue/0", finalslot_get},
  {"put/1", guardedslot_put},
  {"setValue/1", guardedslot_put},
  {"readOnly/0", varslot_readOnly},
  {"isFinal/0", varslot_isFinal},
  {NULL}
};

e_Script e__guardedslot_script;

e_Ref e_new_guardedslot(e_Ref value, e_Ref guard, e_Ref optEjector) {
  e_Ref result, coerced_value;
  e_Selector do_coerce;
  e_make_selector(&do_coerce, "coerce", 2);
  coerced_value = e_call_2(guard, &do_coerce, value, optEjector);
  E_ERROR_CHECK(coerced_value);
  e_Ref *spot = e_malloc(2 * sizeof(e_Ref));
  spot[0] = coerced_value;
  spot[1] = guard;
  result.data.refs = spot;
  result.script = &e__guardedslot_script;
  return result;
}

static void set_up_prims(void) {
  e_ejector_counter = 1;
  e_ejected_value = e_empty_ref;
  e_thrown_problem = e_empty_ref;
  e_make_selector(&e_do_printOn, "__printOn", 1);
  e_make_selector(&e_do_print, "print", 1);
  e_make_selector(&e_do_quote_print, "quote", 1);
  e_make_selector(&e_do_println, "println", 1);
  e_make_selector(&run2, "run", 2);

  e_make_script(&e__null_script, NULL, null_methods, "void");
  e_make_script(&e__boolean_script, NULL, boolean_methods, "Boolean");
  e_make_script(&e__char_script, NULL, char_methods, "char");
  e_make_script(&e__string_script, NULL, string_methods, "String");
  e_make_script(&e__fixnum_script, NULL, fixnum_methods, "int");
  e_make_script(&e__bignum_script, NULL, bignum_methods, "bigint");
  e_make_script(&e__float64_script, NULL, float64_methods, "float64");
  e_make_script(&e__writer_script, NULL, writer_methods, "writer");
  e_make_script(&e__reader_script, NULL, reader_methods, "reader");
  e_make_script(&e__flexmap_script, NULL, flexmap_methods, "FlexMap");
  e_make_script(&e__constmap_script, NULL, constmap_methods, "Map");
  e_make_script(&e__constlist_script, NULL, constlist_methods, "List");
  e_make_script(&e__flexlist_script, NULL, flexlist_methods, "FlexList");
  e_make_script(&e__constset_script, NULL, constset_methods, "Set");
  e_make_script(&e__flexset_script, NULL, flexset_methods, "FlexSet");
  e_make_script(&problem_script, NULL, problem_methods, "problem");
  e_make_script(&e__finalslot_script, NULL, finalslot_methods, "FinalSlot");
  e_make_script(&e__varslot_script, NULL, varslot_methods, "SettableSlot");
  e_make_script(&e__guardedslot_script, NULL, guardedslot_methods, "SettableSlot");
  e_make_script(&e__ejector_script, NULL, ejector_methods, "Ejector");

#if OLD_GIO
  e_stdin  = e_make_reader(g_socket_input_stream_new(fileno(stdin), true));
  e_stdout = e_make_writer(g_socket_output_stream_new(fileno(stdout), false));
  e_stderr = e_make_writer(g_socket_output_stream_new(fileno(stderr), false));
#else
  e_stdin  = e_make_reader(g_unix_input_stream_new(fileno(stdin), true));
  e_stdout = e_make_writer(g_unix_output_stream_new(fileno(stdout), false));
  e_stderr = e_make_writer(g_unix_output_stream_new(fileno(stderr), false));
#endif

  e_true.script = &e__boolean_script;
  e_true.data.fixnum = 1;

  e_false.script = &e__boolean_script;
  e_false.data.fixnum = 0;
}

#ifndef NO_GC

static void do_nothing_free(void *ptr, size_t size) {}
static void do_nothing_free2(void *ptr) {}

static void *gmp_realloc(void *ptr, size_t old, size_t new) {
    return GC_realloc(ptr, new);
}
GMemVTable gc_vtable = {GC_malloc, GC_realloc,
                        do_nothing_free2,
                        NULL, NULL, NULL};
#endif

char e__setup_done = 0;
void e_set_up(void) {
  if (!e__setup_done) {
#ifndef NO_GC
  mp_set_memory_functions(GC_malloc, gmp_realloc, do_nothing_free);
  g_mem_set_vtable(&gc_vtable);
  g_slice_set_config(G_SLICE_CONFIG_ALWAYS_MALLOC, 1);
  g_mem_gc_friendly = 1;
#endif
  g_type_init();
  e__set_up_interner();
  e__miranda_set_up();
  set_up_prims();
  e__ref_set_up();
  e__guards_set_up();
  e__safescope_set_up();
  e__privilegedscope_set_up();
  e__scope_set_up();
  e__setup_done = true;
}
}
