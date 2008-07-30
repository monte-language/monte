#include "elib.h"

#define GET_CHAR_VALUE(_var, _oref)                 \
  {                                                 \
    e_Ref _ref = e_ref_target(_oref);               \
    if (!e_is_char(_ref)) {                         \
      return e_throw_pair("Not a char", _ref);      \
    }                                               \
    _var = _ref.data.chr;                           \
  }


static e_Ref char_add(e_Ref self, e_Ref *args)
{
  e_Ref intguard_args[] = {args[0], e_null};
  e_Ref fval = intguard_coerce(e_null, intguard_args);
  E_ERROR_CHECK(fval);
  int sum = self.data.chr + fval.data.fixnum;
  /* FIXME: check overflow */
  /* XXX Java implementation wraps around instead */
  if (sum < 0 || MAX_CHAR < sum) {
    return e_throw_cstring("Out of range");
  }
  return e_make_char(sum);
}

static e_Ref char_subtract(e_Ref self, e_Ref *args) {
  e_Ref arg = e_ref_target(args[0]);
  if (e_is_fixnum(arg)) {
      int diff = self.data.chr - args[0].data.fixnum;
      /* FIXME: check overflow */
      if (diff < 0 || MAX_CHAR < diff)
	return e_throw_cstring("Out of range");
      return e_make_char(diff);
    } else if (e_is_char(arg)) {
    char c;
    GET_CHAR_VALUE(c, arg);
    int diff = self.data.chr - c;
      return e_make_fixnum(diff);
    } else {
      return e_throw_pair("Bad argument type", arg);
    }
}

static e_Ref char_asInteger (e_Ref self, e_Ref *args) {
  return e_make_fixnum(self.data.chr);
}

static e_Ref char_compareTo(e_Ref self, e_Ref *args) {
  int a = self.data.chr;
  int b;
  GET_CHAR_VALUE(b, args[0]);
  return e_make_fixnum(a - b);
}

static e_Ref
char_escaped(e_Ref self, e_Ref *args) {
  GString *result = NULL;
  int c = self.data.chr;
  switch (c) {
  case '\b': result = g_string_new("\\b"); break;
  case '\t': result = g_string_new("\\t"); break;
  case '\n': result = g_string_new("\\n"); break;
  case '\f': result = g_string_new("\\f"); break;
  case '\r': result = g_string_new("\\r"); break;
  case '\"': result = g_string_new("\\\""); break;
  case '\'': result = g_string_new("\\'"); break;
  case '\\': result = g_string_new("\\\\"); break;
  default:
    {
      result = g_string_sized_new(4);
      if (!g_ascii_isprint(c)) {
        g_string_printf(result, "\\u%x", c);
      } else {
        g_string_printf(result, "%c", c);
      }
    }
  }
  return e_make_gstring(result);
}

static e_Ref char_max(e_Ref self, e_Ref *args) {
  e_Ref arg = args[0];
  char c;
  GET_CHAR_VALUE(c, arg);
  return self.data.chr < c ? arg : self;
}

static e_Ref char_min(e_Ref self, e_Ref *args) {
  e_Ref arg = args[0];
  char c;
  GET_CHAR_VALUE(c, arg);
  return self.data.chr < c ? self : arg;
}

static e_Ref char_next(e_Ref self, e_Ref *args) {
  int c = self.data.chr + 1;
  if (MAX_CHAR < c)
    c = MAX_CHAR;		/* XXX throw error instead? */
  return e_make_char(c);
}

static e_Ref char_previous(e_Ref self, e_Ref *args) {
  int c = self.data.chr - 1;
  if (c < 0)
    c = 0;
  return e_make_char(c);
}

static e_Ref char_printOn(e_Ref self, e_Ref *args) {
  E_ERROR_CHECK(e_print(args[0], e_make_string("'")));
  E_ERROR_CHECK(e_print(args[0], char_escaped(self, NULL)));
  E_ERROR_CHECK(e_print(args[0], e_make_string("'")));
  return e_null;
}

e_Method char_methods[] = {
  { "__printOn/1", char_printOn },
  { "add/1", char_add },
  { "asInteger/0", char_asInteger },
  { "escaped/0", char_escaped },
  { "max/1", char_max },
  { "min/1", char_min },
  { "next/0", char_next },
  { "previous/0", char_previous },
  { "subtract/1", char_subtract },
  { "op__cmp/1", char_compareTo },
  {NULL}
};
e_Script e__char_script;
