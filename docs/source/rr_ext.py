# cribbed from http://sphinx-doc.org/extdev/tutorial.html

from json import dump
from sys import stderr

from docutils.parsers.rst import Directive
from docutils import nodes
from sphinx import addnodes

import railroad_diagrams


def setup(app):
    app.connect('builder-inited', start_module)
    app.connect('build-finished', end_module)

    app.add_node(RailroadDiagram,
                 html=(visit, depart))

    app.add_directive('syntax', RailroadDirective)
    app.add_config_value('syntax_dest', None, 'html')
    app.add_config_value('syntax_fp', None, None)

    return {'version': '0.1'}


def start_module(app):
    if app.config.syntax_dest:
        fp = app.config.syntax_fp = open(app.config.syntax_dest, 'w')
        fp.write("[\n")


def end_module(app, ex):
    if app.config.syntax_dest:
        app.config.syntax_fp.write("null]\n")


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

        if env.config.syntax_fp:
            out = env.config.syntax_fp
            dump({'name': name, 'expr': expr}, out)
            out.write(",\n\n")

        return [targetnode, ix, label, diag]
