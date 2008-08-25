#include "elib.h"
#include "vm.h"

e_Script ecru_vat_script;

e_Ref e_make_vat(e_Ref runner, char *label) {
  e_Ref vat;
  Vat_data *data = e_malloc(sizeof *data);
  data->runner = runner;
  data->label = e_make_string(label);
  data->turncounter = 0;
  data->messageQueue = g_async_queue_new();
  vat.data.other = data;
  vat.script = &ecru_vat_script;
  data->self = vat;
  return vat;
}


void ecru_vat_set_up() {
  e_make_script(&ecru_vat_script, NULL, no_methods, NULL, "vat");
}
