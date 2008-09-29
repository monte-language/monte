/* Copyright 2003 Darius Bacon under the terms of the MIT X license
   found at http://www.opensource.org/licenses/mit-license.html */

#include <errno.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "elib.h"
#include "elib_private.h"

GStaticPrivate e_thrown_problem_key = G_STATIC_PRIVATE_INIT;
GStaticPrivate e_ejected_value_key = G_STATIC_PRIVATE_INIT;
GStaticPrivate e_ejector_counter_key = G_STATIC_PRIVATE_INIT;

e_Selector respondsTo, order, whenBroken, whenMoreResolved, run1,
           optSealedDispatch, conformTo, printOn, optUncall,
           getAllegedType, reactToLostClient, E_AUDITED_BY;

/// Get the last thrown problem in the current thread.
e_Ref e_thrown_problem() {
  e_Ref *prob = g_static_private_get(&e_thrown_problem_key);
  return *prob;
}

/// Get the last ejected value in the current thread.
e_Ref e_ejected_value() {
  e_Ref *val =  g_static_private_get(&e_ejected_value_key);
  return *val;
}

/// Get the number for the most recent ejection in the current thread.
int e_ejector_counter() {
  int *counter = g_static_private_get(&e_ejector_counter_key);
  return *counter;
}

/// Set the problem currently being thrown in this thread.
void e_thrown_problem_set(e_Ref problem) {
  e_Ref *prob = g_static_private_get(&e_thrown_problem_key);
  *prob = problem;
}

/// Set the value currently being ejected in this thread.
void e_ejected_value_set(e_Ref value) {
  e_Ref *val = g_static_private_get(&e_ejected_value_key);
  *val = value;
}

/// Proceed to the next ejector number.
int e_ejector_counter_increment() {
  int *counter = g_static_private_get(&e_ejector_counter_key);
  *counter = *counter + 1;
  return *counter;
}

/// Complain and halt the process. Only for use from top-level driver.
void e_die(e_Ref problem) {
  e_print(e_stderr, e_make_string("Unhandled exception: "));
  e_print_on(problem, e_stderr);
  e_print(e_stderr, e_make_string ("\n"));
  exit (1);
}

/* Throw a problem. */
e_Ref e_throw(e_Ref problem) {
  e_thrown_problem_set(problem);
  return e_empty_ref;
}

e_Ref e_throw_pair(const char *complaint, e_Ref irritant) {
  return e_throw(e_make_problem(complaint, irritant));
}

e_Ref e_throw_cstring(const char *cstring) {
  return e_throw(e_make_string(cstring));
}

/// Creates a problem object from the complaint and irritant. If
/// optEjector is null, it is thrown. Otherwise optEjector is invoked
/// with it.
e_Ref e_ejectOrThrow(e_Ref optEjector, const char *complaint, e_Ref irritant) {

  e_Ref problem = e_make_problem(complaint, irritant);
  return e_ejectOrThrow_problem(optEjector, problem);
}

e_Ref e_ejectOrThrow_problem(e_Ref optEjector, e_Ref problem) {
  if (e_is_null(optEjector)) {
    return e_throw(problem);
  }
  e_Ref val = e_call_1(optEjector, &run1, problem);
  E_ERROR_CHECK(val);
  return e_throw_pair("optEjector returned:", e_null);//XXX printOn for ejectors
}

//@}
/// @ingroup misc
const char *
e_cstring_copy (const char *string)
{
  char *result = e_malloc_atomic(strlen(string) + 1);
  strcpy(result, string);
  return result;
}
/// @ingroup except
void
e_throw_errno (void)
{
  e_throw_cstring(e_cstring_copy(strerror(errno)));
}
/// @ingroup misc
void *
e_malloc_atomic (size_t size)
{
#ifdef NO_GC
  void *p = malloc(size);
#else
  void *p = GC_MALLOC(size);
#endif
  if (NULL == p && 0 != size)
    e_throw_errno ();
  return p;
}
/// @ingroup misc
void * e_malloc (size_t size) {
#ifdef NO_GC
  void *p = malloc(size);
#else
  void *p = GC_MALLOC (size);
#endif
  if (NULL == p && 0 != size)
    e_throw_errno ();
  return p;
}

e_Ref *e_make_array(int size) {
  e_Ref *result = e_malloc(size * sizeof result[0]);
  int i;
  for (i = 0; i < size; ++i)
    result[i] = e_null;
  return result;
}


