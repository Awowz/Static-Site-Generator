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

    def test_quotes(self):
        md = """ 
> hia
> hia1
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>hia hia1</blockquote></div>",
        )

    def test_unordered(self):
        md = """ 
- object1
- object2
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>object1</li><li>object2</li></ul></div>",
        )

    def test_ordered(self):
        md = """ 
1. First item
2. Second item
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_blockquote_added(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_multi_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()