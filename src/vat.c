#include "elib.h"
#include "vm.h"

GStaticPrivate current_vat_key = G_STATIC_PRIVATE_INIT;
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


void e__vat_set_up() {
  e_make_script(&ecru_vat_script, NULL, no_methods, NULL, "vat");
  g_static_private_set(&current_vat_key, &e_null, NULL);
}

void e_vat_set_active(e_Ref vat) {
  Vat_data *v = vat.data.other;
  g_static_private_set(&current_vat_key, &(v->self), NULL);
}

e_Ref e_current_vat() {
  e_Ref *current_vat = g_static_private_get(&current_vat_key);
  return *current_vat;
}

void e_vat_enqueue(e_Ref vat, e_Runnable_Func *f, void *data) {
  Vat_data *v = vat.data.other;
  e_Runnable_Item *item = e_malloc(sizeof *item);
  item->vat = vat;
  item->function = f;
  item->data = data;
  g_async_queue_push(v->messageQueue, item);
}

void e_vat_execute_send(e_Ref vat, void *data) {
}

void e_vat_sendOnly(e_Ref vat, e_Ref self, e_Selector *selector,
                       e_Ref *args) {
    e_PendingDelivery *pd = e_malloc(sizeof *pd);
    pd->object = self;
    pd->selector = selector;
    pd->args = args;
    pd->resolverVat = e_null;
    pd->resolver = e_null;
    e_vat_enqueue(vat, e_vat_execute_send, pd);
}
