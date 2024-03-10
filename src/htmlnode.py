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
        child = (self.tag, self.value, self.children, self.PROPS_TO_HTML())
        for c in child:
            if c is not None:
                print(c)
            else:
                print("None")

html_node = HtmlNode("")
html_node.PROPS_TO_HTML()