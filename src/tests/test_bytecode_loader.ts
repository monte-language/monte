// -*- mode: c -*-
#include <stdio.h>
#include <string.h>

#include "elib.h"
#include "ecru.h"
#include "bytecodes.h"
#include "bytecode_loader.h"

void setup(void) {
  e_set_up();
}

void teardown(void) {
}

ecru_module *load_testdata(char *data, int length) {
  ecru_module *m;
  e_Ref slots[] = {e_null};
  char *names[] = {"null"};
  e_Ref scope = e_make_scope(names, slots, 1);
  GInputStream *stream = g_memory_input_stream_new_from_data(data,
                                                             length, NULL);
  m = ecru_load_bytecode(e_make_reader(stream), scope);
  if (m == NULL) {
    e_println(e_stdout, e_thrown_problem());
    fail("Exception");
  }
  return m;
}

#test integers
{
  GString *str = g_string_new("\x08\x04\x10\xec\xe8\xd2\x02");
  int idx = 0;
  BytecodeField *field1 = bytecode_read_field(str, &idx);
  fail_if(field1 == NULL);
  fail_unless(field1->field_number == 1);
  fail_unless(field1->value_type == 0);
  fail_unless(field1->value.integer == 4);
  BytecodeField *field2 = bytecode_read_field(str, &idx);
  fail_if(field2 == NULL);
  fail_unless(field2->field_number == 2);
  fail_unless(field2->value_type == 0);
  fail_unless(field2->value.integer == 5551212);
}

#test strings
{
  GString *str = g_string_new("\x1a\x03""foo");
  int idx = 0;
  BytecodeField *field1 = bytecode_read_field(str, &idx);
  fail_if(field1 == NULL);
  fail_unless(field1->field_number == 3);
  fail_unless(field1->value_type == 2);
  fail_unless(strcmp(field1->value.string->str, "foo") == 0);
  fail_unless(idx == 5);
}


#test read_empty
{
  // Test reading an empty bytecode file.
  char *data = "";
  ecru_module *m;
  e_Ref slots[] = {e_null};
  char *names[] = {"null"};
  e_Ref scope = e_make_scope(names, slots, 1);
  GInputStream *stream = g_memory_input_stream_new_from_data(data, 0, NULL);
  m = ecru_load_bytecode(e_make_reader(stream), scope);
  if (m == NULL) {
    fail(e_thrown_problem().data.gstring->str);
  }
  fail_unless(m->constants == NULL);
  fail_unless(m->constantsLength == 0);
  fail_unless(e_same(e_scope_getEvalContext(m->scope)[0], slots[0]));
  fail_unless(e_scope_getSize(m->scope) == 1);
  fail_unless(m->scriptsLength == 1);
}

#test read_ints
{
  // Test reading integer constants from a bytecode file.
  char *data = "\n\x05\x08\x00\x10\x82@";

  ecru_module *m = load_testdata(data, 7);
  fail_if(m->constants == NULL);
  fail_unless(m->constantsLength == 1);
  fail_unless(e_same(m->constants[0], e_make_fixnum(4097)));
  fail_unless(m->scriptsLength == 1);
}

#test read_string
{
  // Test reading normal strings from a bytecode file.
  char *data = "\n\n\x08\x01\x1a\x06wibble";
  ecru_module *m = load_testdata(data, 12);
  fail_unless(e_is_string(m->constants[0]));
  fail_unless(strncmp((m->constants[0].data.gstring)->str, "wibble", 6) == 0);
}

#test read_selector
{
  // Test reading selectors from a bytecode file.
  char *data = "\x12\x07\n\x03run\x10\x01";
  e_Selector sel;
  ecru_module *m = load_testdata(data, 9);
  e_make_selector(&sel, "run", 1);
  fail_unless(m->selectors[0].verb == sel.verb);
  fail_unless(m->selectors[0].arity == sel.arity);
}

#test read_float
{
  // Test reading floating-point values from a bytecode file.
  // XXX decide if 255 chars is enough for float representation
  char *data = "\n\x17\x08\x02\x1a\x13""0x1.921fb54442eeap1";
  ecru_module *m = load_testdata(data, 25);
  fail_unless(e_is_float64(m->constants[0]));
  fail_unless(*(m->constants[0].data.float64) == 0x1.921fb54442eeap1);
}

#test read_bignum
{
  char *data = "\n\r\x08\x03\x1a\t\x07\xc2`\xcf\xab\x8f\xe3U\xe9";
  ecru_module *m = load_testdata(data, 15);
  mpz_t num;
  mpz_t diff;
  mpz_init(diff);
  fail_unless(mpz_init_set_str(num, "143133631692849501673", 10) == 0);
  fail_unless(e_is_bignum(m->constants[0]));
  fail_unless(mpz_cmp(*(m->constants[0].data.bignum), num) == 0);
}

#test read_char
{
  char *data = "\n\x05\x08\x04\x10\xf0\x01";
  ecru_module *m = load_testdata(data, 7);
  fail_unless(m->constants[0].data.chr == 'x');
}

#test read_code
{

  char *data = "\x1a%\x08\x04\x12\x0f\x08\x01\x1a\x05run/1\"\x04\x05\x00\n\x00\x12\x10\x08\x00\x1a\tdoStuff/2\"\x01\x01\x1a\x12\x08\x00\x12\x0e\x08\x00\x1a\x05get/0\"\x03\x01\x05\x02\"\x10\x08\t\x1a\x05run/0\"\x05\x05\x00\x03\n\x03";
  char runCode[] = {OP_LITERAL, 0, OP_BIND, 0};
  char mainCode[] = {OP_LITERAL, 0, OP_DUP, OP_BIND, 1};
  ecru_module *m = load_testdata(data, 77);
  ecru_script *mainscript = m->scripts[0];
  ecru_script *script = m->scripts[1];
  fail_unless(m->scriptsLength == 3);
  fail_unless(script->num_methods == 2);
  fail_unless(script->num_matchers == 0);
  fail_unless(script->num_slots == 4);
  fail_unless(script->methods[0].verb == e_intern("run/1"));
  fail_unless(script->methods[0].length == 4);
  fail_unless(memcmp(script->methods[0].code, runCode, 4) == 0);
  fail_unless(script->methods[0].num_locals == 1);
  fail_unless(m->scripts[2]->methods[0].verb == e_intern("get/0"));
  fail_unless(m->scripts[2]->methods[0].length == 3);
  fail_unless(mainscript->methods[0].verb == e_intern("run/0"));
  fail_unless(memcmp(mainscript->methods[0].code, mainCode, 4) == 0);
  fail_unless(mainscript->methods[0].length == 5);
  fail_unless(mainscript->methods[0].num_locals == 9);
}

#test read_handlertable
{
  char *data = "\"!\x08\x00\x12\n\x08\x14\x10\x00\x18\x07 \x02(\x04\x1a\x05run/0\"\n\x14\x05\x05\x00\x15\x16\x03\x01\x05\x00";
  ecru_module *m = load_testdata(data, 35);
  ecru_handler_table_entry *htable = m->scripts[0]->methods[0].handlerTable;
  fail_unless(htable->type == 20);
  fail_unless(htable->stackLevel == 0);
  fail_unless(htable->target == 7);
  fail_unless(htable->start == 2);
  fail_unless(htable->end == 4);
}

#main-pre
{
  tcase_add_checked_fixture(tc1_1, setup, teardown);
}
