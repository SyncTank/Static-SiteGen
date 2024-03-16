from htmlnode import LeafNode

text_type_dict = {
    "text": None,
    "bold": "b",
    "italic": "i",
    "code": "code",
    "link": "a",
    "image": "img"
}
delimiter_dict = {
    "text": None,
    "bold": "**",
    "italic": "*",
    "code": "```",
    "link": "[",
    "image": "!",
    "header": "#",
    "unordered": "* ",
    "quotes": "> ",
    "order": ". "
}


def split_nodes_delimiter(old_node, text_Type) -> list:
    text_node_list = []
    string_builder = ""
    delimiter_type = delimiter_dict[text_Type]
    temp_node = old_node.text.split(' ')

    if old_node.text is None:
        raise Exception("Invalid Markdown syntax")

    if text_Type == "text" or type(old_node) is not TextNode:
        return [TextNode(old_node.text, text_Type)]

    temp_string = ""
    for word in old_node.text:

        string_builder += word


    print(string_builder)
    print(old_node.text)
    print(temp_node)

    #for word in temp_node:
    #    if delimiter_type in word:
    #        if len(string_builder) != 0:
    #            text_node_list.append(TextNode(string_builder, 'text'))
    #            string_builder = ''
#
    #        text_node_list.append(TextNode(word.replace(delimiter_type, ""), text_Type))
    #    else:
    #        string_builder += word + " "
#
    #if len(string_builder) != 0:
    #    text_node_list.append(TextNode(string_builder, 'text'))

    return text_node_list


class TextNode:
    def __init__(self, text, text_Type, url=None) -> None:
        self.text = text
        self.text_Type = text_Type
        self.url = url

    def text_node_to_html_node(self) -> str:
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
