# -*- test-case-name: epsilon.test.test_structlike -*-

class StructBehavior(object):
    __names__ = []
    __defaults__ = []

    def __init__(self, *args, **kw):
        super(StructBehavior, self).__init__()

        # Turn all the args into kwargs
        if len(args) > len(self.__names__):
            raise TypeError("Got %d positional arguments but expected no more than %d" % (len(args), len(self.__names__)))

        for n, v in zip(self.__names__, args):
            if n in kw:
                raise TypeError("Got multiple values for argument " + n)
            kw[n] = v

        # Fill in defaults
        for n, v in zip(self.__names__[::-1], self.__defaults__[::-1]):
            if n not in kw:
                kw[n] = v

        for n in self.__names__:
            if n not in kw:
                raise TypeError('Specify a value for %r' % (n,))
            setattr(self, n, kw.pop(n))

        if kw:
            raise TypeError('Got unexpected arguments: ' + ', '.join(kw))


_NOT_SPECIFIED = object()

def record(*a, **kw):
    """
    Are you tired of typing class declarations that look like this?

        class StuffInfo:
            def __init__(self, a=None, b=None, c=None, d=None, e=None,
                         f=None, g=None, h=None, i=None, j=None):
                self.a = a
                self.b = b
                self.c = c
                self.d = d
                # ...

    Epsilon can help!  That's right - for a limited time only, this function
    returns a class which provides a shortcut.  The above can be simplified
    to::

        StuffInfo = record(a=None, b=None, c=None, d=None, e=None,
                           f=None, g=None, h=None, i=None, j=None)

    if the arguments are required, rather than having defaults, it could be
    even shorter:

        StuffInfo = record('a b c d e f g h i j')

    Put more formally: C{record} optionally takes one positional argument, a
    L{str} representing attribute names as whitespace-separated identifiers; it
    also takes an arbitrary number of keyword arguments, which map attribute
    names to their default values.  If no positional argument is provided, the
    names of attributes will be inferred from the names of the defaults
    instead.
    """
    if len(a) == 1:
        attributeNames = a[0].split()
    elif len(a) == 0:
        if not kw:
            raise TypeError("Attempted to define a record with no attributes.")
        attributeNames = kw.keys()
        attributeNames.sort()
    else:
        raise TypeError("record must be called with zero or one positional arguments")

    # Work like Python: allow defaults specified backwards from the end
    defaults = []
    for attributeName in attributeNames:
        default = kw.pop(attributeName, _NOT_SPECIFIED)
        if defaults:
            if default is _NOT_SPECIFIED:
                raise TypeError("You must specify default values like in Python; backwards from the end of the argument list, with no gaps")
            else:
                defaults.append(default)
        elif default is not _NOT_SPECIFIED:
            defaults.append(default)
        else:
            # This space left intentionally blank.
            pass
    if kw:
        raise TypeError("The following defaults did not apply: %r" % (kw,))

    return type('Record<%s>' % (' '.join(attributeNames),),
                (StructBehavior,),
                dict(__names__=attributeNames,
                     __defaults__=defaults))
