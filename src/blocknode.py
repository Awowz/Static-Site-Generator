from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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