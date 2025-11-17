import re
from enum import Enum
from htmlnode import LeafNode

TextType = Enum('Text', ['TEXT', 'BOLD', 'ITALIC', 'CODE', 'LINK', 'IMAGE'])

class TextNode():
    def __init__(self, text=None, text_type=TextType.TEXT, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        if isinstance(node, TextNode):
            return False
            
        return (
            self.text == node.text and
            self.text_type.value == node.text_type.value and
            self.url == node.url
        )
        
    def __repr__(self):
        return f"TextNode({self.text!r}, {self.text_type!r}, {self.url!r})"
    
def text_node_to_html_node(text_node):    
    text = getattr(text_node, "text")
    url = getattr(text_node, "url")
    value = getattr(text_node, "text")
    props = None

    match getattr(text_node, "text_type"):
        case TextType.TEXT:
            tag = None

        case TextType.BOLD:
            tag = "b"

        case TextType.ITALIC:
            tag = "i"

        case TextType.CODE:
            tag = "code"

        case TextType.LINK:
            tag = "a"
            props = {"href": url}

        case TextType.IMAGE:
            tag = "img"
            value = ""
            props = {"src": url,
                     "alt": text
                     }

        case _:
            raise Exception("Invalid TextType for conversion!")
   
    return LeafNode(tag, value, props)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text

        if text.count(delimiter) % 2 != 0:
            raise Exception("Invalid Markdown syntax!")

        while True:
            if not delimiter in text:
                break;
            parts = text.split(delimiter, 2)
            
            if parts[0] == "":
                new_nodes.append(TextNode(parts[1], text_type))
            else:
                new_nodes.extend(
                    [
                        TextNode(parts[0], TextType.TEXT),
                        TextNode(parts[1], text_type),
                    ]
                )
            text = parts[-1]

        if text != "" and text != getattr(new_nodes[-1], "text"):
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)