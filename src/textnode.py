from enum import Enum
from htmlnode import *
import re

class TextType(Enum):
    TEXT = "text"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK_TEXT = "link"
    IMAGE_TEXT = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, otherTextNode):
        return (otherTextNode.text == self.text and otherTextNode.text_type == self.text_type and otherTextNode.url == self.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text)
        case TextType.LINK_TEXT:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE_TEXT:
            return LeafNode("img", "", {"src": text_node.url, "alt":text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for x in old_nodes:
        if not x.text_type == TextType.TEXT:
            new_list.append(x)
        else:
            str_split = x.text.split(delimiter)
            if len(str_split) % 2 == 0:
                raise Exception("text node is missing a matching delimiter")
            for count in range(len(str_split)):
                if str_split[count] == "":
                    continue
                if count % 2 == 0:
                    new_list.append(TextNode(str_split[count], TextType.TEXT))
                else:
                    new_list.append(TextNode(str_split[count], text_type))
            return new_list

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\]]+)\]\(([^\)]+)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\]]+)\]\(([^\)]+)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_list = []
    for singe_node in old_nodes:
        matches = extract_markdown_images(singe_node.text)
        if matches == []:
            new_list.append(singe_node)
            continue
        for single_extracted_image in matches:
            alt_text, url = single_extracted_image
            split_on_str = f"![{alt_text}]({url})"
            str_split = singe_node.text.split(split_on_str)
            print(str_split)
            print(len(str_split))
            print(singe_node.text)
            for count in range(len(str_split)):
                if str_split[count] == "":
                    continue
                if count % 2 == 0:
                    new_list.append(TextNode(str_split[count], TextType.TEXT))
                else:
                    new_list.append(TextNode(str_split[count], TextType.IMAGE_TEXT))

def split_nodes_link(old_nodes):
    pass