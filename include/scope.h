#ifndef SCOPE_H
#define SCOPE_H

typedef struct Scope_data {
  char **names;
  e_Ref *slots;
  int size;
} Scope_data;

#endif /* SCOPE_H */
