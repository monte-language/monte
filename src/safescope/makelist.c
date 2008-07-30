#include "elib.h"
#include <string.h>

e_Ref makeList_dispatch(e_Ref receiver, e_Selector *selector,
                               e_Ref *args) {
  if (strncmp("run", selector->verb, 3) == 0) {
    return e_constlist_from_array(selector->arity, args);
  } else {
    return otherwise_miranda_methods(receiver, selector, args);
  }
}

e_Script e__makeList_script;
e_Method makeList_methods[] = {
  {NULL}
};

e_Ref e_makeList;
