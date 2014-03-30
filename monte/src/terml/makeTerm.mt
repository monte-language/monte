def TermData := any[void, str, int, float, char]

# Craft a term. The tag represents the functor, and either data or args are
# provided. The args are for complex functors, while the data is for primitive
# functors. The span should relate to the original source string that the term
# is representing.
def makeTerm(tag, data, args, span):
    if (data != null && args != null):
        throw(`Term $tag can't have both data and children`)
    if (data !~ _ :TermData):
        throw(`Term data $data isn't of a valid type`)

    return object term:
        to _uncall():
            return [makeTerm, "run", [tag, data, args, span]]

        to withSpan(newSpan):
            return makeTerm(tag, data, args, newSpan)

        to getTag():
            return tag

        to getData():
            return data

        to getSpan():
            return span

        to getArgs():
            return args

        to withoutArgs():
           return makeTerm(tag, data, [], span)

        to op__cmp(other):
           var tagCmp := tag.op__cmp(other.getTag())
           if (tagCmp != 0):
               return tagCmp
           if (data != null):
               if (other.getData() != null):
                   return -1
           else:
               if (other.getData() == null):
                   return 1
               def dataCmp := data.op__cmp(other.getData())
               if (dataCmp != 0):
                   return dataCmp
           return args.op__cmp(other.getArgs())

        # Used for pretty printing. Oughta be cached, but we need a
        # primitive memoizer for that to be DeepFrozen.
        to getHeight():
            var myHeight := 1
            for a in args:
                def h := a.getHeight()
                if (h + 1 > myHeight):
                    myHeight := h + 1
            return myHeight

        to _conformTo(guard):
            if (args.size() == 0 && [str, float, int, char].contains(guard)):
                if (data == null):
                    return tag.getTagName()
                return data
            else:
                return term

        to _printOn(out):
            out.print(tag)
            out.print("[")
            data._printOn(out)
            out.print("]")
            out.print("(")
            if (args != null):
                for arg in args:
                    arg._printOn(out)
                    out.print(",")
            out.print(")")

        to prettyPrintOn(out, isQuasi :boolean):
            var label := null # should be def w/ later bind
            var reps := null
            var delims := null
            switch (data):
                match ==null:
                    label := tag.getTagName()
                # match _ :float:
                #     if (data.isNaN()):
                #         label := "%NaN"
                #     else if (data.isInfinite()):
                #         if (data > 0):
                #             label := "%Infinity"
                #         else:
                #             label := "-%Infinity"
                #     else:
                #         label := `$data`
                match _ :str:
                    label := data.quote().replace("\n", "\\n")
                match _:
                    label := M.toQuote(data)

            if (isQuasi):
                # Escape QL characters.
                label := label.replace("$", "$$").replace("@", "@@")
                label := label.replace("`", "``")

            if (label == ".tuple."):
                if (term.getHeight() <= 1):
                    out.print("[]")
                    return
                reps := 1
                delims := ["[", ",", "]"]
            else if (label == ".bag."):
                if (term.getHeight() <= 1):
                    out.print("{}")
                    return
                reps := 1
                delims := ["{", ",", "}"]
            else if (args == null):
                out.print("null")
                return
            else if (args.size() == 1 && args[0].getTag().getTagName()):
                reps := label.size()
                delims := ["", null, ""]
            else if (args.size() == 2 && label == ".attr."):
                reps := 4
                delims := ["", ":", ""]
            else:
                out.print(label)
                if (term.getHeight() <= 1):
                    # Leaf, so no parens.
                    return
                reps := label.size() + 1
                delims := ["(", ",", ")"]
            def [open, sep, close] := delims
            if (term.getHeight() == 2):
                # Just leaves, so one line.
                out.print(open)
                args[0].prettyPrintOn(out, isQuasi)
                for a in args.slice(1):
                    out.print(sep + " ")
                    a.prettyPrintOn(out, isQuasi)
                out.print(close)
            else:
                out.print(open)
                def sub := out.indent(" " * reps)
                args[0].prettyPrintOn(sub, isQuasi)
                for a in args.slice(1):
                    sub.println(sep)
                    a.prettyPrintOn(out, isQuasi)
                sub.print(close)
