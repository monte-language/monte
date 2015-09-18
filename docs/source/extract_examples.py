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

    p = doctest.DocTestParser()
    for (section, txt) in inputs:
        caseNames = []
        for (ix, ex) in enumerate(p.get_examples(txt)):
            name = 'test%s_%s' % (section, ix)
            case = caseTemplate.format(name=name,
                                       source=ex.source.strip(),
                                       # TODO: string quoting
                                       want=ex.want.strip())
            caseNames.append(name)
            write(case)

        write(suiteTemplate.format(cases=',\n    '.join(caseNames)))

caseTemplate = u"""
def {name}(assert):
    # assert.equal(M.toString({source}), "{want}")
    assert.equal({source}, {want})

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
