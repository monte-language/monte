#include "elib.h"
#include "string.h"

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

e_Ref flexlist_push(e_Ref self, e_Ref *args) {
  Flexlist_data *list = self.data.other;
  E_ERROR_CHECK(flexlist_put(self, list->size, args[0]));
  return e_null;
}


e_Ref constlist_printOn(e_Ref self, e_Ref *args) {
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

e_Ref flexlist_diverge(e_Ref self, e_Ref *args) {
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

e_Ref flexlist_contains(e_Ref self, e_Ref *args) {
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

e_Ref flexlist_with_1(e_Ref self, e_Ref *args) {
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

e_Ref flexlist_iterate(e_Ref self, e_Ref *args) {
    //XXX selector pooling
    e_Selector run2;
    e_make_selector(&run2, "run", 2);
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
e_Method constlist_methods[] = {
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
e_Method flexlist_methods[] = {
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

