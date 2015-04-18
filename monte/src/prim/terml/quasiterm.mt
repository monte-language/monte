module __makeOrderedSpace, convertToTerm, makeTerm, makeTag, termBuilder, Term
export (makeQFunctor, makeQTerm, makeQSome, makeQDollarHole, makeQAtHole, qEmptySeq, makeQPairSeq)

object qEmptySeq:
    to reserve():
        return 0

    to startShape(values, bindings, prefix, shapeSoFar):
        return shapeSoFar

    to endShape(bindings, prefix, shape):
        pass

    to substSlice(values, indices):
        return []

    to matchBindSlice(args, specimens, bindings, indices, max):
        return 0


def makeQPairSeq(left, right):
    return object qpair:
        to getLeft():
            return left

        to getRight():
            return right

        to getSpan():
            return null

        to startShape(values, bindings, prefix, var shapeSoFar):
            shapeSoFar := left.startShape(values, bindings, prefix, shapeSoFar)
            return right.startShape(values, bindings, prefix, shapeSoFar)

        to endShape(bindings, prefix, shape):
            left.endShape(bindings, prefix, shape)
            right.endShape(bindings, prefix, shape)

        to substSlice(values, indices):
            def v := left.substSlice(values, indices) + right.substSlice(values, indices)
            return v

        to matchBindSlice(args, specimens, bindings, indices, max):
            def leftNum := left.matchBindSlice(args, specimens, bindings, indices,
                                               max - right.reserve())
            if (leftNum < 0):
                return -1
            def rightNum := right.matchBindSlice(args, specimens.slice(leftNum),
                                                 bindings, indices, max - leftNum)
            if (rightNum < 0):
                return -1
            return leftNum + rightNum

        to reserve():
            return left.reserve() + right.reserve()


def matchCoerce(val, isFunctorHole, tag):
    var result := null
    if (isFunctorHole):
        def mkt(name, data, args):
            return makeTerm(makeTag(null, name, Any), data, args, null)
        switch (val):
            match _ :Term:
                if (val.getArgs().size() != 0):
                    return null
                result := val
            match ==null:
                result := mkt("null", null, [])
            match ==true:
                result := mkt("true", null, [])
            match ==false:
                result := mkt("false", null, [])
            match v :str:
                result := mkt(v, null, [])
            match _:
                return null
    else:
        escape e:
            result := convertToTerm(val, e)
        catch _:
            return null
    if (tag == null || tag <=> result.getTag()):
        return result
    return null


def makeQTerm(functor, args):
    def coerce(termoid):
        if (termoid !~ _ :Term):
            return matchCoerce(termoid, functor.getIsFunctorHole(), functor.getTag())
        def newFunctor := matchCoerce(termoid.withoutArgs(), functor.getIsFunctorHole(), functor.getTag())
        if (newFunctor == null):
            return null
        return makeTerm(newFunctor.getTag(), newFunctor.getData(), termoid.getArgs(), termoid.getSpan())

    return object qterm:
        to isHole():
            return false

        to getFunctor():
            return functor

        to getArgs():
            return args

        to startShape(values, bindings, prefix, var shapeSoFar):
            shapeSoFar := functor.startShape(values, bindings, prefix, shapeSoFar)
            shapeSoFar := args.startShape(values, bindings, prefix, shapeSoFar)
            return shapeSoFar

        to endShape(bindings, prefix, shape):
            functor.endShape(bindings, prefix, shape)
            functor.endShape(bindings, prefix, shape)

        to substSlice(values, indices):
            def tFunctor := functor.substSlice(values, indices)[0]
            def tArgs := args.substSlice(values, indices)
            def term := makeTerm(tFunctor.getTag(), tFunctor.getData(),
                                 tArgs, tFunctor.getSpan())
            return [term]

        to matchBindSlice(values, specimens, bindings, indices, max):
            if (specimens.size() <= 0):
                return -1
            def specimen := coerce(specimens[0])
            if (specimen == null):
                return -1
            def matches := functor.matchBindSlice(values, [specimen.withoutArgs()],
                                                  bindings, indices, 1)
            if (matches <= 0):
                return -1
            if (matches != 1):
                throw("Functor may only match 0 or 1 specimen: ", matches)
            def tArgs := specimen.getArgs()
            def num := args.matchBindSlice(values, tArgs,
                                           bindings, indices, tArgs.size())
            if (tArgs.size() == num):
                if (max >= 1):
                  return 1
            return -1

        to reserve():
            return 1

def makeQFunctor(tag, data, span):
    return object qfunctor:
        to _printOn(out):
            out.print(tag.getName())

        to isHole():
            return false

        to getIsFunctorHole():
            return false

        to getTag():
            return tag

        to getData():
            return data

        to getSpan():
            return span

        to asFunctor():
            return qfunctor

        to reserve():
            return 1

        to startShape(args, bindings, prefix, shapeSoFar):
            return shapeSoFar

        to endShape(bindings, prefix, shape):
            pass

        to substSlice(values, indices):
            if (data == null):
                return [termBuilder.leafInternal(tag, null, span)]
            else:
                return [termBuilder.leafData(data, span)]

        to matchBindSlice(args, specimens, bindings, indices, max):
            if (specimens.size() <= 0):
                 return -1
            def spec := matchCoerce(specimens[0], true, tag)
            if (spec == null):
                return -1
            if (data != null):
                def otherData := spec.getData()
                if (otherData == null):
                    return -1
                if (data != otherData):
                    if ([data, otherData] =~ [_ :str, _ :str]):
                        if (data.bare() != otherData.bare()):
                            return -1
            if (max >= 1):
                return 1
            return -1


