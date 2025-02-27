

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props == None or not isinstance(self.props, dict): return ""
        buffer = ""
        for x in self.props:
            buffer += f" {x}=\"{self.props[x]}\""
        return buffer
    
    def __repr__(self):
        return f"HTMLNode -> tag: {self.tag} | value: {self.value} | props: {self.props_to_html()}\nchildren: {self.children}"
    


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None: raise ValueError("LeafNode self.value must have a value")
        if self.tag == None: return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"