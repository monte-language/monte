/* Copyright 2003 Darius Bacon under the terms of the MIT X license
   found at http://www.opensource.org/licenses/mit-license.html */

#ifndef ELIB_H
#define ELIB_H

#include <config.h>

#include <gc/gc.h>
#include <stdarg.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <setjmp.h>
#include <gmp.h>
#include <glib.h>

#if OLD_GIO
#include <gio/ginputstream.h>
#include <gio/goutputstream.h>
#else
#include <gio/gio.h>
#endif

#include "null.h"

/// @defgroup misc Miscellaneous
//@{
/** Initialize the E system. */
/**  Must be called before any other e_foo()
     functions. */
void e_set_up (void);


/** Allocate space on the GC'd heap. */
void *  e_malloc (size_t size);
/** Allocate space on the GC'd heap for an object that will have no
   pointers (useful for efficiency -- this tells the GC it won't have
   to trace it). */
void * e_malloc_atomic (size_t size);

/** Return a heap-allocated copy of a C string. */
const char *e_cstring_copy (const char *string);
//@}

/// @defgroup objects Objects
//@{
typedef union e_Data e_Data;
typedef struct e_Method e_Method;
typedef struct e_Ref e_Ref;
typedef struct e_Script e_Script;
typedef struct e_Selector e_Selector;

/** The possible types of state held by a ref.  Each must fit in a single
   machine word -- if bigger than that, or shared, use a pointer. */
union e_Data {
  long fixnum;			/**< small integer */
  mpz_t *bignum;
  unsigned short chr;
  GString *gstring;
  double *float64;
  e_Ref *refs;			/**< an array, size determined by the script */
  void *other;			/**< anything else */
};


/** A ref is a reference to an E object, represented by a fat pointer:
   the first part, the script, determines the object's behavior, while
   the second part determines its state, as interpreted by the
   script.

   In general, we may assume that everything a ref points to
   (transitively) has indefinite extent except where otherwise
   indicated.  Indefinite extent means it's stored statically or in
   the GCed heap, not on the stack. */
struct e_Ref {
  e_Script *script;
  e_Data data;
};

/** An exec func is the C code underlying a method.  'args' is an array
   of arguments of length equal to the method's arity.  The array may
   be allocated on the stack rather than the heap, so you must assume
   it may be of unchecked dynamic extent.  (But each individual arg is
   an ordinary garbage-collected ref.) */
typedef e_Ref e_Exec_Func (e_Ref self, e_Ref *args);

/** The C code handling a call. */
typedef e_Ref e_Call_Func (e_Ref self, e_Selector *selector, e_Ref *args);

/** The behavior of a ref. */
struct e_Script {
  int num_methods;
  e_Method *methods;		/**< an array of length num_methods */
  e_Call_Func *opt_otherwise;
  GString *typeName;
  /** TODO: add a send function, etc?  check the enative code */
};

/** A method bundles a mangled and interned verb with its behavior.
    Mangled: for example, "add/1" for a method called like foo.add(bar).
    The "/1" part gives its arity (that is, the number of parameters).
    Interned: uniquified by e_intern(), and so may be compared with ==.

    For our purposes at the moment we don't care about the string
    encoding -- we just treat it as a byte array.  But we'll want to
    nail it down later to use UTF8 or something.

    Note that we can't represent a verb with a null character inside it
    -- could that be a problem? */
struct e_Method {
  const char *verb;
  e_Exec_Func *exec_func;
};

/** For use with scripts with no methods. */
extern e_Method no_methods[];

//@}
/** @defgroup messages Messages
    A selector is the type of a message in a call or a send. */
struct e_Selector {
  const char *verb;
  int arity;			/**< Redundantly held for convenience */
  /** TODO: enative has stuff here for call-site caching, etc. */
};


/** @ingroup objects
    Initialize *script.
   'methods' is a an array terminated by an entry with a verb of NULL.
   In initializing, we intern the verbs in place. */
void e_make_script (e_Script *script,
		    e_Call_Func *opt_otherwise,
		    e_Method *methods,
                    const char *typeName);

/** @ingroup objects
    The default implementation of the Miranda methods. If you create a script
    with an "opt_otherwise" function, you must call this from it on any
    selectors you do not implement. */
e_Ref otherwise_miranda_methods(e_Ref self, e_Selector *selector, e_Ref *args);

/// The array of default Miranda method implementations.
extern e_Method e_miranda_methods[];
#define E_NUM_MIRANDA_METHODS 7

/** @ingroup messages
    Return 'verb' as mangled and interned according to 'arity'. */
const char *e_mangle (const char *verb, int arity);

