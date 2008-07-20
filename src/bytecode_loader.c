#include <stdio.h>
#include "string.h"
#include "elib.h"
#include "ecru.h"
#include "bytecode_loader.h"

#if OLD_GIO
#include <gio/ginputstream.h>
#endif


static int read_b128int(GString *str,
                        int *idx,
                        uint64_t *result) {
  char *buffer = str->str;
  int len = str->len;
  int pos = 0;
  *result = 0;
  guchar byte = 0;
  while (*idx <= len) {
    if (pos >= 64) {
      e_die(e_make_problem("Integer value of greater than 64 bits"
                           "is too big to be represented", e_null));
      return 0;
    }
    byte = buffer[*idx];
    *result |= (byte & 0x7f) << pos;
    pos += 7;
    *idx += 1;
    if (!(byte & 0x80)) {
      return 1;
    }
  }
  e_die(e_make_problem("Truncated integer in bytecode", e_null));
  return 0;
}

static int read_string(GString *str,
                       int *idx,
                       GString **result) {
  char *buffer = str->str;
  int len = str->len;
  uint64_t stringSize;
  char *stringBuf;
  int win = read_b128int(str, idx, &stringSize);
  if (!win || *idx + stringSize > len) {
    return 0;
  }
  stringBuf = g_malloc(stringSize * sizeof(gchar *));
  memcpy(stringBuf, buffer + *idx, stringSize);
  *idx += stringSize;
  *result = g_string_new_len(stringBuf, stringSize);
  return 1;
}

static int64_t zzd(uint64_t val) {
  if (val & 1) {
    return (val / 2) ^ -1;
  }
  return (val / 2);
}

BytecodeField *bytecode_read_field(GString *str, int *idx) {
  char *buffer = str->str;
  int len = str->len;
  if (len == 0 || *idx == len) {
    return NULL;
  }
  BytecodeField *field = e_malloc(sizeof *field);
  guchar field_and_type = buffer[*idx];
  *idx += 1;
  field->field_number = field_and_type >> 3;
  field->value_type = field_and_type & 0x7;
  if (field->value_type == 0) {
    if (!read_b128int(str, idx, &field->value.integer)) {
      return NULL;
    }
  } else if (field->value_type == 2) {
    if (!read_string(str, idx, &field->value.string)) {
      return NULL;
    }
  } else {
    e_die(e_make_problem("Unhandled field type tag",
                         e_make_fixnum(field->value_type)));
    return NULL;
  }
  return field;
}

void ecru_make_script(ecru_script *script, ecru_method *methods,
                       int num_methods, ecru_matcher *matchers,
                       int num_matchers, int num_slots) {
  script->num_methods = num_methods;
  script->methods = methods;
  script->num_slots = num_slots;
  script->matchers = matchers;
  script->num_matchers = num_matchers;
}


static e_Ref ecru_readConstant(GString *str) {
  int idx = 0;
  int typeTag;
  int intContents;
  GString *stringContents;
  while (idx < str->len) {
    BytecodeField *field = bytecode_read_field(str, &idx);
    switch (field->field_number) {
    case 1:
      if (field->value_type != INTFIELD) {
        return e_throw_cstring("Type mismatch reading constant");
      }
      typeTag = field->value.integer;
      break;
    case 2:
      if (field->value_type != INTFIELD) {
        return e_throw_cstring("Type mismatch reading constant");
      }
      intContents = zzd(field->value.integer);
      break;
    case 3:
      if (field->value_type != STRINGFIELD) {
        return e_throw_cstring("Type mismatch reading constant");
      }
      stringContents = field->value.string;
    }
  }
  switch (typeTag) {
  case 0:
    return e_make_fixnum(intContents);
  case 1:
    return e_make_gstring(stringContents);
  case 2:
    {
      char *floatend;
      double result = g_strtod(stringContents->str, &floatend);
      if (floatend != (stringContents->str + stringContents->len)) {
        return e_throw_cstring("Premature end of file reading float64");
      }
      return e_make_float64(result);
    }
  case 3:
    {
      mpz_t *bignum = e_malloc(sizeof *bignum);
      mpz_init(*bignum);
      // XXX bignums are represented in big-endian format because Java
      // outputs them that way, though everything else is
      // little-endian. Inconsistency is ensaddening.
      mpz_import(*bignum, stringContents->len, 1, sizeof(char), 1, 0,
                 stringContents->str);
      return e_make_bignum(bignum);
    }
  case 4:
    return e_make_char(intContents);
  default:
    {
      return e_throw_pair("Unrecognized type tag", e_make_fixnum(typeTag));
    }
  }
}

