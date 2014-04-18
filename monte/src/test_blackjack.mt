def [makeNode, NIL] := import("blackjack")
def runTests := import("unittest")


def T := true
def F := false

def makeTests(assert):
    def testBalanceRight():
        def node := makeNode(1, NIL, makeNode(2, NIL, NIL, T), F)
        def balanced := makeNode(2, makeNode(1, NIL, NIL, T), NIL, F)
        assert.equal(node.balance(), balanced)

    def testBalanceFour():
        def node := makeNode(2, makeNode(1, NIL, NIL, T), 
                                makeNode(3, NIL, NIL, T), F)
        def balanced := makeNode(2, makeNode(1, NIL, NIL, F), 
                                    makeNode(3, NIL, NIL, F), T)
        assert.equal(node.balance(), balanced)

    def testBalanceLeftFour():
        def node := makeNode(3, makeNode(2, makeNode(1, NIL, NIL, T), NIL, T), F)
        def balanced := makeNode(2, makeNode(1, NIL, NIL, F),
                                    makeNode(3, NIL, NIL, F), T)
        assert.equal(node.balance(), balanced)

    return [testBalanceRight, testBalanceFour, testBalanceLeftFour]

runTests([makeTests])
