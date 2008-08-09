#include <assert.h>
#include <stdio.h>
#include "elib.h"
#include "ecru.h"
#include "vm.h"

int main(int argc, char **argv) {
  ecru_set_up();

  ecru_module *module = ecru_load_bytecode(e_stdin, e_privilegedScope);
  if (module == NULL) {
    e_println(e_stdout, e_thrown_problem());
    return 1;
  }
  fclose(stdin);
  //e_Ref runner = ecru_make_runner();
  e_Ref vat = ecru_make_vat(e_null, "driver vat");
  ecru_vat_set_active(vat);
  e_Ref result = ecru_vat_run_method(vat, module, 0, 0);
  if (result.script != NULL) {
    e_println(e_stdout, result);
    return 0;
  } else {
    e_println(e_stdout, e_thrown_problem());
    return 1;
  }
}
