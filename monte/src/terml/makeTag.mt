def makeTag(code, name, dataType):
    return object tag:
        to _uncall():
            return [makeTag, "run", [code, name, dataType]]

        to _printOn(out):
            out.print("<")
            out.print(name)
            if (code != null):
                out.print(":")
                out.print(code)
            if (dataType != null):
                out.print(":")
                out.print(dataType)
            out.print(">")

        to getTagCode():
            return code

        to getTagName():
            return name

        to getDataType():
            return dataType

        to isTagForData(data) :boolean:
            if (data == null):
                return true
            if (dataType == null):
                return false

            return data =~ _ :dataType
