#ifndef ECRU_VAT_H
#define ECRU_VAT_H

extern GStaticPrivate current_vat_key;
extern e_Script ecru_vat_script;

typedef struct Vat_data {
  e_Ref runner;
  e_Ref label;
  int turncounter;
} Vat_data;

e_Ref ecru_make_vat(e_Ref runner, char *label);
void ecru_vat_set_active(e_Ref vat);
e_Ref ecru_current_vat();
e_Ref ecru_vat_run_method(e_Ref vat, ecru_module *module,
                          int scriptNum, int methodNum);

void ecru_vat_set_up();

#endif
