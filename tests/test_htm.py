import unittest
from htm import htm


@htm()
def html(tag, props, children):
    return tag, props, children


class TestHTM(unittest.TestCase):
    def test_boolean_attribute(self):
        self.assertEqual(html("<div foo />"), ("div", {"foo": True}, []))
        self.assertEqual(html("<div 'foo' />"), ("div", {"foo": True}, []))
        self.assertEqual(html('<div "foo" />'), ("div", {"foo": True}, []))

    def test_value_attribute(self):
        self.assertEqual(html("<div foo=1 />"), ("div", {"foo": "1"}, []))
        self.assertEqual(html('<div "foo"=1 />'), ("div", {"foo": "1"}, []))
        self.assertEqual(html("<div 'foo'=1 />"), ("div", {"foo": "1"}, []))

    def test_expression_attribute(self):
        self.assertEqual(html("<div foo={1} />"), ("div", {"foo": 1}, []))
        self.assertEqual(html('<div "foo"={1} />'), ("div", {"foo": 1}, []))
        self.assertEqual(html("<div 'foo'={1} />"), ("div", {"foo": 1}, []))

    def test_spread(self):
        self.assertEqual(
            html("<div ...{{'foo': 1}} ...{{'bar': 2}} />"),
            ("div", {"foo": 1, "bar": 2}, []),
        )


if __name__ == "__main__":
    unittest.main()
