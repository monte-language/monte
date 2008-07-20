#include "elib.h"
#include "elib_private.h"
#include "vm.h"
#include "bytecodes.h"
#include "string.h"

e_Script e__rethrower_script = {-1, NULL, NULL};
e_Script e__reEjector_script = {-1, NULL, NULL};
e_Script e__returner_script = {-1, NULL, NULL};
e_Script e__problem_handler_script = {-1, NULL, NULL};
e_Script e__vmObject_script = {-1, NULL, NULL};

e_Method *ecru_miranda_methods;


static e_Selector do_run1, do_get0, do_get1, do_put1, do_size;

/// returners have no methods either.
static e_Method *returner_methods = no_methods;

/// Pass execution to the next unwinder, or to the problem handler.
e_Ref rethrower_run(e_Ref self, e_Ref *args) {
  rethrower_data *info = self.data.other;
  return e_throw(info->thrownObject);
}

/// Pass execution to the next unwinder, or to the ejector.
e_Ref reejector_run(e_Ref self, e_Ref *args) {
  e_Ref eject;
  reEjector_data *info = self.data.other;
  e_ejected_value = info->ejectorValue;
  eject.script = NULL;
  eject.data.fixnum = info->ejectorNumber;
  return eject;
}

static e_Method rethrower_methods[] = {{"run/1", rethrower_run},
                                       {NULL, NULL}};
/// Make a rethrower. Rethrows to the next problem handler when
/// invoked.
e_Ref ecru_make_rethrower(e_Ref argument) {
  e_Ref rethrower;
  rethrower_data *info = e_malloc(sizeof *info);
  info->thrownObject = argument;
  rethrower.script = &e__rethrower_script;
  rethrower.data.other = info;
  return rethrower;
}


static e_Method reEjector_methods[] = {{"run/1", reejector_run},
                                       {NULL, NULL}};
/// Make a re-ejector. Rethrows to the specified ejector when invoked.
e_Ref ecru_make_reEjector(int ejectorNumber, e_Ref ejectorValue) {
  e_Ref reEjector;
  reEjector_data *info = e_malloc(sizeof *info);
  reEjector.script = &e__reEjector_script;
  reEjector.data.other = info;
  info->ejectorValue = ejectorValue;
  info->ejectorNumber = ejectorNumber;
  return reEjector;
}


/// Make a returner.
e_Ref ecru_make_returner() {
  e_Ref returner;
  returner.script = &e__returner_script;
  return returner;
}

int ecru_lookup_handlerIndex(ecru_module *module, int scriptNum, int methodNum, int pc) {
  ecru_method meth = module->scripts[scriptNum]->methods[methodNum];
  ecru_handler_table_entry *ht = meth.handlerTable;
  int len = meth.handlerTableLength;
  for (int i = 0; i < len; i++) {
    if (pc >= ht[i].start && pc <= ht[i].end) {
      return i;
    }
  }
  return -1;
};

int ecru_lookup_ejectorStartIndex(ecru_module *module, int scriptNum, int methodNum, int pc) {
  ecru_method meth = module->scripts[scriptNum]->methods[methodNum];
  ecru_handler_table_entry *ht = meth.handlerTable;
  int len = meth.handlerTableLength;
  for (int i = 0; i < len; i++) {
    if (pc >= ht[i].start && pc <= ht[i].end && (ht[i].type == OP_EJECTOR || ht[i].type == OP_EJECTOR_ONLY)) {
      return i;
    }
  }
  return -1;
};

ecru_stackframe *ecru_create_stackframe(ecru_module *module,
                                          int scriptNum, int methodNum,
                                          char codeState,
                                          e_Ref *stack_bottom,
                                          e_Ref *stack_pointer,
                                          e_Ref *frame,
                                          _Bool keepLast,
                                          ecru_stackframe *parent) {
  ecru_stackframe *stackframe = e_malloc(sizeof *stackframe);
  unsigned char numHandlers = module->scripts[scriptNum]->methods[methodNum].handlerTableLength;
  int localsLength = module->scripts[scriptNum]->methods[methodNum].num_locals;
  stackframe->module = module;
  stackframe->scriptNum = scriptNum;
  stackframe->methodNum = methodNum;
  stackframe->codeState = codeState;
  stackframe->parent = parent;
  stackframe->ejectorBoxes = e_malloc(numHandlers * sizeof(e_Ref *));
  for (int i = 0; i < numHandlers; i++) {
    stackframe->ejectorBoxes[i] = NULL;
  }
  stackframe->pc = 0;
  stackframe->stack_bottom = stack_bottom;
  stackframe->stack_top = stack_pointer;
  stackframe->frame = frame;
  stackframe->keepLast = keepLast;
  stackframe->locals = e_malloc(localsLength * sizeof(e_Ref));

  // XXX this is an unfortunate hack to enable self-reference for
  // OP_BINDOBJECT/OP_VAROBJECT.
  for (int i = 0; i < localsLength; i++) {
    stackframe->locals[i].script = NULL;
    stackframe->locals[i].data.fixnum = i;
}

  return stackframe;
}