//// @ingroup except
//@{
extern e_Script e__ejector_script;
/** Return a new problem. */
e_Ref e_make_problem (const char *complaint, e_Ref irritant);

/** Throw a problem.  'complaint' must have indefinite extent. */
e_Ref e_throw_pair (const char *complaint, e_Ref irritant);

/** Throw 'cstring' as a problem, converting it into an E string. */
e_Ref e_throw_cstring (const char *cstring);

/** Throw an error according to the last C library error code in errno. */
void e_throw_errno (void);

/// XXX does this clobber the docstring in prim.c
e_Ref e_make_ejector();
e_Ref ejector_run(e_Ref self, e_Ref *args);

/// Disable an ejector object.
void e_ejector_disable(e_Ref self);

e_Ref e_ejectOrThrow(e_Ref optEjector, const char *complaint, e_Ref irritant);
e_Ref e_ejectOrThrow_problem(e_Ref optEjector, e_Ref problem);

/// The thrower object. Bound as 'throw' in the universal scope.
extern e_Ref e_thrower;

//@}

/// @ingroup messages
//@{
/** Perform a call. */
e_Ref e_call (e_Ref receiver, e_Selector *selector, e_Ref *args);

/** Make a selector. */
void e_make_selector (e_Selector *selector, const char *verb, int arity);

/** Get the verb of a selector as a string. */
e_Ref e_selector_verb(e_Selector *selector);

/** Perform a call with no arguments.
   Pre: selector has arity 0 */
static inline e_Ref
e_call_0 (e_Ref receiver, e_Selector *selector)
{
  return e_call (receiver, selector, NULL);
}

/** Pre: selector has arity 1 */
static inline e_Ref
e_call_1 (e_Ref receiver, e_Selector *selector, e_Ref arg1)
{
  e_Ref args[] = { arg1 };
  return e_call (receiver, selector, args);
}

/** Pre: selector has arity 2 */
static inline e_Ref
e_call_2 (e_Ref receiver, e_Selector *selector, e_Ref arg1, e_Ref arg2)
{
  e_Ref args[] = { arg1, arg2 };
  return e_call (receiver, selector, args);
}

//@}


/** @defgroup types Builtin types
 Various types of objects.
   We'll need to revisit a lot of them -- we're kind of hacking them
   up just to get something working, not really making a serious ELib
   here. */
//@{
#define e_def_type_predicate(pred_name, script_name) \
  static int                      \
  pred_name (e_Ref ref)                  \
  {                                      \
    return &(script_name) == ref.script; \
  }
e_def_type_predicate(e_is_ejector, e__ejector_script);

/* TODO: similar macro for constructors */
/* TODO: similar macro for immediate-value extractors (char_value etc.) */

/** @defgroup null The null object */
//@{
extern e_Script e__null_script;

extern e_Ref e_null;

e_def_type_predicate (e_is_null, e__null_script);

//@}


/** @defgroup bools Booleans */
//@{

extern e_Script e__boolean_script;

extern e_Ref e_true, e_false;

e_def_type_predicate (e_is_boolean, e__boolean_script);

static inline e_Ref
e_make_boolean (int flag)
{
  return flag ? e_true : e_false;
}
//@}


/** @defgroup file Files */
//@{
extern e_Ref e_stdin;
extern e_Ref e_stdout;
extern e_Ref e_stderr;

extern e_Script e__writer_script;
extern e_Script e__reader_script;

e_Ref e_make_writer(GOutputStream *stream);

static inline e_Ref e_make_reader(GInputStream *stream) {
  e_Ref ref;
  ref.script = &e__reader_script;
  ref.data.other = stream;
  return ref;
}

e_Ref e_make_string_writer();
e_Ref e_string_writer_get_string(e_Ref writer);

//@}

/** @defgroup cstring Strings */
//@{
extern e_Script e__string_script;

e_def_type_predicate (e_is_string, e__string_script);

/** @pre 'cstring' is immutable and of indefinite extent. */
static inline e_Ref
e_make_string (const char *cstring) {
  e_Ref ref;
  ref.script = &e__string_script;
  ref.data.gstring = g_string_new(cstring);
  return ref;
}
/** @pre 'gstring' is immutable and of indefinite extent. */
static inline e_Ref e_make_gstring (GString *gstring) {
  e_Ref ref;
  ref.script = &e__string_script;
  ref.data.gstring = gstring;
  return ref;
}

//@}

/** @defgroup char Characters */
//@{
extern e_Script e__char_script;

e_def_type_predicate (e_is_char, e__char_script);

static inline e_Ref
e_make_char (unsigned short chr)
{
  e_Ref ref;
  ref.script = &e__char_script;
  // pacify valgrind - eq compares fixnums
  ref.data.fixnum = 0;
  ref.data.chr = chr;
  return ref;
}
//@}

