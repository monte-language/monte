def makeTag(code, name, dataType):
    return object tag:
        def _uncall():
            return [makeTag, "run", [code, name, dataType]]

        def printOn(out):
            out.print("<")
            out.print(name)
            if (code != null):
                out.print(":")
                out.print(code)
            if (dataType != null):
                out.print(":")
                out.print(dataType)
            out.print(">")

        def getTagCode():
            return code

        def getTagName():
            return name

        def getDataType():
            return dataType

        def isTagForData(data):
            if (data == null):
                return true
            if (dataType == null):
                return false

            if (data._getAllegedType() == dataType):
                return true