/// @addtogroup messages
//@{
e_Ref e_call(e_Ref receiver, e_Selector *selector, e_Ref *args) {
  e_Script *script = receiver.script;

  /*
  if (strcmp(selector->verb, "__printOn/1") != 0 && (receiver.script != &e__writer_script)) {
    e_print(e_stderr, e_make_gstring(receiver.script->typeName));
    e_print(e_stderr, e_make_string("  "));
    e_print(e_stderr, e_make_string(selector->verb));
    e_print(e_stderr, e_make_string("("));
    if (selector->arity > 0) {
      for (int i = 0; i < selector->arity-1; i++) {
        e_print(e_stderr, args[i]);
        e_print(e_stderr, e_make_string(", "));
      }
      e_print(e_stderr, args[selector->arity-1]);
    }
    e_println(e_stderr, e_make_string(")"));
  }
  */
  for (int i = 0; i < script->num_methods; ++i) {
    if (script->methods[i].verb == selector->verb) {
      return script->methods[i].exec_func (receiver, args);
    }
  }
  e_Ref val = script->opt_otherwise (receiver, selector, args);
  return val;
}

static e_Ref miranda_respondsTo(e_Ref self, e_Ref *args) {
  e_Script *script = self.script;
  e_Ref str = e_coerce(e_StringGuard, args[0], e_null);
  E_ERROR_CHECK(str);
  e_Ref ar = e_coerce(e_IntGuard, args[1], e_null);
  E_ERROR_CHECK(ar);
  int arity = ar.data.fixnum;
  GString *original = str.data.other;
  GString *g_candidate = g_string_new(original->str);
  g_string_append_printf(g_candidate, "/%d", arity);
  const char *candidate = e_intern_find(g_candidate->str);
  if (candidate == NULL) {
    return e_false;
  }
  for (int i = 0; i < script->num_methods; i++) {
    if (script->methods[i].verb == candidate) {
      return e_true;
    }
  }
  for (int i = 0; i < E_NUM_MIRANDA_METHODS; i++) {
    e_Method *method = e_miranda_methods + i;
    if (method->verb == candidate) {
      return e_true;
    }
  }
  return e_false;
}

static e_Ref miranda_order(e_Ref self, e_Ref *args) {
  e_Ref str = e_coerce(e_StringGuard, args[0], e_null);
  E_ERROR_CHECK(str);
  e_Ref arglist = e_coerce(e_ListGuard, args[1], e_null);
  E_ERROR_CHECK(arglist);
  e_Selector sel;
  Flexlist_data *list = arglist.data.other;
  e_make_selector(&sel, str.data.gstring->str, list->size);
  e_Ref res = e_call(self, &sel, list->elements);
  E_ERROR_CHECK(res);
  e_Ref items[] = {res, self};
  return e_constlist_from_array(2, items);
}

static e_Ref miranda_no_op(e_Ref self, e_Ref *args) {
  return e_null;
}

static e_Ref miranda_conformTo(e_Ref self, e_Ref *args) {
  return self;
}

/// The default implementation of '__optUncall'.
static e_Ref miranda_optUncall(e_Ref self, e_Ref *args) {
  return e_null;
}

static e_Ref miranda_printOn(e_Ref self, e_Ref *args) {
  E_ERROR_CHECK(e_print(args[0], e_make_string("<a ")));
  E_ERROR_CHECK(e_print(args[0], e_make_string(self.script->typeName->str)));
  return e_print(args[0], e_make_string(">"));
}

static e_Ref miranda_whenMoreResolved(e_Ref self, e_Ref *args) {
  e_Ref *sendargs = e_malloc(sizeof *sendargs);
  *sendargs = self;
  e_vat_sendOnly(e_current_vat(), args[0], &run1, sendargs);
  return e_null;
}

/** The default implementation of auditor approval checking. This method cannot
    be called from E, but is only invoked by Ecru internals. */
static e_Ref miranda_auditedBy(e_Ref self, e_Ref *args) {
  GArray *approvals = self.script->optApprovals;
  if (approvals == NULL) {
    return e_false;
  } else {
    e_Ref stamp = e_ref_target(args[0]);
    for (int i = 0; i < approvals->len; i++) {
      if (e_same(stamp, g_array_index(approvals, e_Ref, i))) {
          return e_true;
      }
    }
    return e_false;
  }
}

/* Remember that when you add miranda methods you have to change
   E_NUM_MIRANDA_METHODS. */
e_Method e_miranda_methods[] = {
  {"__respondsTo/2", miranda_respondsTo},
  {"__order/2", miranda_order},
  {"__whenBroken/1", miranda_no_op},
  {"__reactToLostClient/1", miranda_no_op},
  {"__optSealedDispatch/2", miranda_no_op},
  {"__optUncall/0", miranda_optUncall},
  {"__conformTo/1", miranda_conformTo},
  {"__printOn/1", miranda_printOn},
  {"__whenMoreResolved/1", miranda_whenMoreResolved},
  {"audited-by-magic-verb", miranda_auditedBy},
  {NULL}};

