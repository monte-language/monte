#ifndef ECRU_REF_PRIVATE_H
#define ECRU_REF_PRIVATE_H
extern e_Script e__SwitchableRef_script;
extern e_Script e__LocalResolver_script;
extern e_Script e__UnconnectedRef_script;
extern e_Script refObject_script;
e_def_type_predicate(e_is_SwitchableRef, e__SwitchableRef_script);
e_def_type_predicate(e_is_LocalResolver, e__LocalResolver_script);
e_def_type_predicate(e_is_UnconnectedRef, e__UnconnectedRef_script);

typedef struct bufferedMessage {
  e_Ref vat;
  e_Ref resolver;
  e_Selector *selector;
  e_Ref *args;
  struct bufferedMessage *next;
} bufferedMessage;

typedef struct SwitchableRef_data {
  e_Ref target;
  _Bool switchable;
  bufferedMessage *messages;
} SwitchableRef_data;

typedef struct LocalResolver_data {
  e_Ref myRef;
} LocalResolver_data;

#endif
