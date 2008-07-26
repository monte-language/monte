/* Copyright 2003 Darius Bacon under the terms of the MIT X license
   found at http://www.opensource.org/licenses/mit-license.html */

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
static e_Selector run2, op__cmp;

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

/// @addtogroup null
//@{
static e_Ref null_printOn(e_Ref self, e_Ref *args) {
  E_ERROR_CHECK(e_print(args[0], e_make_string("null")));
  return e_null;
}

static e_Method null_methods[] = {
  { "__printOn/1", null_printOn },
  {NULL}
};
e_Script e__null_script;

e_Ref e_null = { &e__null_script, {0}};
//@}

/// @addtogroup cstring
//@{
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

static e_Method string_methods[] = {
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
//@}

/// @addtogroup bools
//@{
static e_Ref boolean_printOn(e_Ref self, e_Ref *args) {
  e_Ref string = e_make_string(self.data.fixnum ? "true" : "false");
  E_ERROR_CHECK(e_print(args[0], string));
  return e_null;
}

static inline e_Ref boolean_value(e_Ref ref) {
  ref = e_ref_target(ref);
  if (!e_is_boolean (ref)) {
    return e_throw_pair("Not a boolean", ref);
  }
  return ref;
}

static e_Ref boolean_not(e_Ref self, e_Ref *args) {
  return e_make_boolean(1 - self.data.fixnum);
}

static e_Ref boolean_or(e_Ref self, e_Ref *args) {
  e_Ref bval = boolean_value (args[0]);
  E_ERROR_CHECK(bval);
  return e_make_boolean(self.data.fixnum | bval.data.fixnum);
}

static e_Ref boolean_xor(e_Ref self, e_Ref *args) {
  e_Ref bval = boolean_value (args[0]);
  E_ERROR_CHECK(bval);
  return e_make_boolean (self.data.fixnum ^ bval.data.fixnum);
}

static e_Ref boolean_and(e_Ref self, e_Ref *args) {
  e_Ref bval = boolean_value (args[0]);
  E_ERROR_CHECK(bval);
  return e_make_boolean (self.data.fixnum & bval.data.fixnum);
}

static e_Ref boolean_pick(e_Ref self, e_Ref *args) {
  return args[1 - self.data.fixnum];
}

static e_Method boolean_methods[] = {
  { "__printOn/1", boolean_printOn },
  { "not/0", boolean_not },
  { "and/1", boolean_and },
  { "or/1", boolean_or },
  { "xor/1", boolean_xor },
  { "pick/2", boolean_pick },
  {NULL}
};
e_Script e__boolean_script;

e_Ref e_true, e_false;
//@}


/// @ingroup float64

#define GET_FLOAT64_VALUE(_var, _ref)                    \
  {                                                      \
    e_Ref _ref2 = e_ref_target(_ref);                    \
    if (!e_is_float64(_ref2)) {                          \
      return e_throw_pair("Not a float64", _ref2);       \
  }                                                      \
    _var = _ref2.data.float64[0];                        \
  };


static e_Ref float64_abs(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_float64(fabs(a));
}

static e_Ref float64_ceil(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_float64(ceil(a));
}

static e_Ref float64_cos(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_float64(cos(a));
}

static e_Ref float64_exp(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_float64(exp(a));
}

static e_Ref float64_floor(e_Ref self, e_Ref *args) {
  /* FIXME: return an integer object (see also ceil(), etc.) */
  double a = self.data.float64[0];
  return e_make_float64(floor(a));
}

static e_Ref float64_acos(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_float64(acos(a));
}

static e_Ref float64_asin(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_float64(asin(a));
}

static e_Ref float64_atan(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_float64(atan(a));
}

static e_Ref float64_atan2(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  double b;
  GET_FLOAT64_VALUE(b, args[0]);
  return e_make_float64(atan2(a, b));
}

static e_Ref float64_pow(e_Ref self, e_Ref *args) {
  double b, a = self.data.float64[0];
  GET_FLOAT64_VALUE(b, args[0]);
  return e_make_float64 (pow (a, b));
}

static e_Ref float64_log(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_float64(log(a));
}

static e_Ref float64_round(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_float64(round(a));
}

static e_Ref float64_sin(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_float64(sin(a));
}

static e_Ref float64_sqrt(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_float64(sqrt(a));
}

static e_Ref float64_tan(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_float64(tan(a));
}

static e_Ref float64_truncate(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_float64(trunc(a));
}

static e_Ref float64_negate(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_float64(-a);
}

static e_Ref float64_max(e_Ref self, e_Ref *args) {
  /* FIXME: what's the result if they're incomparable? */
  double b, a = self.data.float64[0];
  GET_FLOAT64_VALUE(b, args[0]);
  return a < b ? args[0] : self;
}

static e_Ref float64_min(e_Ref self, e_Ref *args) {
  /* FIXME: what's the result if they're incomparable? */
  double b, a = self.data.float64[0];
  GET_FLOAT64_VALUE(b, args[0]);
  return a > b ? args[0] : self;
}

static e_Ref float64_add(e_Ref self, e_Ref *args) {
  double b, a = self.data.float64[0];
  GET_FLOAT64_VALUE(b, args[0]);
  return e_make_float64 (a + b);
}

static e_Ref float64_subtract(e_Ref self, e_Ref *args) {
  double b, a = self.data.float64[0];
  GET_FLOAT64_VALUE(b, args[0]);
  return e_make_float64 (a - b);
}

static e_Ref float64_multiply(e_Ref self, e_Ref *args) {
  double b, a = self.data.float64[0];
  GET_FLOAT64_VALUE(b, args[0]);
  return e_make_float64 (a * b);
}

static e_Ref float64_approxDivide(e_Ref self, e_Ref *args) {
  double b, a = self.data.float64[0];
  GET_FLOAT64_VALUE(b, args[0]);
  return e_make_float64 (a / b);
}

static e_Ref float64_compareTo(e_Ref self, e_Ref *args) {
  double b, a = self.data.float64[0];
  GET_FLOAT64_VALUE(b, args[0]);
  double result = 0;
  if (a < b)
    result = -1;
  else if (a == b)
    result = 0;
  else if (a > b)
    result = 1;
  else
    result = 0.0/0.0;
  return e_make_float64(result);
}

static e_Ref float64_isZero(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_boolean(0 == a);
}

static e_Ref
float64_belowZero (e_Ref self, e_Ref *args)
{
  double a = self.data.float64[0];
  return e_make_boolean (a < 0);
}

static e_Ref float64_aboveZero(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_boolean(a > 0);
}

static e_Ref float64_atMostZero(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_boolean(a <= 0);
}

static e_Ref float64_atLeastZero(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_boolean(a >= 0);
}

static e_Ref float64_printOn(e_Ref self, e_Ref *args) {
  GString *buffer = g_string_new(NULL);
  if (isnan(self.data.float64[0])) {
    g_string_printf(buffer, "NaN");
  } else {
    g_string_printf (buffer, "%.16g", *self.data.float64);
    {				/* Add a decimal point if necessary */
      char *b = (buffer->str[0] == '-' ? buffer->str+1 : buffer->str);
      size_t off = strspn(b, "0123456789");
      if ('\0' == b[off]) {
        g_string_append(buffer, ".0");
      }
    }
  }
  E_ERROR_CHECK(e_print(args[0], e_make_gstring(buffer)));
  return e_null;
}

/// Convert a floating-point value to a hexadecimal string.
static e_Ref float64_toHexString(e_Ref self, e_Ref *args) {
  char rep[24];
  int win = snprintf(rep, 24, "%a",  *self.data.float64);
  if (win >= 24) {
    return e_throw_cstring("uh oh it broke");
  }
  return e_make_string(rep);
}

static e_Ref float64_floorDivide(e_Ref self, e_Ref *args) {
  double b, a = self.data.float64[0];
  GET_FLOAT64_VALUE(b, args[0]);
  double q = floor (a / b);
  int result = (int) q;
  if (result != q) {
    mpz_t *bigresult = e_malloc(sizeof *bigresult);
    mpz_init_set_d(*bigresult, q);
    return e_make_bignum(bigresult);
  } else {
    return e_make_fixnum(result);
  }
}

static e_Ref float64_isInfinite(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_boolean(!isfinite(a));
}

static e_Ref float64_isNaN(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_boolean(isnan(a));
}

static e_Ref float64_mod(e_Ref self, e_Ref *args) {
  double b, a = self.data.float64[0];
  GET_FLOAT64_VALUE(b, args[0]);
  double q = floor (a / b);
  double r = a - b * q;
  return e_make_float64(r);
}

static e_Ref float64_modPow(e_Ref self, e_Ref *args) {
  return e_throw_cstring("XXX unimplemented method");
}

static e_Ref float64_next(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_float64(nextafter(a, INFINITY));
}

static e_Ref float64_previous(e_Ref self, e_Ref *args) {
  double a = self.data.float64[0];
  return e_make_float64(nextafter(a, -INFINITY));
}

static e_Ref float64_remainder(e_Ref self, e_Ref *args) {
  double b, a = self.data.float64[0];
  GET_FLOAT64_VALUE(b, args[0]);
  double r = fmod(a, b);
  return e_make_float64(r);
}

static e_Ref float64_truncDivide(e_Ref self, e_Ref *args) {
  double b, a = self.data.float64[0];
  GET_FLOAT64_VALUE(b, args[0]);
  double q = a / b;
  int result = (int) q;
  if (result != (double)result) {
    mpz_t *bigresult = e_malloc(sizeof *bigresult);
    mpz_init_set_d(*bigresult, q);
    return e_make_bignum(bigresult);
  } else {
    return e_make_fixnum(result);
  }
}

static e_Method float64_methods[] = {
  { "aboveZero/0", float64_aboveZero },
  { "abs/0", float64_abs },
  { "acos/0", float64_acos },
  { "add/1", float64_add },
  { "approxDivide/1", float64_approxDivide },
  { "asin/0", float64_asin },
  { "atLeastZero/0", float64_atLeastZero },
  { "atMostZero/0", float64_atMostZero },
  { "atan/0", float64_atan },
  { "atan2/1", float64_atan2 },
  { "belowZero/0", float64_belowZero },
  { "ceil/0", float64_ceil },
  { "compareTo/1", float64_compareTo },
  { "cos/0", float64_cos },
  { "exp/0", float64_exp },
  { "floor/0", float64_floor },
  { "floorDivide/1", float64_floorDivide },
  { "isInfinite/0", float64_isInfinite },
  { "isNaN/0", float64_isNaN },
  { "isZero/0", float64_isZero },
  { "log/0", float64_log },
  { "max/1", float64_max },
  { "mod/1", float64_mod },
  { "modPow/2", float64_modPow },
  { "min/1", float64_min },
  { "multiply/1", float64_multiply },
  { "negate/0", float64_negate },
  { "next/0", float64_next },
  { "pow/1", float64_pow },
  { "round/0", float64_round },
  { "previous/0", float64_previous },
  { "remainder/1", float64_remainder },
  { "sin/0", float64_sin },
  { "sqrt/0", float64_sqrt },
  { "subtract/1", float64_subtract },
  { "tan/0", float64_tan },
  { "truncDivide/1", float64_truncDivide },
  { "truncate/0", float64_truncate },
  { "__printOn/1", float64_printOn },
  { "toHexString/0", float64_toHexString },
  {NULL}
};
e_Script e__float64_script;
//@}


/// @ingroup bignum
//@{
#ifndef NO_GC
static void *gmp_realloc(void *ptr, size_t old, size_t new) {
    return GC_realloc(ptr, new);
}

static void do_nothing_free(void *ptr, size_t size) {}
#endif

#define GET_BIGNUM_VALUE_OR_PUNT(_target, _val, _result, OPNAME)        \
  {                                                                     \
    e_Ref _val2 = e_ref_target(_val);                                   \
    _result = e_null;                                                   \
    if (e_is_fixnum(_val2)) {                                           \
      mpz_init_set_si(_target, _val2.data.fixnum);                      \
    } else if (e_is_bignum(_val2)) {                                    \
      mpz_init_set(_target, *_val2.data.bignum);                        \
    } else if (e_is_float64(_val2)) {                                   \
      _result = float64_##OPNAME(e_bignum_as_float64(self), args);      \
    } else {                                                            \
      return e_throw_pair("Not a number", args[0]);                     \
    }                                                                   \
  };

e_Ref e_bignum_from_fixnum(int a) {
mpz_t *bignum = e_malloc(sizeof *bignum);
  mpz_init_set_si(*bignum, a);
  return e_make_bignum(bignum);
}

static e_Ref e_bignum_as_fixnum(e_Ref big) {
  if (mpz_fits_slong_p(*big.data.bignum)) {
    return e_make_fixnum(mpz_get_si(*big.data.bignum));
  }
  return e_throw_cstring("Number too large to convert to machine-size integer");
}

e_Ref e_bignum_as_float64(e_Ref big) {
  return e_make_float64(mpz_get_d(*big.data.bignum));
}


static e_Ref e_bignum_from_sum(int a, int b) {
  mpz_t *bignum = e_malloc(sizeof *bignum);
  mpz_t bigA;
  mpz_t bigB;
  mpz_init_set_si(bigA, a);
  mpz_init_set_si(bigB, b);
  mpz_add(*bignum, bigA, bigB);
  mpz_clear(bigA);
  mpz_clear(bigB);
  return e_make_bignum(bignum);
}

static e_Ref bignum_toByteArray(e_Ref self, e_Ref *args) {
  char *bits;
  e_Ref *bobs;
  size_t count;
  bits = mpz_export(NULL, &count, 1, sizeof(char), 1, 0, *self.data.bignum);
  bobs = e_make_array(count);
  for (int i = 0; i < count; i++) {
    bobs[i] = e_make_fixnum(bits[i]);
  }
  return e_flexlist_from_array(count, bobs);
}


static e_Ref bignum_add(e_Ref self, e_Ref *args) {
  mpz_t other;
  e_Ref x;
  mpz_t *bigres;
  GET_BIGNUM_VALUE_OR_PUNT(other, args[0], x, add);
  if (!e_same(e_null, x)) {
    return x;
  }
  bigres = e_malloc(sizeof *bigres);
  mpz_init(*bigres);
  mpz_add(*bigres, *self.data.bignum, other);
  return e_make_bignum(bigres);
}

static e_Ref bignum_subtract(e_Ref self, e_Ref *args) {
  mpz_t other;
  e_Ref x;
  mpz_t *bigres;
  GET_BIGNUM_VALUE_OR_PUNT(other, args[0], x, subtract);
  if (!e_same(e_null, x)) {
    return x;
  }
  bigres = e_malloc(sizeof *bigres);
  mpz_init(*bigres);
  mpz_sub(*bigres, *self.data.bignum, other);
  return e_make_bignum(bigres);
}

static e_Ref bignum_multiply(e_Ref self, e_Ref *args) {
  mpz_t other;
  e_Ref x;
  mpz_t *bigres;
  GET_BIGNUM_VALUE_OR_PUNT(other, args[0], x, multiply);
  if (!e_same(e_null, x)) {
    return x;
  }
  bigres = e_malloc(sizeof *bigres);
  mpz_init(*bigres);
  mpz_mul(*bigres, *self.data.bignum, other);
  return e_make_bignum(bigres);
}

static e_Ref bignum_pow(e_Ref self, e_Ref *args) {
  mpz_t other;
  e_Ref x;
  mpz_t *bigres;
  int exp;
  GET_BIGNUM_VALUE_OR_PUNT(other, args[0], x, add);
  if (!e_same(e_null, x)) {
    return x;
  }
  if (mpz_fits_slong_p(other)) {
    exp = mpz_get_si(other);
  } else {
    return e_throw_pair("Exponent too large", args[0]);
  }
  bigres = e_malloc(sizeof *bigres);
  mpz_init(*bigres);
  mpz_pow_ui(*bigres, *self.data.bignum, exp);
  return e_make_bignum(bigres);
}


static e_Ref bignum_approxDivide(e_Ref self, e_Ref *args) {
  mpz_t other;
  e_Ref x;
  GET_BIGNUM_VALUE_OR_PUNT(other, args[0], x, approxDivide);
  if (!e_same(x, e_null)) {
    return x;
  }
  double a = mpz_get_d(*self.data.bignum);
  double b = mpz_get_d(other);
  return e_make_float64(a / b);
}

static e_Ref bignum_mod(e_Ref self, e_Ref *args) {
  mpz_t other;
  e_Ref x;
  mpz_t *bigres;
  GET_BIGNUM_VALUE_OR_PUNT(other, args[0], x, mod);
  if (!e_same(e_null, x)) {
    return x;
  }
  bigres = e_malloc(sizeof *bigres);
  mpz_init(*bigres);
  mpz_fdiv_r(*bigres, *self.data.bignum, other);
  return e_make_bignum(bigres);
}

static e_Ref bignum_remainder(e_Ref self, e_Ref *args) {
  mpz_t other;
  e_Ref x;
  mpz_t *bigres;
  GET_BIGNUM_VALUE_OR_PUNT(other, args[0], x, remainder);
  if (!e_same(e_null, x)) {
    return x;
  }
  bigres = e_malloc(sizeof *bigres);
  mpz_init(*bigres);
  mpz_tdiv_r(*bigres, *self.data.bignum, other);
  return e_make_bignum(bigres);
}

static e_Ref bignum_floorDivide(e_Ref self, e_Ref *args) {
  mpz_t other;
  e_Ref x;
  mpz_t *bigres;
  GET_BIGNUM_VALUE_OR_PUNT(other, args[0], x, floorDivide);
  if (!e_same(e_null, x)) {
    return x;
  }
  bigres = e_malloc(sizeof *bigres);
  mpz_init(*bigres);
  mpz_fdiv_q(*bigres, *self.data.bignum, other);
  return e_make_bignum(bigres);
}

static e_Ref bignum_truncDivide(e_Ref self, e_Ref *args) {
  mpz_t other;
  e_Ref x;
  mpz_t *bigres;
  GET_BIGNUM_VALUE_OR_PUNT(other, args[0], x, truncDivide);
  if (!e_same(e_null, x)) {
    return x;
  }
  bigres = e_malloc(sizeof *bigres);
  mpz_init(*bigres);
  mpz_tdiv_q(*bigres, *self.data.bignum, other);
  return e_make_bignum(bigres);
}

static e_Ref bignum_butNot(e_Ref self, e_Ref *args) {
  mpz_t *other;
  mpz_t fromFixnum;
  mpz_t other2;
  mpz_t *bigres;
  e_Ref arg = e_ref_target(args[0]);
  if (e_is_fixnum(arg)) {
    mpz_init_set_si(fromFixnum, arg.data.fixnum);
    other = &fromFixnum;
  } else if (e_is_bignum(arg)) {
    other = arg.data.bignum;
  } else {
    return e_throw_pair("Not an integer", arg);
  }
  bigres = e_malloc(sizeof *bigres);
  mpz_init(*bigres);
  mpz_init(other2);
  mpz_com(other2, *other);
  mpz_and(*bigres, *self.data.bignum, other2);
  return e_make_bignum(bigres);
}

static e_Ref bignum_compareTo(e_Ref self, e_Ref *args) {
  mpz_t *other;
  mpz_t fromFixnum;
  e_Ref arg = e_ref_target(args[0]);
  if (e_is_fixnum(arg)) {
    mpz_init_set_si(fromFixnum, arg.data.fixnum);
    other = &fromFixnum;
  } else if (e_is_bignum(arg)) {
    other = arg.data.bignum;
  } else {
    return e_throw_pair("Not an integer", arg);
  }
  return e_make_fixnum(mpz_cmp(*self.data.bignum, *other));
}


static e_Ref bignum_gcd(e_Ref self, e_Ref *args) {
  mpz_t *other;
  mpz_t fromFixnum;
  e_Ref x;
  mpz_t *bigres;
  e_Ref arg = e_ref_target(args[0]);
  if (e_is_fixnum(arg)) {
    mpz_init_set_si(fromFixnum, arg.data.fixnum);
    other = &fromFixnum;
  } else if (e_is_bignum(args[0])) {
    other = args[0].data.bignum;
  } else {
    return e_throw_pair("Not an integer", arg);
  }
  if (!e_same(e_null, x)) {
    return x;
  }
  bigres = e_malloc(sizeof *bigres);
  mpz_init(*bigres);
  mpz_gcd(*bigres, *self.data.bignum, *other);
  return e_make_bignum(bigres);
}

static e_Ref bignum_or(e_Ref self, e_Ref *args) {
  mpz_t *other;
  mpz_t fromFixnum;
  e_Ref x;
  mpz_t *bigres;
  e_Ref arg = e_ref_target(args[0]);
  if (e_is_fixnum(arg)) {
    mpz_init_set_si(fromFixnum, arg.data.fixnum);
    other = &fromFixnum;
  } else if (e_is_bignum(arg)) {
    other = arg.data.bignum;
  } else {
    return e_throw_pair("Not an integer", arg);
  }
  if (!e_same(e_null, x)) {
    return x;
  }
  bigres = e_malloc(sizeof *bigres);
  mpz_init(*bigres);
  mpz_ior(*bigres, *self.data.bignum, *other);
  return e_make_bignum(bigres);
}

static e_Ref bignum_xor(e_Ref self, e_Ref *args) {
  mpz_t *other;
  mpz_t fromFixnum;
  e_Ref x;
  mpz_t *bigres;
  e_Ref arg = e_ref_target(args[0]);
  if (e_is_fixnum(arg)) {
    mpz_init_set_si(fromFixnum, arg.data.fixnum);
    other = &fromFixnum;
  } else if (e_is_bignum(arg)) {
    other = arg.data.bignum;
  } else {
    return e_throw_pair("Not an integer", arg);
  }
  if (!e_same(e_null, x)) {
    return x;
  }
  bigres = e_malloc(sizeof *bigres);
  mpz_init(*bigres);
  mpz_xor(*bigres, *self.data.bignum, *other);
  return e_make_bignum(bigres);
}

static e_Ref bignum_and(e_Ref self, e_Ref *args) {
  mpz_t *other;
  mpz_t fromFixnum;
  e_Ref x;
  mpz_t *bigres;
  e_Ref arg = e_ref_target(args[0]);
  if (e_is_fixnum(arg)) {
    mpz_init_set_si(fromFixnum, arg.data.fixnum);
    other = &fromFixnum;
  } else if (e_is_bignum(arg)) {
    other = arg.data.bignum;
  } else {
    return e_throw_pair("Not an integer", arg);
  }
  if (!e_same(e_null, x)) {
    return x;
  }
  bigres = e_malloc(sizeof *bigres);
  mpz_init(*bigres);
  mpz_and(*bigres, *self.data.bignum, *other);
  return e_make_bignum(bigres);
}



static e_Ref bignum_max(e_Ref self, e_Ref *args) {
  mpz_t other;
  e_Ref x;
  GET_BIGNUM_VALUE_OR_PUNT(other, args[0], x, max);
  if (!e_same(e_null, x)) {
    return x;
  }
  if (mpz_cmp(*self.data.bignum, other) > 0) {
    return self;
  } else {
    return args[0];
  }
}

static e_Ref bignum_min(e_Ref self, e_Ref *args) {
  mpz_t other;
  e_Ref x;
  GET_BIGNUM_VALUE_OR_PUNT(other, args[0], x, min);
  if (!e_same(e_null, x)) {
    return x;
  }
  if (mpz_cmp(*self.data.bignum, other) < 0) {
    return self;
  } else {
    return args[0];
  }
}

static e_Ref bignum_negate(e_Ref self, e_Ref *args) {
  mpz_t *res = e_malloc(sizeof *res);
  mpz_init(*res);
  mpz_neg(*res, *self.data.bignum);
  return e_make_bignum(res);
}

static e_Ref bignum_next(e_Ref self, e_Ref *args) {
  mpz_t *res = e_malloc(sizeof *res);
  mpz_init(*res);
  mpz_add_ui(*res, *self.data.bignum, 1);
  return e_make_bignum(res);
}

static e_Ref bignum_previous(e_Ref self, e_Ref *args) {
  mpz_t *res = e_malloc(sizeof *res);
  mpz_init(*res);
  mpz_sub_ui(*res, *self.data.bignum, 1);
  return e_make_bignum(res);
}

static e_Ref bignum_shiftLeft(e_Ref self, e_Ref *args) {
  int other;
  mpz_t *bigres;
  e_Ref arg = e_ref_target(args[0]);
  if (e_is_fixnum(arg)) {
    other = arg.data.fixnum;
  } else if (e_is_bignum(arg)) {
    if (mpz_fits_slong_p(*arg.data.bignum)) {
      other = mpz_get_si(*arg.data.bignum);
    } else {
      return e_throw_pair("Out of range", arg);
    }
  } else {
    return e_throw_pair("Not an integer", arg);
  }
  bigres = e_malloc(sizeof *bigres);
  mpz_init(*bigres);
  mpz_mul_2exp(*bigres, *self.data.bignum, other);
  return e_make_bignum(bigres);
}

static e_Ref bignum_shiftRight(e_Ref self, e_Ref *args) {
  int other;
  mpz_t *bigres;
  e_Ref arg = e_ref_target(args[0]);
  if (e_is_fixnum(arg)) {
    other = arg.data.fixnum;
  } else if (e_is_bignum(arg)) {
    if (mpz_fits_slong_p(*arg.data.bignum)) {
      other = mpz_get_si(*arg.data.bignum);
    } else {
      return e_throw_pair("Out of range", arg);
    }
  } else {
    return e_throw_pair("Not an integer", arg);
  }
  bigres = e_malloc(sizeof *bigres);
  mpz_init(*bigres);
  mpz_fdiv_q_2exp(*bigres, *self.data.bignum, other);
  return e_make_bignum(bigres);
}


static e_Ref bignum_printOn(e_Ref self, e_Ref *args) {
  char *rep;
  gmp_asprintf(&rep, "%Zd", *self.data.bignum);
  E_ERROR_CHECK(e_print(args[0], e_make_string(rep)));
  return e_null;
}

static e_Ref bignum_atMostZero(e_Ref self, e_Ref *args) {
  return e_make_boolean(mpz_cmp_ui(*self.data.bignum, 0) <= 0);
}

static e_Ref bignum_belowZero(e_Ref self, e_Ref *args) {
  return e_make_boolean(mpz_cmp_ui(*self.data.bignum, 0) > 0);
}

static e_Ref bignum_isZero(e_Ref self, e_Ref *args) {
  return e_make_boolean(mpz_cmp_ui(*self.data.bignum, 0) == 0);
}

static e_Ref bignum_aboveZero(e_Ref self, e_Ref *args) {
  return e_make_boolean(mpz_cmp_ui(*self.data.bignum, 0) > 0);
}

static e_Ref bignum_atLeastZero(e_Ref self, e_Ref *args) {
  return e_make_boolean(mpz_cmp_ui(*self.data.bignum, 0) >= 0);
}


static e_Method bignum_methods[] = {
  {"add/1", bignum_add},
  {"subtract/1", bignum_subtract},
  {"multiply/1", bignum_multiply},
  {"pow/1", bignum_pow},
  {"approxDivide/1", bignum_approxDivide},
  {"mod/1", bignum_mod},
  {"remainder/1", bignum_remainder},
  {"floorDivide/1", bignum_floorDivide},
  {"truncDivide/1", bignum_truncDivide},
  {"butNot/1", bignum_butNot},
  {"op__cmp/1", bignum_compareTo},
  {"gcd/1", bignum_gcd},
  {"or/1", bignum_or},
  {"xor/1", bignum_xor},
  {"and/1", bignum_and},
  {"max/1", bignum_max},
  {"min/1", bignum_min},
  {"negate/0", bignum_negate},
  {"next/0", bignum_next},
  {"previous/0", bignum_previous},
  {"shiftLeft/1", bignum_shiftLeft},
  {"shiftRight/1", bignum_shiftRight},
  {"aboveZero/0", bignum_aboveZero},
  {"belowZero/0", bignum_belowZero},
  {"isZero/0", bignum_isZero},
  {"atLeastZero/0", bignum_atLeastZero},
  {"atMostZero/0", bignum_atMostZero},
  {"toByteArray/0", bignum_toByteArray},
  {"__printOn/1", bignum_printOn},
  {NULL}
};
e_Script e__bignum_script;
//@}

/// @ingroup fixnum
#define GET_FIXNUM_VALUE(_var, _oref)                             \
  {                                                               \
    e_Ref _ref = e_ref_target(_oref);                             \
    if (e_is_bignum(_ref)) {                                      \
      _var = e_bignum_as_fixnum(_ref).data.fixnum;                \
    } else {                                                      \
      if (!e_is_fixnum(_ref)) {                                   \
        return e_throw_pair("Not a small integer", _ref);         \
      }                                                           \
      _var = _ref.data.fixnum;                                    \
    }                                                             \
  }

#define GET_INTEGRAL_VALUE(_var, _oref, _res, OPNAME)             \
  {                                                               \
    e_Ref _ref = e_ref_target(_oref);                             \
    if (e_is_bignum(_ref)) {                                      \
      e_Ref bigself = e_bignum_from_fixnum(self.data.fixnum);     \
      _res = bignum_##OPNAME(bigself, args);                      \
    } else {                                                      \
      _res = e_null;                                              \
      if (!e_is_fixnum(_ref)) {                                   \
        return e_throw_pair("Not a small integer", _ref);         \
      }                                                           \
      _var = _ref.data.fixnum;                                    \
    }                                                             \
  }

#define GET_FIXNUM_VALUE_OR_PUNT(_var, _oref, _res, OPNAME)       \
  {                                                               \
    e_Ref _ref = e_ref_target(_oref);                             \
    if (e_is_float64(_ref)) {                                     \
      e_Ref floatself = e_make_float64(self.data.fixnum);         \
      _res = float64_##OPNAME(floatself, &_ref);                  \
    } else if (e_is_bignum(_ref)) {                               \
      e_Ref bigself = e_bignum_from_fixnum(self.data.fixnum);     \
      _res = bignum_##OPNAME(bigself, &_ref);                     \
    } else {                                                      \
      _res = e_null;                                              \
      if (!e_is_fixnum(_ref)) {                                   \
        return e_throw_pair("Not a small integer", _ref);         \
      }                                                           \
      _var = _ref.data.fixnum;                                    \
    }                                                             \
  }

/// @addtogroup char
//@{
#define MAX_CHAR 65535
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
  int fval;
  GET_FIXNUM_VALUE(fval, args[0])
  int sum = self.data.chr + fval;
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

static e_Method char_methods[] = {
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
//@}
/// @addtogroup print
//@{
static e_Ref writer_print(e_Ref self, e_Ref *args, int numItems) {
  GOutputStream *stream = self.data.refs[0].data.other;
  GError *err = NULL;
  for (int i = 0; i < numItems; i++) {
    e_Ref arg = e_ref_target(args[i]);
    if (e_is_string(arg)) {
      _Bool win = g_output_stream_write_all(stream, arg.data.gstring->str,
                                            arg.data.gstring->len,
                                            NULL, NULL, &err);
      if (!win) {
        if (err != NULL) {
          return e_throw_pair(err->message, e_make_fixnum(err->code));
        } else {
          return e_throw_cstring("Unspecified error in writer_print");
        }
      }
    } else {
      E_ERROR_CHECK(e_print_on(arg, self));
    }
  }
  return e_null;
}

static e_Ref writer_print1(e_Ref self, e_Ref *args) {
  return writer_print(self, args, 1);
}

static e_Ref writer_print2(e_Ref self, e_Ref *args) {
  return writer_print(self, args, 2);
}

static e_Ref writer_print3(e_Ref self, e_Ref *args) {
  return writer_print(self, args, 3);
}

static e_Ref writer_print4(e_Ref self, e_Ref *args) {
  return writer_print(self, args, 4);
}

static e_Ref writer_print5(e_Ref self, e_Ref *args) {
  return writer_print(self, args, 5);
}

static e_Ref writer_print6(e_Ref self, e_Ref *args) {
  return writer_print(self, args, 6);
}

static e_Ref writer_print7(e_Ref self, e_Ref *args) {
  return writer_print(self, args, 7);
}

static e_Ref writer_println0(e_Ref self, e_Ref *args) {
  return e_print(self, self.data.refs[1]);
}

static e_Ref writer_println(e_Ref self, e_Ref *args) {
  E_ERROR_CHECK(writer_print1(self, args));
  E_ERROR_CHECK(e_print(self, self.data.refs[1]));
  return e_null;
}

static e_Ref writer_quotePrint(e_Ref self, e_Ref *args) {
  e_Ref arg = e_ref_target(args[0]);
  if (e_is_string(arg)) {
    GString *original = arg.data.other;
    e_Ref escapedString = e_make_string(g_strescape(original->str, NULL));
    E_ERROR_CHECK(e_print(self, e_make_string("\"")));
    E_ERROR_CHECK(writer_print1(self, &escapedString));
    E_ERROR_CHECK(e_print(self, e_make_string("\"")));
  } else {
    E_ERROR_CHECK(writer_print1(self, args));
  }
  return e_null;
}

static e_Ref writer_printOn(e_Ref self, e_Ref *args) {
  E_ERROR_CHECK(e_print(args[0], e_make_string("<writer>")));
  return e_null;
}

static e_Ref writer_indent(e_Ref self, e_Ref *args) {
  e_Ref new = e_make_writer(self.data.refs[0].data.other);
  new.data.refs[1] = args[0];
  return new;
}

e_Ref e_make_writer(GOutputStream *stream) {
  e_Ref result;
  e_Ref *bits = e_malloc(2 * sizeof *bits);
  bits[0].data.other = stream;
  bits[1] = e_make_string("\n");
  result.script = &e__writer_script;
  result.data.other = bits;
  return result;
}

static e_Method writer_methods[] = {
  {"print/1", writer_print1},
  {"print/2", writer_print2},
  {"print/3", writer_print3},
  {"print/4", writer_print4},
  {"print/5", writer_print5},
  {"print/6", writer_print6},
  {"print/7", writer_print7},
  {"println/1", writer_println},
  {"println/0", writer_println0},
  {"quote/1", writer_quotePrint},
  {"__printOn/1", writer_printOn},
  {"indent/1", writer_indent},
  {NULL}
};
e_Script e__writer_script;

e_Ref e_make_string_writer() {
#if OLD_GIO
  GOutputStream *stream = g_memory_output_stream_new(NULL);
#else
#ifdef NO_GC
  GOutputStream *stream = g_memory_output_stream_new(NULL, 0, realloc, NULL);
#else
  GOutputStream *stream = g_memory_output_stream_new(NULL, 0, GC_realloc, NULL);
#endif //NO_GC
#endif //OLD_GIO
  return e_make_writer(stream);
}
e_Ref e_string_writer_get_string(e_Ref writer) {
  GMemoryOutputStream *stream = writer.data.refs[0].data.other;
#if OLD_GIO
   char *output = g_memory_output_stream_get_data(stream)->data;
#else
   char *output = g_memory_output_stream_get_data(stream);
#endif
  return e_make_gstring(
           g_string_new_len(output,
             g_seekable_tell((GSeekable *)stream)));
}


e_Script e__reader_script;

e_Ref e_stdin;
e_Ref e_stdout;
e_Ref e_stderr;

//@}

static e_Ref identity(e_Ref self, e_Ref *args) {
  return self;
}

/// @ingroup fixnum
//@{

/** Return the number of bits in the two's complement representation of
   'a' that differ from its sign bit. */
static int bit_count(int a)
{
  int n = 0;
  int bit = (0 <= a);
  while ((a >> 1) != a)		/* XXX unportable */
    {
      if (bit == (a & 1))
	++n;
      a >>= 1;
    }
  return n;
}

/** Return the number of bits in the minimal two's complement
   representation of 'a', excluding its sign bit. */
static int bit_length(int a)
{
  int n = 0;
  while ((a >> 1) != a)		/* XXX unportable */
    {
      a >>= 1;
      ++n;
    }
  return n;
}

#define def_fixnum0(name, expr)  \
  static e_Ref                   \
  name (e_Ref self, e_Ref *args) \
  {                              \
    int a = self.data.fixnum;    \
    return expr;                 \
  }

static e_Ref fixnum_abs (e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  if (INT_MIN == a) {
    return e_throw_cstring("no bignums yet");
  }
  return e_make_fixnum(abs(a));
}

static e_Ref fixnum_aboveZero (e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  return e_make_boolean(a > 0);
}

static e_Ref fixnum_add(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int b;
  e_Ref res;
  GET_FIXNUM_VALUE_OR_PUNT(b, args[0], res, add);
  if (!e_same(res, e_null)) {
    return res;
  }
  int sum = a + b;
  /* This depends on int being 2's complement with wraparound. */
  if (((sum ^ a) & (sum ^ b)) < 0)
    return e_bignum_from_sum(a, b);
  return e_make_fixnum(sum);
}

static e_Ref fixnum_and(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int b;
  e_Ref res;
  GET_INTEGRAL_VALUE(b, args[0], res, and);
  if (!e_same(res, e_null)) {
    return res;
  }
  return e_make_fixnum(a & b);
}


static e_Ref fixnum_approxDivide(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int b;
  e_Ref res;
  GET_FIXNUM_VALUE_OR_PUNT(b, args[0], res, approxDivide);
  if (!e_same(res, e_null)) {
    return res;
  }
  return e_make_float64((double)a / b);
}

static e_Ref fixnum_asChar(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  if (a < 0 || MAX_CHAR < a) {
    return e_throw_cstring("Out of range");
  }
  return e_make_char (a);
}

def_fixnum0 (fixnum_asFloat64, e_make_float64(a))
def_fixnum0 (fixnum_atLeastZero, e_make_boolean(a >= 0))
def_fixnum0 (fixnum_atMostZero, e_make_boolean(a <= 0))
def_fixnum0 (fixnum_belowZero, e_make_boolean(a < 0))

def_fixnum0 (fixnum_bitCount, e_make_fixnum(bit_count (a)))
def_fixnum0 (fixnum_bitLength, e_make_fixnum(bit_length (a)))

static e_Ref fixnum_butNot (e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int b;
  e_Ref res;
  GET_INTEGRAL_VALUE(b, args[0], res, butNot);
  if (!e_same(res, e_null)) {
    return res;
  }
  return e_make_fixnum(a & ~b);
}
static e_Ref fixnum_compareTo(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int b;
  e_Ref res;
  GET_FIXNUM_VALUE_OR_PUNT(b, args[0], res, compareTo);
  if (!e_same(res, e_null)) {
    return res;
  }
  return e_make_fixnum(a < b ? -1 : a == b ? 0 : 1);
}

static e_Ref fixnum_floorDivide(e_Ref self, e_Ref *args) {
  int64_t numerator = self.data.fixnum;
  int other;
  e_Ref res;
  GET_FIXNUM_VALUE_OR_PUNT(other, args[0], res, floorDivide);
  if (!e_same(res, e_null)) {
    return res;
  }
  /* XXX implementation-defined behavior of the '/' operator */
  if (other < 0) {
    if (numerator >= 0) {
      /* 5 // -3 == -2 */
      /* (5 - 1 - -3).truncDivide(3) == -2 */
      numerator = numerator - 1 - other;
    }
    /* else -5 // -3 == (-5).truncDivide(-3) == 1 */
  } else {
    if (numerator < 0) {
      /* -5 // 3 == -2 */
      /* (-5 + 1 - 3).truncDivide(3) == -2 */
      numerator = numerator + 1 - other;
      /* else 5 // 3 == 5.truncDivide(3) == 1 */
    }
  }
  return e_make_fixnum(numerator / other);
}

def_fixnum0(fixnum_isZero, e_make_boolean(0 == a))

static e_Ref fixnum_multiply(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int b;
  e_Ref res;
  GET_FIXNUM_VALUE_OR_PUNT(b, args[0], res, multiply);
  if (!e_same(res, e_null)) {
    return res;
  }
  // XXX quite possibly naive -- compare to Python's overflow check?
  int64_t product = (int64_t) a * (int64_t) b;
  int ip = product;
  if (product != (int64_t) ip) {
    e_Ref newargs[] = {e_bignum_from_fixnum(b)};
    return bignum_multiply(e_bignum_from_fixnum(a), newargs);
  }
  return e_make_fixnum(ip);
}

static e_Ref fixnum_subtract(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int b;
  e_Ref res;
  GET_FIXNUM_VALUE_OR_PUNT(b, args[0], res, subtract);
  if (!e_same(res, e_null)) {
    return res;
  }
  int diff = a - b;
  /* This depends on int being 2's complement with wraparound. */
  if (((a ^ b) & (diff ^ a)) < 0) {
    return e_bignum_from_sum(-a, b);
  }
  return e_make_fixnum(diff);
}

static e_Ref fixnum_printOn(e_Ref self, e_Ref *args) {
  GString *buffer = g_string_new("");
  g_string_printf(buffer, "%ld", self.data.fixnum);
  E_ERROR_CHECK(e_print(args[0], e_make_gstring(buffer)));
  return e_null;
}

static int gcd(int a, int b) {
  /* CHECKME: handles negatives correctly? */
  while (0 != b) {
      int c = a % b;
      a = b;
      b = c;
    }
  return abs(a);
}

static e_Ref fixnum_gcd(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int b;
  e_Ref res;
  GET_INTEGRAL_VALUE(b, args[0], res, gcd);
    if (!e_same(res, e_null)) {
    return res;
  }
  int g = gcd (a, b);
  return e_make_fixnum(g);
}

static e_Ref fixnum_getLowestSetBit(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int result;
  if (0 == a) {
    result = -1;
  } else {
      result = 0;
      for (; 0 == (a & 1); a >>= 1)
	++result;
    }
  return e_make_fixnum(result);
}

static e_Ref fixnum_isNaN(e_Ref self, e_Ref *args) {
  return e_false;
}

static e_Ref fixnum_max(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int b;
  e_Ref res;
  GET_FIXNUM_VALUE_OR_PUNT(b, args[0], res, max);
  if (!e_same(res, e_null)) {
    return res;
  }
  return a < b ? args[0] : self;
}

static e_Ref fixnum_min(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int b;
  e_Ref res;
  GET_FIXNUM_VALUE_OR_PUNT(b, args[0], res, min);
  if (!e_same(res, e_null)) {
    return res;
  }
  return a < b ? self : args[0];
}

static e_Ref fixnum_mod(e_Ref self, e_Ref *args) {
  /* XXX java/lang/IntegerSugar.java uses longs here for some reason */
  int a = self.data.fixnum;
  int other;
  e_Ref res;
  GET_FIXNUM_VALUE_OR_PUNT(other, args[0], res, mod);
  if (!e_same(res, e_null)) {
    return res;
  }
  int result = a % other;
  if (((other < 0) != (result < 0)) && 0 != result) {
    result += other;
  }
  return e_make_fixnum(result);
  /*
    Should be equivalent, but is more expensive
            return subtract(self,
                            multiply(floorDivide(self, o).intValue(),
                                     o));
  */
}

static e_Ref fixnum_modInverse(e_Ref self, e_Ref *args) {
  return e_throw_cstring ("XXX unimplemented method");
}

static e_Ref fixnum_modPow(e_Ref self, e_Ref *args) {
  return e_throw_cstring ("XXX unimplemented method");
}

static e_Ref fixnum_negate (e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  if (INT_MIN == a)
    return bignum_negate(e_bignum_from_fixnum(a), NULL);
  return e_make_fixnum(-a);
}

static e_Ref fixnum_next (e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int result = a + 1;
  if (0 < a && result < 0) {
    return bignum_next(e_bignum_from_fixnum(a), NULL);
  }
  return e_make_fixnum(result);
}

def_fixnum0 (fixnum_not, e_make_fixnum(~a))

static e_Ref fixnum_or(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int other;
  e_Ref res;
  GET_INTEGRAL_VALUE(other, args[0], res, or);
  if (!e_same(res, e_null)) {
    return res;
  }
  return e_make_fixnum(a | other);
}

static e_Ref fixnum_pow(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int other;
  e_Ref res;
  GET_FIXNUM_VALUE_OR_PUNT(other, args[0], res, pow);
  if (!e_same(res, e_null)) {
    return res;
  }
  if (other < 0) {
    return e_throw_cstring("Negative exponent");
  }
  double p = pow(a, other);
  int result = (int)p;
  if (result != p) {
    mpz_t *bignum = e_malloc(sizeof *bignum);
    mpz_t bigA;
    mpz_init(*bignum);
    mpz_init_set_si(bigA, a);
    mpz_pow_ui(*bignum, bigA, other);
    mpz_clear(bigA);
    return e_make_bignum(bignum);
  }
  return e_make_fixnum(result);
}

static e_Ref fixnum_previous(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int result = a - 1;
  if (a < 0 && 0 < result) {
    return bignum_previous(e_bignum_from_fixnum(a), NULL);
  }
  return e_make_fixnum(result);
}

static e_Ref fixnum_remainder(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int other;
  e_Ref res;
  GET_FIXNUM_VALUE_OR_PUNT(other, args[0], res, remainder);
  if (!e_same(res, e_null)) {
    return res;
  }
  return e_make_fixnum(a % other);
}

enum { int_bits = 32 };	   /* XXX TODO get this out of limits.h or something */

static e_Ref shift_left(int a, int count) {
  int result;
  if (0 <= count) {
    result = a << count;
    if (int_bits <= count || a != (result >> count)) {
      e_Ref args[] = {e_make_fixnum(count)};
      return bignum_shiftLeft(e_bignum_from_fixnum(a), args);
    }
  } else {
    if (int_bits <= -count) {
      result = a >> (int_bits-1);
    } else {
      result = a >> (-count);
    }
      /* XXX this claims result = floor(a / (2**n)):
	 http://java.sun.com/j2se/1.4.2/docs/api/java/math/BigInteger.html
	 rather than rounding to -infinity */
  }
  return e_make_fixnum(result);
}

static e_Ref fixnum_shiftLeft(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int other;
  e_Ref res;
  GET_INTEGRAL_VALUE(other, args[0], res, shiftLeft);
  if (!e_same(res, e_null)) {
    return res;
  }
  return shift_left(a, other);
}

static e_Ref fixnum_shiftRight(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int other;
  e_Ref res;
  GET_INTEGRAL_VALUE(other, args[0], res, shiftRight);
  if (!e_same(res, e_null)) {
    return res;
  }
  if (other > int_bits) {
    return e_make_fixnum(0);
  }
  return shift_left(a, -other);
}

static e_Ref fixnum_signum(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int result = (a < 0 ? -1 : 0 == a ? 0 : 1);
  return e_make_fixnum(result);
}

static e_Ref fixnum_toByteArray(e_Ref self, e_Ref *args) {
  return e_throw_cstring("XXX unimplemented method");
}

static GString *unparse_int(int n, unsigned radix) {
  GString *buf = g_string_new(NULL);
  unsigned u = n < 0 ? -n : n;
  if (n < 0) {
    g_string_append_c(buf, '-');
  }
  if (u == 0) {
    g_string_append_c(buf, '0');
  } else {
    for (; u != 0; u /= radix) {
      unsigned digit = u % radix;
      g_string_prepend_c(buf, digit < 10 ? '0' + digit : 'A' - 10 + digit);
    }
  }
  return buf;
}


static e_Ref fixnum_toString(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int radix;
  GET_FIXNUM_VALUE(radix, args[0]);
  if (!(2 <= radix && radix <= 36)) {
    return e_throw_pair("Unsupported radix", args[0]);
  }
  return e_make_gstring(unparse_int(a, radix));
}

static e_Ref fixnum_toString64(e_Ref self, e_Ref *args) {
  return e_throw_cstring("XXX unimplemented method");
}

static e_Ref fixnum_truncDivide(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int other;
  e_Ref res;
  GET_FIXNUM_VALUE_OR_PUNT(other, args[0], res, truncDivide);
  if (!e_same(res, e_null)) {
    return res;
  }
  return e_make_fixnum(a / other);
}

static e_Ref fixnum_xor(e_Ref self, e_Ref *args) {
  int a = self.data.fixnum;
  int other;
  e_Ref res;
  GET_INTEGRAL_VALUE(other, args[0], res, xor);
  if (!e_same(res, e_null)) {
    return res;
  }
  return e_make_fixnum(a ^ other);
}

static e_Method fixnum_methods[] = {
  { "aboveZero/0", fixnum_aboveZero },
  { "abs/0", fixnum_abs },
  { "add/1", fixnum_add },
  { "and/1", fixnum_and },
  { "approxDivide/1", fixnum_approxDivide },
  { "asChar/0", fixnum_asChar },
  { "asFloat64/0", fixnum_asFloat64 },
  { "atLeastZero/0", fixnum_atLeastZero },
  { "atMostZero/0", fixnum_atMostZero },
  { "belowZero/0", fixnum_belowZero },
  { "bitCount/0", fixnum_bitCount },
  { "bitLength/0", fixnum_bitLength },
  { "butNot/1", fixnum_butNot },
  { "ceil/0", identity },
  { "op__cmp/1", fixnum_compareTo },
  { "floor/0", identity },
  { "floorDivide/1", fixnum_floorDivide },
  { "gcd/1", fixnum_gcd },
  { "getLowestSetBit/0", fixnum_getLowestSetBit },
  { "isNaN/0", fixnum_isNaN },
  { "isZero/0", fixnum_isZero },
  { "max/1", fixnum_max },
  { "min/1", fixnum_min },
  { "mod/1", fixnum_mod },
  { "modInverse/1", fixnum_modInverse },
  { "modPow/2", fixnum_modPow },
  { "multiply/1", fixnum_multiply },
  { "negate/0", fixnum_negate },
  { "next/0", fixnum_next },
  { "not/0", fixnum_not },
  { "or/1", fixnum_or },
  { "pow/1", fixnum_pow },
  { "previous/0", fixnum_previous },
  { "remainder/1", fixnum_remainder },
  { "round/0", identity },
  { "shiftLeft/1", fixnum_shiftLeft },
  { "shiftRight/1", fixnum_shiftRight },
  { "signum/0", fixnum_signum },
  { "subtract/1", fixnum_subtract },
  { "toByteArray/0", fixnum_toByteArray },
  { "toString/1", fixnum_toString },
  { "toString64/0", fixnum_toString64 },
  { "truncDivide/1", fixnum_truncDivide },
  { "truncate/0", identity },
  { "xor/1", fixnum_xor },
  { "__printOn/1", fixnum_printOn },
  {NULL}
};
e_Script e__fixnum_script;
//@}

/// @ingroup except
//@{
static e_Script problem_script;
e_Ref e_empty_ref = {NULL, {0}};
static e_Ref problem_printOn(e_Ref self, e_Ref *args) {
  e_Ref out = args[0];
  E_ERROR_CHECK(e_print(out, e_make_string("<problem ")));
  E_ERROR_CHECK(e_print(out, self.data.refs[0]));
  E_ERROR_CHECK(e_print(out, e_make_string(": ")));
  E_ERROR_CHECK(e_print_on(self.data.refs[1], out));
  E_ERROR_CHECK(e_print(out, e_make_string(">")));
  return e_null;
}

static e_Method problem_methods[] = {
  { "__printOn/1", problem_printOn },
  {NULL}
};

e_Ref e_make_problem(const char *complaint, e_Ref irritant) {
  e_Ref result, *data = e_malloc(2 * sizeof data[0]);
  data[0] = e_make_string(complaint);
  data[1] = irritant;
  result.script = &problem_script;
  result.data.refs = data;
  return result;
}

void e_ejector_disable(e_Ref self) {
  self.data.refs[0] = e_empty_ref;
}

/// Perform a non-local exit to the escape block that created this
/// ejector.
e_Ref ejector_run(e_Ref self, e_Ref *args) {
  e_Ref ej;
    if (self.data.refs[0].data.fixnum == 0) {
      return e_throw_cstring("Failed: ejector must be enabled");
    }
  e_ejected_value = args[0];
  ej.script = NULL;
  ej.data.fixnum = self.data.refs[0].data.fixnum;
  return ej;
}

/// Run this ejector with no argument (and thus use 'null' as the ejected value).
static e_Ref ejector_run0(e_Ref self, e_Ref *args) {
  return ejector_run(self, &e_null);
}

/// Test whether this ejector is enabled or not.
static e_Ref ejector_isEnabled(e_Ref self, e_Ref *args) {
  return e_make_boolean(!e_same(self.data.refs[0], e_empty_ref));
}

static e_Ref ejector_disable(e_Ref self, e_Ref *args) {
  self.data.refs[0] = e_empty_ref;
  return e_null;
}

static e_Method ejector_methods[] = {
  {"run/0", ejector_run0},
  {"run/1", ejector_run},
  {"disable/0", ejector_disable},
  {"isEnabled/0", ejector_isEnabled},
  {NULL}
};

e_Script e__ejector_script;

/// Create an ejector object.
/** Ejectors are E objects with 'run' methods that unwind the stack to the
    escape expression that creates them. */
e_Ref e_make_ejector() {
  e_Ref ej;
  ej.script = &e__ejector_script;
  ej.data.refs = e_malloc(sizeof(e_Ref));
  ej.data.refs[0].script = NULL;
  ej.data.refs[0].data.fixnum = e_ejector_counter++;
  if (e_ejector_counter <= 0) {
    printf("WARNING: ejector counter rollover!\n");
    e_ejector_counter = 1;
  }
  return ej;
}

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
e_Script e__flexmap_script;
e_Script e__constmap_script;

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

static e_Ref flexmap_getvalues(e_Ref self, e_Ref *args);
static e_Ref flexmap_getkeys(e_Ref self, e_Ref *args);

static e_Ref flexmap_iterate(e_Ref self, e_Ref *args) {
    Flexmap_data *map = self.data.other;
    for (int i = 0; i < map->size; i++) {
      e_Ref res = e_call_2(args[0], &run2, map->keys[i],
                           map->values[i]);
      E_ERROR_CHECK(res);
    }
    return e_null;
}

static e_Method flexmap_methods[] = {
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

e_Ref e_make_constmap(int initial_size) {
  e_Ref result = e_make_flexmap(initial_size);
  result.script = &e__constmap_script;
  return result;
}

static e_Method constmap_methods[] = {
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
static void flexlist_setSize(e_Ref self, int newSize) {
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
  int index;
  GET_FIXNUM_VALUE(index, args[0]);
  return flexlist_put(self, index, args[1]);
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


e_Script e__constset_script;
static e_Method constset_methods[] = {
  {"__printOn/1", constset_printOn},
  {"size/0", flexlist_size},
  {"getElements/0", flexlist_snapshot},
  {"with/1", constset_with},
  {"iterate/1", flexlist_iterate},
  {NULL}};

e_Script e__flexset_script;
static e_Method flexset_methods[] = {
  {"__printOn/1", flexset_printOn},
  {"size/0", flexlist_size},
  {"getElements/0", flexlist_snapshot},
  {"with/1", constset_with},
  {"iterate/1", flexlist_iterate},
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
  e_make_selector(&op__cmp, "op__cmp", 1);

  e_make_script(&e__null_script, NULL, null_methods, "void");
  e_make_script(&e__boolean_script, NULL, boolean_methods, "Boolean");
  e_make_script(&e__char_script, NULL, char_methods, "char");
  e_make_script(&e__string_script, NULL, string_methods, "String");
  e_make_script(&e__fixnum_script, NULL, fixnum_methods, "int");
  e_make_script(&e__bignum_script, NULL, bignum_methods, "bigint");
  e_make_script(&e__float64_script, NULL, float64_methods, "float64");
  e_make_script(&e__writer_script, NULL, writer_methods, "writer");
  e_make_script(&e__reader_script, NULL, no_methods, "reader");
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
static void do_nothing_free2(void *ptr) {}
#ifndef NO_GC
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