/** @defgroup fixnum Small integers */
//@{
extern e_Script e__fixnum_script;

e_def_type_predicate (e_is_fixnum, e__fixnum_script);

static inline e_Ref
e_make_fixnum (int fixnum)
{
  e_Ref ref;
  ref.script = &e__fixnum_script;
  ref.data.fixnum = fixnum;
  return ref;
}
//@}

/// Return whether the specimen is of a primitive integral type.
char e_is_integer(e_Ref specimen);

/** @defgroup bignum Big integers */
//@{
extern e_Script e__bignum_script;

e_def_type_predicate (e_is_bignum, e__bignum_script);

static inline e_Ref
e_make_bignum (mpz_t *bignum)
{
  e_Ref ref;
  ref.script = &e__bignum_script;
  ref.data.bignum = bignum;
  return ref;
}

e_Ref e_bignum_as_float64(e_Ref big);
e_Ref e_bignum_from_fixnum(int a);
//@}


/** @defgroup float64 Float64 */
//@{
extern e_Script e__float64_script;

e_def_type_predicate (e_is_float64, e__float64_script);

static inline e_Ref
e_make_float64 (double value)
{
  e_Ref ref;
  double *p = e_malloc_atomic (sizeof *p);
  *p = value;
  ref.script = &e__float64_script;
  ref.data.float64 = p;
  return ref;
}
//@}

/** Return a new array of 'size' elements, all initially null. */
e_Ref *e_make_array (int size);


/** @defgroup Map Maps */
//@{
e_Ref e_make_flexmap (int initial_size);
e_Ref e_make_constmap (int initial_size);

/// XXX arguably these should be not be public.
e_Ref e_flexmap_put(e_Ref self, e_Ref *args);
e_Ref e_flexmap_removeKey(e_Ref self, e_Ref *args);

typedef struct Flexmap_data {
  int size;		 /**< count of associations elements can hold, > 0 */
  int occupancy;		/**< count of associations stored */
  e_Ref *keys;
  e_Ref *values;
} Flexmap_data;

extern e_Script e__flexmap_script;
extern e_Script e__constmap_script;
/// The safe-scope object bound to '__makeMap'.
extern e_Ref e_makeMap;

e_def_type_predicate (e_is_flexmap, e__flexmap_script);
e_def_type_predicate (e_is_constmap, e__constmap_script);
//@}


/// @defgroup list Lists
//@{

e_Ref e_constlist_from_array(int size, e_Ref* contents);
e_Ref e_flexlist_from_array(int size, e_Ref* contents);

extern e_Script e__constlist_script;
extern e_Script e__flexlist_script;

/// XXX probably shouldn't be public
e_Ref flexlist_snapshot(e_Ref self, e_Ref *args);
e_Ref flexlist_size(e_Ref self, e_Ref *args);

typedef struct Flexlist_data {
  int size;
  int capacity;
  e_Ref elementGuard;
  e_Ref *elements;
} Flexlist_data;

e_def_type_predicate(e_is_constlist, e__constlist_script);
e_def_type_predicate(e_is_flexlist, e__flexlist_script);

/// The safe-scope object bound to '__makeList'.
extern e_Ref e_makeList;
//@}

/// @defgroup set Sets
//@{

/// Create an immutable set object with the given contents.
e_Ref e_constset_from_array(int size, e_Ref* contents);

extern e_Script e__constset_script;
extern e_Script e__flexset_script;
e_def_type_predicate(e_is_constset, e__constset_script);
//@}

/// @defgroup slot Slots
//@{

e_Ref e_make_finalslot(e_Ref value);
extern e_Script e__finalslot_script;

e_def_type_predicate (e_is_finalslot, e__finalslot_script);

e_Ref e_make_varslot(e_Ref value);
extern e_Script e__varslot_script;

e_def_type_predicate (e_is_varslot, e__varslot_script);

//@}
//@}

/// @defgroup Guards
//@{
extern e_Ref e_IntGuard;
extern e_Ref e_Float64Guard;
extern e_Ref e_CharGuard;
extern e_Ref e_StringGuard;
extern e_Ref e_BooleanGuard;
extern e_Ref e_EListGuard;

extern e_Script e__guardedslot_script;
e_Ref e_new_guardedslot(e_Ref value, e_Ref guard, e_Ref optEjector);
e_def_type_predicate(e_is_guardedslot, e__guardedslot_script);
char e_is_slot(e_Ref specimen);

/// Coerce method on BooleanGuard. Declared here because it's useful
/// on its own.
e_Ref booleanguard_coerce(e_Ref self, e_Ref *args);
/// Coercer to a primitive list.
e_Ref elistguard_coerce(e_Ref self, e_Ref *args);

