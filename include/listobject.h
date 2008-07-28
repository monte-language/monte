#ifndef ECRU_LIST_H
#define ECRU_LIST_H
e_Ref e_constlist_from_array(int size, e_Ref* contents);
e_Ref e_flexlist_from_array(int size, e_Ref* contents);

extern e_Script e__constlist_script;
extern e_Script e__flexlist_script;
extern e_Method constlist_methods[];
extern e_Method flexlist_methods[];

/// XXX probably shouldn't be public
e_Ref flexlist_snapshot(e_Ref self, e_Ref *args);
e_Ref flexlist_size(e_Ref self, e_Ref *args);
e_Ref flexlist_contains(e_Ref self, e_Ref *args);
e_Ref flexlist_with_1(e_Ref self, e_Ref *args);
e_Ref flexlist_diverge(e_Ref self, e_Ref *args);
e_Ref flexlist_push(e_Ref self, e_Ref *args);
e_Ref flexlist_iterate(e_Ref self, e_Ref *args);
e_Ref constlist_printOn(e_Ref self, e_Ref *args);

void  flexlist_setSize(e_Ref self, int newSize);

typedef struct Flexlist_data {
  int size;
  int capacity;
  e_Ref elementGuard;
  e_Ref *elements;
} Flexlist_data;

e_def_type_predicate(e_is_constlist, e__constlist_script);
e_def_type_predicate(e_is_flexlist, e__flexlist_script);

#endif
