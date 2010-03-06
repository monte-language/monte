/* -*- mode: c -*- */
#include <check.h>
#include <stdlib.h>
#include "vm.h"
#include "bytecodes.h"
#include "elib.h"

#define STACK_LEVEL() ((lastStackFrame->stack_top - lastStackFrame->stack_bottom))
#define STACK_EMPTY() (STACK_LEVEL() == 0)
#define FIRST() lastStackFrame->stack_top[-1]
#define SECOND() lastStackFrame->stack_top[-2]
#define THIRD() lastStackFrame->stack_top[-3]
#define HAS_PROBLEM(val) (val.script == NULL && val.data.fixnum == 0)
#define ERROR_CHECK(x)                          \
  if (HAS_PROBLEM(x)) {                         \
    if (e_thrown_problem().script != NULL) {    \
      e_println(e_stdout, e_thrown_problem());  \
      fail("Unhandled exception");              \
    } else {                                    \
      e_println(e_stdout, e_ejected_value());   \
      fail("Unhandled ejection");               \
    }                                           \
  }

e_Selector do_get, do_run1;
ecru_stackframe *lastStackFrame;
e_Ref empty_scope;
void setup(void) {
  ecru_set_up();
  e_make_selector(&do_get, "get", 0);
  e_make_selector(&do_run1, "run", 1);
  empty_scope = e_make_scope(NULL, NULL, 0);
}

void teardown(void) {
}

void vm_fail_unless(e_Ref result) {
  fail_unless(result.script != NULL);
}

// Convenience definitions for tests that don't need to reuse modules.
e_Ref vm_exec_constants(unsigned char *code, int codelen,
                      e_Ref *constants, int constantslen, int localslen) {
  ecru_module module = {NULL, 0, NULL, 0, empty_scope, NULL, 0, 0};
  ecru_method method = {e_intern("run/0"), code, codelen, localslen,
                         NULL, 0};
  ecru_script script = {1, &method, 0, NULL, 0};
  ecru_script *scripts[] = {&script};
  module.constants = constants;
  module.constantsLength = constantslen;
  module.scripts = scripts;
  e_Ref res = ecru_vm_execute(0, 0, METHOD, false, &module, NULL, 0, &lastStackFrame);
  return res;
}

e_Ref vm_exec_constants_sels_htable(unsigned char *code, int codelen,
                                    e_Ref *constants, int constantslen,
                                    int localslen,
                                    e_Selector *sels, int selectorslen,
                                    ecru_handler_table_entry *ht, int htlen) {
  ecru_module module = {NULL, 0, NULL, 0, empty_scope, NULL, 0, 0};
  ecru_method method = {e_intern("run/0"), code, codelen, localslen,
                         ht, htlen};
  ecru_script script = {1, &method, 0, NULL, 0};
  ecru_script *scripts[] = {&script};
  module.scripts = scripts;
  module.constants = constants;
  module.constantsLength = constantslen;
  module.selectors = sels;
  module.selectorsLength = selectorslen;
  e_Ref res = ecru_vm_execute(0, 0, METHOD, false, &module, NULL, 0, &lastStackFrame);
  return res;
}

e_Ref vm_exec_constants_sels(unsigned char *code, int codelen,
                             e_Ref *constants, int constantslen,
                             int localslen,
                             e_Selector *sels, int selectorslen) {
  return vm_exec_constants_sels_htable(code, codelen, constants,
                                       constantslen, localslen, sels,
                                       selectorslen, NULL, 0);
}

e_Ref vm_exec_scope(unsigned char *code, int codelen,
                    e_Ref *constants, int constantslen,
                    e_Ref *globals, int globalslen) {
  ecru_module module = {NULL, 0, NULL, 0, empty_scope, NULL, 0, 0};
  ecru_method method = {e_intern("run/0"), code, codelen, 0, NULL, 0};
  ecru_script script = {1, &method, 0, NULL, 0};
  ecru_script *scripts[] = {&script};
  char **fakeNames = e_malloc(globalslen * sizeof(char *));
  for (int i = 0; i < globalslen; i++) {
    fakeNames[i] = "";
  }
  module.scope = e_make_scope(fakeNames, globals, globalslen);
  module.scripts = scripts;
  module.constants = constants;
  module.constantsLength = constantslen;

  e_Ref res = ecru_vm_execute(0, 0, METHOD, false, &module, NULL, 0, &lastStackFrame);
  return res;
}

e_Ref vm_exec_frame(unsigned char *code, int codelen,
                    e_Ref *constants, int constantslen,
                    e_Ref *globals, int globalslen,
                    ecru_script **scripts, int scriptslen,
                    e_Ref *frame, int framelen, int localslen) {
  ecru_module module = {NULL, 0, NULL, 0, empty_scope, NULL, 0, 0};
  ecru_method method = {e_intern("run/0"), code, codelen, localslen, NULL, 0};
  ecru_script script = {1, &method, 0, NULL, 0};
  char **fakeNames = e_malloc(globalslen * sizeof(char *));
  for (int i = 0; i < globalslen; i++) {
    fakeNames[i] = "";
  }
  module.scope = e_make_scope(fakeNames, globals, globalslen);
  module.constants = constants;
  module.constantsLength = constantslen;
  module.scripts = scripts;
  fail_unless(module.scripts[0] == NULL,
              "must leave script0 empty to use vm_exec_frame");
  module.scripts[0] = &script;
  module.scriptsLength = scriptslen;

  e_Ref res = ecru_vm_execute(0, 0, false, frame, &module, NULL, 0, &lastStackFrame);
  return res;
}

