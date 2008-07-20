extern e_Script e__SwitchableRef_script;
extern e_Script e__LocalResolver_script;
extern e_Script e__UnconnectedRef_script;
e_Script refObject_script;
e_def_type_predicate(e_is_SwitchableRef, e__SwitchableRef_script);
e_def_type_predicate(e_is_LocalResolver, e__LocalResolver_script);
e_def_type_predicate(e_is_UnconnectedRef, e__UnconnectedRef_script);

typedef struct bufferedMessage {
  e_Selector *selector;
  e_Ref *args;
} bufferedMessage;

typedef struct messageBuffer {
  bufferedMessage *head;
  bufferedMessage *tail;
} messageBuffer;

typedef struct SwitchableRef_data {
  e_Ref myTarget;
  _Bool myIsSwitchable;
} SwitchableRef_data;

typedef struct LocalResolver_data {
  e_Ref myRef;
  messageBuffer *buf;
} LocalResolver_data;
