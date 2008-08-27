#include <assert.h>
#include <stdio.h>
#include "elib.h"
#include "ecru.h"
#include "vm.h"

e_Ref e_make_vmobject(ecru_module *module, int scriptNum) {
  e_Ref obj;
  ecru_object *objdata = e_malloc(sizeof *objdata);
  objdata->module = module;
  objdata->scriptNum = scriptNum;
  objdata->frame = NULL;
  obj.script = &e__vmObject_script;
  obj.data.other = objdata;
  return obj;
}

int main(int argc, char **argv) {
  ecru_set_up();

  ecru_module *module = ecru_load_bytecode(e_stdin, e_privilegedScope);
  if (module == NULL) {
    e_println(e_stdout, e_thrown_problem());
    return 1;
  }
  fclose(stdin);
  e_Ref vat = e_make_vat(e_null, "driver vat");
  e_vat_set_active(vat);
  e_Ref obj = e_make_vmobject(module, 0);
  e_Selector run, get;
  e_make_selector(&run, "run", 0);
  e_make_selector(&get, "get", 1);
  e_Ref ppair = e_make_promise_pair();
  e_Ref result = e_call_1(ppair, &get, e_make_fixnum(0));
  e_Ref resolver = e_call_1(ppair, &get, e_make_fixnum(1));
  e_vat_send(vat, obj, &run, NULL, vat, resolver);

  while (e_vat_execute_turn(vat)) {};

  e_println(e_stdout, result);
  if (e_ref_state(result) != BROKEN) {
    return 0;
  } else {
    return 1;
  }
}