def multiget(args, num, indices, repeat):
    var result := args[num]
    for i in indices:
         if (result =~ rlist :List):
            result := rlist[i]
         else:
            if (repeat):
                return result
            throw("index out of bounds")
    return result


def multiput(bindings, holeNum, indices, newVal):
    var list := bindings
    var dest := holeNum
    for i in indices:
        if (list.size() < dest + 1):
            throw("Index out of bounds")
        var next := list[dest]
        if (next == null):
            next := [].diverge()
            list[dest] := next
        list := next
        dest := i
    var result := null
    if (list.size() > dest):
        result := list[dest]
        list[dest] := newVal
    else if (list.size() == dest):
        list.push(newVal)
    else:
        throw("what's going on in here")
    return result


def makeQDollarHole(tag, holeNum, isFunctorHole):
    return object qdollarhole:

        to isHole():
            return true

        to getTag():
            return tag

        to getHoleNum():
            return holeNum

        to getSpan():
            return null

        to getIsFunctorHole():
            return isFunctorHole

        to asFunctor():
            if (isFunctorHole):
                return qdollarhole
            else:
                return makeQDollarHole(tag, holeNum, true)

        to startShape(values, bindings, prefix, shapeSoFar):
            def t := multiget(values, holeNum, prefix, true)
            if (t =~ vals :List):
                def result := vals.size()
                if (![-1, result].contains(shapeSoFar)):
                    throw(`Inconsistent shape: $shapeSoFar vs $result`)
                return result
            return shapeSoFar

        to endShape(bindings, prefix, shape):
            pass

        to substSlice(values, indices):
            def termoid := multiget(values, holeNum, indices, true)
            def term := matchCoerce(termoid, isFunctorHole, tag)
            if (term == null):
                throw(`Term $termoid doesn't match $qdollarhole`)
            return [term]

        to matchBindSlice(args, specimens, bindings, indices, max):
            if (specimens.size() <= 0):
                return -1
            def specimen := specimens[0]
            def termoid := multiget(args, holeNum, indices, true)
            def term := matchCoerce(termoid, isFunctorHole, tag)
            if (term == null):
                throw(`Term $termoid doesn't match $qdollarhole`)
            if (term <=> specimen):
                if (max >= 1):
                    return 1
            return -1

        to reserve():
            return 1


def makeQAtHole(tag, holeNum, isFunctorHole):
    return object qathole:
        to isHole():
            return true

        to getTag():
            return tag

        to getSpan():
            return null

        to getHoleNum():
            return holeNum

        to getIsFunctorHole():
            return isFunctorHole

        to asFunctor():
            if (isFunctorHole):
                return qathole
            else:
                return makeQAtHole(tag, holeNum, true)

        to startShape(values, bindings, prefix, shapeSoFar):
            # if (bindings == null):
            #     throw("no at-holes in a value maker")
            multiput(bindings, holeNum, prefix, [].diverge())
            return shapeSoFar

        to endShape(bindings, prefix, shape):
            def bits := multiget(bindings, holeNum, prefix, false)
            multiput(bindings, holeNum, prefix, bits.slice(0, shape))

        to substSlice(values, indices):
            throw("A quasiterm with an @-hole may not be used in a value context")

        to matchBindSlice(args, specimens, bindings, indices, max):
            if (specimens.size() <= 0):
                return -1
            def spec := matchCoerce(specimens[0], isFunctorHole, tag)
            if (spec == null):
                return -1
            def oldVal := multiput(bindings, holeNum, indices, spec)
            if (oldVal == null || oldVal <=> spec):
                if (max >= 1):
                    return 1

            return -1

        to reserve():
            return 1

def inBounds(num, quant):
    switch (quant):
        match =="?":
            return num == 0 || num == 1
        match =="+":
            return num >= 1
        match =="*":
            return num >= 0
    return false

def makeQSome(subPattern, quant, span):
    return object qsome:
        to getSubPattern():
            return subPattern

        to getQuant():
            return quant

        to getSpan():
            return span
        to reserve():
            switch (quant):
                match =="?":
                    return 0
                match =="+":
                    return subPattern.reserve()
                match =="*":
                    return 0

        to startShape(values, bindings, prefix, shapeSoFar):
            return subPattern.startShape(values, bindings, prefix, shapeSoFar)

        to endShape(bindings, prefix, shape):
            return subPattern.endShape(bindings, prefix, shape)

        to substSlice(values, indices):
            def shape := subPattern.startShape(values, [], indices, -1)
            if (shape < 0):
                throw(`Indeterminate repetition: $qsome`)
            def result := [].diverge()
            for i in 0..!shape:
                result.extend(subPattern.substSlice(values, indices + [i]))
            subPattern.endShape([], indices, shape)
            if (!inBounds(result.size(), quant)):
                throw(`Improper quantity: $shape vs $quant`)
            return result.snapshot()

        to matchBindSlice(values, var specimens, bindings, indices, var max):
            def maxShape := subPattern.startShape(values, bindings, indices, -1)
            var result := 0
            var shapeSoFar := 0
            while (maxShape == -1 || shapeSoFar < maxShape):
                if (specimens.size() == 0):
                    break
                if (quant == "?" && result > 0):
                    break
                def more := subPattern.matchBindSlice(values, specimens, bindings,
                                                      indices + [shapeSoFar], max)
                if (more == -1):
                    break
                max -= more
                if (more < 0 && maxShape == -1):
                    throw(`Patterns of indeterminate rank must make progress: $qsome vs $specimens`)
                result += more
                specimens := specimens.slice(more)
                shapeSoFar += 1
            subPattern.endShape(bindings, indices, shapeSoFar)
            if (!inBounds(result, quant)):
                throw("Improper quantity: $result vs $quant")
            return result
