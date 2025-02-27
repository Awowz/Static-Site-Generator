import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()