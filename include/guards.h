#ifndef ECRU_GUARDS_H
#define ECRU_GUARDS_H



extern e_Ref e_StringGuard;
extern e_Ref e_BooleanGuard;
extern e_Ref e_EListGuard;


/// Coercer to an integer.
e_Ref intguard_coerce(e_Ref self, e_Ref *args);
extern e_Ref e_IntGuard;
extern e_Script intguard_script;
extern e_Method intguard_methods[];

/// Coercer to a float.
e_Ref float64guard_coerce(e_Ref self, e_Ref *args);
extern e_Ref e_Float64Guard;
extern e_Script float64guard_script;
extern e_Method float64guard_methods[];

/// Coercer to a character.
extern e_Ref e_CharGuard;
extern e_Script charguard_script;
extern e_Method charguard_methods[];

/// Coerce method on BooleanGuard. Declared here because it's useful
/// on its own.
e_Ref booleanguard_coerce(e_Ref self, e_Ref *args);
extern e_Ref e_BooleanGuard;
extern e_Script booleanguard_script;
extern e_Method booleanguard_methods[];

/// Coercer to a primitive list.
e_Ref elistguard_coerce(e_Ref self, e_Ref *args);
extern e_Ref e_EListGuard;


/// Coercer to a string.
e_Ref stringguard_coerce(e_Ref self, e_Ref *args);
extern e_Script stringguard_script;
extern e_Method stringguard_methods[];
extern e_Ref e_StringGuard;

#endif
