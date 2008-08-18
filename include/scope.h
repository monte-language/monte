#ifndef SCOPE_H
#define SCOPE_H

typedef struct Scope_data {
  GArray *names; ///< Array of names, as C strings.
  GArray *slots; ///< Array of slot objects.
} Scope_data;

#endif /* SCOPE_H */
