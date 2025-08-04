class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        to_return = ""
        for k, v in self.props.items():
            to_return += f" {k}=\"{v}\""
        return to_return

    def __repr__(self):
        return f"tag = {self.tag if not None else "None"}, value = {self.value if not None else "None"}, children = {self.children if not None else "None"}, props = {self.props if not None else "None"}"
