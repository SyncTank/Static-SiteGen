class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def TO_HTML(self):
        raise NotImplementedError("TO_HTML method is not implemented")

    def PROPS_TO_HTML(self):
        if self.props is None:
            return "None"
        temp_string = ""
        for key, value in self.props.items():
            temp_string += " "
            temp_string += f'{key}="{value}"'
        return temp_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def TO_HTML(self):
        if self.value is None:
            raise ValueError("LeafNode value cannot be None")
        elif self.tag is None:
            return f"self.value"
        else:
            if self.tag == "p":
                return f"<{self.tag}>{self.value}</{self.tag}>"
            elif self.tag == "a":
                return f"<{self.tag}{self.PROPS_TO_HTML()}>{self.value}</{self.tag}>"
            else:
                return None

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
