#ifndef ECRU_VAT_H
#define ECRU_VAT_H

typedef struct Vat_data {
  e_Ref self;
  e_Ref runner;
  e_Ref label;
  int turncounter;
  GAsyncQueue *messageQueue;
} Vat_data;

void e__vat_set_up();
e_Ref e_make_vat(e_Ref runner, char *label);
void e_vat_set_active(e_Ref vat);
e_Ref e_current_vat();

typedef void e_Runnable_Func(e_Ref vat, void *data);

typedef struct e_Runnable_Item {
  e_Ref vat;
  e_Runnable_Func *function;
  void *data;
} e_Runnable_Item;

typedef struct e_PendingDelivery {
  e_Ref object;
  e_Selector *selector;
  e_Ref *args;
  e_Ref resolverVat;
  e_Ref resolver;
} e_PendingDelivery;

void e_vat_enqueue(e_Ref vat, e_Runnable_Func *f, void *data);
void e_vat_execute_send(e_Ref vat, void *pd);
void e_vat_sendOnly(e_Ref vat, e_Ref self, e_Selector *selector,
                    e_Ref *args);
void e_vat_send(e_Ref vat, e_Ref self, e_Selector *selector,
                   e_Ref *args, e_Ref resolverVat, e_Ref resolver);

_Bool e_vat_execute_turn(e_Ref vat);

#endif
