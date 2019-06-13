# htm.py [![CircleCI](https://circleci.com/gh/jviide/htm.py.svg?style=shield)](https://circleci.com/gh/jviide/htm.py) [![PyPI](https://img.shields.io/pypi/v/htm.svg?color=blue)](https://pypi.org/project/htm/)

A Python version of [developit/htm](https://github.com/developit/htm) - JSX-like syntax in plain ~~JavaScript~~ Python.

![](https://user-images.githubusercontent.com/19776768/59420458-99d60000-8dd5-11e9-9d29-02fff6c83a55.png)

## Installation

```sh
$ pip3 install htm
```

## Usage

```py
from htm import htm

@htm()
def html(tag, props, children):
    return tag, props, children

a = 1
b = {"bar": 100}
c = "span"
d = "world"

html("""
  <div foo={a+2} ...{b}>
    <{c}>Hello, {d}!<//>
  </div>
""")
# ('div', {'foo': 3, 'bar': 100}, [('span', {}, ['Hello,', 'world', '!'])])
```

## Development

### Running Tests

```sh
$ python3 -m unittest discover -s tests
```

## License

This library is licensed under the MIT license. See [./LICENSE](./LICENSE).
