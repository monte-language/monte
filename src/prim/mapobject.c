#include "elib.h"
#include <string.h>

/** Return a pointer to the array element holding the value that 'key'
   maps to, if any; otherwise NULL. */
static e_Ref *flexmap_find(e_Ref self, e_Ref key) {
  Flexmap_data *data = (Flexmap_data *)self.data.other;
  int i;
  for (i = 0; i < data->occupancy; ++i) {
    if (e_same (key, data->keys[i])) {
      return &data->values[i];
    }
  }
  return NULL;
}

static e_Ref flexmap_maps(e_Ref self, e_Ref *args) {
  e_Ref *pvalue = flexmap_find(self, args[0]);
  if (pvalue == NULL) {
    return e_false;
  } else {
    return e_true;
  }
}

static e_Ref flexmap_fetch(e_Ref self, e_Ref *args) {
  e_Ref *pvalue = flexmap_find(self, args[0]);
  if (pvalue == NULL) {
    return args[1];
  } else {
    return *pvalue;
  }
}


static e_Ref constmap_printOn(e_Ref self, e_Ref *args) {
  Flexmap_data *map = self.data.other;
  e_Ref out = args[0];
  if (map->occupancy == 0) {
    E_ERROR_CHECK(e_print(out, e_make_string("[].asMap()")));
    return e_null;
  }
  E_ERROR_CHECK(e_print(out, e_make_string("[")));
  for (int i = 0; i < map->occupancy; i++) {
    E_ERROR_CHECK(e_quote_print(out, map->keys[i]));
    E_ERROR_CHECK(e_print(out, e_make_string(" => ")));
    E_ERROR_CHECK(e_quote_print(out, map->values[i]));
    if (i+1 != map->occupancy) {
      E_ERROR_CHECK(e_print(out, e_make_string(", ")));
    }
  }
  E_ERROR_CHECK(e_print(out, e_make_string("]")));
  return e_null;
}

static e_Ref flexmap_printOn(e_Ref self, e_Ref *args) {
  E_ERROR_CHECK(constmap_printOn(self, args));
  E_ERROR_CHECK(e_print(args[0], e_make_string(".diverge()")));
  return e_null;
}

static e_Ref flexmap_get_2(e_Ref self, e_Ref *args) {
  e_Ref key = args[0];
  e_Ref other = args[1];
  e_Ref *pvalue = flexmap_find(self, key);
  return NULL != pvalue ? *pvalue : other;
}

static e_Ref flexmap_get_1(e_Ref self, e_Ref *args) {
  e_Ref key = args[0];
  e_Ref *pvalue = flexmap_find(self, key);
  if (NULL != pvalue)
    return *pvalue;
  return e_throw_pair("Key not in FlexMap", key);
}

static void flexmap_grow(e_Ref flexmap) {
  Flexmap_data *data = (Flexmap_data *)flexmap.data.other;
  int newSize = data->size + 1;
  int newCapacity = (newSize >> 3) + (newSize < 9 ? 3 : 6) + newSize;
  e_Ref *newKeys = e_make_array(newCapacity);
  e_Ref *newValues = e_make_array(newCapacity);
  memcpy(newKeys, data->keys, data->size * sizeof *data->keys);
  memcpy(newValues, data->values, data->size * sizeof *data->values);
  data->keys = newKeys;
  data->values = newValues;
  data->size = newSize;
}

e_Ref e_flexmap_put(e_Ref self, e_Ref *args) {
  e_Ref key = args[0];
  e_Ref value = args[1];
  e_Ref *pvalue = flexmap_find(self, key);
  if (NULL != pvalue) {
    *pvalue = value;
  } else {
    Flexmap_data *data = (Flexmap_data *)self.data.other;
    if (data->occupancy == data->size) {
      flexmap_grow(self);
    }
    data->keys[data->occupancy] = key;
    data->values[data->occupancy] = value;
    data->occupancy++;
  }
  return e_null;
}

static e_Ref flexmap_size(e_Ref self, e_Ref *args) {
  Flexmap_data *data = self.data.other;
  return e_make_fixnum(data->occupancy);
}

static e_Ref flexmap_diverge(e_Ref self, e_Ref *args) {
  e_Ref result;
  Flexmap_data *map = e_malloc(sizeof *map);
  memcpy(map, self.data.other, sizeof *map);
  e_Ref *newKeys = e_make_array(map->size);
  e_Ref *newValues = e_make_array(map->size);
  memcpy(newKeys, map->keys, map->size * sizeof *map->keys);
  memcpy(newValues, map->values, map->size * sizeof *map->values);
  map->keys = newKeys;
  map->values = newValues;
  result.data.other = map;
  result.script = &e__flexmap_script;
  return result;
}