e_Ref vm_exec_frame_sels_htable(unsigned char *code, int codelen,
                                e_Ref *constants, int constantslen,
                                e_Ref *globals, int globalslen,
                                ecru_script **scripts, int scriptslen,
                                e_Ref *frame, int framelen, int localslen,
                                e_Selector *sels, int selectorslen,
                                ecru_handler_table_entry *ht, int htlen) {
  ecru_module module = {NULL, 0, NULL, 0, empty_scope, NULL, 0, 0};
  ecru_method method = {e_intern("run/0"), code, codelen, localslen,
                         ht, htlen};
  ecru_script script = {1, &method, 0, NULL, 0};
  char **fakeNames = e_malloc(globalslen * sizeof(char *));
  for (int i = 0; i < globalslen; i++) {
    fakeNames[i] = "";
  }
  module.scope = e_make_scope(fakeNames, globals, globalslen);
  module.constants = constants;
  module.constantsLength = constantslen;
  module.scripts = scripts;
  fail_unless(module.scripts[0] == NULL,
              "must leave script0 empty to use vm_exec_frame_sels");
  module.scripts[0] = &script;
  module.scriptsLength = scriptslen;
  module.selectors = sels;
  module.selectorsLength = selectorslen;
  e_Ref res = ecru_vm_execute(0, 0, false, frame, &module, NULL, 0, &lastStackFrame);
  return res;
}

e_Ref vm_exec_frame_sels(unsigned char *code, int codelen,
                         e_Ref *constants, int constantslen,
                         e_Ref *globals, int globalslen,
                         ecru_script **scripts, int scriptslen,
                         e_Ref *frame, int framelen, int localslen,
                         e_Selector *sels, int selectorslen) {
  return vm_exec_frame_sels_htable(code, codelen, constants, constantslen,
                                   globals, globalslen, scripts, scriptslen,
                                   frame, framelen, localslen,
                                   sels, selectorslen, NULL, 0);
}

#test op_dup
{
  // Test that OP_DUP duplicates the top item on the stack.
  unsigned char code[3] = {OP_LITERAL, 0, OP_DUP};
  e_Ref fixnum = e_make_fixnum(42);
  e_Ref constants[1] = { fixnum };
  e_Ref stackTop = vm_exec_constants(code, 3, constants, 1, 0);
  e_Ref stack2nd = FIRST();
  fail_unless(STACK_LEVEL() == 1);
  fail_unless(e_same(stackTop, stack2nd));
  fail_unless(e_same(stackTop, fixnum));
}

#test op_pop
{
  // Test that OP_POP removes the top item from the stack.
  unsigned char code[] = {OP_LITERAL, 0, OP_LITERAL, 0, OP_POP};
  e_Ref fixnum = e_make_fixnum(42);
  e_Ref constants[1] = { fixnum };
  vm_fail_unless(vm_exec_constants(code, 5, constants, 1, 0));
  fail_unless(STACK_EMPTY());
}

#test op_swap
{
  // test that OP_SWAP swaps the top two items on the stack.
  unsigned char code[5] = {OP_LITERAL, 1, OP_LITERAL, 0, OP_SWAP};
  e_Ref constants[2] = { e_make_fixnum(42), e_make_fixnum(19) };
  e_Ref stackTop = vm_exec_constants(code, 5, constants, 2, 0);
  e_Ref stack2nd = FIRST();
  fail_unless(STACK_LEVEL() == 1);
  fail_unless(e_same(stackTop, constants[1]));
  fail_unless(e_same(stack2nd, constants[0]));
}

#test op_rot
{
  // test that OP_ROT moves the top item on the stack to the third item.
  unsigned char code[] = {OP_LITERAL, 2, OP_LITERAL, 1, OP_LITERAL, 0, OP_ROT};
  e_Ref constants[3] = { e_make_fixnum(42), e_make_fixnum(19), e_make_fixnum(3) };
  e_Ref stackTop = vm_exec_constants(code, 7, constants, 3, 0);
  e_Ref stack2nd = FIRST();
  e_Ref stack3rd = SECOND();
  fail_unless(STACK_LEVEL() == 2);
  fail_unless(e_same(stackTop, constants[1]));
  fail_unless(e_same(stack2nd, constants[2]));
  fail_unless(e_same(stack3rd, constants[0]));
}

#test op_literal1
{
  // Test that OP_LITERAL pushes a value from the constant pool onto the stack.
  unsigned char code[2] = {OP_LITERAL, 0};
  e_Ref c = e_make_fixnum(17);
  e_Ref constants[1] = {c};
  fail_unless(e_same(vm_exec_constants(code, 2, constants, 1, 0), c));

}

#test op_literal2
{
  // Test that more than one value can be loaded from the constant pool.
  unsigned char code[4] = {OP_LITERAL, 3, OP_LITERAL, 0};
  char values[5] = {17, 24, 19, 47, 99};
  e_Ref *constants = e_malloc(5 * sizeof(e_Ref));
  for (int i = 0; i < 5; i++) {
    constants[i] = e_make_fixnum(values[i]);
  };
  e_Ref top = vm_exec_constants(code, 4, constants, 5, 0);
  fail_unless(STACK_LEVEL() == 1);
  fail_unless(top.data.fixnum == 17, "%d != %d",
              top.data.fixnum, 17);
  fail_unless(FIRST().data.fixnum == 47, "%d != %d",
              FIRST().data.fixnum, 47);
}

#test op_noun_outer
{
  // test that OP_NOUN_OUTER loads the indexed item from the outer scope and
  // places it on the stack.
  unsigned char code[] = {OP_NOUN_OUTER, 0};
  e_Ref scope[] = { e_make_finalslot(e_make_fixnum(42)) };
  fail_unless((vm_exec_scope(code, 2, NULL, 0, scope, 1)).data.fixnum == 42);
}

#test op_assign_outer
{
  /// OP_ASSIGN_OUTER should effectively call put() on the indexed slot
  /// in the outer scope.
  e_Ref scope[] = { e_make_varslot(e_make_fixnum(42)) };
  e_Ref constants[] = {e_make_fixnum(99), e_null};
  unsigned char code[] = {OP_LITERAL, 1, OP_LITERAL, 0, OP_ASSIGN_OUTER, 0};
  fail_unless(e_same(vm_exec_scope(code, 6, constants, 2, scope, 1), e_null));
  fail_unless(e_same(scope[0].data.refs[0], constants[0]));
}

