#include "elib.h"
#include "ref.h"
#include "scope.h"
#include <string.h>

static e_Ref scopeLayout_getSynEnv(e_Ref self, e_Ref *args) {
  Scope_data *sc = self.data.other;
  e_Ref map = e_make_flexmap(sc->names->len);
  for (int i = 0; i < sc->names->len; i++) {
    // XXX later reference some AST nodes maybe? do we care?
    char *name = g_array_index(sc->names, char *, i);
    e_Ref putArgs[] = {e_make_string(name), e_null};
    e_flexmap_put(map, putArgs);
  }
  map.script = &e__constmap_script;
  return map;
}

static e_Ref scope_getScopeLayout(e_Ref self, e_Ref *args) {
  self.script = &e__scopeLayout_script;
  return self;
}

/** Take a list of names and bind them in a new scope, shadowing existing
    definitions. */
static e_Ref scope_withOuterSlots(e_Ref self, e_Ref *args) {
  Scope_data *oldsc = self.data.other;
  e_Ref newScope = e_make_scope((char **)oldsc->names->data,
                                (e_Ref *)oldsc->slots->data,
                                oldsc->names->len);
  Scope_data *sc = newScope.data.other;
  GArray *newNames = sc->names, *newSlots = sc->slots;
  e_Ref nameList = e_coerce(e_ListGuard, args[0], e_null);
  E_ERROR_CHECK(nameList);
  e_Ref slotList = e_coerce(e_ListGuard, args[1], e_null);
  E_ERROR_CHECK(slotList);
  Flexlist_data *nameData = nameList.data.other,*slotData = slotList.data.other;
  if (nameData->size != slotData->size) {
    return e_throw_cstring("Unequal numbers of names and slots provided");
  }
  e_Ref *extraNames = nameData->elements;
  e_Ref *extraSlots = slotData->elements;
  for (int i = 0; i < nameData->size; i++) {
    e_Ref name = e_coerce(e_StringGuard, nameData->elements[i], e_null);
    E_ERROR_CHECK(name);
    for (int j = 0; j < sc->names->len; j++) {
      if (strcmp((extraNames->data).gstring->str,
                 g_array_index(sc->names, char *, j)) == 0) {
        g_array_remove_index(sc->names, j);
        g_array_remove_index(sc->slots, j);
        j--; // rescan this index since there's a new element in it
      }
    }
  }
  for (int i = 0; i < nameData->size; i++) {
    e_Ref newName = e_coerce(e_StringGuard, extraNames[i], e_null);
    E_ERROR_CHECK(newName);
    for (int j = 0; j < newName.data.gstring->len; j++) {
      if (newName.data.gstring->str[j] == '\0') {
        return e_throw_cstring("NULL characters are not allowed in"
                               "variable names");
      }
    }
    g_array_append_val(newNames, newName.data.gstring->str);
    g_array_append_val(newSlots, extraSlots[i]);
  }
  return newScope;
}

static e_Method scopeLayout_methods[] = {
  {"getSynEnv/0", scopeLayout_getSynEnv},
  {NULL}};

static e_Method scope_methods[] = {
  {"getScopeLayout/0", scope_getScopeLayout},
  {"withOuterSlots/2", scope_withOuterSlots},
  {NULL}
};

e_Script e__scope_script;
e_Script e__scopeLayout_script;

e_Ref e_make_scope(char **names, e_Ref *slots, int size) {
    Scope_data *sc = e_malloc(sizeof *sc);
    e_Ref scopeObj;
    sc->names = g_array_sized_new(false, false, sizeof (char *), size);
    sc->slots = g_array_sized_new(false, false, sizeof (e_Ref), size);
    g_array_append_vals(sc->names, names, size);
    g_array_append_vals(sc->slots, slots, size);
    scopeObj.script = &e__scope_script;
    scopeObj.data.other = sc;
    return scopeObj;
}

e_Ref *e_scope_getEvalContext(e_Ref self) {
    Scope_data *sc = self.data.other;
    return (e_Ref *)sc->slots->data;
}

int e_scope_getSize(e_Ref self) {
    Scope_data *sc = self.data.other;
    return sc->names->len;
}


char *safeScope_names[] = {
  "null", "false", "true", "throw", "__loop", "__makeList", "__makeMap",
  "__makeProtocolDesc", "__makeMessageDesc", "__makeParamDesc", "any",
  "void", "boolean", "__makeOrderedSpace", "Guard", "require",
  "__makeVerbFacet", "__MatchContext", "__is", "__splitList", "__suchThat",
  "__bind", "__extract", "__Empty", "__matchBind", "__Test", "NaN",
  "Infinity", "__identityFunc", "__makeInt", "escape", "for", "if", "try",
  "while", "__makeFinalSlot", "__makeTwine", "__makeSourceSpan",
  "__auditedBy", "near", "pbc", "PassByCopy", "DeepPassByCopy",
  "Data", "Persistent", "DeepFrozen", "int", "float64", "char",
  "String", "Twine", "TextWriter", "List", "Map", "Set", "nullOk",
  "Tuple", "__Portrayal", "notNull", "vow", "rcvr", "ref", "nocall",
  "SturdyRef", "simple__quasiParser", "twine__quasiParser",
  "rx__quasiParser", "olde__quasiParser", "e__quasiParser",
  "epatt__quasiParser", "sml__quasiParser", "term__quasiParser",
  "__equalizer", "__comparer", "Ref", "E", "promiseAllFulfilled", "EIO",
  "help", "safeScope", "__eval", "resource__uriGetter", "type__uriGetter",
  "elib__uriGetter", "elang__uriGetter", "opaque__uriGetter",
  "__abortIncarnation", "when", "import__uriGetter", "traceln"
};

