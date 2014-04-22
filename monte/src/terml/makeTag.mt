interface Tag :DeepFrozen guards TagStamp :DeepFrozen:
    pass

object makeTag implements DeepFrozen:
    to asType():
        return Tag
    to run(code :nullOk[int >= 0], name :str, dataGuard :DeepFrozen):
        return object tag implements Selfless, Transparent, TagStamp:
            to _uncall():
                return [makeTag, "run", [code, name, dataGuard]]

            to _printOn(out):
                out.print("<")
                out.print(name)
                if (code != null):
                    out.print(":")
                    out.print(code)
                if (dataGuard != null):
                    out.print(":")
                    out.print(dataGuard)
                out.print(">")

            to getTagCode():
                return code

            to getTagName():
                return name

            to getDataGuard():
                return dataGuard

            to isTagForData(data) :boolean:
                if (data == null):
                    return true
                if (dataGuard == null):
                    return false

                return data =~ _ :dataGuard
