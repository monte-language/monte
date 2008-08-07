#ifndef ECRU_NUMBER_H
#define ECRU_NUMBER_H


extern e_Script e__fixnum_script;
extern e_Method fixnum_methods[];
extern e_Script e__bignum_script;
extern e_Method bignum_methods[];
extern e_Script e__float64_script;
extern e_Method float64_methods[];


e_def_type_predicate (e_is_fixnum, e__fixnum_script);
e_def_type_predicate (e_is_bignum, e__bignum_script);
e_def_type_predicate (e_is_float64, e__float64_script);

static inline e_Ref e_make_fixnum (int fixnum) {
  e_Ref ref;
  ref.script = &e__fixnum_script;
  ref.data.fixnum = fixnum;
  return ref;
}

static inline e_Ref e_make_bignum (mpz_t *bignum) {
  e_Ref ref;
  ref.script = &e__bignum_script;
  ref.data.bignum = bignum;
  return ref;
}

static inline e_Ref e_make_float64(double value) {
  e_Ref ref;
  double *p = e_malloc_atomic(sizeof *p);
  *p = value;
  ref.script = &e__float64_script;
  ref.data.float64 = p;
  return ref;
}

/// Return whether the specimen is of a primitive integral type.
char e_is_integer(e_Ref specimen);

e_Ref e_bignum_as_float64(e_Ref big);
e_Ref e_bignum_from_fixnum(int a);

#endif