ecru_handler_table_entry *handler_table(ecru_stackframe *s) {
  switch (s->codeState) {
  case METHOD:
    return s->module->scripts[s->scriptNum]->methods[s->methodNum].handlerTable;
  case MATCHER_PATTERN:
    return s->module->scripts[s->scriptNum]->matchers[s->methodNum].patternHandlerTable;
  case MATCHER_BODY:
    return s->module->scripts[s->scriptNum]->matchers[s->methodNum].bodyHandlerTable;
  }
  return NULL;
}

int handler_table_length(ecru_stackframe *s) {
  switch (s->codeState) {
  case METHOD:
    return s->module->scripts[s->scriptNum]->methods[s->methodNum].handlerTableLength;
  case MATCHER_PATTERN:
    return s->module->scripts[s->scriptNum]->matchers[s->methodNum].patternHandlerTableLength;
  case MATCHER_BODY:
    return s->module->scripts[s->scriptNum]->matchers[s->methodNum].bodyHandlerTableLength;
  }
  return -1;
}



/** Locate the stack frame for the given exit number -- 0 indicates a throw,
    positive values an ejection. Starts at `initialEntry` in the current stack
    frame and searches upward, returning NULL when failing to locate a
    handler. Treats `foundIndex` as an out arg. */

ecru_stackframe *find_exit_stackframe(ecru_stackframe *searchStackframe,
                                       int exitNumber,
                                       int initialEntry,
                                       int *foundIndex) {
  int i = initialEntry;
  while (searchStackframe != NULL) {
    int searchPc = searchStackframe->pc;
    ecru_handler_table_entry *ht = handler_table(searchStackframe);
    int htLength = handler_table_length(searchStackframe);
    for (; i < htLength; i++) {
      // skip handlers not containing this pc
      if (searchPc < ht[i].start || searchPc-1 > ht[i].end) {
        continue;
      }
      if (ht[i].type == OP_TRY && exitNumber != 0) {
        continue;
      }
      // if this is an ejector handler, only use it if ejector numbers match
      if (ht[i].type == OP_EJECTOR || ht[i].type == OP_EJECTOR_ONLY) {
        e_Ref *box = searchStackframe->ejectorBoxes[i];
        if (exitNumber == 0 || box == NULL || box->data.fixnum != exitNumber) {
          continue;
        }
      }
      *foundIndex = i;
      return searchStackframe;
    }
    searchStackframe = searchStackframe->parent;
    i = 0;
  }
  return NULL;
}

ecru_stackframe *ecru_error_check(e_Ref ref, ecru_stackframe *stackframe) {
  int i = 0;
  stackframe = find_exit_stackframe(stackframe, ref.data.fixnum,
                                    0, &i);
  if (stackframe == NULL) {
    return NULL;
  }
  ecru_handler_table_entry *ht = handler_table(stackframe);
  stackframe->stack_top = stackframe->stack_bottom + ht[i].stackLevel;
  if (ht[i].type == OP_EJECTOR) {
    *(stackframe->stack_top)++ = e_ejected_value;
    e_ejected_value = e_empty_ref;
  } else if (ht[i].type == OP_TRY) {
    *(stackframe->stack_top)++ = e_thrown_problem;
    e_thrown_problem = e_empty_ref;
  } else if (ht[i].type == OP_UNWIND) {
    if (ref.data.fixnum == 0) {
      *stackframe->stack_top++ = e_null;
      *stackframe->stack_top++ = ecru_make_rethrower(e_thrown_problem);
      e_thrown_problem = e_empty_ref;
    } else {
      *stackframe->stack_top++ = e_null;
      *stackframe->stack_top++ = ecru_make_reEjector(ref.data.fixnum,
                                                      e_ejected_value);
      e_ejected_value = e_empty_ref;
    }
  }
  stackframe->pc = ht[i].target;
  return stackframe;
}
#define NEXT_CODEBYTE() code[pc++]; if (pc > codeLength) return e_throw_pair("Ran out of code at opcode", e_make_fixnum(op))
#define NEXT_TWO_CODEBYTES(x) code[pc] | (code[pc+1] << 8); pc += 2; if (pc > codeLength) return e_throw_pair("Ran out of code at opcode", e_make_fixnum(op))  ;

