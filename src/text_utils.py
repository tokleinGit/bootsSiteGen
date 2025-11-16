from textnode import TextNode, TextType

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
            if not delimiter in text:
                break;

        if text != "" and text != getattr(new_nodes[-1], "text"):
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes