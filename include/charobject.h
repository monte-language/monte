#ifndef ECRU_CHAR_H
#define ECRU_CHAR_H
extern e_Script e__char_script;
extern e_Method char_methods[];

e_def_type_predicate (e_is_char, e__char_script);

static inline e_Ref e_make_char(unsigned short chr) {
  e_Ref ref;
  ref.script = &e__char_script;
  // pacify valgrind - eq compares fixnums
  ref.data.fixnum = 0;
  ref.data.chr = chr;
  return ref;
}

#endif
