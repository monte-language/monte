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
  e_Ref result = ecru_vm_execute(0, 0, false, NULL, module, NULL, 0, NULL);
  if (result.script != NULL) {
    e_println(e_stdout, result);
    return 0;
  } else {
    e_println(e_stdout, e_thrown_problem());
    return 1;
  }
}
