# htm.py

A Python version of [developit/htm](https://github.com/developit/htm) - JSX-like syntax in plain ~~JavaScript~~ Python.

![](https://user-images.githubusercontent.com/19776768/59381467-1af4af00-8d64-11e9-919d-62cad30a4a2e.png)

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
b = 100
c = "span"
d = "world"

html("""
  <div foo={a+2} ...{{"bar": b}}>
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
