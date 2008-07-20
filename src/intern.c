/* Copyright 2003 Darius Bacon under the terms of the MIT X license
   found at http://www.opensource.org/licenses/mit-license.html */

#include <string.h>

#include "elib.h"


/* TODO: use weak refs */

typedef struct Symbol Symbol;
struct Symbol {
  const char *string;		/* Print-name */
  Symbol *next;			/* Hash bucket list link */
};

/* The hash table */
enum { num_buckets = 128 };
static Symbol *buckets[num_buckets];

/* Return the symbol named 'string', if it's in the hash table, or
   NULL otherwise. */
static Symbol *
find (Symbol *symbol, const char *string)
{
  for (; NULL != symbol; symbol = symbol->next)
    if (0 == strcmp (string, symbol->string))
      return symbol;
  return NULL;
}

/* One-at-a-Time Hash from http://burtleburtle.net/bob/hash/doobs.html */
static unsigned
hash (const char *key)
{
  const unsigned char *k = (unsigned char *)key;
  unsigned hash = 0, i;
  for (i = 0; k[i]; ++i)
    {
      hash += k[i];
      hash += hash << 10;
      hash ^= hash >> 6;
    }
  hash += hash << 3;
  hash ^= hash >> 11;
  hash += hash << 15;
  return hash % num_buckets;
}

void
e__set_up_interner (void)
{
  int i;
  for (i = 0; i < num_buckets; ++i)
    buckets[i] = NULL;
}

const char *
e_intern (const char *string)
{
  unsigned b = hash (string);
  Symbol *symbol = find (buckets[b], string);
  if (NULL == symbol)
    {
      symbol = e_malloc (sizeof *symbol);
      symbol->string = string;
      symbol->next = buckets[b];
      buckets[b] = symbol;
    }

  return symbol->string;
}

/// Used by __respondsTo to determine if a string names an existing method.
const char *e_intern_find(const char *string) {
  unsigned b = hash(string);
  Symbol *symbol = find(buckets[b], string);
  if (NULL == symbol) {
    return NULL;
  } else {
    return symbol->string;
  }
}
