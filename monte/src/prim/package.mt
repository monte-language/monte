def unittest := pkg.testCollector()
def files := pkg.readFiles(".")

def [=> OrderedSpaceMaker,
     => OrderedRegionMaker] := files["regions"]([=> unittest])

def [=> __makeOrderedSpace,
     => charSpace,
     => intSpace,
     => floatSpace] := files["primSpaces"]([=> OrderedSpaceMaker])

pkg.makeModule([
    => __makeOrderedSpace,
    "char" => charSpace,
    "int" => intSpace,
    "float" => floatSpace])
