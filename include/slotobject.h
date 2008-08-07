extern e_Script e__finalslot_script;
extern e_Script e__varslot_script;
extern e_Script e__guardedslot_script;

extern e_Method finalslot_methods[];
extern e_Method varslot_methods[];
extern e_Method guardedslot_methods[];

e_Ref e_make_finalslot(e_Ref value);
e_def_type_predicate (e_is_finalslot, e__finalslot_script);

e_Ref e_make_varslot(e_Ref value);
e_def_type_predicate (e_is_varslot, e__varslot_script);

e_Ref e_new_guardedslot(e_Ref value, e_Ref guard, e_Ref optEjector);
e_def_type_predicate(e_is_guardedslot, e__guardedslot_script);

extern _Bool e_is_slot(e_Ref specimen);
