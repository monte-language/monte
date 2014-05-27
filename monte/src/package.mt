# Loaded only to execute tests.

# def unittest := pkg.testCollector()
# def files := pkg.readFiles(".")
# def heap := files["heap"]([=> unittest, ...])

def terml := pkg.readPackage("./terml")()

pkg.makeModule(terml)
