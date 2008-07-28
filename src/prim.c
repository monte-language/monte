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
static e_Selector run2;

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


e_Ref e_empty_ref = {NULL, {0}};

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

/// @ingroup list
//@{

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

static e_Ref flexset_diverge(e_Ref self, e_Ref *args) {
  e_Ref res = flexlist_diverge(self, args);
  res.script = &e__flexset_script;
  return res;
}

static e_Ref flexset_addElement(e_Ref self, e_Ref *args) {
  if (e_same(flexlist_contains(self, args), e_false)) {
    E_ERROR_CHECK(flexlist_push(self, args));
  }
  return e_null;
}

static e_Ref flexset_snapshot(e_Ref self, e_Ref *args) {
  e_Ref result = flexlist_diverge(self, NULL);
  result.script = &e__constset_script;
  return result;
}

e_Script e__constset_script;
static e_Method constset_methods[] = {
  {"__printOn/1", constset_printOn},
  {"size/0", flexlist_size},
  {"getElements/0", flexlist_snapshot},
  {"with/1", constset_with},
  {"iterate/1", flexlist_iterate},
  {"diverge/0", flexset_diverge},
  {NULL}};

e_Script e__flexset_script;
static e_Method flexset_methods[] = {
  {"__printOn/1", flexset_printOn},
  {"size/0", flexlist_size},
  {"getElements/0", flexlist_snapshot},
  {"with/1", constset_with},
  {"iterate/1", flexlist_iterate},
  {"addElement/1", flexset_addElement},
  {"snapshot/0", flexset_snapshot},
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

  e_make_script(&e__null_script, NULL, null_methods, "void");
  e_make_script(&e__boolean_script, NULL, boolean_methods, "Boolean");
  e_make_script(&e__char_script, NULL, char_methods, "char");
  e_make_script(&e__string_script, NULL, string_methods, "String");
  e_make_script(&e__fixnum_script, NULL, fixnum_methods, "int");
  e_make_script(&e__bignum_script, NULL, bignum_methods, "bigint");
  e_make_script(&e__float64_script, NULL, float64_methods, "float64");
  e_make_script(&e__writer_script, NULL, writer_methods, "writer");
  e_make_script(&e__reader_script, NULL, reader_methods, "reader");
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

#ifndef NO_GC

static void do_nothing_free(void *ptr, size_t size) {}
static void do_nothing_free2(void *ptr) {}

static void *gmp_realloc(void *ptr, size_t old, size_t new) {
    return GC_realloc(ptr, new);
}
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