/// Coercer to an integer.
e_Ref intguard_coerce(e_Ref self, e_Ref *args);

/// Coercer to a float.
e_Ref float64guard_coerce(e_Ref self, e_Ref *args);

/// Coercer to a string.
e_Ref stringguard_coerce(e_Ref self, e_Ref *args);

//@}

/// @ingroup file
/// @defgroup print Printing

//@{
extern e_Selector e_do_printOn;
extern e_Selector e_do_print;
extern e_Selector e_do_quote_print;
extern e_Selector e_do_println;

static inline e_Ref
e_print (e_Ref out, e_Ref ref)
{
  return e_call_1 (out, &e_do_print, ref);
}

static inline e_Ref
e_println (e_Ref out, e_Ref ref)
{
  return e_call_1 (out, &e_do_println, ref);
}

static inline e_Ref
e_print_on (e_Ref ref, e_Ref out)
{
  return e_call_1 (ref, &e_do_printOn, out);
}

static inline e_Ref
e_quote_print (e_Ref out, e_Ref ref)
{
  return e_call_1 (out, &e_do_quote_print, ref);
}

//@}

/** @ingroup misc
    @brief Interning uniquifies C strings.

    Return the string's unique representative.  'string' must be
    immutable and of indefinite extent, because it might end up as the
    representative.  Thus you must treat the return value the same
    way. */
const char *e_intern(const char *string);

/** Return the string's unique representative if it has been interned already.
    Otherwise returns NULL. */
const char *e_intern_find(const char *string);

/// @ingroup scopes
/// @{

extern e_Script e__scope_script;
extern e_Script e__scopeLayout_script;

e_def_type_predicate(e_is_scopeLayout, e__scopeLayout_script);
e_def_type_predicate(e_is_scope, e__scope_script);

/// Get the array of objects in this scope.
e_Ref *e_scope_getEvalContext(e_Ref self);

/// Get the number of mappings in this scope.
int e_scope_getSize(e_Ref self);

/// Create a new scope object from an array of names and an array of slots.
e_Ref e_make_scope(char **names, e_Ref *slots, int size);

/// @}

/// @ingroup objects
/// @{

/// Compares E references for pointer equality.
static inline _Bool e_eq(e_Ref ref1, e_Ref ref2) {
  return ref1.script == ref2.script &&
    ref1.data.fixnum == ref2.data.fixnum;
}

/// Compares E references for equality of primitive types, or pointer equality. 
_Bool e_same(e_Ref ref1, e_Ref ref2);

/// The safe-scope object for performing equality comparisons.
extern e_Ref e_equalizer;

/// The safe-scope object for performing comparisons.
extern e_Ref e_comparer;

/// The safe-scope object for 'while' loops.
extern e_Ref e_looper;

/// The safe-scope object 'require'.
extern e_Ref e_require;

/// The safe-scope object for created ordered spaces (used by the `..' operator)
extern e_Ref e_makeOrderedSpace;

/// The safe-scope object '__Test'.
extern e_Ref e__Test;

/// The safe-scope object '__bind'.
extern e_Ref e__bind;

/// The safe-scope object '__is'.
extern e_Ref e__is;

/// The safe-scope object '__makeVerbFacet'.
extern e_Ref e__makeVerbFacet;

/// The safe-scope object '__suchThat'.
extern e_Ref e__suchThat;

/// The safe-scope object 'simple__quasiParser'.
extern e_Ref e_simple__quasiParser;

/// The safe-scope object 'import__uriGetter'.
extern e_Ref e_import__uriGetter;

/// The safe-scope object 'E'.
extern e_Ref THE_E;

/// The safe-scope object 'traceln'.
extern e_Ref e_traceln;

/// The privileged-scope object 'timer'.
extern e_Ref e_timer;

/// The privileged-scope object 'print'.
extern e_Ref e_print_object;

/// The privileged-scope object 'println'.
extern e_Ref e_println_object;


/// The scope in which code with no capabilities is evaluated.
extern e_Ref e_safeScope;

/// The default top-level scope for non-interactive code.
extern e_Ref e_privilegedScope;


e_Ref e_module_import(GString *module_name);

///@}
/// @defgroup except Exception handling

extern /* TLS */ e_Ref e_thrown_problem;
extern /* TLS */ e_Ref e_ejected_value;
extern /* TLS */ int e_ejector_counter;

extern e_Ref e_empty_ref;

/** Throw a problem. */
e_Ref e_throw(e_Ref problem);

/// Halt the process and print a problem.
void e_die(e_Ref problem);

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

//@}

#endif /* ELIB_H */
