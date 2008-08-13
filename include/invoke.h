#ifndef ECRU_INVOKE_H
#define ECRU_INVOKE_H

/** Return a heap-allocated copy of a C string. */
const char *e_cstring_copy (const char *string);

/** Return 'verb' as mangled and interned according to 'arity'. */
const char *e_mangle (const char *verb, int arity);

/** @brief Interning uniquifies C strings.

    Return the string's unique representative.  'string' must be
    immutable and of indefinite extent, because it might end up as the
    representative.  Thus you must treat the return value the same
    way. */
const char *e_intern(const char *string);


/** Return the string's unique representative if it has been interned already.
    Otherwise returns NULL. */
const char *e_intern_find(const char *string);

/** Make a selector. */
void e_make_selector (e_Selector *selector, const char *verb, int arity);

/** Get the verb of a selector as a string. */
e_Ref e_selector_verb(e_Selector *selector);

/** Perform a call. */
e_Ref e_call (e_Ref receiver, e_Selector *selector, e_Ref *args);

/** Perform a call with no arguments.
   Pre: selector has arity 0 */
static inline e_Ref e_call_0 (e_Ref receiver, e_Selector *selector) {
  return e_call (receiver, selector, NULL);
}

/** Pre: selector has arity 1 */
static inline e_Ref e_call_1(e_Ref receiver, e_Selector *selector, e_Ref arg1) {
  e_Ref args[] = { arg1 };
  return e_call (receiver, selector, args);
}

/** Pre: selector has arity 2 */
static inline e_Ref e_call_2(e_Ref receiver, e_Selector *selector,
                             e_Ref arg1, e_Ref arg2) {
  e_Ref args[] = { arg1, arg2 };
  return e_call (receiver, selector, args);
}


extern GStaticPrivate e_thrown_problem_key;
extern GStaticPrivate e_ejected_value_key;
extern GStaticPrivate e_ejector_counter_key;

/** Throw a problem. */
e_Ref e_throw(e_Ref problem);

/// Halt the process and print a problem.
void e_die(e_Ref problem);

e_Ref e_thrown_problem();
e_Ref e_ejected_value();
int e_ejector_counter();

void e_thrown_problem_set(e_Ref problem);
void e_ejected_value_set(e_Ref value);
int e_ejector_counter_increment();

void e__exit_set_up();

#define E_ERROR_CHECK(expr)                      \
  {e_Ref _val = expr;                            \
    if (_val.script == NULL) {                   \
      return _val;                               \
    }                                            \
  }

#define e_ESCAPE(ej)                            \
  e_Ref ej = e_make_ejector();

#define e_ON_EJECTION(val, ej)                                          \
  if (val.script == NULL && val.data.fixnum == ej.data.refs[0].data.fixnum && \
      (e_ejector_disable(ej), true))


#endif
