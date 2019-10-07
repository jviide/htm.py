from os import chdir, getcwd
from pathlib import Path
from shutil import rmtree
import sys
from tempfile import mkdtemp

from sybil import Sybil
from sybil.parsers.codeblock import CodeBlockParser
from sybil.parsers.doctest import DocTestParser


def sybil_setup(namespace):
    import htm
    basic_usage = Path(htm.__file__).parents[1] / 'docs' / 'basic_usage'
    sys.path.append(str(basic_usage))

    rendering_components = Path(htm.__file__).parents[1] / 'docs' / 'rendering_components'
    sys.path.append(str(rendering_components))
    # there are better ways to do temp directories, but it's a simple example:
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
    path='../docs/rendering_components',
    pattern='*.rst',
    setup=sybil_setup, teardown=sybil_teardown
).unittest()
