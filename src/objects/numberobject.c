#include <math.h>
#include <string.h>
#include "elib.h"

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

e_Method float64_methods[] = {
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


/// @ingroup float64

//@}


/// @ingroup bignum
//@{

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


e_Method bignum_methods[] = {
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

static e_Ref identity(e_Ref self, e_Ref *args) {
  return self;
}

/// Return whether the specimen is of a primitive integral type.
char e_is_integer(e_Ref specimen) {
  return e_is_fixnum(specimen) || e_is_bignum(specimen);
}

e_Method fixnum_methods[] = {
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
