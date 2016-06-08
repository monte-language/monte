'''extract_examples -- extract examples/tests from docs

Usage:

  extract_examples dest.json section1.rst section2.rst ...

Examples are saved in .json format.
'''
import doctest
import json
import logging

log = logging.getLogger(__name__)


def main(access):
    inputs, save = access()

    p = doctest.DocTestParser()
    suite = []
    for (section, txt) in inputs:
        for ex in p.get_examples(txt):
            suite.append(dict(section=section,
                              lineno=ex.lineno,
                              source=ex.source,
                              want=ex.want))
    save(suite)


def mkInputs(argv, open, splitext):
    return [(splitext(arg)[0], open(arg).read()) for arg in argv[2:]]


if __name__ == '__main__':
    def _script():
        from io import open as io_open
        from sys import argv
        from os.path import splitext

        def access():
            logging.basicConfig(level=logging.INFO)
            dest = argv[1]
            save = lambda obj: json.dump(obj, io_open(dest, 'wb'), indent=2)
            return mkInputs(argv, io_open, splitext), save

        main(access)

    _script()