e_Ref ecru_readSelector(GString *str) {
  e_Ref result = e_null; // until a script for selector objs gets written
  e_Selector *sel = e_malloc(sizeof (*sel));
  char *name;
  int arity;
  int idx = 0;
  while (idx < str->len) {
    BytecodeField *field = bytecode_read_field(str, &idx);
    switch (field->field_number) {
    case 1:
      if (field->value_type != STRINGFIELD) {
        return e_throw_cstring("Type mismatch reading selector");
      }
      name = field->value.string->str;
      // going from a length-prefixed to a NULL-terminated API, so check
      for (int i = 0; i < field->value.string->len; i++) {
        if (name[i] == '\0') {
          return e_throw_cstring("a NULL character is not allowed in"
                                 " selector names");
        }
      }
      break;
    case 2:
      if (field->value_type != INTFIELD) {
        return e_throw_cstring("Type mismatch reading selector");
      }
      arity = field->value.integer;
      break;
    }
  }
  e_make_selector(sel, name, arity);
  result.data.other = sel;
  return result;
}


e_Ref ecru_readHandlerTable(GString *str) {
  e_Ref result = e_null;
  int idx = 0;
  ecru_handler_table_entry *handlerTable = e_malloc(sizeof *handlerTable);
  while (idx < str->len) {
    BytecodeField *field = bytecode_read_field(str, &idx);
    if (field->value_type != INTFIELD) {
      e_die(e_make_problem("Type mismatch reading handler table", e_null));
    }
    switch (field->field_number) {
    case 1:
      handlerTable->type = field->value.integer;
    case 2:
      handlerTable->stackLevel = field->value.integer;
    case 3:
      handlerTable->target = field->value.integer;
    case 4:
      handlerTable->start = field->value.integer;
    case 5:
      handlerTable->end = field->value.integer;
    }
  }
  result.data.other = handlerTable;
  return result;
}

e_Ref ecru_readMethod(GString *str) {
  e_Ref result = e_null;
  int idx = 0;
  int num_locals = 0;
  GString *verb, *sub, *code;
  e_Ref htable = e_flexlist_from_array(0, NULL);
  ecru_method *method = e_malloc(sizeof *method);
  e_Selector do_push, do_size;
  e_make_selector(&do_push, "push", 1);
  e_make_selector(&do_size, "size", 0);
  while (idx < str->len) {
    BytecodeField *field = bytecode_read_field(str, &idx);
    switch (field->field_number) {
    case 1:
      if (field->value_type != INTFIELD) {
        e_die(e_make_problem("Type mismatch reading method", e_null));
      }
      num_locals = field->value.integer;
      break;
    case 2:
      if (field->value_type != STRINGFIELD) {
        e_die(e_make_problem("Type mismatch reading method", e_null));
      }
      sub = field->value.string;
      e_call_1(htable, &do_push, ecru_readHandlerTable(sub));
      break;
    case 3:
      if (field->value_type != STRINGFIELD) {
        e_die(e_make_problem("Type mismatch reading method", e_null));
      }
      verb = field->value.string;
      break;
    case 4:
      if (field->value_type != STRINGFIELD) {
        e_die(e_make_problem("Type mismatch reading method", e_null));
      }
      code = field->value.string;
      break;
    }
  }
  method->num_locals = num_locals;
  method->handlerTableLength = e_call_0(htable, &do_size).data.fixnum;
  if (method->handlerTableLength == 0) {
    method->handlerTable = NULL;
  } else {
    method->handlerTable = e_malloc(sizeof(ecru_handler_table_entry) *
                                    method->handlerTableLength);
    e_Ref *handlerTableList = ((Flexlist_data *)htable.data.other)->elements;
    for (int i = 0; i < method->handlerTableLength; i++) {
      method->handlerTable[i] = *(ecru_handler_table_entry *)(handlerTableList[i].data.other);
    }
  }
  // going from a length-prefixed to a NULL-terminated API, so check
  for (int i = 0; i < verb->len; i++) {
    if (verb->str[i] == '\0') {
      return e_throw_cstring("a NULL character is not allowed in"
                             " method names");
    }
  }
  method->verb = e_intern(verb->str);
  method->length = code->len;
  method->code = code->str;
  result.data.other = method;
  return result;
}