#test op_slot_outer
{
  // Test that OP_SLOT_OUTER retrieves the indexed slot from the outer scope
  // and places it on the stack.
  unsigned char code[] = {OP_SLOT_OUTER, 0};
  e_Ref scope[] = { e_make_finalslot(e_make_fixnum(42)) };
  fail_unless(e_same(vm_exec_scope(code, 2, NULL, 0, scope, 1), scope[0]));
}

#test op_noun_local
{
  // Test that OP_NOUN_LOCAL retrieves the indexed slot from the local scope
  // and places it on the stack.
  unsigned char code[] = {OP_LITERAL, 0, OP_BINDSLOT, 0, OP_NOUN_LOCAL, 0};
  e_Ref constants[] = {e_make_finalslot(e_make_fixnum(99))};
  fail_unless(e_same(vm_exec_constants(code, 6, constants, 1, 1),
                     e_call_0(constants[0], &do_get)));
}

#test op_slot_local
{
  // Test that OP_SLOT_LOCAL retrieves the indexed slot from the local scope
  // and places it on the stack.
  unsigned char code[] = {OP_LITERAL, 0, OP_BINDSLOT, 0, OP_SLOT_LOCAL, 0};
  e_Ref constants[] = {e_make_finalslot(e_make_fixnum(99))};
  fail_unless(e_same(constants[0],
                     vm_exec_constants(code, 6, constants, 1, 1)));
}

#test op_bind
{
  // Test that OP_BIND makes the slot for the specified local refer to the object on
  // the top of the stack.
  unsigned char code[] = {OP_LITERAL, 0, OP_BIND, 0, OP_NOUN_LOCAL, 0};
  e_Ref constants[] = {e_make_fixnum(99)};
  fail_unless(e_same(vm_exec_constants(code, 6, constants, 1, 1),
                     constants[0]));
}

#test op_bindslot
{
  // Test that OP_BINDSLOT associates the specified local with the slot on the top
  // of the stack.
  unsigned char code[] = {OP_LITERAL, 0, OP_BINDSLOT, 0, OP_SLOT_LOCAL, 0};
  e_Ref constants[] = {e_make_finalslot(e_make_fixnum(99))};
  fail_unless(e_same(constants[0],
                     vm_exec_constants(code, 6, constants, 1, 1)));
}

#test op_call
{
  // Test that OP_CALL uses the specified object in the constant pool as a verb
  // in a message to the object on top of the stack, along with the specified number
  // of args on the stack.
  unsigned char code[] = {OP_LITERAL, 0, OP_LITERAL, 1, OP_CALL, 0};
  e_Ref constants[] = {e_make_fixnum(10), e_make_fixnum(1)};
  e_Selector sels[1];
  e_make_selector(sels, "add", 1);
  e_Ref res = vm_exec_constants_sels(code, 6, constants, 2, 0, sels, 1);
  fail_unless(res.data.fixnum == 11);
}


#test op_list_patt
{
  // Test that 'OP_LIST_PATT x' produces x instances of the optEjector on the
  // top of stack interleaved with all x items of the 2nd item on the stack.

  unsigned char code[] = {OP_LITERAL, 0, OP_LITERAL, 1, OP_LIST_PATT, 3};
  e_Ref test_array[3] = {e_make_fixnum(2), e_make_fixnum(4), e_make_fixnum(7)};
  e_Ref constants[] = {e_constlist_from_array(3, test_array),
                    e_null};
  e_Ref res = vm_exec_constants(code, 6, constants, 2, 0);
  ERROR_CHECK(res);
  e_Ref results[6] = {res, e_true, e_true, e_true, e_true, e_true};
  fail_unless(STACK_LEVEL() == 5);
  for (int i = 1; i < 6; i++) {
    results[i] = FIRST();
    lastStackFrame->stack_top--;
  }
  fail_unless(e_same(results[0], e_null));
  fail_unless(e_same(results[1], test_array[0]));
  fail_unless(e_same(results[2], e_null));
  fail_unless(e_same(results[3], test_array[1]));
  fail_unless(e_same(results[4], e_null));
  fail_unless(e_same(results[5], test_array[2]));
}

#test op_simplevarslot
{
  // Test that OP_SIMPLEVARSLOT takes the top item on the stack and replaces it
  // with a varslot containing it.
  unsigned char code[] = {OP_LITERAL, 0, OP_SIMPLEVARSLOT};
  e_Ref constants[] = {e_make_fixnum(1)};
  e_Ref res = vm_exec_constants(code, 3, constants, 1, 0);
  fail_unless(e_is_varslot(res));
  fail_unless(e_same(e_call_0(res, &do_get), constants[0]));
}

#test op_guardedvarslot
{
  // OP_GUARDEDVARSLOT should take the top three items on the stack: specimen,
  // optional ejector, and guard. It should then coerce the specimen with the
  // guard, ejecting on failure. On success, a guarded slot goes on the stack.
  unsigned char code[] = {OP_LITERAL, 2, OP_LITERAL, 1, OP_LITERAL, 0, OP_GUARDEDVARSLOT};
  e_Ref constants[] = {e_IntGuard, e_null, e_make_fixnum(7)};
  e_Ref ej = e_make_ejector();
  e_Ref constants2[] = {e_IntGuard, e_null, e_make_string("seven")};
  e_Ref constants3[] = {e_IntGuard, ej, e_make_string("7")};
  e_Ref res = vm_exec_constants(code, 7, constants, 3, 0);
  vm_fail_unless(res);
  fail_unless(e_is_guardedslot(res));
  fail_unless(e_same(e_call_0(res, &do_get), constants[2]));

  res = vm_exec_constants(code, 7, constants2, 3, 0);
  fail_if(e_is_guardedslot(res));

  res = vm_exec_constants(code, 7, constants3, 3, 0);
  e_ON_EJECTION(res, ej) {
    fail_unless(STACK_EMPTY());
  } else if (res.script == NULL) {
    fail("OP_GUARDEDVARSLOT did not call its ejector on coercion failure.");
  }
}

