class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        # An HTMLNode without a tag will just render as raw text
        self.tag = tag
        # An HTMLNode without a value will be assumed to have children
        self.value = value
        # An HTMLNode without children will be assumed to hava a value
        self.children = children
        # An HTMLNode without props simply won't have any attributes
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        parts = []
        for key, value in self.props.items():
            parts.append(f' {key}="{value}"')
        
        return "".join(sorted(parts))
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("Missing Value!")
        
        if self.tag is None:
            return f"{self.value}"
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing HTML-Tag!")
        
        if self.children is None:
            raise ValueError("Missing children!")
        
        parts = []
        for child in self.children:
            if hasattr(child, "to_html"):
                func = getattr(child, "to_html")
                parts.append(func())
        
        return f"<{self.tag}{self.props_to_html()}>{''.join(parts)}</{self.tag}>" 