e_Ref ecru_readMatcher(GString *str) {
  e_Ref result = e_null;
  int idx = 0;
  int num_locals = 0;
  GString *pattern, *body, *sub;
  e_Ref bodyHTable = e_flexlist_from_array(0, NULL);
  e_Ref patternHTable = e_flexlist_from_array(0, NULL);
  ecru_matcher *matcher = e_malloc(sizeof *matcher);
  e_Selector do_push, do_size;
  e_make_selector(&do_push, "push", 1);
  e_make_selector(&do_size, "size", 0);
  while (idx < str->len) {
    BytecodeField *field = bytecode_read_field(str, &idx);
    switch (field->field_number) {
    case 1:
      if (field->value_type != INTFIELD) {
        e_die(e_make_problem("Type mismatch reading matcher", e_null));
      }
      num_locals = field->value.integer;
      break;
    case 2:
      if (field->value_type != STRINGFIELD) {
        e_die(e_make_problem("Type mismatch reading matcher", e_null));
      }
      sub = field->value.string;
      e_call_1(patternHTable, &do_push, ecru_readHandlerTable(sub));
      break;
    case 3:
      if (field->value_type != STRINGFIELD) {
        e_die(e_make_problem("Type mismatch reading matcher", e_null));
      }
      sub = field->value.string;
      e_call_1(bodyHTable, &do_push, ecru_readHandlerTable(sub));
      break;
    case 4:
      if (field->value_type != STRINGFIELD) {
        e_die(e_make_problem("Type mismatch reading method", e_null));
      }
      pattern = field->value.string;
      break;
    case 5:
      if (field->value_type != STRINGFIELD) {
        e_die(e_make_problem("Type mismatch reading method", e_null));
      }
      body = field->value.string;
      break;
    }
  }
  matcher->num_locals = num_locals;
  matcher->patternHandlerTableLength = e_call_0(patternHTable,
                                                &do_size).data.fixnum;
  if (matcher->patternHandlerTableLength == 0) {
    matcher->patternHandlerTable = NULL;
  } else {
    matcher->patternHandlerTable = e_malloc(sizeof(ecru_handler_table_entry) *
                                            matcher->patternHandlerTableLength);
    e_Ref *handlerTableList = ((Flexlist_data *)patternHTable.data.other
                               )->elements;
    for (int i = 0; i < matcher->patternHandlerTableLength; i++) {
      matcher->patternHandlerTable[i] = *(ecru_handler_table_entry *)handlerTableList[i].data.other;
    }
  }
  matcher->bodyHandlerTableLength = e_call_0(bodyHTable, &do_size).data.fixnum;
  if (matcher->bodyHandlerTableLength == 0) {
    matcher->bodyHandlerTable = NULL;
  } else {
    matcher->bodyHandlerTable = e_malloc(sizeof(ecru_handler_table_entry) *
                                            matcher->bodyHandlerTableLength);
    e_Ref *handlerTableList = ((Flexlist_data *)bodyHTable.data.other
                               )->elements;
    for (int i = 0; i < matcher->bodyHandlerTableLength; i++) {
      matcher->bodyHandlerTable[i] = *(ecru_handler_table_entry *)handlerTableList[i].data.other;
    }
  }

  matcher->bodyLength = body->len;
  matcher->body = body->str;
  matcher->patternLength = pattern->len;
  matcher->pattern = pattern->str;
  result.data.other = matcher;
  return result;
}


e_Ref ecru_readScript(GString *str) {
  e_Ref result = e_null;
  int num_slots = 0;
  GString *sub;
  int idx = 0;
  int num_methods, num_matchers;
  e_Ref methods = e_flexlist_from_array(0, NULL);
  e_Ref matchers = e_flexlist_from_array(0, NULL);
  e_Selector do_push, do_size;
  ecru_script *script = e_malloc(sizeof *script);
  e_make_selector(&do_push, "push", 1);
  e_make_selector(&do_size, "size", 0);
  while (idx < str->len) {
    BytecodeField *field = bytecode_read_field(str, &idx);
    switch (field->field_number) {
    case 1:
      if (field->value_type != INTFIELD) {
        e_die(e_make_problem("Type mismatch reading script", e_null));
      }
      num_slots = field->value.integer;
      break;
    case 2:
      if (field->value_type != STRINGFIELD) {
        e_die(e_make_problem("Type mismatch reading script", e_null));
      }
      sub = field->value.string;
      e_call_1(methods, &do_push, ecru_readMethod(sub));
      break;
    case 3:
      if (field->value_type != STRINGFIELD) {
        e_die(e_make_problem("Type mismatch reading script", e_null));
      }
      sub = field->value.string;
      e_call_1(matchers, &do_push, ecru_readMatcher(sub));
      break;
    }
  }
  num_methods = e_call_0(methods, &do_size).data.fixnum;
  num_matchers = e_call_0(matchers, &do_size).data.fixnum;
  script->num_slots = num_slots;
  script->num_methods = num_methods;
  script->num_matchers = num_matchers;
  if (num_methods > 0) {
    e_Ref *methodobjs = ((Flexlist_data *)methods.data.other)->elements;
    script->methods = e_malloc(num_methods * sizeof(ecru_method));
    for (int i = 0; i < num_methods; i++) {
      script->methods[i] = *(ecru_method *)methodobjs[i].data.other;
    }
  }
  if (num_matchers > 0) {
    e_Ref *matcherobjs = ((Flexlist_data *)matchers.data.other)->elements;
    script->matchers = e_malloc(num_matchers * sizeof(ecru_matcher));
    for (int i = 0; i < num_matchers; i++) {
      script->matchers[i] = *(ecru_matcher *)matcherobjs[i].data.other;
    }
  }
  result.data.other = script;
  return result;
}

