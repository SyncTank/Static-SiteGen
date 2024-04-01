from src.htmlnode import LeafNode
from textnode import TextNode
from os import path, mkdir, listdir

def dir_copy():
    pass

def main() -> None:
    text_node = TextNode('This is a text node', 'link', 'https://www.boot.dev')
    print(text_node)


main()
