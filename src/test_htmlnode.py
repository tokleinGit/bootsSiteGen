import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        s = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), s)

    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_sorted_output(self):
        node = HTMLNode(props={"b": "2", "a": "1"})
        out = node.props_to_html()
        self.assertTrue(out.index(' a="1"') < out.index(' b="2"'))

    def test_repr_includes_fields(self):
        child = HTMLNode(tag="span", value="hi")
        node = HTMLNode(tag="a", value=None, children=[child], props={"href": "x"})
        r = repr(node)
        self.assertIn("tag", r)
        self.assertIn("a", r)
        self.assertIn("children", r)
        self.assertIn("href", r)

    def test_leaf_to_html_a(self):
        node = LeafNode(tag="a",value="Click me!",props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),'<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_p(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_n(self):
        node = LeafNode(tag=None, value="Here's the answer!", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "Here's the answer!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()