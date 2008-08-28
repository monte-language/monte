#include "elib.h"
#include "ecru.h"

#ifndef ECRU_VM_H
#define ECRU_VM_H


extern e_Script e__reEjector_script;
extern e_Script e__rethrower_script;
extern e_Script e__reEjector_script;
extern e_Script e__returner_script;
extern e_Script e__problem_handler_script;
extern e_Script e__vmObject_script;

enum e_vm_state_enum {METHOD=0, MATCHER_PATTERN, MATCHER_BODY};
///@defgroup vm VM
///@{

/// An activation frame for the VM.
typedef struct ecru_stackframe {
  ecru_module *module;
  int pc;
  int scriptNum;
  int methodNum;
  char codeState;
  int patternEjectorNumber;
  e_Ref **ejectorBoxes;
  e_Ref *stack_bottom;
  e_Ref *stack_top;
  e_Ref *locals;
  e_Ref *frame;
  _Bool keepLast;
  struct ecru_stackframe *parent;
} ecru_stackframe;

/// The contents of an object created via bytecode.
typedef struct ecru_object {
  /// The module this object executes in.
  ecru_module *module;
  /// The index of the bytecode script for this object in the script pool.
  unsigned char scriptNum;
  /// The instance variables for this object.
  e_Ref *frame;
  int ejectorCounter;
} ecru_object;


e_Ref e_make_vmobject(ecru_module *module, int scriptIdx, e_Ref *frame);
e_def_type_predicate(e_is_vmObject, e__vmObject_script);

/// Create a bytecode script.
void ecru_make_script(ecru_script *script,
                       ecru_method *methods, int num_methods,
                       ecru_method *matchers, int num_matchers,
                       int num_slots);

e_Ref ecru_vm_execute(unsigned char scriptNum,
                       unsigned char methodNum,
                       char codeState,
                       e_Ref *frame,
                       ecru_module *module,
                       e_Ref *args,
                       int argLength,
                       ecru_stackframe **lastStackFrame);

e_Ref ecru_vm_execute_interactive(
                                   e_Ref *initials,
                                   int initialLength,
                                   unsigned char scriptNum,
                                   unsigned char methodNum,
                                   char codeState,
                                   e_Ref *frame,
                                   ecru_module *module,
                                   e_Ref *args,
                                   int argLength,
                                   ecru_stackframe **lastStackFrame);

/// contents of a rethrower
typedef struct rethrower_data {
  /// the thrown object
  e_Ref thrownObject;
} rethrower_data;

/// contents of a reEjector
typedef struct reEjector_data {
  /// the ejector number
  int ejectorNumber;
  /// the value ejected
  e_Ref ejectorValue;
} reEjector_data;

/// Create a rethrower, for try/finally blocks.
e_Ref ecru_make_rethrower(e_Ref argument);
e_def_type_predicate(e_is_rethrower, e__rethrower_script);

/// Create a re-ejector, for try/finally blocks.
e_Ref ecru_make_reEjector(int ejectorNumber, e_Ref ejectorValue);
e_def_type_predicate(e_is_reEjector, e__reEjector_script);


/// Create a returner, for try/finally blocks.
e_Ref ecru_make_returner();
e_def_type_predicate(ecru_is_returner, e__returner_script);


/// Create a problem handler.
e_Ref e_make_problem_handler(int target, int stackHeight);
e_def_type_predicate(e_is_problem_handler, e__problem_handler_script);
///@}

#endif /* ECRU_VM_H */
