import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("howdy", "howdy", None, {"href": "https://www.google.com","target": "_blank",})
        self.assertEqual(node.props_to_html(),  " href=\"https://www.google.com\" target=\"_blank\"")

    def test_props_to_html_single(self):
        node = HTMLNode("howdy", "howdy", None, {"href": "https://www.google.com",})
        self.assertEqual(node.props_to_html(),  " href=\"https://www.google.com\"")
    
    def test_props_to_html_none(self):
        node = HTMLNode("howdy", "howdy", None, None)
        self.assertEqual(node.props_to_html(),  "")

    def test_props_to_html_not_dict(self):
        node = HTMLNode("howdy", "howdy", None, "howdy")
        self.assertEqual(node.props_to_html(),  "")

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_leaf_to_html_no_value(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")



if __name__ == "__main__":
    unittest.main()