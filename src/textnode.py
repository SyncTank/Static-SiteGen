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

inline_delimiter_dict_pattern = {
    "bold": r'(?<!\*)\*\*([^\*]+)\*\*',  # **
    "italic": r'(?<!\*)\*([^\*]+)\*(?!\*)',  # *
    "code": r'`(.*?)`',  # `
    "link": r'\s\[(.*?)\]\((.*?)\)',  # [*](*)
    "image": r'!\[(.*?)\]\((.*?)\)',  # ![*](*)
}

block_delimiter_dict_pattern = {
    "paragraph": r'^[A-Za-z\s]*$',  # Just text
    "heading": r'^\s*[\#]\s*(.*)',  # (1-6 number of # words)
    "code": r'```([\s\S]*?)```',  # ``` words ```
    "quote": r'^\s*[\>]\s*(.*)',  # > words
    "unordered": r'^\s*[\*-]\s*(.*)',  # * or - words
    "ordered": r'^\s*[\d]\s*(.*)',  # 1. words
}


def match_reg(reg: str, sent: str, type_reg: str, matches=None):
    if matches is None:
        matches = []
    found_match = re.search(reg, sent)
    if bool(found_match):
        start_index, end_index = found_match.span()
        matches.append((start_index, end_index, found_match.group(), type_reg))
        new_sent = sent[:start_index] + len(sent[start_index:end_index]) * " " + sent[end_index:]
        match_reg(reg, new_sent, type_reg, matches)
    else:
        return None
    return matches


def inline_markdown_capture(old_node, old_node_type=None) -> list:
    text_node_list = []
    buffer_list = []
    temp_buffer_list = []
    long_buffer = []
    string_copy = old_node
    string_builder = ""

    if old_node is None:
        raise Exception("Invalid Markdown syntax")

    if old_node_type == "text":
        return [TextNode(old_node, 'text', None)]  # Careful for TextNode Tag on Text

    if old_node is TextNode:
        return old_node

    for limit in inline_delimiter_dict_pattern:
        temp_buffer_list.append(match_reg(inline_delimiter_dict_pattern[limit], string_copy, limit))

    for item in temp_buffer_list:
        if item:
            buffer_list.append(item)

    sort_buffer = sorted(buffer_list)

    for items in sort_buffer:
        for item in items:
            long_buffer.append(item)

    counter_buffer = 0
    for i, v in enumerate(string_copy):
        if i == long_buffer[counter_buffer][0]:
            if len(string_builder) != 0:
                text_node_list.append(TextNode(string_builder, "text"))
                string_builder = ""

            slice_setter = long_buffer[counter_buffer]
            if long_buffer[counter_buffer][3] == 'italic' or long_buffer[counter_buffer][3] == 'code':
                text_node_list.append(TextNode(string_copy[slice_setter[0] + 1:slice_setter[1] - 1], slice_setter[3]))
            elif long_buffer[counter_buffer][3] == 'bold':
                text_node_list.append(TextNode(string_copy[slice_setter[0] + 2:slice_setter[1] - 2], slice_setter[3]))
            elif long_buffer[counter_buffer][3] == 'image':
                image_text = long_buffer[counter_buffer][2][2:-1]
                image_buffer = image_text.split("](")
                text_node_list.append(TextNode(image_buffer[0], slice_setter[3], image_buffer[1]))
            elif long_buffer[counter_buffer][3] == 'link':
                link_text = long_buffer[counter_buffer][2][2:-1]
                link_buffer = link_text.split("](")
                text_node_list.append(TextNode(link_buffer[0], slice_setter[3], link_buffer[1]))
        else:
            if i < long_buffer[counter_buffer][0] or i > long_buffer[counter_buffer][1]:
                string_builder += v
        if i == long_buffer[counter_buffer][1] and len(long_buffer) - 1 > counter_buffer:
            counter_buffer += 1

    if len(string_copy) > long_buffer[counter_buffer][1]:
        final_text = long_buffer[counter_buffer][1]
        text_node_list.append(TextNode(string_copy[final_text:], "text"))

    return text_node_list


def markdown_block(markdown) -> list:
    text_nodes_final = []
    mark_buffer = markdown.split('\n')
    temp_buffer = []
    text = []
    text_inline = []
    text_blocks = []

    for item in mark_buffer:
        if not item.isspace() and item != '':
            temp_buffer.append(item.strip().rstrip())

    string_builder = ""
    capturing = False
    for item in temp_buffer:
        if item == '```':
            capturing = not capturing
            if len(string_builder) > 0:
                string_builder += '```'
                text.append(string_builder)
        if capturing:
            string_builder += item + "\n"
        elif not capturing and item != '```':
            text.append(item)

    temp_buffer = []
    for i, v in enumerate(text):
        text_match = re.search(block_delimiter_dict_pattern["paragraph"], v)
        print(i, v, bool(text_match))
        if bool(text_match):
            temp_buffer.append(inline_markdown_capture(v, "text"))
        else:
            temp_buffer.append(v)

    print()

    for i, v in enumerate(temp_buffer):
        print(i, v)

    return text_nodes_final


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
