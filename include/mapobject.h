#ifndef ECRU_MAP_H
#define ECRU_MAP_H

extern e_Script e__flexmap_script;
extern e_Script e__constmap_script;
extern e_Method flexmap_methods[];
extern e_Method constmap_methods[];

e_Ref e_make_flexmap (int initial_size);
e_Ref e_make_constmap (int initial_size);

/// XXX arguably these should be not be public.
e_Ref e_flexmap_put(e_Ref self, e_Ref *args);
e_Ref e_flexmap_removeKey(e_Ref self, e_Ref *args);

typedef struct Flexmap_data {
  int size;		 /**< count of associations elements can hold, > 0 */
  int occupancy;		/**< count of associations stored */
  e_Ref *keys;
  e_Ref *values;
} Flexmap_data;


e_def_type_predicate (e_is_flexmap, e__flexmap_script);
e_def_type_predicate (e_is_constmap, e__constmap_script);

#endif
