def trace(x):
    if isinstance(x, unicode):
        x = x.encode("utf-8")
    print x,

def traceln(x):
    if isinstance(x, unicode):
        x = x.encode("utf-8")
    print x
