#It's gonna be the future soon, I won't always be this way
from __future__ import absolute_import

import sys
from unittest import TestCase
from twisted.python import failure

class TestCase(TestCase):

    def assertRaises(self, exception, f, *args, **kwargs):
        """
        Fail the test unless calling the function C{f} with the given
        C{args} and C{kwargs} raises C{exception}. The failure will report
        the traceback and call stack of the unexpected exception.

        @param exception: exception type that is to be expected
        @param f: the function to call

        @return: The raised exception instance, if it is of the given type.
        @raise self.failureException: Raised if the function call does
            not raise an exception or if it raises an exception of a
            different type.
        """
        try:
            result = f(*args, **kwargs)
        except exception as inst:
            return inst
        except:
            raise self.failureException('%s raised instead of %s:\n %s'
                                        % (sys.exc_info()[0],
                                           exception.__name__,
                                           failure.Failure().getTraceback()))
        else:
            raise self.failureException('%s not raised (%r returned)'
                                        % (exception.__name__, result))
