#include <stdbool.h>
#include "elib.h"
#include "elib_private.h"

e_Ref TheViciousRef, THE_REF;


/** Produce a broken promise, i.e. one that throws its problem on every message
 *  send and produces another broken promise for every eventual send.
 */
e_Ref e_make_broken_promise(e_Ref problem) {
  e_Ref ref;
  ref.script = &e__UnconnectedRef_script;
  ref.data.refs = e_malloc(sizeof(e_Ref));
  ref.data.refs[0] = problem;
  return ref;
}


static e_Ref e_set_target(e_Ref ref, e_Ref newTarget) {
  if (e_is_ref(ref)) {
    if (e_is_SwitchableRef(ref)) {
      SwitchableRef_data *data = ref.data.other;
      if (data->switchable) {
        data->target = e_ref_target(newTarget);
        if (e_eq(ref, data->target)) {
          // XXX use UnconnectedRef
          return e_throw_cstring("Ref loop");
        } else {
          bufferedMessage *msg = data->messages;
          while (msg != NULL) {
            e_Ref vat = e_current_vat();
            e_vat_send(vat, data->target, msg->selector, msg->args,
                       msg->vat, msg->resolver);
           msg = msg->next;
          }
          return e_null;
        }
      } else {
        return e_throw_cstring("No longer switchable");
      }
    } else {
      return e_throw_cstring("Can't happen: tried to set target of a non-ref");
    }
  }
  return e_null;
}

/// Adjust a ref as needed after resolving it.
e_Ref e_ref_commit(e_Ref self) {
  if (e_is_ref(self)) {
    if (e_is_SwitchableRef(self)) {
      SwitchableRef_data *ref = self.data.other;
      e_Ref newTarget = e_ref_target(ref->target);
      ref->target = TheViciousRef;
      ref->switchable = false;
      newTarget = e_ref_target(newTarget);
      if (e_eq(newTarget, TheViciousRef)) {
        // XXX use UnconnectedRef here
        return e_throw_cstring("Ref loop");
      } else {
        return ref->target = newTarget;
      }
    }
    return e_throw_cstring("Unhandled ref type");
  }
  return e_throw_cstring("Can't happen: e_ref_commit called on a non-ref");
}

// Private function for shortening a SwitchableRef.
static void sRef_shorten(SwitchableRef_data *ref) {
  if (e_is_ref(ref->target) && (e_ref_state(ref->target) == NEAR)) {
    ref->target = e_ref_target(ref->target);
  }
}

static e_Ref sRef_isResolved(e_Ref self) {
  SwitchableRef_data *ref = self.data.other;
  if (ref->switchable) {
    return e_false;
  } else {
    sRef_shorten(ref);
    if (e_is_ref(ref->target)) {
      return e_ref_isResolved(ref->target);
    } else {
      return e_true;
    }
  }
}

e_Ref sRef_dispatch(e_Ref receiver, e_Selector *selector, e_Ref *args) {
  SwitchableRef_data *ref = receiver.data.other;
  if (ref->switchable) {
    if (selector->verb == printOn.verb) {
      e_print(args[0], e_make_string("<Promise>"));
    }
    if (selector->eventual) {
      bufferedMessage *buf = e_malloc(sizeof *buf);
      e_Selector get;
      e_make_selector(&get, "get", 1);
      e_Ref ppair = e_make_promise_pair();
      e_Ref result = e_call_1(ppair, &get, e_make_fixnum(0));
      e_Ref resolver = e_call_1(ppair, &get, e_make_fixnum(1));
      buf->vat = e_current_vat();
      buf->resolver = resolver;
      buf->selector = selector;
      buf->args = args;
      buf->next = ref->messages;
      ref->messages = buf;
      return result;
    } else {
      return e_throw_cstring("not synchronously callable");
    }
  } else {
    sRef_shorten(ref);
    return e_call(ref->target, selector, args);
  }
}

e_Script e__SwitchableRef_script;
static e_Method SwitchableRef_methods[] = {
  {NULL}
};

e_Ref LocalResolver_resolve(e_Ref self, e_Ref *args) {
  e_Ref target = args[0];
  e_Ref strict = args[1];
  LocalResolver_data *res;
  res = self.data.other;
  if (e_same(res->myRef, e_null)) {
    if (e_same(strict, e_true)) {
      return e_throw_cstring("Already resolved");
    } else {
      return e_false;
    }
  } else {
    E_ERROR_CHECK(e_set_target(res->myRef, target));
    E_ERROR_CHECK(e_ref_commit(res->myRef));
  }
  return e_true;
}

e_Ref LocalResolver_resolve_1(e_Ref self, e_Ref *args) {
  e_Ref newargs[] = { args[0], e_true };
  E_ERROR_CHECK(LocalResolver_resolve(self, newargs));
  return e_null;
}

