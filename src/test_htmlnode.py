import unittest
from htmlnode import HtmlNode, LeafNode


class TestHtmlNode(unittest.TestCase):
    def test_html_node_None(self):
        html_node = HtmlNode()
        html_props = (html_node.tag, html_node.value, html_node.children, html_node.props)
        for prop in html_props:
            self.assertIsNone(prop)

    def test_html_node_props_to_html(self):
        html_node = HtmlNode("raww", "{Key: 2342, pair: {one : 1, Two: 2}}", "325235",
                             {"href": "https://www.google.com", "target": "_blank"}
                             )
        self.assertEqual(html_node.PROPS_TO_HTML(), ' href="https://www.google.com" target="_blank"')

    def test_html_leaf_node(self):
        New_leaf = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(New_leaf.TO_HTML(), "<p>This is a paragraph of text.</p>")

    def test_html_leaf_node_two(self):
        New_leaf2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(New_leaf2.TO_HTML(), '<a href="https://www.google.com">Click me!</a>')

if __name__ == "__main__":
    unittest.main()
