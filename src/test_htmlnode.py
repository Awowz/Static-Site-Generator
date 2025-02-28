import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_to_html_with_children_parent_prop(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"href": "https://www.google.com",})
        self.assertEqual(parent_node.to_html(), "<div href=\"https://www.google.com\"><span>child</span></div>")

    def test_to_html_with_children_prop(self):
        child_node = LeafNode("span", "child",{"href": "https://www.google.com",})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span href=\"https://www.google.com\">child</span></div>")

    def test_to_html_with_children_both_prop(self):
        child_node = LeafNode("span", "child",{"href": "https://www.google.com",})
        parent_node = ParentNode("div", [child_node], {"href": "https://www.google.com",})
        self.assertEqual(parent_node.to_html(), "<div href=\"https://www.google.com\"><span href=\"https://www.google.com\">child</span></div>")

    def test_to_html_with_grandchildren_and_multi_child(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = LeafNode("p", "seperate child")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><p>seperate child</p></div>",
        )    



if __name__ == "__main__":
    unittest.main()