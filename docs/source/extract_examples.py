'''extract_examples -- extract examples/tests from docs

Usage:

  extract_examples output_dir section1.rst section2.rst ...

Results are section1_0.mt, section1_0_expected.txt etc. in output_dir.
'''
import logging
import doctest

log = logging.getLogger(__name__)


def main(access):
    inputs, output = access()

    p = doctest.DocTestParser()
    for (section, txt) in inputs:
        for (ix, ex) in enumerate(p.get_examples(txt)):
            output('%s_%s.mt' % (section, ix), ex.source)
            output('%s_%s_expected.txt' % (section, ix), ex.want)


def mkInputs(argv, open, splitext):
    return [(splitext(arg)[0], open(arg).read()) for arg in argv[2:]]


def mkOutput(argv, open, join):
    where = argv[1]

    def output(fn, txt):
        log.info('output: %s', (where, fn))
        open(join(where, fn), 'w').write(txt)
    return output

if __name__ == '__main__':
    def _script():
        from io import open
        from sys import argv
        from os.path import splitext, join

        def access():
            logging.basicConfig(level=logging.INFO)
            return mkInputs(argv, open, splitext), mkOutput(argv, open, join)

        main(access)

    _script()
