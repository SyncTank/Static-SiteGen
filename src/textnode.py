from htmlnode import LeafNode
import re

text_type_dict = {
    "text": None,
    "bold": "b",
    "italic": "i",
    "code": "code",
    "link": "a",
    "image": "img"
}
delimiter_dict = {
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

delimiter_dict_pattern = {
    #"text": r'(?<![`*])[a-zA-Z]+(?![`*])',
    "bold": r'(?<!\*\s)\*\*([^\*]+)\*\*',  # **
    "italic": r'(?<!\*\s)\*([^\*]+)\*(?!\*)',  # *
    "code": r'```(.*?)```',  # ```
    "link": r'\[(.*?)\]\((.*?)\)',  # [*](*)
    "image": r'\!\[(.*?)\]\((.*?)\)',  # ![*](*)
}


def split_nodes_delimiter(old_node) -> list:
    text_node_list = []
    buffer_list = {}
    string_builder = ""
    temp_node = old_node.text.split(' ')
    temp3 = old_node.text

    print(temp3)

    if old_node.text is None:
        raise Exception("Invalid Markdown syntax")

    if old_node.text_Type == "text":
        return [TextNode(old_node.text, 'text', None)]

    for key, value in delimiter_dict_pattern.items():
        found_match = re.findall(delimiter_dict_pattern[key], temp3)
        position_match = re.search(delimiter_dict_pattern[key], temp3)
        if bool(found_match):
            buffer_list[f'{key}'] = found_match

    print(buffer_list)
    text_obj = {}
    for item in buffer_list:
        if len(buffer_list[item]) > 1:
            for sub in buffer_list[item]:
                text_obj[temp3.index(sub)] = (item, sub)
        else:
            obj_key = temp3.index((buffer_list[item][0]))
            obj_value = buffer_list[item][0]
            text_obj[obj_key] = (item, obj_value)

    sort_text_obj = dict(sorted(text_obj.items()))

    print(sort_text_obj)

    #print(temp_node)
    #delimiter_type = delimiter_dict[old_node.text_Type]
#
    #for word in temp_node:
    #    if delimiter_type in word:
    #        if len(string_builder) != 0:
    #            text_node_list.append(TextNode(string_builder, 'text'))
    #            string_builder = ''
    #            text_node_list.append(TextNode(word.replace(delimiter_type, ""), old_node.text_Type))
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
