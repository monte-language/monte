# cribbed from http://sphinx-doc.org/extdev/tutorial.html

from docutils.parsers.rst import Directive
from docutils import nodes

import railroad_diagrams


def setup(app):
    app.add_node(RailroadDiagram,
                 html=(visit, depart))

    app.add_directive('syntax', RailroadDirective)

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

        targetid = "syntax-%d" % env.new_serialno('syntax')
        targetnode = nodes.target('', '', ids=[targetid])

        diag = RailroadDiagram(eval(''.join(self.content),
                                    railroad_diagrams.__dict__))

        return [targetnode, diag]
