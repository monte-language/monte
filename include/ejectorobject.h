#ifndef ECRU_EJECTOR_H
#define ECRU_EJECTOR_H

extern e_Script e__ejector_script;
extern e_Method ejector_methods[];

e_def_type_predicate(e_is_ejector, e__ejector_script);

e_Ref e_make_ejector();
e_Ref ejector_run(e_Ref self, e_Ref *args);

/// Disable an ejector object.
void e_ejector_disable(e_Ref self);

e_Ref e_ejectOrThrow(e_Ref optEjector, const char *complaint, e_Ref irritant);
e_Ref e_ejectOrThrow_problem(e_Ref optEjector, e_Ref problem);

#endif
