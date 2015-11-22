# cribbed from http://sphinx-doc.org/extdev/tutorial.html

from sys import stderr

from docutils.parsers.rst import Directive
from docutils import nodes
from sphinx import addnodes

import railroad_diagrams
import rr_happy


def setup(app):
    app.add_node(RailroadDiagram,
                 html=(visit, depart))

    app.add_directive('syntax', RailroadDirective)
    app.add_config_value('syntax_file', None, 'html')

    return {'version': '0.1'}


class RailroadDiagram(nodes.hint):
    def __init__(self, diagram):
        nodes.hint.__init__(self)
        self._diag = diagram


def visit(self, node):
    self.body.append('<figure>')
    node._diag.writeSvg(self.body.append)


def depart(self, node):
    self.body.append('</figure>')


class RailroadDirective(Directive):

    has_content = True

    def run(self):
        env = self.state.document.settings.env

        name = self.content[0].strip()
        expr = '\n'.join(self.content[1:]).strip()

        targetid = "syntax-%s" % name
        targetnode = nodes.target('', '', ids=[targetid])
        label = nodes.paragraph('', '', nodes.strong(text=name))
        ix = addnodes.index(entries=[
            ("single", "syntax; " + name, targetid, False)])

        try:
            it = eval(expr,
                      railroad_diagrams.__dict__)
        except Exception as ex:
            print >>stderr, "@@eek!", self.content
            print >>stderr, "@@", ex
            raise

        diag = RailroadDiagram(railroad_diagrams.Diagram(it))

        if env.config.syntax_file:
            with open(env.config.syntax_file, 'a') as out:
                for line in rr_happy.gen_rule(name, it, expr):
                    print >>out, line

        return [targetnode, ix, label, diag]
