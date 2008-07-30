#include "elib.h"
#include <string.h>

static e_Ref string_size(e_Ref self, e_Ref *args) {
  GString *string = self.data.gstring;
  return e_make_fixnum(string->len);
}

static e_Ref string_printOn(e_Ref self, e_Ref *args) {

  E_ERROR_CHECK(e_print(args[0], self));
  return e_null;
}

static e_Ref string_append(e_Ref self, e_Ref *args) {
  e_Ref otherString = stringguard_coerce(e_null, args);
  E_ERROR_CHECK(otherString);
  GString *result = g_string_new_len(self.data.gstring->str,
                                     self.data.gstring->len);
  g_string_append_len(result, otherString.data.gstring->str,
                      otherString.data.gstring->len);
  return e_make_gstring(result);
}

static e_Ref string_getBytes(e_Ref self, e_Ref *args) {
  e_Ref bytes[self.data.gstring->len];
  for (int i = 0; i < self.data.gstring->len; i++) {
    bytes[i] = e_make_fixnum(self.data.gstring->str[i]);
  }
  return e_constlist_from_array(self.data.gstring->len, bytes);
}

static e_Ref string_get(e_Ref self, e_Ref *args) {
  e_Ref intguard_args[] = {args[0], e_null};
  e_Ref arg = intguard_coerce(e_null, intguard_args);
  E_ERROR_CHECK(arg);
  if (arg.data.fixnum < 0 || arg.data.fixnum >= self.data.gstring->len) {
    return e_throw_pair("Index out of bounds", arg);
  }
  return e_make_char(self.data.gstring->str[arg.data.fixnum]);
}

static e_Ref string_multiply(e_Ref self, e_Ref *args) {
  e_Ref intguard_args[] = {args[0], e_null};
  e_Ref arg = intguard_coerce(e_null, intguard_args);
  E_ERROR_CHECK(arg);
  int times = arg.data.fixnum;
  GString *result = g_string_new_len(self.data.gstring->str,
                                     self.data.gstring->len);

  for (int i = 0; i < times; i++) {
  g_string_append_len(result,
                      self.data.gstring->str,
                      self.data.gstring->len);
  }
  return e_make_gstring(result);
}

static e_Ref string_compareTo(e_Ref self, e_Ref *args) {
  e_Ref stringguard_args[] = {args[0], e_null};
  e_Ref arg = stringguard_coerce(e_null, stringguard_args);
  E_ERROR_CHECK(arg);
  int a = self.data.gstring->len;
  int b = arg.data.gstring->len;
  if (a != b) {
    return e_make_fixnum(a < b ? -1 : 1);
  }
  return e_make_fixnum(strncmp(self.data.gstring->str,
                               arg.data.gstring->str, a));
}

static e_Ref string_run2(e_Ref self, e_Ref *args) {
  e_Ref intguard_args[] = {args[0], e_null};
  e_Ref arg = intguard_coerce(e_null, intguard_args);
  E_ERROR_CHECK(arg);
  int start = arg.data.fixnum;
  e_Ref intguard2_args[] = {args[1], e_null};
  arg = intguard_coerce(e_null, intguard2_args);
  E_ERROR_CHECK(arg);
  int end = arg.data.fixnum;
  if (start < 0 || start >= self.data.gstring->len
      || end < start || end > self.data.gstring->len) {
    return e_throw_cstring("String index out of bounds");
  }
  GString *newstr = g_string_new_len(self.data.gstring->str + start,
                                     end - start);
  return e_make_gstring(newstr);
}

static e_Ref string_run1(e_Ref self, e_Ref *args) {
  e_Ref newargs[] = {args[0], e_make_fixnum(self.data.gstring->len)};
  return string_run2(self, newargs);
}

e_Method string_methods[] = {
  {"add/1", string_append },
  { "size/0", string_size },
  { "__printOn/1", string_printOn },
  {"getBytes/0", string_getBytes},
  {"multiply/1", string_multiply},
  {"get/1", string_get},
  {"op__cmp/1", string_compareTo},
  {"run/2", string_run2},
  {"run/1", string_run1},
  {NULL}
};
e_Script e__string_script;