#test op_coercetoslot
{
  // OP_COERCETOSLOT takes the top two items on the stack, specimen
  // and optional ejector; it then attempts to coerce the specimen to
  // a slot. On success, a slot is pushed to the stack. On failure,
  // the ejector is invoked.

  unsigned char code[] = {OP_LITERAL, 0, OP_LITERAL, 1, OP_COERCETOSLOT};
  e_Ref constants[] = {e_make_varslot(e_make_fixnum(42)), e_null};
  e_Ref ej = e_make_ejector();
  e_Ref constants2[] = {e_make_fixnum(42), ej};
  e_Ref res = vm_exec_constants(code, 5, constants, 2, 0);
  vm_fail_unless(res);
  fail_unless(STACK_EMPTY());
  fail_unless(e_same(res, constants[0]));
  res = vm_exec_constants(code, 5, constants, 2, 0);
  e_ON_EJECTION(res, ej) {
    fail_unless(STACK_EMPTY());
  } else if (res.script == NULL) {
    fail("OP_COERCETOSLOT didn't eject on failure.");
  }
  e_ejector_disable(ej);
}

#test op_assign_local
{
  /// OP_ASSIGN_LOCAL should effectively call put() on the indexed slot
  /// in the locals array.
  unsigned char code[] = {OP_LITERAL, 0, OP_BINDSLOT, 0, OP_LITERAL, 1,
                 OP_ASSIGN_LOCAL, 0, OP_NOUN_LOCAL, 0};
  e_Ref constants[] = {e_make_varslot(e_make_fixnum(17)), e_make_fixnum(42)};
  fail_unless(e_same(constants[1], vm_exec_constants(code, 10, constants, 2, 1)));
}

#test op_ejector
{
  /// OP_EJECTOR pushes an ejector to the stack. Invoking it
  /// activates its handler table entry.
  unsigned char code[] = {OP_EJECTOR, 9, 0, OP_LITERAL, 0, OP_SWAP, OP_CALL, 0,
                 OP_JUMP, 4, 0, OP_END_HANDLER, OP_LITERAL, 1, OP_SWAP};
  e_Ref constants[] = {e_make_fixnum(17), e_make_fixnum(99)};
  e_Selector sels[] = {do_run1};
  ecru_handler_table_entry ht[] = {{OP_EJECTOR, 0, 12, 3, 11}};
  e_Ref res = vm_exec_constants_sels_htable(code, 15, constants, 2, 0,
                                            sels, 1, ht, 1);
  ERROR_CHECK(res);
  fail_if(STACK_EMPTY());
  fail_unless(e_same(res, constants[0]));
  fail_unless(e_same(FIRST(), constants[1]));
}

#test ejector_disabling
{
  /// Ejectors are disabled when their corresponding OP_END_HANDLER is
  /// executed.
  e_Selector isEnabled;
  unsigned char code[] = {OP_EJECTOR, 4, 0, OP_LITERAL, 0, OP_POP, OP_END_HANDLER};
  e_Ref constants[] = {e_make_fixnum(17)};
  ecru_handler_table_entry ht[] = {{OP_EJECTOR, 0, 7, 3, 6}};
  e_Ref res = vm_exec_constants_sels_htable(code, 7, constants, 1, 0,
                                            NULL, 0, ht, 1);
  e_make_selector(&isEnabled, "isEnabled", 0);
  ERROR_CHECK(res);
  fail_unless(STACK_EMPTY());
  fail_unless(e_is_ejector(res));
  fail_unless(e_same(e_call_0(res, &isEnabled), e_false));
}


#test op_unwinder_invoke
{
  /// Invoking the handler created by OP_UNWIND should branch to the
  /// label and push a rethrower.

  unsigned char code[] = {OP_EJECTOR, 9, 0, OP_UNWIND, 6, 0, OP_LITERAL, 0, OP_SWAP, OP_CALL, 0, OP_END_HANDLER};
  e_Ref constants[] = {e_make_fixnum(17)};
  e_Selector sels[] = {do_run1};
  ecru_handler_table_entry ht[] = {{OP_UNWIND, 1, 12, 6, 10}, {OP_EJECTOR, 0, 12, 3, 10}};
  e_Ref res = vm_exec_constants_sels_htable(code, 12, constants, 1, 0, sels, 1, ht, 2);
  fail_if(STACK_EMPTY());
  ERROR_CHECK(res);
  fail_unless(e_is_reEjector(res));
  fail_unless(e_same(FIRST(), e_null));
}

#test op_unwinder_reeject
{
  /// Invoking the re-ejector pushed by an invoked unwinder should
  /// invoke the next ejection handler.
  unsigned char code[] = { OP_EJECTOR, 17, 0, OP_UNWIND, 8, 0, OP_LITERAL, 2, OP_SWAP,
                  OP_CALL, 0, OP_LITERAL, 2, OP_END_HANDLER,
                  OP_CALL, 0, OP_LITERAL, 0, OP_LITERAL, 3, OP_END_HANDLER};

  e_Ref constants[] = {e_make_fixnum(17), e_null, e_make_fixnum(21),
                       e_make_fixnum(99)};
  e_Selector sels[] = {do_run1};
  ecru_handler_table_entry ht[] = {{OP_UNWIND, 1, 14, 6, 13}, {OP_EJECTOR, 0, 21, 3, 20}};
  e_Ref res = vm_exec_constants_sels_htable(code, 21, constants, 4, 0, sels, 1, ht, 2);
  fail_unless(e_same(res, constants[2]));
  fail_unless(STACK_EMPTY());
}

