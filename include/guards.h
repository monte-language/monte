#ifndef ECRU_GUARDS_H
#define ECRU_GUARDS_H

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

#endif
