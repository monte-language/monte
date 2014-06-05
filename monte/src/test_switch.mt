module unittest
export (makeIntPatternTests)

def makeIntPatternTests(assert):

    def test_pattern_equal():
        def foo(n):
            switch (n){
                match == 0 { return 0 }
                match _    { return 1 }
            }
        assert.equal(foo(0), 0)
        assert.equal(foo(42), 1)

    def test_suchthat_pythonic():
        def foo(n):
            switch(n):
                match x ? (x < 3): 
                    return 0
                match _ :
                    return 1

        assert.equal(foo(0), 0)
        assert.equal(foo(42), 1)

    def test_suchthat_brackets():
        def foo(n):
            switch(n){
                match n ? (n < 3) { return 0 }
                match _           { return 1 }
            }
        assert.equal(foo(0), 0)
        assert.equal(foo(42), 1)

    def test_mixing_brackets():
        def foo(n):
            switch(n):
                match n ? (n < 3) { return 0 }
                match _           { return 1 }
        assert.equal(foo(0), 0)
        assert.equal(foo(42), 1)

    return [test_pattern_equal, test_suchthat_pythonic, test_suchthat_brackets,
            test_mixing_brackets]

    unittest([makeIntPatternTests])
