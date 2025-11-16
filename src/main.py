from textnode import *
from text_utils import *
def main():
    textNode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(textNode)

    node = TextNode(
            "This text is followed by a `code block`",
            TextType.TEXT
        )

    results = split_nodes_delimiter([node], '`', TextType.CODE)
    for result in results:
        print(result)


main()

