from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have a tag.")
        if not self.children:
            raise ValueError("All parent nodes must have at least 1 child.")
        resultant_str = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            resultant_str += child.to_html()
        resultant_str += f"</{self.tag}>"
        return resultant_str