#test op_buried_unwinder
{
  /// Invoking an ejector should trigger unwinders above it in the
  /// handler table.

  unsigned char code[] = { OP_EJECTOR, 18, 0, OP_UNWIND, 13, 0, OP_EJECTOR, 7, 0,
                  OP_SWAP, OP_LITERAL, 2, OP_SWAP, OP_CALL, 0,
                  OP_END_HANDLER, OP_LITERAL, 2, OP_END_HANDLER, OP_LITERAL, 0,
                  OP_LITERAL, 3};

  e_Ref constants[] = {e_make_fixnum(17), e_null, e_make_fixnum(21),
                       e_make_fixnum(99)};
  e_Selector sels[] = {do_run1};
  ecru_handler_table_entry ht[] = {{OP_EJECTOR, 1, 15, 9, 14}, {OP_UNWIND, 1, 19, 6, 18}, {OP_EJECTOR, 0, 23, 3, 22}};
  e_Ref res = vm_exec_constants_sels_htable(code, 23, constants, 4, 0, sels, 1, ht, 3);
  fail_unless(e_same(res, constants[3]));
  fail_unless(e_same(FIRST(), constants[0]));
  fail_unless(e_is_reEjector(SECOND()));
}

#test buried_unwinder2
{
  /// Dropping an unwinder should push a returner and not break outer handlers.
  unsigned char code[] = {OP_EJECTOR, 13, 0, OP_POP, OP_UNWIND, 3, 0, OP_LITERAL, 0,
                 OP_END_HANDLER, OP_LITERAL, 1, OP_POP,
                 OP_CALL, 0, OP_END_HANDLER};
  e_Ref constants[] = {e_make_fixnum(17), e_null, e_make_fixnum(21)};
  e_Selector sels[] = {do_run1};
  ecru_handler_table_entry ht[] = {{OP_UNWIND, 0, 10, 7, 9},
                                    {OP_EJECTOR, 0, 16, 3, 15}};
  e_Ref res = vm_exec_constants_sels_htable(code, 16, constants, 2, 0, sels, 1,
                                            ht, 2);
  e_println(e_stdout, res);
  fail_unless(e_same(res, constants[0]));
}

#test op_unwinder_end
{
  /// Dropping the handler created by OP_UNWIND should push a returner.
  unsigned char code[] = {OP_UNWIND, 5, 0, OP_LITERAL, 0, OP_END_HANDLER, OP_LITERAL, 1};
  e_Ref constants[] = {e_make_fixnum(17), e_make_fixnum(99)};
  ecru_handler_table_entry ht[] = {{OP_UNWIND, 0, 8, 3, 5}};
  e_thrown_problem_set(e_empty_ref);
  e_Ref res = vm_exec_constants_sels_htable(code, 8, constants, 2, 0, NULL, 0, ht, 1);
  fail_unless(e_same(e_thrown_problem(), e_empty_ref));
  fail_unless(e_same(constants[1], res));
  fail_unless(ecru_is_returner(FIRST()));
}


#test op_try
{

  /// Invoking the handler associated with an OP_TRY should truncate
  /// the value stack and branch to its label.

  unsigned char code[] = { OP_LITERAL, 0, OP_TRY, 10, 0, OP_LITERAL, 2, OP_LITERAL, 3,
                  OP_CALL, 0, OP_JUMP, 3, 0, OP_END_HANDLER, OP_SWAP, OP_POP};
   e_Ref constants[] = {e_make_fixnum(17), e_null, e_make_fixnum(21), e_thrower};
  e_Selector sels[] = {do_run1};
  ecru_handler_table_entry ht[] = {{OP_TRY, 1, 15, 5, 14}};
  e_Ref res = vm_exec_constants_sels_htable(code, 17, constants, 4, 0, sels, 1,
                                            ht, 1);
  fail_unless(e_same(res, constants[2]));

}

#test op_try_unwind
{
  /// Invoking a problem handler should walk the handler stack and
  /// execute the unwinders above it in order.
  unsigned char code[] = { OP_TRY, 12, 0, OP_UNWIND, 10, 0, OP_LITERAL, 2,  OP_LITERAL, 2, OP_LITERAL, 0,
                  OP_CALL, 0, OP_END_HANDLER, OP_END_HANDLER};
  e_Ref constants[] = {e_thrower, e_null,  e_make_fixnum(21)};
  e_Selector sels[] = {do_run1};
  ecru_handler_table_entry ht[] = {{OP_UNWIND, 0, 16, 6, 14}, {OP_TRY, 0, 16, 3, 15}};
  e_Ref res = vm_exec_constants_sels_htable(code, 16, constants, 3, 0, sels, 1, ht, 2);
  fail_unless(e_is_rethrower(res));
  fail_unless(e_is_null(FIRST()));
  fail_unless(STACK_LEVEL() == 1);
}

#test unhandled_exception
{
  /// Throwing a problem when no problem handlers exist should cause
  /// the execution to fail by returning 0.
  unsigned char code[] = {OP_LITERAL, 0, OP_CALL, 0};
  e_Ref constants[] = {e_thrower, e_make_string("run")};
  e_Selector sels[1];
  e_make_selector(sels, "run", 0);
  e_Ref res = vm_exec_constants_sels(code, 4, constants, 2, 0, sels, 1);
  fail_unless(res.script == NULL);
  fail_unless(res.data.other == NULL);
}

#test op_jump
{
  /// Test that OP_JUMP jumps to the right place.
  unsigned char code[] = {OP_JUMP, 2, 0, OP_LITERAL, 0, OP_LITERAL, 0};
  e_Ref constants[] = {e_make_fixnum(17)};
  e_Ref res = vm_exec_constants(code, 7, constants, 1, 0);
  fail_unless(e_same(res, constants[0]));
  fail_unless(STACK_EMPTY());
}

