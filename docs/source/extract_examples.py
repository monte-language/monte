'''extract_examples -- extract examples/tests from docs

Usage:

  extract_examples dest.mt section1.rst section2.rst ...

Examples are converted to monte unit tests.
'''
import logging
import doctest

log = logging.getLogger(__name__)


def main(access):
    inputs, write = access()

    write(testTop)

    p = doctest.DocTestParser()
    for (section, txt) in inputs:
        write(u'\n# {section}\n'.format(section=section))
        caseNames = []
        for (ix, ex) in enumerate(p.get_examples(txt)):
            name = 'test%s_%s' % (section.replace('-', '_'), ix)
            fixup = '.canonical()' if 'm`' in ex.source else ''
            delay = ('when (actual) ->\n        '
                     if '->' in ex.source or '<-' in ex.source
                     else '')
            case = caseTemplate.format(name=name,
                                       source=indent(ex.source, levels=3),
                                       fixup=fixup, delay=delay,
                                       want=ex.want.strip())
            caseNames.append(name)
            write(case)

        write(suiteTemplate.format(cases=',\n    '.join(caseNames)))


def indent(source, levels):
    lines = source.split('\n')
    indent = ' ' * (levels * 4)
    return '\n'.join(indent + line for line in lines)


testTop = ur"""
import "unittest" =~ [=> unittest]
exports ()

def mockFileResource(path):
    var contents := b``
    return object fileResource:
        to setContents(bs :Bytes):
            contents := bs
        to getContents() :Bytes:
            def [p, r] := Ref.promise()
            r <- resolve(contents)
            return p

"""

caseTemplate = u"""
def {name}(assert):
    object example:
        method test():
            "doc"
{source}

    def actual := example.test(){fixup}
    {delay}assert.equal(actual, {want}{fixup})

"""

suiteTemplate = u"""
unittest([
    {cases}
])

"""


def mkInputs(argv, open, splitext):
    return [(splitext(arg)[0], open(arg).read()) for arg in argv[2:]]


if __name__ == '__main__':
    def _script():
        from io import open
        from sys import argv
        from os.path import splitext

        def access():
            logging.basicConfig(level=logging.INFO)
            dest = argv[1]
            write = open(dest, 'w').write
            return mkInputs(argv, open, splitext), write

        main(access)

    _script()