char *privilegedScope_names[] = {
  "file__uriGetter", "fileURL__uriGetter", "jar__uriGetter",
  "http__uriGetter", "ftp__uriGetter", "gopher__uriGetter",
  "news__uriGetter", "captp__uriGetter", "makeCommand", "stdout",
  "stderr", "stdin", "print", "println", "interp", "entropy", "timer",
  "introducer", "identityMgr", "makeSturdyRef", "timeMachine",
  "unsafe__uriGetter", "currentVat", "rune", "awt__uriGetter",
  "swing__uriGetter", "JPanel__quasiParser", "swt__uriGetter",
  "currentDisplay", "swtGrid__quasiParser", "swtWatch", "privilegedScope"
};

void e__scope_set_up() {

  e_make_script(&e__scopeLayout_script, NULL, scopeLayout_methods,
                NULL, "ScopeLayout");
  e_make_script(&e__scope_script, NULL, scope_methods, NULL, "Scope");

  e_Ref safeScope[] = {e_make_finalslot(e_null),
                       e_make_finalslot(e_false), e_make_finalslot(e_true),
                       e_make_finalslot(e_thrower),
                       e_make_finalslot(e_looper),
                       e_make_finalslot(e_makeList),
                       e_make_finalslot(e_makeMap),
                       e_null, e_null, e_null, e_null, e_null,
                       e_make_finalslot(e_BooleanGuard),
                       e_make_finalslot(e_makeOrderedSpace),
                       e_null,
                       e_make_finalslot(e_require),
                       e_make_finalslot(e__makeVerbFacet),
                       e_null, // __MatchContext
                       e_make_finalslot(e__is),
                       e_null, //__splitList
                       e_make_finalslot(e__suchThat),
                       e_make_finalslot(e__bind),
                       e_null, e_null, e_null,
                       e_make_finalslot(e__Test),
                       e_null, e_null, e_null, e_null, e_null, e_null,
                       e_null, e_null, e_null, e_null, e_null, e_null,
                       e_null, e_null, e_null, e_null, e_null, e_null,
                       e_null, e_null,
                       e_make_finalslot(e_IntGuard),
                       e_make_finalslot(e_Float64Guard),
                       e_make_finalslot(e_CharGuard),
                       e_make_finalslot(e_StringGuard),
                       e_null, e_null, e_null, e_null, e_null, e_null,
                       e_null, e_null, e_null, e_null, e_null, e_null,
                       e_null, e_null,
                       e_make_finalslot(e_simple__quasiParser),
                       e_null, e_null, e_null,
                       e_null, e_null, e_null, e_null,
                       e_make_finalslot(e_equalizer),
                       e_make_finalslot(e_comparer),
                       e_make_finalslot(THE_REF),
                       e_make_finalslot(THE_E), e_null, e_null, e_null,
                       e_empty_ref, // safeScope, filled in below
                       e_null,
                       e_null, e_null, e_null, e_null, e_null, e_null, e_null,
                       e_make_finalslot(e_import__uriGetter),
                       e_make_finalslot(e_traceln)
  };

  e_safeScope = e_make_scope(safeScope_names, safeScope, 90);
  // self-reference is awkward
  e_Ref *_safeScope = (e_Ref *)((Scope_data *)e_safeScope.data.other)->slots->data;
  _safeScope[79] = e_make_finalslot(e_safeScope);

  e_Ref privilegedScope[] = {e_null, e_null, e_null,
                             e_null, e_null, e_null,
                             e_null, e_null, e_null,
                             e_make_finalslot(e_stdout),
                             e_make_finalslot(e_stderr),
                             e_make_finalslot(e_stdin),
                             e_make_finalslot(e_print_object),
                             e_make_finalslot(e_println_object),
                             e_null, e_null,
                             e_make_finalslot(e_timer),
                             e_null, e_null, e_null, e_null,
                             e_null, e_null, e_null, e_null,
                             e_null, e_null, e_null,
                             e_null, e_null, e_null, e_empty_ref,
  };
  e_Ref psSlotsList = e_constlist_from_array(32, privilegedScope);
  e_Ref psNamesList = e_flexlist_from_array(0, NULL);
  e_Selector withOuterSlots, push;
  e_make_selector(&withOuterSlots, "withOuterSlots", 2);
  e_make_selector(&push, "push", 1);
  for (int i = 0; i < 32; i++) {
    e_call_1(psNamesList, &push, e_make_string(privilegedScope_names[i]));
  }
  e_privilegedScope = e_call_2(e_safeScope, &withOuterSlots,
                             psNamesList, psSlotsList);
  e_Ref *_privilegedScope = (e_Ref *)((Scope_data *)e_privilegedScope.data.other)->slots->data;
  _privilegedScope[121] = e_make_finalslot(e_privilegedScope);

}
