from src.htmlnode import LeafNode
from textnode import TextNode


def main() -> None:
    text_node = TextNode('This is a text node', 'link', 'https://www.boot.dev')
    print(text_node)


main()
