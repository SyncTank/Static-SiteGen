class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("TO_HTML method is not implemented")

    def props_to_html(self):
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
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode value cannot be None")
        elif self.tag is None and self.value is not None:
            return f"{self.value}"
        else:
            if self.tag == "a":
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            else:
                return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children, props)
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag has no object")
        elif self.children is None:
            raise ValueError("No child")
        else:
            means = ""
            means += "<" + self.tag + ">"

            for child in self.children:
                means += child.to_html()

            means += "</" + self.tag + ">"
