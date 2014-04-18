from StringIO import StringIO

from monte.compiler import TextWriter


class MonteWriter(object):
    """
    Moderately-pretty printer for expanded Monte.
    """

    def __init__(self, tree):
        self.tree = tree

    def output(self, origOut):
        out, flush = origOut.delay()
        val = self._generate(out, self.tree)
        flush()
        origOut.writeln(val)

    def _generate(self, out, node):
        name = node.tag.name
        if name == "null":
            return "null"
        return getattr(self, "generate_" + name)(out, node)

    def generate_LiteralExpr(self, out, node):
        litNode = node.args[0]
        if litNode.tag.name == 'Character':
            out.write("'%r'" % litNode.args[0].data)
        else:
            lit = litNode.data
            # If it's not unicode already, then it must have been UTF-8 and not
            # yet decoded from when it was parsed.
            if isinstance(lit, str):
                lit = lit.decode("utf-8")
            out.write(repr(lit))

    def generate_NounExpr(self, out, node):
        name = node.args[0].data
        out.write(name)

    def generate_BindingExpr(self, out, node):
        print "Wat!"

    def generate_SeqExpr(self, out, node):
        exprs = node.args[0].args
        for e in exprs:
            self._generate(out, e)
            out.write(";")

    def generate_MethodCallExpr(self, out, node):
        rcvr, verb, args = node.args
        self._generate(out, rcvr)
        out.write(".%s(" % verb.data)
        for arg in args.args:
            self._generate(out, arg)
            out.write(",")
        out.write(")")

    def generate_Def(self, out, node):
        patt, ej, expr = node.args
        out.write("def ")
        self._generate(out, patt)
        self._generate(out, ej)
        out.write(" := ")
        self._generate(out, expr)

    def generate_Escape(self, out, node):
        patt, body, catcher = node.args
        out.write("escape ")
        self._generate(out, patt)
        out.write(" { ")
        self._generate(out, body)
        out.write(" } ")
        self._generate(out, catcher)

    def generate_Object(self, out, node):
        doc, nameNode, auditorExprs, script = node.args
        out.write(" object ")
        self._generate(out, nameNode)
        out.write(" implements ")
        for iface in auditorExprs.args:
            self._generate(out, iface)
            out.write(",")
        out.write(" { ")
        self._generate(out, script)
        out.write(" } ")

    def generate_Script(self, out, node):
        derp, methods, matchers = node.args
        print "derp", derp
        for method in methods.args:
            self._generate(out, method)
            out.write(";")
        for matcher in matchers.args:
            self._generate(matcher)

    def generate_Method(self, out, node):
        derp, name, params, rv, body = node.args
        print "derp", derp
        out.write("to %s(" % name.data)
        for param in params.args:
            self._generate(out, param)
            out.write(",")
        out.write(")")
        self._generate(out, rv)
        out.write(" { ")
        self._generate(out, body)
        out.write(" } ")

    def generate_Assign(self, out, node):
        patt, expr = node.args
        self._generate(out, patt)
        out.write(" := ")
        self._generate(out, expr)

    def generate_Finally(self, out, node):
        block, fin = node.args
        out.write("try { ")
        self._generate(out, block)
        out.write(" } finally { ")
        self._generate(out, fin)
        out.write(" } ")

    def generate_KernelTry(self, out, node):
        block, patt, catchblock = node.args
        out.write(" try { ")
        self._generate(out, block)
        out.write(" } catch ")
        self._generate(out, patt)
        out.write(" { ")
        self._generate(out, catchblock)
        out.write(" } ")

    def generate_HideExpr(self, out, node):
        print "Hide?"

    def generate_If(self, out, node):
        test, consq, alt = node.args
        out.write(" if ( ")
        self._generate(out, test)
        out.write(" ) { ")
        self._generate(out, consq)
        out.write(" } else { ")
        self._generate(out, alt)
        out.write(" } ")

    def generate_Meta(self, out, node):
        print "Meta"

    def generate_FinalPattern(self, out, node):
        name, guard = node.args
        out.write("def ")
        self._generate(out, name)
        out.write(" :(")
        self._generate(out, guard)
        out.write(")")

    def generate_IgnorePattern(self, out, node):
        guard = node.args[0]
        out.write("_ :(")
        self._generate(out, guard)
        out.write(")")

    def generate_VarPattern(self, out, node):
        nameExpr, guard = node.args
        name = nameExpr.args[0].data
        out.write("var %s :(" % name)
        self._generate(out, guard)
        out.write(")")

    def generate_ListPattern(self, out, node):
        pattsTerm, extra = node.args
        patts = pattsTerm.args
        out.write(" [")
        for patt in patts:
            self._generate(out, patt)
            out.write(",")
        out.write("]")

    def generate_ViaPattern(self, out, node):
        print "via?"
        self._generate(out, node.args[0])
        self._generate(out, node.args[1])

    def generate_BindingPattern(self, out, node):
        print "bind?"
        name = node.args[0].args[0].data
        out.write("bind %s" % name)

def format(ast):
    f = StringIO()
    MonteWriter(ast).output(TextWriter(f))
    return f.getvalue()
