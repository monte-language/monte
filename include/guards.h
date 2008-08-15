#ifndef ECRU_GUARDS_H
#define ECRU_GUARDS_H

/// Convenience function for coercing an object with a guard.
e_Ref e_coerce(e_Ref guard, e_Ref specimen, e_Ref optEjector);

/// Create a new guard object that only passes objects with the given script.
e_Ref e_make_typeguard(e_Script *script);

/// Coercer to an integer.
e_Ref intguard_coerce(e_Ref self, e_Ref *args);
extern e_Ref e_IntGuard;
extern e_Script intguard_script;
extern e_Method intguard_methods[];

/// Coercer to a float.
extern e_Ref e_Float64Guard;

/// Coercer to a character.
extern e_Ref e_CharGuard;

/// Coerce method on BooleanGuard. Declared here because it's useful
/// on its own.
extern e_Ref e_BooleanGuard;

/// Coercer to a primitive list (mutable or otherwise).
extern e_Ref e_ListGuard;
extern e_Script listguard_script;
extern e_Method listguard_methods[];

extern e_Ref e_ConstListGuard;
extern e_Ref e_FlexListGuard;

/// Coercer to a string.
extern e_Ref e_StringGuard;

#endif
