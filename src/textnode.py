from htmlnode import LeafNode

text_type_dict = {
    "text": None,
    "bold": "b",
    "italic": "i",
    "code": "code",
    "link": "a",
    "image": "img"
}


class TextNode:
    def __init__(self, text, text_Type, url=None) -> None:
        self.text = text
        self.text_Type = text_Type
        self.url = url

    def text_node_to_html_node(self) -> LeafNode:
        if self.text_Type not in text_type_dict:
            raise Exception(f"Text type not supported: {self.text_Type}")
        else:
            if self.text_Type == "link":
                return LeafNode(text_type_dict[self.text_Type], self.text, {"href": f"{self.url}"}).to_html()
            elif self.text_Type == "image":
                return LeafNode(text_type_dict[self.text_Type], "", {"src": f"{self.url}", "alt": self.text}).to_html()
            else:
                return LeafNode(text_type_dict[self.text_Type], self.text).to_html()

    def __eq__(self, other):
        return (
                self.text == other.text and
                self.text_Type == other.text_Type and
                self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode( {self.text}, {self.text_Type}, {self.url} )"

# node = TextNode("Hello World", 'bold', url="")
# node.text_node_to_html_node()