#define PUSH(v)	(*stack_pointer++ = (v))
#define POP()	(*--stack_pointer)
#define EMPTY() ((int)(stack_pointer - stackframe->stack_bottom) == 0)
#define STACK_HEIGHT() ((int)(stack_pointer - stackframe->stack_bottom))
#define SET_STACK_HEIGHT(i) (stackframe->stack_top = stack_pointer = \
                             &stackframe->stack_bottom[i]);
#define FIRST()		(stack_pointer[-1])
#define SECOND()	(stack_pointer[-2])
#define THIRD() 	(stack_pointer[-3])
#define FOURTH()	(stack_pointer[-4])
#define SET_FIRST(v)	(stack_pointer[-1] = (v))
#define SET_SECOND(v)	(stack_pointer[-2] = (v))
#define SET_THIRD(v)	(stack_pointer[-3] = (v))
#define SET_FOURTH(v)	(stack_pointer[-4] = (v))
#define POP_INTO(loc)                                                   \
  if (EMPTY()) {                                                        \
    return e_throw_pair("Stack underflow at", e_make_fixnum(pc));       \
  } else {loc = POP();};

#define ECRU_COLLECT_ARGS(sel, _args)                                  \
  e_Ref quickArgs[] = {e_empty_ref, e_empty_ref};                       \
  if (sel.arity == 0) {                                                 \
    _args = NULL;                                                       \
  } else if (sel.arity == 1) {                                          \
    POP_INTO(quickArgs[0]);                                             \
    _args = quickArgs;                                                  \
  } else if (sel.arity == 2) {                                          \
    POP_INTO(quickArgs[1]);                                             \
    POP_INTO(quickArgs[0]);                                             \
    _args = quickArgs;                                                  \
  } else {                                                              \
    _args = e_malloc(sel.arity * sizeof(e_Ref));                        \
    for (int i = sel.arity-1; i >= 0; i--) {                            \
      POP_INTO(_args[i]);                                               \
    }                                                                   \
  }                                                                     \


/** ecru_error_check will deal with all nonlocal exits that can be handled
    within this C stack frame and set things up for continuing execution. Other
    ejections/throws are given to our caller. */
#define ECRU_ERROR_CHECK(__val)                                        \
  {                                                                     \
    e_Ref _val = __val;                                                 \
    if (_val.script == NULL) {                                          \
      stackframe->pc = pc;                                              \
      stackframe->stack_top = stack_pointer;                            \
      ecru_stackframe *__stf = NULL;                                   \
      if (stackframe->codeState == MATCHER_PATTERN) {                   \
        if (_val.data.fixnum != 0 &&                                    \
            stackframe->patternEjectorNumber == _val.data.fixnum) {     \
          /* The ejector indicating pattern failure has been invoked */ \
          if (stackframe->methodNum + 1 < stackframe->module->scripts[stackframe->scriptNum]->num_matchers) { \
            stackframe->methodNum++;                                    \
            pc = 0;                                                     \
            stack_pointer = stackframe->stack_bottom;                   \
            stackframe->stack_top = stack_pointer;                      \
            goto startExecuting;                                        \
          } else {                                                      \
            _val = e_throw_pair("Unknown method",                       \
                  e_call_1(matchArgument, &do_get1, e_make_fixnum(0))); \
          }                                                             \
        }                                                               \
      }                                                                 \
      __stf = ecru_error_check(_val, stackframe);                      \
      if (__stf != NULL) {                                              \
        stackframe = __stf;                                             \
        pc = stackframe->pc;                                            \
        stack_pointer = stackframe->stack_top;                          \
        goto startExecuting;                                            \
      } else {                                                          \
        return _val;                                                    \
      }                                                                 \
    }                                                                   \
  }

