import unittest

from building_functions import *
from textnode import *

class TestTextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("ALT TEXT", TextType.IMAGE_TEXT, "URL PATH")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), "<img src=\"URL PATH\" alt=\"ALT TEXT\"></img>")

    def test_split_delimiter(self):
        node = TextNode("the word **text** is in bold", TextType.TEXT)
        output = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        buffer = ""
        for x in output:
            buffer += x.__repr__()
        self.assertEqual("TextNode(the word , text, None)TextNode(text, bold, None)TextNode( is in bold, text, None)", buffer)
        
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD_TEXT),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD_TEXT),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD_TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD_TEXT),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD_TEXT),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC_TEXT)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD_TEXT),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_extract_images_single(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif), [am fake](https:/)"
        extract_list = extract_markdown_images(text)
        compaire_list = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertListEqual(extract_list, compaire_list)

    def test_extract_images_double(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extract_list = extract_markdown_images(text)
        compaire_list = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(extract_list, compaire_list)
    
    def test_extract_images_none(self):
        text = "This is text with a ![rick roll]whats up"
        extract_list = extract_markdown_images(text)
        compaire_list = []
        self.assertEqual(extract_list, compaire_list)

    def test_extract_links_double(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extract_list = extract_markdown_links(text)
        compaire_list = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(extract_list, compaire_list)

    def test_extract_links_single(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
        extract_list = extract_markdown_links(text)
        compaire_list = [("to boot dev", "https://www.boot.dev")]
        self.assertListEqual(extract_list, compaire_list)

    def test_extract_links_none(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](ajfklsa;"
        extract_list = extract_markdown_links(text)
        compaire_list = []
        self.assertEqual(extract_list, compaire_list)


    def test_split_images_single(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif), [am fake](https:/)"
        nodes = [TextNode(text, TextType.TEXT)]
        compaire_nodes = [TextNode("This is text with a ", TextType.TEXT), TextNode("rick roll", TextType.IMAGE_TEXT, "https://i.imgur.com/aKaOqIh.gif"),TextNode(", [am fake](https:/)", TextType.TEXT)]
        extract_list = split_nodes_image(nodes)
        self.assertListEqual(extract_list, compaire_nodes)

    def test_split_images_end_edgecase(self):
        text = "this is the begining![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        nodes = [TextNode(text, TextType.TEXT)]
        compaire_nodes = [TextNode("this is the begining", TextType.TEXT), TextNode("rick roll", TextType.IMAGE_TEXT, "https://i.imgur.com/aKaOqIh.gif")]
        extract_list = split_nodes_image(nodes)
        self.assertListEqual(extract_list, compaire_nodes)
  
    def test_split_images_start_edgecase(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif)this is the begining"
        nodes = [TextNode(text, TextType.TEXT)]
        compaire_nodes = [TextNode("rick roll", TextType.IMAGE_TEXT, "https://i.imgur.com/aKaOqIh.gif"), TextNode("this is the begining", TextType.TEXT),]
        extract_list = split_nodes_image(nodes)
        self.assertListEqual(extract_list, compaire_nodes)

    def test_split_images_solo(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        nodes = [TextNode(text, TextType.TEXT)]
        compaire_nodes = [TextNode("rick roll", TextType.IMAGE_TEXT, "https://i.imgur.com/aKaOqIh.gif")]
        extract_list = split_nodes_image(nodes)
        self.assertListEqual(extract_list, compaire_nodes)

    def test_split_images_multi_dif(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif)this is the begining![meowmeow](https://i.imgur.com/aKa1qIh.gif)"
        nodes = [TextNode(text, TextType.TEXT)]
        compaire_nodes = [TextNode("rick roll", TextType.IMAGE_TEXT, "https://i.imgur.com/aKaOqIh.gif"), TextNode("this is the begining", TextType.TEXT),TextNode("meowmeow", TextType.IMAGE_TEXT, "https://i.imgur.com/aKa1qIh.gif")]
        extract_list = split_nodes_image(nodes)
        self.assertListEqual(extract_list, compaire_nodes)
    
    def test_split_images_multi_same(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif)this is the begining![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        nodes = [TextNode(text, TextType.TEXT)]
        compaire_nodes = [TextNode("rick roll", TextType.IMAGE_TEXT, "https://i.imgur.com/aKaOqIh.gif"), TextNode("this is the begining", TextType.TEXT),TextNode("rick roll", TextType.IMAGE_TEXT, "https://i.imgur.com/aKaOqIh.gif")]
        extract_list = split_nodes_image(nodes)
        self.assertListEqual(extract_list, compaire_nodes)

    def test_split_links_single(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif), ![am fake](https:/)"
        nodes = [TextNode(text, TextType.TEXT)]
        compaire_nodes = [TextNode("This is text with a ", TextType.TEXT), TextNode("rick roll", TextType.LINK_TEXT, "https://i.imgur.com/aKaOqIh.gif"),TextNode(", ![am fake](https:/)", TextType.TEXT)]
        extract_list = split_nodes_link(nodes)
        self.assertListEqual(extract_list, compaire_nodes)




    def test_split_link_end_edgecase(self):
        text = "this is the begining[rick roll](https://i.imgur.com/aKaOqIh.gif)"
        nodes = [TextNode(text, TextType.TEXT)]
        compaire_nodes = [TextNode("this is the begining", TextType.TEXT), TextNode("rick roll", TextType.LINK_TEXT, "https://i.imgur.com/aKaOqIh.gif")]
        extract_list = split_nodes_link(nodes)
        self.assertListEqual(extract_list, compaire_nodes)
  
    def test_split_link_start_edgecase(self):
        text = "[rick roll](https://i.imgur.com/aKaOqIh.gif)this is the begining"
        nodes = [TextNode(text, TextType.TEXT)]
        compaire_nodes = [TextNode("rick roll", TextType.LINK_TEXT, "https://i.imgur.com/aKaOqIh.gif"), TextNode("this is the begining", TextType.TEXT),]
        extract_list = split_nodes_link(nodes)
        self.assertListEqual(extract_list, compaire_nodes)

    def test_split_link_solo(self):
        text = "[rick roll](https://i.imgur.com/aKaOqIh.gif)"
        nodes = [TextNode(text, TextType.TEXT)]
        compaire_nodes = [TextNode("rick roll", TextType.LINK_TEXT, "https://i.imgur.com/aKaOqIh.gif")]
        extract_list = split_nodes_link(nodes)
        self.assertListEqual(extract_list, compaire_nodes)

    def test_split_link_multi_dif(self):
        text = "[rick roll](https://i.imgur.com/aKaOqIh.gif)this is the begining[meowmeow](https://i.imgur.com/aKa1qIh.gif)"
        nodes = [TextNode(text, TextType.TEXT)]
        compaire_nodes = [TextNode("rick roll", TextType.LINK_TEXT, "https://i.imgur.com/aKaOqIh.gif"), TextNode("this is the begining", TextType.TEXT),TextNode("meowmeow", TextType.LINK_TEXT, "https://i.imgur.com/aKa1qIh.gif")]
        extract_list = split_nodes_link(nodes)
        self.assertListEqual(extract_list, compaire_nodes)
    
    def test_split_link_multi_same(self):
        text = "[rick roll](https://i.imgur.com/aKaOqIh.gif)this is the begining[rick roll](https://i.imgur.com/aKaOqIh.gif)"
        nodes = [TextNode(text, TextType.TEXT)]
        compaire_nodes = [TextNode("rick roll", TextType.LINK_TEXT, "https://i.imgur.com/aKaOqIh.gif"), TextNode("this is the begining", TextType.TEXT),TextNode("rick roll", TextType.LINK_TEXT, "https://i.imgur.com/aKaOqIh.gif")]
        extract_list = split_nodes_link(nodes)
        self.assertListEqual(extract_list, compaire_nodes)

    def test_text_to_textnodes_simple(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        extracted_nodes = text_to_textnodes(text)
        compaire_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK_TEXT, "https://boot.dev"),
        ]
        self.assertListEqual(extracted_nodes, compaire_nodes)

    def test_text_to_textnodes_dup_image(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        extracted_nodes = text_to_textnodes(text)
        compaire_nodes = [
            TextNode("obi wan image", TextType.IMAGE_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK_TEXT, "https://boot.dev"),
        ]
        self.assertListEqual(extracted_nodes, compaire_nodes)

    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


        
if __name__ == "__main__":
    unittest.main()