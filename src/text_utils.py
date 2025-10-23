from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = list()
    for node in old_nodes:
        old_type = getattr(node, "text_type")

        if old_type is not TextType.TEXT:
            new_nodes.append(node)
            next
    
        text = getattr(node, "text")

        if text.count(delimiter) % 2 != 0:
            raise Exception("Invalid Markdown syntax!")
        
        while True:
            
            text_nodes = text.split(delimiter,2)
            if text_nodes[0] == "":
                new_nodes.append(TextNode(text_nodes[1],text_type))
            
            else:
                new_nodes.extend(
                    [TextNode(text_nodes[0],TextType.TEXT), TextNode(text_nodes[1],text_type)])
            
            text = text_nodes[-1]
            if not delimiter in text:
                break
        
        if text != "" and text != getattr(new_nodes[-1], "text"):
            new_nodes.append(TextNode(text, TextType.TEXT))
        print(f"DEBUG 1: {new_nodes}")
    return new_nodes