#define ECRU_CALL(receiver, sel, keepLast)                              \
  {                                                                     \
    if (e_is_vmObject(receiver)) {                                      \
      ecru_object *_obj = receiver.data.other;                          \
      ecru_script *_script = _obj->module->scripts[_obj->scriptNum];    \
      int _methodNum;                                                   \
      e_Ref res = ecru_object_pre_call_setup(receiver,                  \
                                              _script, &sel,            \
                                              stackframe,               \
                                              &stack_pointer,           \
                                              &_methodNum,              \
                                              &codeState,               \
                                              NULL, true);              \
      if (_methodNum < 0) {                                             \
        ECRU_ERROR_CHECK(res);                                          \
        if (keepLast) {                                                 \
          PUSH(res);                                                    \
        }                                                               \
      } else {                                                          \
        if (codeState == MATCHER_PATTERN) {                             \
          e_Ref *_args;                                                 \
          ECRU_COLLECT_ARGS(sel, _args)                                 \
            e_Ref patternArg[] = {e_null, e_null};                      \
          patternArg[0] = e_selector_verb(&sel);                        \
          patternArg[1] = e_constlist_from_array(sel.arity, _args);     \
          matchArgument = e_constlist_from_array(2, patternArg);        \
        }                                                               \
        stackframe->pc = pc;                                            \
        frame = _obj->frame;                                            \
        stackframe = ecru_create_stackframe(_obj->module,               \
                                            _obj->scriptNum,            \
                                             _methodNum,                \
                                             codeState,                 \
                                             stack_pointer - sel.arity, \
                                             stack_pointer,             \
                                             frame,                     \
                                             keepLast,                  \
                                             stackframe);               \
        module = _obj->module;                                          \
        scriptNum = _obj->scriptNum;                                    \
        methodNum = _methodNum;                                         \
        pc = 0;                                                         \
        goto startExecuting;                                            \
      }                                                                 \
    } else {                                                            \
      e_Ref *_args;                                                     \
      ECRU_COLLECT_ARGS(sel, _args)                                     \
        stackframe->stack_top = stack_pointer;                          \
      stackframe->pc = pc;                                              \
      e_Ref result = e_call(receiver, &sel, _args);                     \
      ECRU_ERROR_CHECK(result);                                         \
      if (keepLast) {                                                   \
        PUSH(result);                                                   \
      }                                                                 \
    }                                                                   \
  }

/** Look up a method in this script and put its index into finalMethodNum or -1
    if not implemented by this script. In the latter case, if it is a Miranda
    method, call the default implementation. */
static e_Ref ecru_object_pre_call_setup(e_Ref self,
                                         ecru_script *script,
                                         e_Selector *sel,
                                         ecru_stackframe *stackframe,
                                         e_Ref **stack_pointer_addr,
                                         int *finalMethodNum,
                                         char *codeState,
                                         e_Ref *args,
                                         _Bool inVM) {
  e_Ref *stack_pointer = NULL;
  if (stack_pointer_addr != NULL) {
    stack_pointer = *stack_pointer_addr;
  }
  *codeState = METHOD;
  int _methodNum;
  int pc = 0; // to appease POP_INTO() :-/
  for (_methodNum = 0; _methodNum < script->num_methods; _methodNum++) {
    if (script->methods[_methodNum].verb == sel->verb) {
      break;
    }
  }
  /*
  if (strcmp(sel->verb, "__printOn/1") != 0) {
        e_print(e_stderr, e_make_string(sel->verb));
        e_print(e_stderr, e_make_string("("));
        e_println(e_stderr, e_make_string(")"));
  }
  */
  if (_methodNum == script->num_methods) {
    *finalMethodNum = -1;
    for (int i = 0; i < E_NUM_MIRANDA_METHODS; i++) {
      e_Method *method = ecru_miranda_methods + i;
      if (method->verb == sel->verb) {
        if (inVM) {
          ECRU_COLLECT_ARGS((*sel), args);
        }
        return method->exec_func(self, args);
      }
    }
    if (script->num_matchers > 0) {
      *codeState = MATCHER_PATTERN;
      *finalMethodNum = 0;
      return e_null;
    } else {
      return e_throw_pair("Unknown method", e_make_string(sel->verb));
    }
  }
  *finalMethodNum = _methodNum;
  return e_null;
}

static e_Ref ecru_object_respondsTo(e_Ref self, e_Ref *args) {
  ecru_object *obj = self.data.other;
  ecru_script *script = obj->module->scripts[obj->scriptNum];
  int _methodNum;
  e_Ref stringguard_args[] = {args[0], e_null};
  e_Ref str = stringguard_coerce(e_null, stringguard_args);
  E_ERROR_CHECK(str);
  e_Ref intguard_args[] = {args[1], e_null};
  e_Ref ar = intguard_coerce(e_null, intguard_args);
  E_ERROR_CHECK(ar);
  int arity = ar.data.fixnum;
  GString *original = str.data.other;
  GString *g_candidate = g_string_new(original->str);
  g_string_append_printf(g_candidate, "/%d", arity);
  const char *candidate = e_intern_find(g_candidate->str);
  if (candidate == NULL) {
    return e_false;
  }
  for (_methodNum = 0; _methodNum < script->num_methods; _methodNum++) {
    if (script->methods[_methodNum].verb == candidate) {
      return e_true;
    }
  }
  for (int i = 0; i < E_NUM_MIRANDA_METHODS; i++) {
    e_Method *method = ecru_miranda_methods + i;
    if (method->verb == candidate) {
      return e_true;
    }
  }
  return e_false;
}

