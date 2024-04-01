from htmlnode import LeafNode, ParentNode
import re

text_type_dict = {
    "text": None,
    "blockquote": "blockquote",
    "br": "br",
    "bold": "b",
    "italic": "i",
    "code": "code",
    "codeblock": "codeblock",
    "link": "a",
    "image": "img",
    "para": "p"
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

block_delimiter_simple_pattern = {
    "paragraph": r'^[A-Za-z\s]*$',  # Just text
    "blockquote": r'^\s*[\>]\s*(.*)',  # > words
    "code": r'```([\s\S]*?)```',  # ``` words ```
}

block_delimiter_dict_pattern = {
    "h": r'^\s*[\#]\s*(.*)',  # (1-6 number of # words)
    "ul": r'^\s*[\*-]\s*(.*)',  # * or - words unordered list
    "ol": r'^\s*[\d]\s*(.*)',  # 1. words ordered list
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
    second_buffer = []
    text = []

    for item in mark_buffer:
        second_buffer.append(item.strip().rstrip())

    string_builder = ""
    capturing = False
    for item in second_buffer:
        if item == '```':
            capturing = not capturing
            if len(string_builder) > 0:
                text.append(TextNode(string_builder, "codeblock", None))
        if capturing and item != '```':
            string_builder += item + "\n"
        elif not capturing and item != '```':
            text.append(item)

    temp_buffer = []
    for i, v in enumerate(text):
        find_match = False
        for limit in block_delimiter_simple_pattern:
            if type(v) is TextNode:
                break
            if v == '' or v.isspace():
                break
            find_match = re.search(block_delimiter_simple_pattern[limit], v)
            if bool(find_match):
                if limit == 'paragraph':
                    temp_buffer.append(TextNode(v, "para", None))
                    break
                elif limit == 'blockquote':
                    temp_buffer.append(TextNode(v[2:], "blockquote", None))
                    break
        if not find_match:
            temp_buffer.append(v)

    block_items = []
    temp_block = []
    limit_type = None
    for i, v in enumerate(temp_buffer):
        if type(v) is TextNode:
            block_items.append(v)
            continue
        if v == '' or v.isspace():
            if len(temp_block) > 0:
                leaf_childerns = []
                if limit_type == 'ul' or limit_type == 'ol':
                    for item in temp_block:
                        leaf_childerns.append(LeafNode("li", item[2:]))
                    block_items.append(ParentNode(limit_type, leaf_childerns.copy(), None))
                elif limit_type == 'h':
                    for j in range(0, len(temp_block)):
                        temp_value = temp_block[j].strip("#").lstrip(" ")
                        block_items.append(LeafNode("h" + str(temp_block[j].count("#")), temp_value, None))
                else:
                    block_items.append(temp_block.copy())
                temp_block = []
                limit_type = None
                block_items.append(v)
            else:
                block_items.append(v)
        else:
            if limit_type is not None and not limit_type.isspace() and limit_type != '':
                old_match = re.search(block_delimiter_dict_pattern[limit_type], v)
                if bool(old_match):
                    temp_block.append(v)
                else:
                    leaf_childerns = []
                    if limit_type == 'ul' or limit_type == 'ol':
                        for item in temp_block:
                            leaf_childerns.append(LeafNode("li", item[2:]))
                        block_items.append(ParentNode(limit_type, leaf_childerns.copy(), None))
                    elif limit_type == 'h':
                        for j in range(0, len(temp_block)):
                            temp_value = temp_block[j].strip("#").lstrip(" ")
                            block_items.append(LeafNode("h" + str(temp_block[j].count("#")), temp_value, None))
                    else:
                        block_items.append(temp_block.copy())
                    temp_block = []
                    limit_type = None
            if limit_type is None:
                for limit in block_delimiter_dict_pattern:
                    matching = re.search(block_delimiter_dict_pattern[limit], v)
                    if bool(matching):
                        limit_type = limit
                        temp_block.append(v)
                        break
                if not temp_block:
                    block_items.append(v)

    for i, v in enumerate(block_items):
        if type(v) is not str:
            text_nodes_final.append(v)
        else:
            if v.isspace() or v == "":
                text_nodes_final.append(TextNode("", "br"))
            else:
                text_nodes_final.append(inline_markdown_capture(v))

    return text_nodes_final


def html_builder(blocks) -> list:
    html_elements = []
    html_buffer = []

    if len(blocks) == 0:
        raise Exception("No blocks found")
    elif len(blocks) == 1:
        temp_buffer = markdown_block(blocks[0])
        for block in temp_buffer:
            block_relation = type(block)
            if block_relation is LeafNode or block_relation is ParentNode:
                html_elements.append(block.to_html())
            elif block_relation is TextNode:
                html_elements.append(block.text_node_to_html_node())
            elif block_relation is list:
                string_builder = ""
                for block_node in block:
                    string_builder += block_node.text_node_to_html_node()
                html_elements.append(string_builder)
    elif len(blocks) > 1:
        for block in blocks:
            temp_buffer = markdown_block(block)
            for block_node in temp_buffer:
                block_relation = type(block_node)
                if block_relation is LeafNode or block_relation is ParentNode:
                    html_buffer.append(block_node.to_html())
                elif block_relation is TextNode:
                    html_buffer.append(block_node.text_node_to_html_node())
                elif block_relation is list:
                    string_builder = ""
                    for node in block_node:
                        string_builder += node.text_node_to_html_node()
                    html_buffer.append(string_builder)
            html_elements.append(html_buffer)
    else:
        raise Exception("Not a expected block")

    return html_elements


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
