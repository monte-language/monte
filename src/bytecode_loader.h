#ifndef BYTECODE_LOADER_H
#define BYTECODE_LOADER_H

#include <stdint.h>
///@defgroup bytecode_loader Bytecode unmarshaller
///@{

/// Types of bytecode fields.
enum bytecode_field_value_type { INTFIELD, UNUSED, STRINGFIELD };

///A key-value pair loaded from a bytecode file.
typedef struct BytecodeField {
  ///The field's key.
  uint64_t field_number;
  /// The type of the field.
  enum bytecode_field_value_type value_type;
  /// The field's value.
  union {
    /// The value for fields of type INTFIELD.
    uint64_t integer;
    /// the value for fields of type STRINGFIELD.
    GString *string;
  } value;
} BytecodeField;

/** Load a bytecode field from str, starting at idx (and setting idx
    to the index immediately after the returned field). Returns NULL
    at end of string.
*/
BytecodeField *bytecode_read_field(GString *str, int *idx);

///@}
#endif /* BYTECODE_LOADER_H */
