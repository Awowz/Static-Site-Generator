

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None or not isinstance(self.props, dict): return ""
        buffer = ""
        for x in self.props:
            buffer += f" {x}=\"{self.props[x]}\""
        return buffer
    
    def __repr__(self):
        return f"HTMLNode -> tag: {self.tag} | value: {self.value} | props: {self.props_to_html()}\nchildren: {self.children}"