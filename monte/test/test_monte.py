import os

from zope.interface import implementer
from twisted.trial import unittest
from twisted.python import failure
from twisted.trial.itrial import ITestCase

import monte
from monte.runtime.load import TestCollector, buildPackage, eval as monte_eval
from monte.runtime.scope import bootScope, createSafeScope
from monte.runtime.tables import ConstMap

@implementer(ITestCase)
class MonteTestCase(object):

    failureException = unittest.FailTest

    def __init__(self, name, obj, asserts):
        self.name = name
        self.obj = obj
        self.asserts = asserts

    def shortDescription(self):
        return self.name

    def id(self):
        return self.name

    def countTestCases(self):
        return 1

    def __call__(self, result):
        return self.run(result)

    def run(self, result):
        result.startTest(self)
        try:
            self.obj.run(self.asserts)
        except RuntimeError as e:
            result.addFailure(self, failure.Failure())
        else:
            result.addSuccess(self)
        result.stopTest(self)


def testSuite():
    srcdir = os.path.join(os.path.dirname(monte.__file__), 'src')
    safeScope = createSafeScope(bootScope)
    asserts = monte_eval(open(os.path.join(srcdir, "unittest.mt")).read(), safeScope)
    tests = []
    c = TestCollector()
    pkg = buildPackage(srcdir, u"", safeScope, c)
    pkg.configure(None).load(ConstMap({}))
    testlist = sorted(c.tests.d.items())
    for (name, obj) in testlist:
        tests.append(MonteTestCase(name.bare().s, obj, asserts))
    return unittest.TestSuite(tests)
