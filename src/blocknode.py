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
    matches = re.findall(r"^(#{1,6} )", markdown_block_text)
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
    html_parents = []
    for single_markdown_block in block_list_of_markdown:
        block_type = block_to_block_type(single_markdown_block)
        stripped_text = single_markdown_block.replace("\n", " ")
        broken_down_str = single_markdown_block.split("\n")
        
        match block_type:
            case BlockType.PARAGRAPH:
                html_childs_list = text_to_children(stripped_text)
                html_parent = ParentNode("p", html_childs_list)
                html_parents.append(html_parent)
            case BlockType.QUOTE:
                for x in range(len(broken_down_str)):
                    broken_down_str[x] = broken_down_str[x][2:]
                put_together = " ".join(broken_down_str)
                html_childs_list = text_to_children(put_together)
                html_parent = ParentNode("blockquote", html_childs_list)
                html_parents.append(html_parent)
            case BlockType.HEADING:
                count = 0
                for x in range(len(stripped_text)):
                    if x > 6 or stripped_text[x] != "#":
                        break
                    count += 1
                stripped_text = stripped_text[count + 1:]
                html_parent = ParentNode(f"h{count}", text_to_children(stripped_text))
                html_parents.append(html_parent)
            case BlockType.CODE:
                clean_str = single_markdown_block.replace("```\n", "")
                clean_str = clean_str.replace("```", "")
                html_parent = ParentNode("pre", [LeafNode("code", clean_str)])
                html_parents.append(html_parent)
            case BlockType.UNORDERED_LIST:
                for x in range(len(broken_down_str)):
                    broken_down_str[x] = broken_down_str[x][2:]
                html_childs_list = []
                for x in broken_down_str:
                    html_childs_list.append(ParentNode("li", text_to_children(x)))
                html_parent = ParentNode("ul", html_childs_list)
                html_parents.append(html_parent)
            case BlockType.ORDERED_LIST:
                for x in range(len(broken_down_str)):
                    broken_down_str[x] = broken_down_str[x][3:]
                html_childs_list = []
                for x in broken_down_str:
                    html_childs_list.append(ParentNode("li", text_to_children(x)))
                html_parent = ParentNode("ol", html_childs_list)
                html_parents.append(html_parent)
    html_block = ParentNode("div", html_parents)
    return html_block