/** Default behavior for an object with no 'otherwise' call func specified. */
e_Ref otherwise_miranda_methods(e_Ref receiver, e_Selector *selector,
                                e_Ref *args) {
  for (int i = 0; i < E_NUM_MIRANDA_METHODS; i++) {
    e_Method *method = e_miranda_methods + i;
    if (method->verb == selector->verb) {
      return method->exec_func (receiver, args);
    }
  }
  e_Ref memWriter = e_make_string_writer();
  e_quote_print(memWriter, receiver);
  e_Ref methodDesc =  e_string_writer_get_string(memWriter);
  g_string_append_c(methodDesc.data.gstring, '.');
  g_string_append(methodDesc.data.gstring, selector->verb);
  return e_throw_pair ("Unknown method", methodDesc);
}
//@}
/// @ingroup object
void e_make_script (e_Script *script, e_Call_Func *opt_otherwise,
                    e_Method *methods, e_Ref *optApprovals,
                    const char *typeName) {
  int i;
  for (i = 0; NULL != methods[i].verb; ++i)
    methods[i].verb = e_intern (methods[i].verb);
  script->num_methods = i;
  script->methods = methods;
  script->opt_otherwise =
    (NULL == opt_otherwise ? otherwise_miranda_methods : opt_otherwise);
  script->typeName = g_string_new(typeName);
  script->optApprovals = NULL;
  if (optApprovals != NULL) {
    script->optApprovals = g_array_new(false, false, sizeof(e_Ref));
    for (int i = 0; NULL != optApprovals[i].script; ++i) {
      g_array_append_val(script->optApprovals, optApprovals[i]);
    }
  }
}

/// Returns whether an auditor has approved an object's script or not.
_Bool e_approved_by(e_Ref specimen, e_Ref auditor) {
  return e_eq(e_true, e_call_1(specimen, &E_AUDITED_BY, auditor));
}

/// @addtogroup messages
//@{
const char *
e_mangle (const char *verb, int arity)
{
  // this is 22 because 2**64 in decimal is a string of 20 characters.
  char *mangled, buffer[22];
  sprintf (buffer, "%d", arity);
  mangled = e_malloc_atomic (strlen (verb) + 1 + strlen (buffer) + 1);
  sprintf (mangled, "%s/%d", verb, arity);
  return e_intern (mangled);
}

void
e_make_selector (e_Selector *selector, const char *verb, int arity)
{
  selector->verb = e_mangle (verb, arity);
  selector->arity = arity;
}
/// Get the verb from this selector as an E string.
e_Ref e_selector_verb(e_Selector *selector) {
  int nameLength = strstr(selector->verb, "/") - selector->verb;
  return e_make_gstring(g_string_new_len(selector->verb, nameLength));
}
//@}

void e__miranda_set_up() {
  E_AUDITED_BY.verb = e_intern("audited-by-magic-verb");
  E_AUDITED_BY.arity = 1;
  e_make_selector(&respondsTo, "__respondsTo", 2);
  e_make_selector(&order, "__order", 2);
  e_make_selector(&whenBroken, "__whenBroken", 1);
  e_make_selector(&reactToLostClient, "__reactToLostClient", 1);
  e_make_selector(&optSealedDispatch, "__optSealedDispatch", 1);
  e_make_selector(&conformTo, "__conformTo", 1);
  e_make_selector(&printOn, "__printOn", 1);
  e_make_selector(&whenMoreResolved, "__whenMoreResolved", 1);
  e_make_selector(&run1, "run", 1);
  e_make_selector(&getAllegedType, "__getAllegedType", 0);
  e_make_selector(&optUncall, "__optUncall", 0);
  for (int i = 0; i < E_NUM_MIRANDA_METHODS; i++) {
    e_miranda_methods[i].verb = e_intern(e_miranda_methods[i].verb);
  }
}

void e__exit_set_up() {
  e_Ref *problem = e_malloc(sizeof *problem);
  e_Ref *value = e_malloc(sizeof *value);
  int *counter = e_malloc(sizeof *counter);
  g_static_private_set(&e_thrown_problem_key, problem, NULL);
  g_static_private_set(&e_ejected_value_key, value, NULL);
  g_static_private_set(&e_ejector_counter_key, counter, NULL);
  e_thrown_problem(e_empty_ref);
  e_ejected_value_set(e_empty_ref);
  *counter = 1;
}
