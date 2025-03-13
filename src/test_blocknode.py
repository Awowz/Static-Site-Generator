import unittest

from blocknode import *

class TestBlocknode(unittest.TestCase):
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


    

    def test_blocktype_heading(self):
        text = "### whats up\nhows it going?\n ok goodbye\n```"
        blocktype = block_to_block_type(text)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_blocktype_heading_newline(self):
        text = "whats up\n###hows it going?\n ok goodbye\n```"
        blocktype = block_to_block_type(text)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_blocktype_code(self):
        text = "```whats up\nhows it going?\n ok goodbye\n```"
        blocktype = block_to_block_type(text)
        self.assertEqual(blocktype, BlockType.CODE)

    def test_blocktype_quote(self):
        text = ">whats up\n>hows it going?\n> ok goodbye"
        blocktype = block_to_block_type(text)
        self.assertEqual(blocktype, BlockType.QUOTE)

    def test_blocktype_unordered(self):
        text = "- whats up\n- hows it going?\n- ok goodbye"
        blocktype = block_to_block_type(text)
        self.assertEqual(blocktype, BlockType.UNORDERED_LIST)
    
    def test_blocktype_unordered_no_space(self):
        text = "-whats up\n- hows it going?\n-ok goodbye"
        blocktype = block_to_block_type(text)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_blocktype_ordered(self):
        text = "1.whats up\n2.hows it going?\n3.ok goodbye"
        blocktype = block_to_block_type(text)
        self.assertEqual(blocktype, BlockType.ORDERED_LIST)

    def test_blocktype_ordered_fail(self):
        text = "1.whats up\nhows it going?\nok goodbye"
        blocktype = block_to_block_type(text)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()        
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )





    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = "# This is a Heading h1"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a Heading h1</h1></div>",
        )

    def test_headings6(self):
        md = "###### This is a Heading h6"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h6>This is a Heading h6</h6></div>",
        )

if __name__ == "__main__":
    unittest.main()