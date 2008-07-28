#include "elib.h"

static e_Ref problem_printOn(e_Ref self, e_Ref *args) {
  e_Ref out = args[0];
  E_ERROR_CHECK(e_print(out, e_make_string("<problem ")));
  E_ERROR_CHECK(e_print(out, self.data.refs[0]));
  E_ERROR_CHECK(e_print(out, e_make_string(": ")));
  E_ERROR_CHECK(e_print_on(self.data.refs[1], out));
  E_ERROR_CHECK(e_print(out, e_make_string(">")));
  return e_null;
}

e_Ref e_make_problem(const char *complaint, e_Ref irritant) {
  e_Ref result, *data = e_malloc(2 * sizeof data[0]);
  data[0] = e_make_string(complaint);
  data[1] = irritant;
  result.script = &problem_script;
  result.data.refs = data;
  return result;
}

e_Script problem_script;
e_Method problem_methods[] = {
  { "__printOn/1", problem_printOn },
  {NULL}
};
