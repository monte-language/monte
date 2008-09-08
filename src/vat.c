#include "elib.h"
#include "vm.h"

GStaticPrivate current_vat_key = G_STATIC_PRIVATE_INIT;
GStaticPrivate resolve_selector_key = G_STATIC_PRIVATE_INIT;
e_Script e__vat_script;

// Create a vat object.
e_Ref e_make_vat(e_Ref runner, char *label) {
  e_Ref vat;
  Vat_data *data = e_malloc(sizeof *data);
  data->runner = runner;
  data->label = e_make_string(label);
  data->turncounter = 0;
  data->messageQueue = g_async_queue_new();
  vat.data.other = data;
  vat.script = &e__vat_script;
  data->self = vat;
  return vat;
}

// process-global vat system setup
void e__vat_set_up() {
  e_make_script(&e__vat_script, NULL, no_methods, NULL, "vat");
  g_static_private_set(&current_vat_key, &e_null, NULL);

  //XXX move into thread-init function
  e_Selector *resolve = e_malloc(sizeof *resolve);
  e_make_selector(resolve, "resolve", 1);
  g_static_private_set(&resolve_selector_key, resolve, NULL);
}

// Set the current vat for this thread.
void e_vat_set_active(e_Ref vat) {
  Vat_data *v = vat.data.other;
  g_static_private_set(&current_vat_key, &(v->self), NULL);
}

// Returns the current vat for this thread.
e_Ref e_current_vat() {
  e_Ref *current_vat = g_static_private_get(&current_vat_key);
  return *current_vat;
}

// Low-level vat runnable-function enqueuing function.
void e_vat_enqueue(e_Ref vat, e_Runnable_Func *f, void *data) {
  Vat_data *v = vat.data.other;
  e_Runnable_Item *item = e_malloc(sizeof *item);
  item->vat = vat;
  item->function = f;
  item->data = data;
  g_async_queue_push(v->messageQueue, item);
}

// Function run by a vat to execute a normal message send.
void e_vat_execute_send(e_Ref vat, void *data) {
  e_PendingDelivery *pd = data;
  Vat_data *vatdata = vat.data.other;
  e_Ref result = e_call(pd->object, pd->selector, pd->args);
  if (!e_eq(pd->resolver, e_null)) {
        e_Selector *resolve = g_static_private_get(&resolve_selector_key);
    e_Ref *arg = e_malloc(sizeof *arg);
    *arg = result;
    e_vat_sendOnly(pd->resolverVat, pd->resolver, resolve, arg);
  }
  vatdata->turncounter++;
}

// Enqueue a message send, ignoring the return value.
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

// Enqueue a message send along with a resolver that will receive the reply.
void e_vat_send(e_Ref vat, e_Ref self, e_Selector *selector,
                e_Ref *args, e_Ref resolverVat, e_Ref resolver) {
    e_PendingDelivery *pd = e_malloc(sizeof *pd);
    pd->object = self;
    pd->selector = selector;
    pd->args = args;
    pd->resolverVat = resolverVat;
    pd->resolver = resolver;
    e_vat_enqueue(vat, e_vat_execute_send, pd);
}

/** Execute one turn in this vat. Must be run in this vat's thread. Returns
    whether further turns are currently pending. */
_Bool e_vat_execute_turn(e_Ref vat) {
  Vat_data *data = vat.data.other;
  e_Runnable_Item *r;
  if ((r = g_async_queue_try_pop(data->messageQueue)) != NULL) {
    if (r->function != NULL) {
      r->function(r->vat, r->data);
    }
  }
  if (g_async_queue_length(data->messageQueue) > 0) {
    return true;
  } else {
    return false;
  }
}