static e_Ref ecru_object_call(e_Ref receiver, e_Selector *selector,
                               e_Ref *args) {
  ecru_object *obj = receiver.data.other;
  ecru_script *script = obj->module->scripts[obj->scriptNum];
  int methodNum;
  char codeState;
  e_Ref res = ecru_object_pre_call_setup(receiver, script, selector,
                                          NULL, NULL, &methodNum,
                                          &codeState, args, false);
  if (codeState == MATCHER_PATTERN) {
    e_Ref patternArgs[] = {e_null};
    e_Ref patternArg[] = {e_null, e_null};
    patternArg[0] = e_selector_verb(selector);
    patternArg[1] = e_constlist_from_array(selector->arity, args);
    patternArgs[0] = e_constlist_from_array(2, patternArg);
    args = patternArgs;
  }
  if (methodNum >= 0) {
    // TODO keep traceback information
    res = ecru_vm_execute(obj->scriptNum, methodNum, codeState,
                           obj->frame, obj->module, args,
                           selector->arity, NULL);
  }
  return res;
}

e_Ref _ecru_vm_execute(ecru_stackframe *stackframe,
                        e_Ref *args, int argLength,
                        ecru_stackframe **lastStackFrame) {
  int scriptNum, methodNum, pc = 0;
  e_Ref *constants, *scope, *locals, *frame, patternFailureEjector,
     matchArgument;
  int constantsLength, scopeLength, scriptsLength, codeLength, localsLength,
    frameLength;
  ecru_module *module;
  ecru_script **scripts;
  unsigned char *code;
  char codeState = stackframe->codeState;
  e_Ref *stack_pointer = stackframe->stack_top;

  if (codeState == MATCHER_PATTERN) {
    matchArgument = args[0];
  } else {
    // Push arguments to the stack, if any are supplied.
    for (int i = 0; i < argLength; i++) {
      PUSH(args[i]);
      args[i] = e_empty_ref;
    }
  }
  args = NULL;

 startExecuting:
  module = stackframe->module;
  scriptNum = stackframe->scriptNum;
  methodNum = stackframe->methodNum;
  codeState = stackframe->codeState;
  frame = stackframe->frame;
  constants = module->constants;
  constantsLength = module->constantsLength;
  scope = module->scope;
  scopeLength = module->scopeLength;
  scripts = module->scripts;
  scriptsLength = module->scriptsLength;
  if (codeState == MATCHER_PATTERN) {
    code = module->scripts[scriptNum]->matchers[methodNum].pattern;
    codeLength = module->scripts[scriptNum]->matchers[methodNum].patternLength;
    localsLength = module->scripts[scriptNum]->matchers[methodNum].num_locals;
    patternFailureEjector = e_make_ejector();
    stackframe->patternEjectorNumber = patternFailureEjector.data.refs[0].data.fixnum;
    PUSH(matchArgument);
    PUSH(patternFailureEjector);
  } else if (codeState == MATCHER_BODY) {
    code = module->scripts[scriptNum]->matchers[methodNum].body;
    codeLength = module->scripts[scriptNum]->matchers[methodNum].bodyLength;
    localsLength = module->scripts[scriptNum]->matchers[methodNum].num_locals;
  } else {
    code = module->scripts[scriptNum]->methods[methodNum].code;
    codeLength = module->scripts[scriptNum]->methods[methodNum].length;
    localsLength = module->scripts[scriptNum]->methods[methodNum].num_locals;
  }
  frameLength = module->scripts[scriptNum]->num_slots;
  locals = stackframe->locals;
  while (pc < codeLength) {
    unsigned char op = NEXT_CODEBYTE();
    int idx;
    switch (op) {

    case OP_DUP:
      {
        e_Ref x = FIRST();
        PUSH(x);
        break;
      }
    case OP_SWAP:
      {
        e_Ref one, two;
        POP_INTO(one);
        POP_INTO(two);
        PUSH(one);
        PUSH(two);
      }
      break;

    case OP_POP:
      (void)POP();
      break;

    case OP_ROT:
      {
        e_Ref a = FIRST();
        e_Ref b = SECOND();
        e_Ref c = THIRD();

        SET_FIRST(b);
        SET_SECOND(c);
        SET_THIRD(a);
      }
      break;

    case OP_LITERAL:
      idx = NEXT_CODEBYTE();
      if (idx >= constantsLength) {
        return e_throw_pair("idx > constantsLength in OP_LITERAL at",
                            e_make_fixnum(pc));
      }
      PUSH(constants[idx]);
      break;

    case OP_NOUN_OUTER:
      {
        e_Ref x;
        idx = NEXT_CODEBYTE();
        if (idx >= scopeLength) {
          return e_throw_pair("idx > scopeLength in OP_NOUN_OUTER at",
                              e_make_fixnum(pc));
        }
        x = scope[idx];
        ECRU_CALL(x, do_get0, true);
      }
      break;
    case OP_SLOT_OUTER:
      idx = NEXT_CODEBYTE();
      if (idx >= scopeLength) {
        return e_throw_pair("idx > scopeLength in OP_SLOT_OUTER at",
                            e_make_fixnum(pc));
      }
      PUSH(scope[idx]);
      break;

    case OP_NOUN_LOCAL:
      idx = NEXT_CODEBYTE();
      if (idx >= localsLength) {
        return e_throw_pair("idx > localsLength in OP_NOUN_LOCAL at",
                            e_make_fixnum(pc));
      }
      ECRU_CALL(locals[idx], do_get0, true);

      break;

    case OP_SLOT_LOCAL:
      idx = NEXT_CODEBYTE();
      if (idx >= localsLength) {
        return e_throw_pair("idx > localsLength in OP_SLOT_LOCAL at",
                            e_make_fixnum(pc));
      }
      PUSH(locals[idx]);
      break;

    case OP_BIND:
      {
        e_Ref val;
        idx = NEXT_CODEBYTE();
        if (idx >= localsLength) {
          return e_throw_pair("idx > localsLength in OP_BIND at",
                              e_make_fixnum(pc));
        }
        POP_INTO(val);
        locals[idx] = e_make_finalslot(val);
      }
      break;
    case OP_BINDSLOT:
      idx = NEXT_CODEBYTE();
      if (idx >= localsLength) {
        return e_throw_pair("idx > localsLength in OP_BINDSLOT at",
                            e_make_fixnum(pc));
      }
      POP_INTO(locals[idx]);
      break;

    case OP_CALL:
      {
        idx = NEXT_CODEBYTE();
        if (idx >= module->selectorsLength) {
          return e_throw_pair("idx > selectorsLength OP_CALL at",
                              e_make_fixnum(pc));
        }
        e_Ref rcvr;
        e_Selector sel = module->selectors[idx];
        POP_INTO(rcvr);
        if (ecru_is_returner(rcvr) && sel.verb == do_run1.verb) {
          continue;
        } else {
          ECRU_CALL(rcvr, sel, true);
        }
      }
      break;

    case OP_LIST_PATT:
      {
        int size = NEXT_CODEBYTE();
        e_Ref args[] = {e_null, e_null};
        e_Ref listobj;
        POP_INTO(args[1]); // optEjector
        POP_INTO(args[0]); // specimen
        listobj = elistguard_coerce(e_null, args);
        ECRU_ERROR_CHECK(listobj);
        // OK to use e_call here because it's constrained to be non-bytecode
        e_Ref listsize = e_call_0(listobj, &do_size);
        if (listsize.data.fixnum != size) {
          ECRU_ERROR_CHECK(e_ejectOrThrow(args[1],
                                           "List/pattern size mismatch",
                                           listsize));
        }
        for (int i = size-1; i >= 0; i--) {
          e_Ref value = e_call_1(listobj, &do_get1,
                                     e_make_fixnum(i));
          ECRU_ERROR_CHECK(value);
          PUSH(value);
          PUSH(args[1]);
        }
      }
      break;

    case OP_SIMPLEVARSLOT:
      {
        e_Ref value, slot;
        POP_INTO(value);
        slot = e_make_varslot(value);
        PUSH(slot);
      }
      break;

    case OP_GUARDEDVARSLOT:
      {
        e_Ref specimen, optEjector, guard;
        POP_INTO(specimen);
        POP_INTO(optEjector);
        POP_INTO(guard);
        e_Ref slot = e_new_guardedslot(specimen, guard, optEjector);
        ECRU_ERROR_CHECK(slot);
        PUSH(slot);
      }
      break;

    case OP_COERCETOSLOT:
      {
        e_Ref specimen, optEjector;
        POP_INTO(optEjector);
        POP_INTO(specimen);
        // TODO actual coercion protocol
        if (e_is_slot(specimen)) {
          PUSH(specimen);
        } else {
          e_ejectOrThrow(optEjector, "Not a slot: ", specimen);
        }
      }
      break;

    case OP_ASSIGN_LOCAL:
      {
        idx = NEXT_CODEBYTE();
        if (idx >= localsLength) {
         return e_throw_pair("idx > localsLength in OP_ASSIGN_LOCAL at",
                             e_make_fixnum(pc));
        }
        ECRU_CALL(locals[idx], do_put1, false);
      }
      break;

    case OP_EJECTOR:
    case OP_EJECTOR_ONLY:
      {
        idx = NEXT_TWO_CODEBYTES();
        e_Ref ej = e_make_ejector();
        int handlerIndex = ecru_lookup_ejectorStartIndex(stackframe->module,
                                                          stackframe->scriptNum,
                                                          stackframe->methodNum,
                                                          pc);
        stackframe->ejectorBoxes[handlerIndex] = ej.data.refs;
        PUSH(ej);
      }
      break;
    case OP_UNWIND:
    case OP_TRY:
      pc += 2;
      break;
    case OP_END_HANDLER:
      {
        int handlerIndex = ecru_lookup_handlerIndex(stackframe->module,
                                                     stackframe->scriptNum,
                                                     stackframe->methodNum,
                                                     pc-1);
        ecru_handler_table_entry *h = module->scripts[scriptNum]->methods[methodNum].handlerTable;
        e_Ref *box = stackframe->ejectorBoxes[handlerIndex];
        if (box != NULL) {
          *box = e_empty_ref;
        }
        if (h[handlerIndex].type == OP_UNWIND) {
          PUSH(ecru_make_returner());
        }
      }
      break;
    case OP_JUMP:
      {
        idx = NEXT_TWO_CODEBYTES();
        pc += idx;
      }
      break;
    case OP_BRANCH:
      {
        e_Ref res;
        e_Ref args[] = {e_null, e_null};
        POP_INTO(args[0]); // specimen
        POP_INTO(args[1]); // optEjector
        res = booleanguard_coerce(e_null, args);
        ECRU_ERROR_CHECK(res);
        if (e_same(res, e_false)) {
          if (e_same(args[1], e_null)) {
            e_throw_pair("No ejector provided for branch at pc:",
                         e_make_fixnum(pc));
          } else {
            PUSH(args[0]);
            ECRU_CALL(args[1], do_run1, false);
          }
        }
      }
      break;
    case OP_BINDOBJECT:
    case OP_VAROBJECT:
    case OP_OBJECT:
      {
        ecru_script *script;
        int frameSize;
        e_Ref *newFrame;
        ecru_object *objdata = e_malloc(sizeof *objdata);
        e_Ref obj;
        unsigned char scriptIdx;
        int selfRefIdx = -1;
        scriptIdx = 1 + NEXT_CODEBYTE();
        if (scriptIdx >= scriptsLength) {
          printf("OP_OBJECT@%d: scriptIdx > scriptsLength\n", pc);
        }
        script = scripts[scriptIdx];
        frameSize = script->num_slots;
        newFrame = e_malloc(frameSize * sizeof *newFrame);
        objdata->module = module;
        objdata->scriptNum = scriptIdx;
        objdata->frame = newFrame;
        obj.script = &e__vmObject_script;
        obj.data.other = objdata;

        if (op == OP_BINDOBJECT) {
          int localIdx = NEXT_CODEBYTE();
          locals[localIdx] = e_make_finalslot(obj);
        } else if (op == OP_VAROBJECT) {
          int localIdx = NEXT_CODEBYTE();
          locals[localIdx] = e_make_varslot(obj);
        }
        for (int i = frameSize-1; i >= 0; i--) {
          POP_INTO(newFrame[i]);
          // that self-ref hack
          if (newFrame[i].script == NULL) {
            if (selfRefIdx != -1) {
              return e_throw_pair(
                  "More than one hacked self-ref slot in OP_BINDOBJECT at",
                  e_make_fixnum(pc));
            }
            selfRefIdx = newFrame[i].data.fixnum;
            newFrame[i] = locals[selfRefIdx];
          }
        }
        PUSH(obj);
      }
      break;
    case OP_NOUN_FRAME:
      {
        idx = NEXT_CODEBYTE();
        if (idx >= frameLength) {
          printf("OP_NOUN_FRAME@%d: idx > frameLength\n", pc);

        }
        ECRU_CALL(frame[idx], do_get0, true);
      }
      break;
    case OP_ASSIGN_FRAME:
      {
        idx = NEXT_CODEBYTE();
        if (idx >= frameLength) {
          return e_throw_pair("idx > frameLength in OP_ASSIGN_FRAME at",
                              e_make_fixnum(pc));
        }

        ECRU_CALL(frame[idx], do_put1, false);
      }
      break;
    case OP_SLOT_FRAME:
      {
        idx = NEXT_CODEBYTE();
        if (idx >= frameLength) {
          return e_throw_pair("idx > frameLength in OP_SLOT_FRAME at",
                              e_make_fixnum(pc));
        }
        PUSH(frame[idx]);
      }
      break;
    default:
      return e_throw_pair("Unknown opcode at",
                          e_make_fixnum(pc));
    }

  }
  if (codeState == MATCHER_PATTERN) {
    // the pattern must have matched - execute the body
    stackframe->codeState = MATCHER_BODY;
    pc = 0;
    //stack_pointer = stackframe->stack_top =  stackframe->stack_bottom;
    goto startExecuting;
  }
  // if we're here it must be time to go up a stack frame
  if (stackframe->parent != NULL) {
    stackframe = stackframe->parent;
    pc = stackframe->pc;
       if (!stackframe->keepLast) {
         (void)POP();
      }
    goto startExecuting;
  } else {

#ifdef STACK_DEBUG
    // ifdef'd because some tests depend on stuff being left on the stack
    if (STACK_HEIGHT() != 1) {
      return e_throw_pair("Stack height at end of execution was",
                          e_make_fixnum(STACK_HEIGHT()));
    }
#endif
    e_Ref val = POP();
    stackframe->stack_top = stack_pointer;
    if (lastStackFrame != NULL) {
      *lastStackFrame = stackframe;
    }
    return val;

  }
}


