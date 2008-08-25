#ifndef ECRU_VAT_H
#define ECRU_VAT_H

typedef struct Vat_data {
  e_Ref self;
  e_Ref runner;
  e_Ref label;
  int turncounter;
  GAsyncQueue *messageQueue;
} Vat_data;

void e_vat_set_up();
e_Ref e_make_vat(e_Ref runner, char *label);

#endif
