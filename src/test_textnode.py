import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This was a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_uneq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_uneq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "http://...")
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def assertEqual(self, node, node2):
        return node == node2

    def assertNotEqual(self, node, node2):
        return not node == node2

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode('print("Hello World!")', TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("Click me!", TextType.BOLD, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href=": "https://www.google.com"})

    def test_link(self):
        node = TextNode("Description of image", TextType.BOLD, "url/of/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src=": "url/of/image.jpg",
                                           "alt=": "Description of image"})

class TestSplitNodesDelimiter(unittest.TestCase):
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

class TestExtractImage(unittest.TestCase):
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

class TestExtractLink(unittest.TestCase):
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

class TestSplitNodeImage(unittest.TestCase):
    def test_split_nodes_image_debug_output(self):
        old_nodes = [
            TextNode("This is text with an ", 'TEXT'),
            TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", 'IMAGE'),
            TextNode(" and another ", 'TEXT'),
            TextNode("![second image](https://i.imgur.com/3elNhQu.png)"),
        ]

        result = split_nodes_image(old_nodes)

        print("\n--- Debug-Ausgabe: split_nodes_image ---")
        for i, node in enumerate(result):
            print(f"Node {i}: {node.__dict__}")
        
        print("----------------------------------------\n")

class TestSplitNodeLink(unittest.TestCase):
    def test_split_nodes_Link_debug_output(self):
        old_nodes = [
            TextNode("This is text with a link ", 'TEXT'),
            TextNode("[to boot dev](https://boot.dev)", 'LINK'),
            TextNode(" and ", 'TEXT'),
            TextNode("[to youtube](https://www.youtube.com/@bootdotdev).", 'LINK'),
        ]

        result = split_nodes_image(old_nodes)

        print("\n--- Debug-Ausgabe: split_nodes_link ---")
        for i, node in enumerate(result):
            print(f"Node {i}: {node.__dict__}")
        
        print("----------------------------------------\n")

if __name__ == "__main__":
    unittest.main()