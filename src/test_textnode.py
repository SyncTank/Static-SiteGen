import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_neg(self):
        node = TextNode("This is not a drill", "bold")
        node2 = TextNode("This is not a drill", "bold")
        self.assertEqual(node, node2)

    def test_eq_set(self):
        node = TextNode("This is not a drill", "Italic")
        node2 = TextNode("This is not a drill", "Italic", None)
        self.assertEqual(node, node2)

    def test_text_to_html_p(self):
        node = TextNode("This is not a drill", "text")
        self.assertIsNotNone(node.text_node_to_html_node(), print(node.text_node_to_html_node()))

    def test_text_to_html_bold(self):
        node = TextNode("This is not a drill", "bold")
        self.assertIsNotNone(node.text_node_to_html_node(), print(node.text_node_to_html_node()))

    def test_text_to_html_no_link(self):
        node = TextNode("This is not a drill", "link")
        self.assertIsNotNone(node.text_node_to_html_node(), print(node.text_node_to_html_node()))

    def test_text_to_html_link(self):
        node = TextNode("This is not a drill", "link", "https://www.google.com")
        self.assertIsNotNone(node.text_node_to_html_node(), print(node.text_node_to_html_node()))

    def test_text_to_html_image(self):
        node = TextNode("This is not a drill", "image", "url/of/image.jpg")
        self.assertIsNotNone(node.text_node_to_html_node(), print(node.text_node_to_html_node()))


if __name__ == "__main__":
    unittest.main()