static e_Ref flexmap_snapshot(e_Ref self, e_Ref *args) {
  e_Ref new = flexmap_diverge(self, args);
  new.script = &e__constmap_script;
  return new;
}

static int e_ref_comparer(const void *one, const void *other,
                          void *data) {
  //XXX work out a strategy for pooling selectors for C methods
  e_Selector op__cmp;
  e_make_selector(&op__cmp, "op__cmp", 1);
  e_Ref *left = (void *)one;
  e_Ref *right = (void *)other;
  char *sort_failure = data;
  if (*sort_failure != -1) {
    return 0;
  } else {
    e_Ref res = e_call(*left, &op__cmp, right);
    if (res.script == NULL) {
      *sort_failure = res.data.fixnum;
      return 0;
    } else {
      e_Ref f64guard_args[] = {res, e_null};
      e_Ref f64res = float64guard_coerce(e_null, f64guard_args);
      if (f64res.script == NULL) {
        *sort_failure = 0;
        return 0;
      } else {
        return *f64res.data.float64;
      }
    }
  }
}

static e_Ref flexmap_sortKeys(e_Ref self, e_Ref *args) {
  Flexmap_data *original = self.data.other;
  e_Ref result = e_make_flexmap(original->occupancy);
  e_Ref *keys = e_make_array(original->occupancy);
  memcpy(keys, original->keys, original->occupancy * sizeof *original->keys);
  char sort_failure = -1;
  g_qsort_with_data(keys, original->occupancy, sizeof *keys, e_ref_comparer,
                    &sort_failure);
  if (sort_failure != -1) {
    e_Ref err;
    err.script = NULL;
    err.data.fixnum = sort_failure;
    return err;
  } else {
    for (int i = 0; i < original->occupancy; i++) {
      e_Ref putargs[] = {keys[i], flexmap_get_1(self, keys + i)};
      e_flexmap_put(result, putargs);
    }
  }
  result.script = &e__constmap_script;
  return result;
}

static int e_custom_comparer(const void *one, const void *other,
                          void *bits) {
  //XXX selector pooling
  e_Selector run2;
  e_make_selector(&run2, "run", 2);
  e_Ref *left = (void *)one;
  e_Ref *right = (void *)other;
  e_Ref *sortBits = bits;
  if (!e_same(sortBits[1], e_null)) {
    return 0;
  } else {
    e_Ref res = e_call_2(sortBits[0], &run2, *left, *right);
    if (res.script == NULL) {
      sortBits[1] = res;
      return 0;
    } else {
      e_Ref f64guard_args[] = {res, e_null};
      e_Ref f64res = float64guard_coerce(e_null, f64guard_args);
      if (f64res.script == NULL) {
        sortBits[1] = f64res;
        return 0;
      } else {
        return *f64res.data.float64;
      }
    }
  }
}

static e_Ref flexmap_sortKeys_1(e_Ref self, e_Ref *args) {
  Flexmap_data *original = self.data.other;
  e_Ref result = e_make_flexmap(original->occupancy);
  e_Ref *keys = e_make_array(original->occupancy);
  memcpy(keys, original->keys, original->occupancy * sizeof *original->keys);
  e_Ref sortBits[] = {args[0], e_null};
  g_qsort_with_data(keys, original->occupancy, sizeof *keys, e_custom_comparer,
                    &sortBits);
  if (!e_same(sortBits[1], e_null)) {
    return sortBits[1];
  } else {
    for (int i = 0; i < original->occupancy; i++) {
      e_Ref putargs[] = {keys[i], flexmap_get_1(self, keys + i)};
      e_flexmap_put(result, putargs);
    }
  }
  result.script = &e__constmap_script;
  return result;
}


e_Ref flexmap_with(e_Ref self, e_Ref *args) {
  e_Ref result = flexmap_diverge(self, NULL);
  e_flexmap_put(result, args);
  result.script = &e__constmap_script;
  return result;
}

e_Ref e_flexmap_removeKey(e_Ref self, e_Ref *args) {
  Flexmap_data *data = self.data.other;
  int i;
  e_Ref key = args[0];
  for (i = 0; i < data->occupancy; ++i) {
    if (e_same(key, data->keys[i])) {
      data->keys[i] = data->keys[data->occupancy-1];
      data->values[i] = data->values[data->occupancy-1];
      data->occupancy--;
      return e_null;
    }
  }
  return e_null;
}

