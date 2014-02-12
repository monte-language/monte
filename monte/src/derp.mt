object empty:
    to derive(c):
        empty
    to isEmpty():
        true
    to nullable():
        false
    to onlyNull():
        false
    to trees():
        []

object nullSet:
    to derive(c):
        empty
    to isEmpty():
        false
    to nullable():
        true
    to onlyNull():
        true
    to trees():
        [null]

def term(ts):
    object o:
        to derive(c):
            empty
        to empty():
            false
        to nullable():
            true
        to onlyNull():
            true
        to trees():
            ts
    o

object anything:
    to derive(c):
        term([c])
    to isEmpty():
        false
    to nullable():
        false
    to onlyNull():
        false
    to trees():
        []

def ex(t):
    object o:
        to derive(c):
            if (c == t):
                term([c])
            else:
                empty
        to empty():
            false
        to nullable():
            false
        to onlyNull():
            false
        to trees():
            []
    o

def red(l, f):
    object o:
        to derive(c):
            def d := l.derive(c)
            if (d.empty()):
                return empty
            if (d.onlyNull()):
                return term([f(t) for t in d.trees()])
            return red(d, f)
        to empty():
            l.empty()
        to nullable():
            l.nullable()
        to onlyNull():
            l.onlyNull()
        to trees():
            [f(t) for t in l.trees()]
    o

def alt(a, b):
    if (a == empty):
        return b
    if (b == empty):
        return a
    object o:
        to derive(c):
            alt(a.derive(c), b.derive(c))
        to empty():
            a.empty() & b.empty()
        to nullable():
            a.nullable() | b.nullable()
        to onlyNull():
            a.onlyNull() & b.onlyNull()
        to trees():
            a.trees() + b.trees()
    return o

def cat(a, b):
    object o:
        to derive(c):
            if (a.empty()):
                return empty
            if (b == empty):
                return empty
            def da := a.derive(c)
            def l := cat(da, b)
            if (a.nullable()):
                def db := b.derive(c)
                alt(l, cat(term(a.trees()), db))
        to empty():
            a.empty() | b.empty()
        to nullable():
            a.nullable() & b.nullable()
        to onlyNull():
            a.onlyNull() & b.onlyNull()
        to trees():
            def l := [].diverge()
            for x in a.trees():
                for y in b.trees():
                    l.append([x, y])
            l
    o

def rep(l):
    if (l == empty):
        return empty
    object o:
        to derive(c):
            cat(l.derive(c), rep(l))
        to empty():
            l.empty()
        to nullable():
            true
        to onlyNull():
            false
        to trees():
            [null]
    return o

def parse(var l, cs):
    for c in cs:
        l := l.derive(c)
    l.trees()

traceln(parse(rep(ex("x")), "xxx"))