#test op_ejector_only
{
  /// Test that OP_EJECTOR_ONLY behaves like OP_EJECTOR, except
  /// without pushing its argument after invocation.
  unsigned char code[] = {OP_LITERAL, 0, OP_EJECTOR_ONLY, 10, 0, OP_LITERAL, 2, OP_SWAP,
                 OP_CALL, 0, OP_END_HANDLER};
  e_Ref constants[] = {e_make_fixnum(17), e_null, e_make_fixnum(21)};
  e_Selector sels[] = {do_run1};
  ecru_handler_table_entry ht[] = {{OP_EJECTOR_ONLY, 1, 11, 5, 10}};
  e_Ref res = vm_exec_constants_sels_htable(code, 11, constants, 3, 0, sels, 1, ht, 1);
  fail_unless(e_same(res, constants[0]));
  fail_unless(STACK_EMPTY());
}

#test op_branch_eject
{
  /// Test that OP_BRANCH ejects if its argument is false and an ejector is
  /// provided.

  unsigned char code[] = {OP_EJECTOR, 6, 0, OP_LITERAL, 0, OP_BRANCH, OP_LITERAL, 1, OP_END_HANDLER};
  e_Ref constants[] = {e_false, e_make_fixnum(37)};
  ecru_handler_table_entry ht[] = {{OP_EJECTOR, 0, 9, 5, 8}};
  e_Ref res = vm_exec_constants_sels_htable(code, 9, constants, 1, 0, NULL, 0, ht, 1);
  fail_if(e_same(res, constants[1]));
}


#test op_branch_throw
{
  /// Test that OP_BRANCH throws a problem if its argument is false and an ejector is
  /// provided.

  unsigned char code[] = {OP_LITERAL, 1, OP_LITERAL, 0, OP_BRANCH, OP_LITERAL, 0};
  e_Ref constants[] = {e_false, e_null};
  e_Ref res = vm_exec_constants(code, 9, constants, 2, 0);
  fail_unless(res.script == NULL);
  fail_unless(res.data.other == NULL);
}

#test op_branch_fallthru
{
  /// Test that OP_BRANCH continues execution as normal if its arg is true.

  unsigned char code[] = {OP_EJECTOR, 5, 0, OP_LITERAL, 0, OP_BRANCH, OP_LITERAL, 1, OP_END_HANDLER};
  e_Ref constants[] = {e_true, e_null};
  ecru_handler_table_entry ht[] = {{OP_EJECTOR, 0, 9, 3, 8}};
  e_Ref res = vm_exec_constants_sels_htable(code, 9, constants, 2, 0, NULL, 0, ht, 1);
  fail_unless(e_same(res, constants[1]));
}

#test op_branch3
{
  /// Test that OP_BRANCH raises an error if its argument is not a boolean.
  unsigned char code[] = {OP_LITERAL, 1, OP_LITERAL, 0, OP_BRANCH, OP_LITERAL, 0};
  e_Ref constants[] = {e_make_fixnum(17), e_null};
  e_Ref res = vm_exec_constants(code, 7, constants, 2, 0);
  fail_unless(res.script == NULL);
  fail_unless(res.data.other == NULL);
}

#test make_script
{
  /// Test that ecru_make_script sets the proper fields in the
  /// script and that method structs are set up right.
  ecru_script script;
  unsigned char runcode[] = {OP_LITERAL, 0};
  unsigned char getcode[] = {OP_POP, OP_CALL, 1};
  ecru_method methods[] = {{e_intern("run/1"), runcode, 2, 1,  NULL, 0},
                            {e_intern("get/2"), getcode, 3, 2, NULL, 0}};
  ecru_make_script(&script, methods, 2, NULL, 0, 4);
  fail_unless(script.num_methods == 2);
  fail_unless(script.methods[0].verb == e_intern("run/1"));
  fail_unless(script.methods[0].length == 2);
  fail_unless(script.methods[0].num_locals == 1);
  fail_unless(script.methods[1].verb == e_intern("get/2"));
  fail_unless(script.methods[1].length == 3);
  fail_unless(script.methods[1].num_locals == 2);
  fail_unless(script.num_matchers == 0);
  fail_unless(script.matchers == NULL);
  fail_unless(script.num_slots == 4);
}

#test op_object
{
  /// Test that OP_OBJECT creates an object with the specified script
  /// and slots.
  unsigned char code[] = {OP_LITERAL, 0, OP_LITERAL, 1, OP_OBJECT, 0};
  e_Ref constants[] = {e_make_finalslot(e_make_fixnum(99)),
                       e_make_varslot(e_make_fixnum(21))};
  unsigned char runcode[] = {OP_LITERAL, 0};
  unsigned char getcode[] = {OP_POP, OP_CALL, 1};
  ecru_method methods[] = {{e_intern("run/1"), runcode, 2, 0, NULL, 0},
                            {e_intern("get/2"), getcode, 3, 0, NULL, 0}};
  ecru_script script;
  ecru_script *scripts[] = {NULL, &script};
  ecru_object *obj;
  ecru_make_script(&script, methods, 2, NULL, 0, 2);
  e_Ref res = vm_exec_frame(code, 6, constants, 2,
                            NULL, 0, scripts, 2, NULL, 0, 0);
  vm_fail_unless(res);
  fail_unless(e_is_vmObject(res));
  obj = res.data.other;
  fail_unless(obj->scriptNum == 1);
  fail_unless(e_same(obj->frame[0], constants[0]));
  fail_unless(e_same(obj->frame[1], constants[1]));
}

