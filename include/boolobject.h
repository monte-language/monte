#ifndef ECRU_BOOL_H
#define ECRU_BOOL_H
extern e_Script e__boolean_script;
extern e_Method boolean_methods[];
extern e_Ref e_true, e_false;

e_def_type_predicate (e_is_boolean, e__boolean_script);

static inline e_Ref e_make_boolean(int flag) {
  return flag ? e_true : e_false;
}
#endif
