import unittest
from htm import htm, ParseError


@htm
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

    def test_preserve_whitespace_between_text_values(self):
        self.assertEqual(html("<div>  a  {'b'}  c  </div>"), ("div", {}, ["  a  ", "b", "  c  "]))

    def test_collapse_whitespace_lines_in_text(self):
        self.assertEqual(html("<div>    \n    a    b    c    \n    </div>"), ("div", {}, ["a    b    c"]))
        self.assertEqual(html("<div>a   \n   {'b'}    \n    c    \n    </div>"), ("div", {}, ["a", "b", "c"]))

    def test_value_tag(self):
        self.assertEqual(html("<div />"), ("div", {}, []))
        self.assertEqual(html("<'div' />"), ("div", {}, []))
        self.assertEqual(html('<"div" />'), ("div", {}, []))

    def test_expression_tag(self):
        tag = "div"
        self.assertEqual(html("<{tag} />"), ("div", {}, []))

    def test_boolean_prop(self):
        self.assertEqual(html("<div foo />"), ("div", {"foo": True}, []))
        self.assertEqual(html("<div 'foo' />"), ("div", {"foo": True}, []))
        self.assertEqual(html('<div "foo" />'), ("div", {"foo": True}, []))

    def test_value_prop_name(self):
        self.assertEqual(html("<div foo=1 />"), ("div", {"foo": "1"}, []))
        self.assertEqual(html('<div "foo"=1 />'), ("div", {"foo": "1"}, []))
        self.assertEqual(html("<div 'foo'=1 />"), ("div", {"foo": "1"}, []))
        self.assertEqual(html("<div foo='1' />"), ("div", {"foo": "1"}, []))
        self.assertEqual(html('<div foo="1" />'), ("div", {"foo": "1"}, []))

    def test_expression_prop_value(self):
        a = 1
        self.assertEqual(html("<div foo={a} />"), ("div", {"foo": 1}, []))
        self.assertEqual(html('<div "foo"={a} />'), ("div", {"foo": 1}, []))
        self.assertEqual(html("<div 'foo'={a} />"), ("div", {"foo": 1}, []))

    def test_concatenated_prop_value(self):
        a = 1
        self.assertEqual(html("<div foo={a}{2} />"), ("div", {"foo": "12"}, []))
        self.assertEqual(html("<div foo=0/{a}/{2} />"), ("div", {"foo": "0/1/2"}, []))

    def test_slash_in_prop_value(self):
        self.assertEqual(html("<div foo=/bar/quux />"), ("div", {"foo": "/bar/quux"}, []))

    def test_spread(self):
        foo = {"foo": 1}
        self.assertEqual(
            html("<div ...{foo} ...{({'bar': 2})} />"),
            ("div", {"foo": 1, "bar": 2}, []),
        )

    def test_comments(self):
        self.assertEqual(
            html("""
                <div>
                    before
                    <!--
                        multiple lines, {"variables"} and "quotes
                        get ignored
                    -->
                    after
                </div>
            """),
            ("div", {}, ["before", "after"])
        )
        self.assertEqual(
            html("<div><!-->slight deviation from HTML comments<--></div>"),
            ("div", {}, [])
        )

    def test_tag_errors(self):
        with self.assertRaisesRegex(ParseError, "no token found"):
            html("< >")
        with self.assertRaisesRegex(ParseError, "no token found"):
            html("<>")
        with self.assertRaisesRegex(ParseError, "no token found"):
            html("<'")
        with self.assertRaisesRegex(ParseError, "unexpected end of data"):
            html("<")

    def test_attribute_name_errors(self):
        with self.assertRaisesRegex(ParseError, "expression not allowed"):
            html("<div {1}>")
        with self.assertRaisesRegex(ParseError, "unexpected end of data"):
            html("<div ")
        with self.assertRaisesRegex(ParseError, "no token found"):
            html("<div '")

    def test_attribute_value_errors(self):
        with self.assertRaisesRegex(ParseError, "invalid character"):
            html("<div 'a'x")
        with self.assertRaisesRegex(ParseError, "expression not allowed"):
            html("<div a{1}")
        with self.assertRaisesRegex(ParseError, "unexpected end of data"):
            html("<div a")
        with self.assertRaisesRegex(ParseError, "unexpected end of data"):
            html("<div a=")

    def test_structural_errors(self):
        with self.assertRaisesRegex(ParseError, "all opened tags not closed"):
            html("<div>")


if __name__ == "__main__":
    unittest.main()
