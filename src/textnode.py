from htmlnode import LeafNode


class TextNode:
    def __init__(self, text, text_Type, url=None) -> None:
        self.text = text
        self.text_Type = text_Type
        self.url = url
        self.text_type_dict = {
            "text": "",
            "bold": "b",
            "italic": "i",
            "code": "code",
            "link": "a",
            "image": "img"
        }

    def text_node_to_html_node(self):
        if self.text_Type not in self.text_type_dict: # test types to work good
            raise Exception(f"Text type not supported: {self.text_Type}")
        else:
            if self.text_Type == "html":
                return LeafNode(self.text_type_dict[self.text_Type], self.text, self.url).to_html()
            else:
                return LeafNode(self.text_type_dict[self.text_Type], self.text).to_html()

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
