from monte.nodes import Character
from monte import bridge

class EObjectWrapper(object):
    def __init__(self, val):
        self._contents = val

    def __getattr__(self, name):
        def wrapper(*args):
            return bridge.e_call(self,  name, *args)
        return wrapper

bridge.setup(EObjectWrapper, Character)

e_privilegedScope = bridge.getPrivilegedScope()

def parse(source):
    from eparser import EParser
    p = EParser(source.strip())
    tree = p.apply("start")
    x = p.input.data[p.input.position:]
    if len(x) != 0:
        raise ValueError("Syntax error", ''.join(x))
    return tree.forValue(None)


def eval(expr, scope):
    try:
        ktree = parse(expr)
        return bridge.interactiveEval(ktree, scope)
    except Exception, ex:
        return [repr(ex), scope]


def repl():
    import readline
    scope = e_privilegedScope
    ps1 = "? "
    ps2 = "> "
    prompt = ps1
    delimiters = { "(": ")", "[": "]", "{": "}"}
    quotes = '"\''
    stack = []
    quoted = False
    expr = ""
    while True:
        try:
            line = raw_input(prompt)
        except EOFError:
            return None
        for i, c in enumerate(line):
            if c in quotes:
                if quoted:
                    if line[i-1] != "\\" and c == stack[-1]:
                        stack.pop()
                        quoted = False
                else:
                    stack.append(c)
                    quoted = True
            elif not quoted:
                if c in delimiters:
                    stack.append(c)
                elif len(stack) > 0 and c == delimiters[stack[-1]]:
                    stack.pop()
        expr += line + '\n'
        if len(stack) == 0:
            prompt = ps1
            [res, scope] = eval(expr, scope)
            print res
            expr = ""
        else:
            prompt = ps2


if __name__ == "__main__":
    repl()
