import unittest

from textnode import TextNode, TextType
from text_utils import *

class TextTextUtils(unittest.TestCase):
    def test_extract_link(self):
        text_link_1 = "[alt text](https://www.google.com)"
        text_link_2 = "[link](http://www.unsicher.de)"
        text_cat = text_link_1 + " lorem ipsum " + text_link_2

        self.assertEqual(
            extract_markdown_links(text_link_1), 
            [("alt text", "https://www.google.com")])

        self.assertEqual(
            extract_markdown_links(text_link_2),
            [("link", "http://www.unsicher.de")]
        )

        self.assertEqual(
            len(extract_markdown_links(text_cat)),
            len([text_link_1, text_link_2])
        )
        
        self.assertEqual(extract_markdown_images(text_link_1), [])
        self.assertEqual(extract_markdown_images(text_link_2), [])
        self.assertEqual(extract_markdown_images(text_cat), [])

    def test_extract_image(self):
        text_img_1 = "![picture description](url/to/image.png)" 
        text_img_2 = "![Bildbeschreibung](./relativ.png)"
        text_cat = text_img_1 + " lorem ipsum " + text_img_2
        self.assertEqual(
            extract_markdown_images(text_img_1),
            [("picture description", "url/to/image.png")]
        )
        
        self.assertEqual(
            extract_markdown_images(text_img_2),
            [("Bildbeschreibung", "./relativ.png")]
        )
       
        self.assertEqual(
            len(extract_markdown_images(text_cat)),
            len([text_img_1, text_img_2])
        )

        self.assertEqual(extract_markdown_links(text_img_1), [])
        self.assertEqual(extract_markdown_links(text_img_2), [])
        self.assertEqual(extract_markdown_links(text_cat), [])

    def test_code(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        test_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        def nodes_equal(node1, node2):
            return (node1.text == node2.text and
                    node1.text_type == node2.text_type and
                    node1.url == node2.url)

        # Im Test:
        for i in range(len(test_nodes)):
            self.assertTrue(
                nodes_equal(new_nodes[i], test_nodes[i]),
                f"Nodes not equal: {new_nodes[i]} != {test_nodes[i]}"
            )


        # for i in range(0, 2):
        #     print(f"Erwartet {i}: {test_nodes[i]}")
        #     print(f"Erhalten {i}: {new_nodes[i]}")
        #     self.assertEqual(new_nodes[i], test_nodes[i])

        # self.assertListEqual(
        #     test_nodes,
        #     new_nodes,
        # )

if __name__ == "__main__":
    unittest.main()