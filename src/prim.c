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

e_Method no_methods[] = {{NULL, NULL}};
e_Ref e_empty_ref = {NULL, {0}};

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

e_Ref e_spread_uncall(e_Ref obj) {
  // XXX selector pooling
  e_Selector optUncall, add, run, get;
  e_make_selector(&optUncall, "__optUncall", 0);
  e_make_selector(&add, "add", 1);
  e_make_selector(&run, "run", 2);
  e_make_selector(&get, "get", 1);
  e_Ref uncall = e_ref_target(e_call_0(obj, &optUncall));
  if (!e_eq(uncall, e_null)) {
    e_Ref front = e_call_2(uncall, &run, e_make_fixnum(0), e_make_fixnum(2));
    e_Ref args = e_call_1(uncall, &get, e_make_fixnum(2));
    return e_call_1(front, &add, args);
  } else {
    return e_null;
  }
}

static void set_up_prims(void) {
  e_make_selector(&e_do_printOn, "__printOn", 1);
  e_make_selector(&e_do_print, "print", 1);
  e_make_selector(&e_do_quote_print, "quote", 1);
  e_make_selector(&e_do_println, "println", 1);

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
  e__exit_set_up();
  set_up_prims();
  e__ref_set_up();
  e__guards_set_up();
  e__safescope_set_up();
  e__privilegedscope_set_up();
  e__scope_set_up();
  e__setup_done = true;
}
}
