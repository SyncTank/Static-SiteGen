from src.htmlnode import LeafNode
from textnode import TextNode


def text_node_to_html_node(text_node):
    if text_node.text_Type not in text_node.text_type_dict:
        raise Exception(f"Text type not supported: {text_node.text_type}")
    else:
        if text_node.text_Type == "html":
            return LeafNode(text_node.text_type_dict[text_node.text_Type], text_node.text, text_node.url)
        else:
            return LeafNode(text_node.text_type_dict[text_node], text_node.text)


def main() -> None:
    text_node = TextNode('This is a text node', 'bold', 'https://www.boot.dev')
    html_node = text_node_to_html_node(text_node)
    print()


main()
