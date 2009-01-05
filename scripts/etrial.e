#!/usr/bin/env rune

def makeTestResults := <import:com.twistedmatrix.eunit.makeTestResults>;
def makeTestLoader := <import:com.twistedmatrix.eunit.makeTestLoader>;
def makeTestSuite := <import:com.twistedmatrix.eunit.makeTestSuite>;

def runTest(testRunnable) {
  def results := makeTestResults()
  def res := testRunnable.run(results)
  for report in res.reportFailures() {
    stdout.println()
    stdout.println(report)
  }
  stdout.println(res.summary())

}
def testLoader := makeTestLoader(<file>);
def <test> {
  to get(testFQN) {
    def suite := makeTestSuite()
    for testCaseMaker in testLoader.loadTestCase(testFQN) {
      var testCase := testCaseMaker()
      for testName in testCase.collectTestMethods() {
        suite.add(testCase, testName)
        testCase := testCaseMaker()
      }
    }
    return suite
  }
}


runTest(<test>[interp.getArgs()[0]])




# def makeRunnerTest := <import:com.twistedmatrix.eunit.tests.testRunner>
# def suite2 := makeTestSuite()
# def results2 := makeTestResults()
# suite2.add(makeRunnerTest(), "test_runSuite")
# suite2.run(null, results).summary()

# Test List!!

# test runner
#  test discovery
#   retrieve tests by FQN
#    retrieve an emaker by FQN and run all the tests in the test suite in it
#    retrieve a package and collect all the emakers in it that return tests
#  updoc runner
#  updoc discovery
