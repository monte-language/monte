def unittest := pkg.testCollector()
def files := pkg.readFiles(".")

def [=> OrderedSpaceMaker,
     => OrderedRegionMaker] := files["regions"]([=> unittest])

def [=> charSpace,
     => intSpace,
      => floatSpace] := files["primSpaces"]([=> OrderedSpaceMaker])

pkg.makeModule([
    "__makeOrderedSpace" => OrderedSpaceMaker,
    "char" => charSpace,
    "int" => intSpace,
    "float" => floatSpace])