e_Ref LocalResolver_printOn(e_Ref self, e_Ref *args) {
  E_ERROR_CHECK(e_print(args[0], e_make_string("<Resolver>")));
  return e_null;
}

e_Script e__LocalResolver_script;
static e_Method LocalResolver_methods[] = {
  {"resolve/1", LocalResolver_resolve_1},
  {"__printOn/1", LocalResolver_printOn},
  {NULL}
};

e_Script e__UnconnectedRef_script;
static e_Method UnconnectedRef_methods[] = {
  {NULL}
};

/// Create an object that will transparently forward messages to
/// another object.
e_Ref e_make_SwitchableRef() {
  e_Ref sRef, zero;
  zero.script = NULL+1; // XXX pretty bad
  zero.data.other = NULL+1;
  SwitchableRef_data *ref = e_malloc(sizeof*ref);
  ref->switchable = true;
  ref->target = zero;
  ref->messages = NULL;
  sRef.script = &e__SwitchableRef_script;
  sRef.data.other = ref;
  return sRef;
}

/// Create an object capable of changing the target of a SwitchableRef.
e_Ref e_make_LocalResolver(e_Ref ref) {
  e_Ref resolver;
  LocalResolver_data *data = e_malloc(sizeof*data);
  data->myRef = ref;
  resolver.script = &e__LocalResolver_script;
  resolver.data.other = data;
  return resolver;
}

/// Produce a SwitchableRef/Resolver pair.
e_Ref e_make_promise_pair() {
  e_Ref sRef = e_make_SwitchableRef();
  e_Ref bits[] = { sRef, e_make_LocalResolver(sRef) };
  return e_constlist_from_array(2, bits);
}

// --- Generic Ref Functions ---

_Bool e_is_ref(e_Ref maybeRef) {
	return e_is_SwitchableRef(maybeRef);
}

/// Describe the state of an E object as NEAR, EVENTUAL or BROKEN.
int e_ref_state(e_Ref ref) {
  if (e_is_SwitchableRef(ref)) {
    SwitchableRef_data *data = ref.data.other;
    if (data->switchable) {
      return EVENTUAL;
    } else {
      if ((data->target).script == &e__UnconnectedRef_script) {
        return BROKEN;
      }
      return NEAR;
    }
  } else {
    return NEAR;
  }
}

/// Retrieve the object this ref points at. (or self, if not a ref)
e_Ref e_ref_target(e_Ref self) {
  if (e_is_SwitchableRef(self)) {
    SwitchableRef_data *ref = self.data.other;
    if (ref->switchable) {
      return self;
    } else {
      return ref->target;
    }
  } else {
    return self;
  }
}

/// Determine if a ref is resolved or eventual.
e_Ref e_ref_isResolved(e_Ref self) {
  if (e_is_SwitchableRef(self)) {
    return sRef_isResolved(self);
  } else {
    return e_throw_cstring("Can't happen: called isResolved on a non-ref");
  }
}

/// Convert this resolver's ref to a broken promise.
e_Ref e_resolver_smash(e_Ref self, e_Ref problem) {
  e_Selector resolve;
  e_make_selector(&resolve, "resolve", 1);
  return e_call_1(self, &resolve, e_make_broken_promise(problem));
}

static e_Ref refObject_promise(e_Ref self, e_Ref *args) {
  return e_make_promise_pair();
}

static e_Ref refObject_isResolved(e_Ref self, e_Ref *args) {
  if (!e_is_ref(args[0])) {
    return e_true;
  } else {
    return e_ref_isResolved(args[0]);
  }
}

static e_Ref refObject_fulfillment(e_Ref self, e_Ref *args) {
  int state = e_ref_state(args[0]);
  if (state == EVENTUAL) {
    e_throw_pair("Failed: Not resolved", args[0]);
  } else if (state == BROKEN) {
    SwitchableRef_data *data = args[0].data.other;
    return e_throw(data->target.data.refs[0]);
  } else {
    return e_ref_target(args[0]);
  }
}
e_Script refObject_script;
e_Method refObject_methods[] = {{"promise/0", refObject_promise},
                                {"isResolved/1", refObject_isResolved},
                                {"fulfillment/1", refObject_fulfillment},
                                {NULL, NULL}};

void e__ref_set_up() {
  e_make_script(&e__SwitchableRef_script, sRef_dispatch,
                SwitchableRef_methods, NULL, "SwitchableRef");
  e_make_script(&e__LocalResolver_script, NULL, LocalResolver_methods,
                NULL, "LocalResolver");
  e_make_script(&e__UnconnectedRef_script, NULL, UnconnectedRef_methods,
                NULL, "UnconnectedRef");
  TheViciousRef = e_make_broken_promise(e_make_string("Caught in a forwarding loop"));
  e_make_script(&refObject_script, NULL, refObject_methods,
                NULL, "Ref");
  THE_REF.script = &refObject_script;
}

