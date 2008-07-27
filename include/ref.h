#ifndef E_REF_H
#define E_REF_H
enum e_ref_state_enum {NEAR=0, EVENTUAL, BROKEN};
e_Ref e_make_SwitchableRef();
e_Ref e_make_LocalResolver();
e_Ref e_make_promise_pair();
int e_ref_state(e_Ref ref);
_Bool e_is_ref(e_Ref maybeRef);
e_Ref e_ref_isResolved(e_Ref ref);
e_Ref e_ref_target(e_Ref ref);
e_Ref e_ref_commit(e_Ref ref);
e_Ref e_resolver_smash(e_Ref self, e_Ref problem);
extern e_Ref TheViciousRef;
extern e_Ref THE_REF;

#endif // E_REF_H
