#ifndef ECRU_STRING_H
#define ECRU_STRING_H
extern e_Script e__string_script;
extern e_Method string_methods[];

e_def_type_predicate (e_is_string, e__string_script);

/** @pre 'cstring' is immutable and of indefinite extent. */
static inline e_Ref e_make_string(const char *cstring) {
  e_Ref ref;
  ref.script = &e__string_script;
  ref.data.gstring = g_string_new(cstring);
  return ref;
}
/** @pre 'gstring' is immutable and of indefinite extent. */
static inline e_Ref e_make_gstring(GString *gstring) {
  e_Ref ref;
  ref.script = &e__string_script;
  ref.data.gstring = gstring;
  return ref;
}
#endif