/** Core bytecode execution loop, roughly corresponding to a reactor turn. A
 problem is returned if bytecode execution fails.  See smallcaps.txt for
 description of bytecode. */
e_Ref ecru_vm_execute(unsigned char scriptNum,
                       unsigned char methodNum,
                       char codeState,
                       e_Ref *frame,
                       ecru_module *module,
                       e_Ref *args, int argLength,
                       ecru_stackframe **lastStackFrame) {
  // XXX actually use stack depth computed at compile time
  e_Ref *stack_pointer = e_malloc(sizeof(e_Ref) * 100);
  ecru_stackframe *stackframe = ecru_create_stackframe(module,
                                                         scriptNum,
                                                         methodNum,
                                                         codeState,
                                                         stack_pointer,
                                                         stack_pointer,
                                                         frame,
                                                         true,
                                                         NULL);
  return _ecru_vm_execute(stackframe, args, argLength, lastStackFrame);
}

/// Alternate entry point for VM loop, for use from an interactive session.
e_Ref ecru_vm_execute_interactive(e_Ref *initials,
                                   int initialLength,
                                   unsigned char scriptNum,
                                   unsigned char methodNum,
                                   char codeState,
                                   e_Ref *frame,
                                   ecru_module *module,
                                   e_Ref *args, int argLength,
                                   ecru_stackframe **lastStackFrame) {
  // XXX actually use stack depth computed at compile time
  e_Ref *stack_pointer = e_malloc(sizeof(e_Ref) * 100);
  ecru_stackframe *stackframe = ecru_create_stackframe(module,
                                                         scriptNum,
                                                         methodNum,
                                                         codeState,
                                                         stack_pointer,
                                                         stack_pointer,
                                                         frame,
                                                         true,
                                                         NULL);
  for (int i = 0; i < initialLength; i++) {
    stackframe->locals[i] = initials[i];
  }
  return _ecru_vm_execute(stackframe, args, argLength, lastStackFrame);
}


