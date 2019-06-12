import unittest
from htm import htm


@htm()
def html(tag, props, children):
    return tag, props, children


class TestHTM(unittest.TestCase):
    def test_single_root(self):
        self.assertEqual(html("<div />"), ("div", {}, []))

    def test_multiple_roots(self):
        self.assertEqual(html("<div /><span />"), [("div", {}, []), ("span", {}, [])])

    def test_value_children(self):
        self.assertEqual(html("<div>foo</div>"), ("div", {}, ["foo"]))
        self.assertEqual(html("<div><span /></div>"), ("div", {}, [("span", {}, [])]))

    def test_expression_children(self):
        value = "foo"
        self.assertEqual(html("<div>{value}</div>"), ("div", {}, ["foo"]))
        self.assertEqual(
            html("<div>{html('<span/>')}</div>"), ("div", {}, [("span", {}, [])])
        )

    def test_expression_tag(self):
        tag = "div"
        self.assertEqual(html("<{tag} />"), ("div", {}, []))

    def test_value_tag(self):
        self.assertEqual(html("<div />"), ("div", {}, []))
        self.assertEqual(html("<'div' />"), ("div", {}, []))
        self.assertEqual(html('<"div" />'), ("div", {}, []))

    def test_expression_tag(self):
        tag = "div"
        self.assertEqual(html("<{tag} />"), ("div", {}, []))

    def test_boolean_attribute(self):
        self.assertEqual(html("<div foo />"), ("div", {"foo": True}, []))
        self.assertEqual(html("<div 'foo' />"), ("div", {"foo": True}, []))
        self.assertEqual(html('<div "foo" />'), ("div", {"foo": True}, []))

    def test_value_attribute_name(self):
        self.assertEqual(html("<div foo=1 />"), ("div", {"foo": "1"}, []))
        self.assertEqual(html('<div "foo"=1 />'), ("div", {"foo": "1"}, []))
        self.assertEqual(html("<div 'foo'=1 />"), ("div", {"foo": "1"}, []))
        self.assertEqual(html("<div foo='1' />"), ("div", {"foo": "1"}, []))
        self.assertEqual(html('<div foo="1" />'), ("div", {"foo": "1"}, []))

    def test_expression_attribute(self):
        a = 1
        self.assertEqual(html("<div foo={a} />"), ("div", {"foo": 1}, []))
        self.assertEqual(html('<div "foo"={a} />'), ("div", {"foo": 1}, []))
        self.assertEqual(html("<div 'foo'={a} />"), ("div", {"foo": 1}, []))

    def test_spread(self):
        foo = {"foo": 1}
        self.assertEqual(
            html("<div ...{foo} ...{{'bar': 2}} />"), ("div", {"foo": 1, "bar": 2}, [])
        )


if __name__ == "__main__":
    unittest.main()
