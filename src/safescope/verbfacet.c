#include "elib.h"
#include <string.h>

e_Ref verbFacet_dispatch(e_Ref self, e_Selector *selector, e_Ref *args) {
  e_Selector currySel;
  if (strncmp(selector->verb, "run", 3) != 0) {
    return otherwise_miranda_methods(self, selector, args);
  }
  e_make_selector(&currySel, self.data.refs[1].data.gstring->str, selector->arity);
  return e_call(self.data.refs[0], &currySel, args);
}



static e_Ref makeVerbFacet_curryCall(e_Ref self, e_Ref *args) {
  e_Ref facet;
  facet.script = &verbFacet_script;
  facet.data.refs = e_malloc(sizeof(e_Ref) * 2);
  facet.data.refs[0] = args[0];
  facet.data.refs[1] = args[1];
  return facet;

}

e_Script verbFacet_script;
e_Script e__makeVerbFacet_script;
e_Method makeVerbFacet_methods[] = {
  {"curryCall/2", makeVerbFacet_curryCall},
  {NULL}};

e_Ref e__makeVerbFacet;
