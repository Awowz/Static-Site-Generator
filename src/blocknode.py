from enum import Enum
import re

from htmlnode import *
from building_functions import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown_doc):
    split_str = markdown_doc.split("\n\n")
    clean_blocks = []
    for x in range(len(split_str)):
        if split_str[x] == "":
            continue
        clean_str = split_str[x].strip()
        str_line = clean_str.split("\n")
        if len(str_line) > 1:
            scrubbed = []
            for line in str_line:
                scrubbed.append(line.strip())
            clean_str = "\n".join(scrubbed)
        clean_blocks.append(clean_str)
    return clean_blocks
    

def block_to_block_type(markdown_block_text):
    lines = markdown_block_text.split("\n")
    matches = re.findall(r"^(#{1,6})", markdown_block_text)
    if matches:
        return BlockType.HEADING
    
    if markdown_block_text.startswith("```") and markdown_block_text.endswith("```"):
        return BlockType.CODE
    
    if markdown_block_text.startswith(">"):
        split_lessthan = markdown_block_text.split("\n>")
        if len(lines) == len(split_lessthan):
            return BlockType.QUOTE
        
    if markdown_block_text.startswith("- "):
        split_dash = markdown_block_text.split("\n- ")
        if len(lines) == len(split_dash):
            return BlockType.UNORDERED_LIST
        
    if markdown_block_text.startswith("1."):
        for x in range(len(lines)):
            if not lines[x].startswith(f"{x+1}."):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
            
    return BlockType.PARAGRAPH

def text_to_children(text):
    block_as_list_of_textnodes = text_to_textnodes(text)
    html_child_list = []
    for textnode in block_as_list_of_textnodes:
        html_child_list.append(text_node_to_html_node(textnode))
    return html_child_list


def markdown_to_html_node(markdown):
    block_list_of_markdown = markdown_to_blocks(markdown)
    for single_markdown_block in block_list_of_markdown:
        block_type = block_to_block_type(single_markdown_block)
        
        match block_type:
            case BlockType.PARAGRAPH:
                html_childs_list = text_to_children(single_markdown_block)
                html_parent = ParentNode("p", html_childs_list)
            case BlockType.QUOTE:
                pass
            case BlockType.HEADING:
                pass
            case BlockType.CODE:
                pass
            case BlockType.UNORDERED_LIST:
                pass
            case BlockType.ORDERED_LIST:
                pass
