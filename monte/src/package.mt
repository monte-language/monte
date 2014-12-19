# Loaded only to execute tests.

def unittest := pkg.testCollector()

# pkg.readFile("heap.mt")([=> unittest, ...])

def blackjack := pkg.readFile("blackjack.mt")([=> unittest])
def example := pkg.readFile("examples/testing.mt")([=> unittest])
def regionTests := pkg.readFile("test_regions.mt")([=> unittest])
def [=> makeOMeta] := pkg.readFile("ometa.mt")()
def ometaTests := pkg.readFile("test_ometa.mt")([=> makeOMeta, => unittest])
def testUnicode := pkg.readFile("test_unicode.mt")([=> unittest])
def testSwitch := pkg.readFile("test_switch.mt")([=> unittest])
def testOperators := pkg.readFile("test_operators.mt")([=> unittest])
def testTerml := pkg.readFile("test_terml.mt")([=> unittest])
pkg.makeModule(blackjack | example | ometaTests | testUnicode | regionTests | testOperators | testTerml)
