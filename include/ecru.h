#include "elib.h"

#ifndef ECRU_H
#define ECRU_H
///@defgroup vm VM
///@{
/// Information about an exit handler.
typedef struct ecru_handler_table_entry {
  /// The type of exit (corresponds to the bytecode that creates it)
  char type;
  /// The stack level to pop to when invoking this exit.
  char stackLevel;
  /// The location to jump to when invoked.
  int target;
  /// The beginning of the range in which this exit can occur.
  int start;
  /// The end of the range in which this exit can occur.
  int end;
} ecru_handler_table_entry;

/// A method implemented in bytecode.
typedef struct ecru_method {
  /// The name of this method.
  const char *verb;
  /// The bytecode for this method.
  unsigned char *code;
  /// How many bytecodes this method has.
  int length;
  /// The number of local variables to allocate when executing this
  /// method.
  unsigned char num_locals;
  /// An array of exit handler table entries for this method.
  ecru_handler_table_entry *handlerTable;
  /// The length of the exit handler table.
  unsigned char handlerTableLength;
} ecru_method;

/// A matcher implemented in bytecode.
typedef struct ecru_matcher {
  /// The bytecode for the pattern that must succeed for this matcher to run.
  unsigned char *pattern;
  /// How many bytecodes in the pattern.
  int patternLength;
  /// The bytecode for the body of this matcher.
  unsigned char *body;
  /// How many bytecodes this matcher's body has.
  int bodyLength;
  /// The number of local variables to allocate when executing this
  /// matcher.
  unsigned char num_locals;
  /// An array of exit handler table entries for this matcher's pattern.
  ecru_handler_table_entry *patternHandlerTable;
  /// The length of the exit handler table for the pattern.
  unsigned char patternHandlerTableLength;
  /// An array of exit handler table entries for this matcher's body.
  ecru_handler_table_entry *bodyHandlerTable;
  /// The length of the exit handler table for the body.
  unsigned char bodyHandlerTableLength;

} ecru_matcher;


/// The script for a bytecode object.
typedef struct ecru_script {
  /// How many methods this script has.
  int num_methods;
  /// The array of methods this script implements.
  ecru_method *methods;
  /// How many matchers this script has.
  int num_matchers;
  /// The array of matchers this script implements.
  ecru_matcher *matchers;
  /// The number of instance variables objects with this script must
  /// have.
  int num_slots;
} ecru_script;

/** The constant information associated with a group of code objects
    in the same scope. */
typedef struct ecru_module {
  /// The constant pool for this module.
  e_Ref *constants;
  /// The length of the constant pool.
  unsigned char constantsLength;
  /// The selectors pool for this module.
  e_Selector *selectors;
  /// The length of the selector pool.
  unsigned char selectorsLength;
  /// The outer scope for this module.
  e_Ref scope;
  /// The script pool for this module.
  ecru_script **scripts;
  /// The number of scripts in this module.
  unsigned char scriptsLength;
  /// The maximum stack depth code in this module requires.
  unsigned char stackDepth;
} ecru_module;

int ecru_lookup_handlerIndex(ecru_module *module, int scriptNum, int methodNum, int pc);
int ecru_lookup_ejectorStartIndex(ecru_module *module, int scriptNum, int methodNum, int pc);

/// Load a bytecode file and create a module from it with the given scope.
ecru_module *ecru_load_bytecode(e_Ref reader, e_Ref scope);

/** Load the data structures required by the VM as well as the rest of the E
    runtime. */
void ecru_set_up();
///@}
#endif /* ECRU_H */