#test op_bindobject
{
  // OP_BINDOBJECT should create an object and bind it to a final slot.
  unsigned char code[] = {OP_LITERAL, 0, OP_LITERAL, 1, OP_BINDOBJECT, 0, 0,
                 OP_SLOT_LOCAL, 0};
  e_Ref constants[] = {e_make_finalslot(e_make_fixnum(99)),
                       e_make_varslot(e_make_fixnum(21))};
  unsigned char runcode[] = {OP_LITERAL, 0};
  unsigned char getcode[] = {OP_POP, OP_CALL, 1};
  ecru_method methods[] = {{e_intern("run/1"), runcode, 2, 0, NULL, 0},
                            {e_intern("get/2"), getcode, 3, 0, NULL, 0}};
  ecru_script script;
  ecru_script *scripts[] = {NULL, &script};
  ecru_object *obj;
  e_Ref localObj;
  ecru_make_script(&script, methods, 2, NULL, 0, 2);
  e_Ref res = vm_exec_frame(code, 9, constants, 2,
                            NULL, 0, scripts, 2, NULL, 0, 1);
  fail_unless(STACK_LEVEL() == 1);
  fail_unless(e_is_vmObject(FIRST()));
  fail_unless(e_is_finalslot(res));
  localObj = e_call_0(res, &do_get);
  fail_unless(e_eq(FIRST(), localObj));
  obj = localObj.data.other;
  fail_unless(obj->scriptNum == 1);
  fail_unless(e_same(obj->frame[0], constants[0]));
  fail_unless(e_same(obj->frame[1], constants[1]));
}


#test op_varobject
{
  // OP_VAROBJECT should create an object and bind it to a variable slot.
  unsigned char code[] = {OP_LITERAL, 0, OP_LITERAL, 1, OP_VAROBJECT, 0, 0,
                 OP_SLOT_LOCAL, 0};
  e_Ref constants[] = {e_make_finalslot(e_make_fixnum(99)),
                       e_make_varslot(e_make_fixnum(21))};
  unsigned char runcode[] = {OP_LITERAL, 0};
  unsigned char getcode[] = {OP_POP, OP_CALL, 1};
  ecru_method methods[] = {{e_intern("run/1"), runcode, 2, 0, NULL, 0},
                            {e_intern("get/2"), getcode, 3, 0, NULL, 0}};
  ecru_script script;
  ecru_script *scripts[] = {NULL, &script};
  ecru_object *obj;
  e_Ref localObj;
  ecru_make_script(&script, methods, 2, NULL, 0, 2);
  e_Ref res = vm_exec_frame(code, 9, constants, 2,
                            NULL, 0, scripts, 2, NULL, 0, 1);
  fail_unless(STACK_LEVEL() == 1);
  fail_unless(e_is_vmObject(FIRST()));
  fail_unless(e_is_varslot(res));
  localObj = e_call_0(res, &do_get);
  fail_unless(e_eq(FIRST(), localObj));
  obj = localObj.data.other;
  fail_unless(obj->scriptNum == 1);
  fail_unless(e_same(obj->frame[0], constants[0]));
  fail_unless(e_same(obj->frame[1], constants[1]));
}

#test object_selfreference
{

  // It is OK for OP_BINDOBJECT to be given a slot that isn't bound yet
  // as an instance var, and fix it up in the frame once it's bound it.
  unsigned char code[] = {OP_LITERAL, 0, OP_SLOT_LOCAL, 0, OP_BINDOBJECT, 0, 0,
                 OP_SLOT_LOCAL, 0};
  ecru_method mainMethod = {e_intern("run/0"), code, 9, 1, NULL, 0};
  ecru_script mainScript = {1, &mainMethod, 0, NULL, 0};
  e_Ref constants[] = {e_make_finalslot(e_make_fixnum(99)),
                       e_make_varslot(e_make_fixnum(21))};
  unsigned char runcode[] = {OP_SLOT_FRAME, 0};
  ecru_method methods[] = {{e_intern("run/0"), runcode, 2, 0, NULL, 0}};
  ecru_script script;
  ecru_script *scripts[] = {&mainScript, &script};
  e_Selector do_run;
  e_make_selector(&do_run, "run", 0);
  ecru_object *obj;
  e_Ref localObj;
  ecru_module module = {constants, 2, NULL, 0, empty_scope, scripts, 2, 1};
  ecru_make_script(&script, methods, 1, NULL, 0, 1);
  e_Ref res = ecru_vm_execute(0, 0, false, NULL, &module, NULL, 0, &lastStackFrame);
  fail_unless(e_is_finalslot(res));
  localObj = e_call_0(res, &do_get);
  fail_unless(e_eq(FIRST(), localObj));
  // frame slot 0 should be identical to locals slot 0
  fail_unless(e_same(e_call_0(localObj, &do_run), res));
}

#test vmobject_call
{
  // Calling objects created from bytecode should work.
  unsigned char code[] = {OP_OBJECT, 0, OP_CALL, 0};
  e_Ref constants[] = {e_make_string("foo")};
  unsigned char runcode[] = {OP_LITERAL, 0};
  ecru_method methods[] = {{e_intern("run/0"), runcode, 2, 0, NULL, 0}};
  ecru_script script;
  ecru_script *scripts[] = {NULL, &script};
  e_Selector sels[1];
  e_make_selector(sels, "run", 0);
  ecru_make_script(&script, methods, 1, NULL, 0, 0);
  e_Ref res = vm_exec_frame_sels(code, 4, constants, 1, NULL, 0,
                                 scripts, 2, NULL, 0, 0, sels, 1);
  ERROR_CHECK(res);
  fail_unless(STACK_EMPTY());
  fail_unless(e_same(res, constants[0]));
}