e_Ref flexmap_or(e_Ref self, e_Ref *args) {
  e_Ref other = e_ref_target(args[0]);
  if (!(e_is_flexmap(other) || e_is_constmap(other))) {
    return e_throw_pair("Not a map", other);
  }
  Flexmap_data *original = self.data.other;
  Flexmap_data *behind = other.data.other;
  if (original->occupancy == 0) {
    return flexmap_snapshot(other, NULL);
  } else if (behind->occupancy == 0) {
    return flexmap_snapshot(self, NULL);
  }
  e_Ref result = flexmap_diverge(other, NULL);
    for (int i = 0; i < original->occupancy; i++) {
      e_Ref args[] = {original->keys[i], original->values[i]};
      e_flexmap_put(result, args);
    }
    result.script = &e__constmap_script;
    return result;
}

static e_Ref flexmap_getvalues(e_Ref self, e_Ref *args) {
  Flexmap_data *data = self.data.other;
  e_Ref list = e_constlist_from_array(0, NULL);
  Flexlist_data *listData = list.data.other;
  flexlist_setSize(list, data->occupancy);
  flexlist_setSize(list, data->occupancy);
  memcpy(listData->elements, data->values, sizeof(e_Ref) * data->occupancy);
  return list;
}

static e_Ref flexmap_getkeys(e_Ref self, e_Ref *args) {
  Flexmap_data *data = self.data.other;
  e_Ref list = e_constlist_from_array(0, NULL);
  Flexlist_data *listData = list.data.other;
  flexlist_setSize(list, data->occupancy);
  memcpy(listData->elements, data->keys, sizeof(e_Ref) * data->occupancy);
  return list;
}

static e_Ref flexmap_iterate(e_Ref self, e_Ref *args) {
  //XXX selector pooling
  e_Selector run2;
  e_make_selector(&run2, "run", 2);
    Flexmap_data *map = self.data.other;
    for (int i = 0; i < map->size; i++) {
      e_Ref res = e_call_2(args[0], &run2, map->keys[i],
                           map->values[i]);
      E_ERROR_CHECK(res);
    }
    return e_null;
}


e_Ref e_make_flexmap(int initial_size) {
  e_Ref result;
  Flexmap_data *data = e_malloc(sizeof *data);
  if (initial_size <= 0)
    initial_size = 1;
  data->size = initial_size;
  data->occupancy = 0;
  data->keys = e_make_array(initial_size);
  data->values = e_make_array(initial_size);
  result.script = &e__flexmap_script;
  result.data.other = data;
  return result;
}


e_Ref e_make_constmap(int initial_size) {
  e_Ref result = e_make_flexmap(initial_size);
  result.script = &e__constmap_script;
  return result;
}


e_Script e__flexmap_script;
e_Script e__constmap_script;

e_Method flexmap_methods[] = {
  {"__printOn/1", flexmap_printOn},
  {"get/2", flexmap_get_2},
  {"get/1", flexmap_get_1},
  {"put/2", e_flexmap_put},
  {"size/0", flexmap_size},
  {"diverge/0", flexmap_diverge},
  {"getValues/0", flexmap_getvalues},
  {"getKeys/0", flexmap_getkeys},
  {"maps/1", flexmap_maps},
  {"fetch/2", flexmap_fetch},
  {"sortKeys/0", flexmap_sortKeys},
  {"with/2", flexmap_with},
  {"snapshot/0", flexmap_snapshot},
  {"or/1", flexmap_or},
  {"removeKey/1", e_flexmap_removeKey},
  {"iterate/1", flexmap_iterate},
  {NULL}
};

e_Method constmap_methods[] = {
  {"__printOn/1", constmap_printOn},
  {"get/2", flexmap_get_2},
  {"get/1", flexmap_get_1},
  {"size/0", flexmap_size},
  {"diverge/0", flexmap_diverge},
  {"getValues/0", flexmap_getvalues},
  {"getKeys/0", flexmap_getkeys},
  {"maps/1", flexmap_maps},
  {"fetch/2", flexmap_fetch},
  {"sortKeys/0", flexmap_sortKeys},
  {"sortKeys/1", flexmap_sortKeys_1},
  {"with/2", flexmap_with},
  {"or/1", flexmap_or},
  {"iterate/1", flexmap_iterate},
  {NULL}
};
