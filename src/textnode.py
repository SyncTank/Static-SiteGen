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
