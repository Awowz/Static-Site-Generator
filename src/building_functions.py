import re
from textnode import TextNode, TextType

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
        if singe_node.text_type != TextType.TEXT:
            new_list.append(singe_node)
            continue
        matches = extract_markdown_images(singe_node.text)
        if matches == []:
            new_list.append(singe_node)
            continue
        remaining_text = singe_node.text
        for single_extracted_image in matches:
            alt_text, url = single_extracted_image
            split_on_str = f"![{alt_text}]({url})"
            str_split = remaining_text.split(split_on_str, 1)
            if str_split[0] == '' and str_split[1] == '':
                new_list.append(TextNode(alt_text, TextType.IMAGE_TEXT, url))
                continue
            elif str_split[0]: ##not empty
                new_list.append(TextNode(str_split[0], TextType.TEXT))
            new_list.append(TextNode(alt_text, TextType.IMAGE_TEXT, url))
            if len(matches) > 1:
                remaining_text = str_split[1] if len(str_split) > 1 else ""
            elif str_split[1]:
                new_list.append(TextNode(str_split[1], TextType.TEXT))
    return new_list

def split_nodes_link(old_nodes):
    new_list = []
    for singe_node in old_nodes:
        if singe_node.text_type != TextType.TEXT:
            new_list.append(singe_node)
            continue
        matches = extract_markdown_links(singe_node.text)
        if matches == []:
            new_list.append(singe_node)
            continue
        remaining_text = singe_node.text
        for single_extracted_image in matches:
            alt_text, url = single_extracted_image
            split_on_str = f"[{alt_text}]({url})"
            str_split = remaining_text.split(split_on_str, 1)
            if str_split[0] == '' and str_split[1] == '':
                new_list.append(TextNode(alt_text, TextType.LINK_TEXT, url))
                continue
            elif str_split[0]: ##not empty
                new_list.append(TextNode(str_split[0], TextType.TEXT))
            new_list.append(TextNode(alt_text, TextType.LINK_TEXT, url))
            if len(matches) > 1:
                remaining_text = str_split[1] if len(str_split) > 1 else ""
            elif str_split[1]:
                new_list.append(TextNode(str_split[1], TextType.TEXT))
    return new_list