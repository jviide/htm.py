from os import chdir, getcwd
from pathlib import Path
from shutil import rmtree
import sys
from tempfile import mkdtemp

from sybil import Sybil
from sybil.parsers.codeblock import CodeBlockParser
from sybil.parsers.doctest import DocTestParser

TARGET = 'hyperpython'


def sybil_setup(namespace):
    import htm

    t = Path(htm.__file__).parents[1] / 'docs' / TARGET
    sys.path.append(str(t))
    namespace['path'] = path = mkdtemp()
    namespace['cwd'] = getcwd()
    chdir(path)


def sybil_teardown(namespace):
    chdir(namespace['cwd'])
    rmtree(namespace['path'])


load_tests = Sybil(
    parsers=[
        DocTestParser(),
        CodeBlockParser(future_imports=['print_function']),
    ],
    path=f'../docs/{TARGET}',
    pattern='*.rst',
    setup=sybil_setup, teardown=sybil_teardown
).unittest()
