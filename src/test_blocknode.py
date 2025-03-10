import unittest

from blocknode import *

class TestBlocknode(unittest.TestCase):
    def test_blocktype_heading(self):
        text = "###whats up\nhows it going?\n ok goodbye\n```"
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




if __name__ == "__main__":
    unittest.main()