#test vmobject_callArgs
{
  // Passing args to objects created from bytecode should work.
  unsigned char code[] = {OP_LITERAL, 1, OP_OBJECT, 0, OP_CALL, 0};
  e_Ref constants[] = {e_null, e_make_fixnum(97)};
  unsigned char runcode[] = {OP_LITERAL, 0};
  ecru_method methods[] = {{e_intern("run/1"), runcode, 2, 0, NULL, 0}};
  ecru_script script;
  ecru_script *scripts[] = {NULL, &script};
  e_Selector sels[1] = {do_run1};
  ecru_make_script(&script, methods, 1, NULL, 0, 0);
  e_Ref res = vm_exec_frame_sels(code, 6, constants, 2,
                                 NULL, 0, scripts, 2, NULL, 0, 0, sels, 1);
  fail_unless(STACK_LEVEL() == 1);
  fail_unless(e_same(res, constants[0]));
  fail_unless(e_same(FIRST(), constants[1]));
}

#test crossframe_ejection
{
  // Ejectors can be invoked in frames below the one they were created in.
  unsigned char code[] = {OP_BINDOBJECT, 0, 0, OP_POP, OP_EJECTOR, 15, 0, OP_BIND, 1,
                 OP_NOUN_LOCAL, 1, OP_LITERAL, 0, OP_NOUN_LOCAL, 0,
                 OP_CALL, 1, OP_POP, OP_LITERAL, 1, OP_END_HANDLER};
  unsigned char runcode[] = {OP_SWAP, OP_CALL, 0, OP_LITERAL, 2};
  e_Ref constants[] = {e_make_fixnum(2), e_make_fixnum(3), e_null};
  ecru_method methods[] = {{e_intern("run/2"), runcode, 5, 0, NULL, 0}};
  ecru_script script;
  ecru_script *scripts[] = {NULL, &script};
  e_Selector sels[] = {do_run1, {NULL}};
  ecru_handler_table_entry ht[] = {{OP_EJECTOR, 0, 20, 7, 21}};
  e_make_selector(sels+1, "run", 2);
  ecru_make_script(&script, methods, 1, NULL, 0, 0);

  e_Ref res = vm_exec_frame_sels_htable(code, 21, constants, 3,
                                        NULL, 0, scripts, 2, NULL, 0, 2,
                                        sels, 2, ht, 1);
  fail_unless(e_same(res, constants[0]));
}

#test op_noun_frame
{
  // Test that OP_NOUN_FRAME retrieves the indexed slot from the
  // object's instance variables and places it on the stack.
  unsigned char code[] = {OP_LITERAL, 0, OP_OBJECT, 0, OP_CALL, 0};
  e_Ref constants[] = {e_make_varslot(e_make_fixnum(99))};
  unsigned char runcode[] = {OP_NOUN_FRAME, 0};
  ecru_method methods[] = {{e_intern("run/0"), runcode, 2, 0, NULL, 0}};
  ecru_script script;
  ecru_script *scripts[] = {NULL, &script};
  e_Selector sels[1];
  e_make_selector(sels, "run", 0);
  ecru_make_script(&script, methods, 1, NULL, 0, 1);
  e_Ref res = vm_exec_frame_sels(code, 6, constants, 2, NULL, 0,
                                 scripts, 2, NULL, 0, 0, sels, 1);
  ERROR_CHECK(res);
  fail_unless(e_same(constants[0].data.refs[0], res));
}

#test op_assign_frame
{
  /// OP_ASSIGN_FRAME should effectively call put() on the indexed slot
  /// in the frame array.
  unsigned char code[] = {OP_LITERAL, 1, OP_OBJECT, 0, OP_CALL, 0};
  e_Ref constants[] = {e_make_string("foo"), e_make_varslot(e_null)};
  unsigned char runcode[] = {OP_LITERAL, 0, OP_DUP, OP_ASSIGN_FRAME, 0};
  ecru_method methods[] = {{e_intern("run/0"), runcode, 5, 0, NULL, 0}};
  ecru_script script;
  ecru_script *scripts[] = {NULL, &script};
  e_Selector sels[1];
  e_make_selector(sels, "run", 0);
  ecru_make_script(&script, methods, 1, NULL, 0, 1);
  e_Ref res = vm_exec_frame_sels(code, 6, constants, 2, NULL, 0,
                                 scripts, 2, NULL, 0, 0, sels, 1);
  ERROR_CHECK(res);
  fail_unless(e_same(constants[0], constants[1].data.refs[0]));
}

#test op_slot_frame
{
  // Test that OP_SLOT_FRAME retrieves the indexed slot from the
  // object's instance variables and places it on the stack.
  unsigned char code[] = {OP_LITERAL, 0, OP_OBJECT, 0, OP_CALL, 0};
  e_Ref constants[] = {e_make_varslot(e_make_fixnum(99))};
  unsigned char runcode[] = {OP_SLOT_FRAME, 0};
  ecru_method methods[] = {{e_intern("run/0"), runcode, 2, 0, NULL, 0}};
  ecru_script script;
  ecru_script *scripts[] = {NULL, &script};
  e_Selector sels[1];
  e_make_selector(sels, "run", 0);
  ecru_make_script(&script, methods, 1, NULL, 0, 1);
  e_Ref res = vm_exec_frame_sels(code, 6, constants, 2, NULL, 0,
                                 scripts, 2, NULL, 0, 0, sels, 1);
  ERROR_CHECK(res);
  fail_unless(e_same(constants[0], res));
}

#test stack_depth
{
  /// Stack management is consistent across calls.
  unsigned char code [] = {OP_LITERAL, 0, OP_LITERAL, 0, OP_LITERAL, 0,
                 OP_CALL, 0, OP_CALL, 0};
  e_Ref constants[] = {e_make_fixnum(1)};
  e_Selector sels[1];
  e_make_selector(sels, "add", 1);
  e_Ref res = vm_exec_constants_sels(code, 10, constants, 1, 0, sels, 1);
  fail_unless(STACK_EMPTY());
  fail_unless(e_same(res, e_make_fixnum(3)));
}

#main-pre
{
  tcase_add_checked_fixture(tc1_1, setup, teardown);
}