/** Load a bytecode file and create a module from it. Top-level code goes into
    script 0, followed by declared scripts.  */
ecru_module *ecru_load_bytecode(e_Ref reader, e_Ref scope) {
  GInputStream *stream = reader.data.other;
  GError *err = NULL;
  GString *str = g_string_sized_new(4096);
  int siz;
  char *buf;
  while (1) {
    buf = e_malloc(4096 * sizeof *buf);
    siz = g_input_stream_read(stream, buf, 4096, NULL, &err);
    if (siz == 0) {
      break;
    }
    g_string_append_len(str, buf, siz);
  }
  int idx = 0;
  ecru_module *module = e_malloc(sizeof *module);
  BytecodeField *field;
  e_Selector do_push, do_size;
  e_make_selector(&do_push, "push", 1);
  e_make_selector(&do_size, "size", 0);
  e_Ref constantpool = e_flexlist_from_array(0, NULL);
  e_Ref selectorpool = e_flexlist_from_array(0, NULL);
  e_Ref scriptpool = e_flexlist_from_array(0, NULL);
  ecru_script *mainScript = e_malloc(sizeof *mainScript);
  ecru_method *mainMethod = NULL;
  while ((field = bytecode_read_field(str, &idx)) != NULL) {
    if (field->value_type != STRINGFIELD) {
      e_die(e_make_problem("Non-string type in module field",
                           e_make_fixnum(field->field_number)));
    }
    GString* sub = field->value.string;
    if (sub->len == 0) {
      continue;
    }
    switch (field->field_number) {
    case 1:
      e_call_1(constantpool, &do_push, ecru_readConstant(sub));
      break;
    case 2:
      e_call_1(selectorpool, &do_push, ecru_readSelector(sub));
      break;
    case 3:
      e_call_1(scriptpool, &do_push, ecru_readScript(sub));
      break;
    case 4:
      mainMethod = ecru_readMethod(sub).data.other;
      break;
    default:
      // ignore unknown fields
      break;
    }
  }
  module->constantsLength = e_call_0(constantpool, &do_size).data.fixnum;
  if (module->constantsLength == 0) {
    module->constants = NULL;
  } else {
    module->constants = e_make_array(module->constantsLength);
    memcpy(module->constants,
           ((Flexlist_data *)constantpool.data.other)->elements,
           module->constantsLength * sizeof(e_Ref));
  }
  module->selectorsLength = e_call_0(selectorpool, &do_size).data.fixnum;
  if (module->selectorsLength == 0) {
    module->selectors = NULL;
  } else {
    module->selectors = e_malloc(module->selectorsLength * sizeof(e_Selector));
    e_Ref *selobjs = ((Flexlist_data *)selectorpool.data.other)->elements;
    for (int i = 0; i < module->selectorsLength; i++) {
      module->selectors[i] = *(e_Selector *)selobjs[i].data.other;
    }
  }
  module->scriptsLength = e_call_0(scriptpool, &do_size).data.fixnum + 1;
  module->scripts = e_malloc(module->scriptsLength * sizeof (ecru_script *));
  e_Ref *scriptobjs = ((Flexlist_data *)scriptpool.data.other)->elements;
  for (int i = 1; i < module->scriptsLength; i++) {
    ecru_script *script = scriptobjs[i-1].data.other;
    module->scripts[i] = script;
  }

  module->scope = e_scope_getEvalContext(scope);
  module->scopeLength = e_scope_getSize(scope);

  module->stackDepth = 0; // currently not used

  mainScript->num_methods = 1;
  mainScript->num_matchers = 0;
  mainScript->num_slots = 0;
  mainScript->methods = mainMethod;
  module->scripts[0] = mainScript;
  return module;
}
