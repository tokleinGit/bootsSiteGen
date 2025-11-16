import unittest

from textnode import TextNode, TextType
from text_utils import *

class TextTextUtils(unittest.TestCase):
    def test_code(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT
        )
        self.assertCountEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ],
            split_nodes_delimiter([node], '`', TextType.CODE),
        )

if __name__ == "__main__":
    unittest.main()