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

#endif
