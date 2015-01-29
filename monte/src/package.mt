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
def monte_lexer := pkg.readFile("monte_lexer.mt")([=> unittest])
def monte_ast := pkg.readFile("monte_ast.mt")([=> unittest])
pkg.makeModule(monte_ast | monte_lexer | blackjack | example | ometaTests | testUnicode | regionTests | testOperators)
