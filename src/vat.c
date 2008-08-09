#include "elib.h"
#include "vm.h"

GStaticPrivate current_vat_key = G_STATIC_PRIVATE_INIT;
e_Script ecru_vat_script;

e_Ref ecru_make_vat(e_Ref runner, char *label) {
  e_Ref vat;
  Vat_data *data = e_malloc(sizeof *data);
  data->runner = runner;
  data->label = e_make_string(label);
  data->turncounter = 0;
  vat.data.other = data;
  vat.script = &ecru_vat_script;
  return vat;
}

void ecru_vat_set_active(e_Ref vat) {
  e_Ref *current_vat = g_static_private_get(&current_vat_key);
  *current_vat = vat;
}

e_Ref ecru_current_vat() {
  e_Ref *current_vat = g_static_private_get(&current_vat_key);
  return *current_vat;
}

e_Ref ecru_vat_run_method(e_Ref vat, ecru_module *module,
                          int scriptNum, int methodNum) {
  Vat_data *data = vat.data.other;
  if (!e_same(vat, ecru_current_vat())) {
    return e_throw_cstring("Attempting to run code not in the current vat");
  }
  e_Ref result = ecru_vm_execute(scriptNum, methodNum, false,
                                 NULL, module, NULL, 0, NULL);
  data->turncounter++;
  return result;
}

void ecru_vat_set_up() {
  e_Ref *current_vat = e_malloc(sizeof *current_vat);
  *current_vat = e_null;
  g_static_private_set(&current_vat_key, current_vat, NULL);
  e_make_script(&ecru_vat_script, NULL, no_methods, "vat");
}
