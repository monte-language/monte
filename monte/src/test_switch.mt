module unittest
export (foo)

def foo := null

def makeIntPatternTests(assert):

    def test_equal():
        def foo(n):
            switch(n):
                match == 0 { return 0 }
                match _    { return 1 }
        assert.equal(foo(0), 0)
        assert.equal(foo(42), 1)

    def test_lessthan():
        def foo(n):
            switch(n):
                match < 3 { return 0 }
                match _   { return 1 }
        assert.equal(foo(0), 0)
        assert.equal(foo(42), 1)

    def test_overlapping():
        def foo(n):
            var out := 1
            switch(n):
                # first match wins
                match < 3  { out += 4 }
                match <= 5 { out *= 2 }
                match _    { out := 0 }
            return out
        assert.equal(foo(4), 2)
        assert.equal(foo(1), 5)
        assert.equal(foo(42), 0)
    return [test_equal, test_lessthan, test_overlapping]

unittest([makeIntPatternTests])
