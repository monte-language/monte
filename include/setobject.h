#ifndef ECRU_SET_H
#define ECRU_SET_H

extern e_Script e__constset_script;
extern e_Script e__flexset_script;

extern e_Method constset_methods[];
extern e_Method flexset_methods[];


e_Ref e_constset_from_array(int size, e_Ref* contents);

extern e_Script e__constset_script;
extern e_Script e__flexset_script;
e_def_type_predicate(e_is_constset, e__constset_script);

#endif