void ecru_set_up() {
  if (!e__setup_done) {
    e_set_up();
    e_make_script(&e__rethrower_script, NULL, rethrower_methods,
                  "vm_internal_rethrower");
    e_make_script(&e__returner_script, NULL, returner_methods,
                  "vm_internal_returner");
    e_make_script(&e__reEjector_script, NULL, reEjector_methods,
                  "vm_internal_reEjector");
    e_make_script(&e__vmObject_script, &ecru_object_call,
                  no_methods, "vm_Object");
    e_make_selector(&do_run1, "run", 1);
    e_make_selector(&do_get0, "get", 0);
    e_make_selector(&do_get1, "get", 1);
    e_make_selector(&do_put1, "put", 1);
    e_make_selector(&do_size, "size", 0);
    ecru_miranda_methods = e_malloc(E_NUM_MIRANDA_METHODS
                                     * sizeof *e_miranda_methods);
    memcpy(ecru_miranda_methods, e_miranda_methods,
           E_NUM_MIRANDA_METHODS * sizeof *e_miranda_methods);
    /* __respondsTo must be special-cased since it depends on method lookup
       internals. */
    for (int i = 0; i < E_NUM_MIRANDA_METHODS; i++) {
      if (strcmp("__respondsTo/2", ecru_miranda_methods[i].verb) == 0) {
        ecru_miranda_methods[i].exec_func = ecru_object_respondsTo;
        break;
      }
    }
  }
}
