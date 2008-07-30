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

#include "ecruobject.h"

/** Initialize the E system. */
/**  Must be called before any other e_foo()
     functions. */
void e_set_up (void);


/** Allocate space on the GC'd heap. */
void * e_malloc (size_t size);

/** Allocate space on the GC'd heap for an object that will have no
   pointers (useful for efficiency -- this tells the GC it won't have
   to trace it). */
void * e_malloc_atomic (size_t size);

/** Return a new array of 'size' elements, all initially null. */
e_Ref *e_make_array (int size);

#define e_def_type_predicate(pred_name, script_name) \
  static int                      \
  pred_name (e_Ref ref)                  \
  {                                      \
    return &(script_name) == ref.script; \
  }



#include "invoke.h"

#include "problemobject.h"
#include "ejectorobject.h"
#include "null.h"
#include "boolobject.h"
#include "streamobject.h"
#include "charobject.h"
#include "numberobject.h"
#include "stringobject.h"
#include "mapobject.h"
#include "listobject.h"
#include "setobject.h"
#include "slotobject.h"

#include "safescope.h"

extern e_Ref e_IntGuard;
extern e_Ref e_Float64Guard;
extern e_Ref e_CharGuard;
extern e_Ref e_StringGuard;
extern e_Ref e_BooleanGuard;
extern e_Ref e_EListGuard;


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


/// The default top-level scope for non-interactive code.
extern e_Ref e_privilegedScope;

e_Ref e_module_import(GString *module_name);

#include "ref.h"
#include "ref_private.h"

#endif /* ELIB_H */
