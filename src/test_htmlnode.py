import unittest
from htmlnode import HtmlNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_html_node_None(self) -> None:
        html_node = HtmlNode()
        html_props = (html_node.tag, html_node.value, html_node.children, html_node.props)
        for prop in html_props:
            self.assertIsNone(prop)

    def test_html_node_props_to_html(self) -> None:
        html_node = HtmlNode("raw", "{Key: 2342, pair: {one : 1, Two: 2}}", "325235",
                             {"href": "https://www.google.com", "target": "_blank"}
                             )
        self.assertEqual(html_node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        print(html_node)

    def test_html_leaf_node(self) -> None:
        new_leaf = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(new_leaf.to_html(), "<p>This is a paragraph of text.</p>")
        print(new_leaf.to_html())

    def test_html_leaf_node_two(self) -> None:
        new_leaf2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(new_leaf2.to_html(), '<a href="https://www.google.com">Click me!</a>')
        print(new_leaf2.to_html())

    def test_parent_node_leafs(self) -> None:
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertIsNotNone(node.to_html(), print(node.to_html()))

    def test_parent_node_parents(self) -> None:
        node = ParentNode("p", ParentNode("p", [
            LeafNode("b", "Bold text"),
            LeafNode("i", "italic text"),
            LeafNode("a", "Normal text"),
            LeafNode("b", "teste"),
        ]))
        self.assertIsNotNone(node.to_html(), print(node.to_html()))

    def test_parent_node_parents_double(self) -> None:
        node = ParentNode("p", ParentNode("p", ParentNode("p",
                                                          [
                                                              LeafNode("b", "Bold text"),
                                                              LeafNode("i", "italic text"),
                                                              LeafNode("a", "Normal text"),
                                                              LeafNode("b", "teste"),
                                                          ]
                                                          )))
        self.assertIsNotNone(node.to_html(), print(node.to_html()))

    def test_parent_node_parents_fail(self) -> None:
        node = ParentNode("p", [])
        with self.assertRaises(ValueError) as context:
            node.to_html()

        self.assertEqual(str(context.exception), "No child")

    def test_parent_node_leaf_fail(self) -> None:
        node = LeafNode("b", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()

        self.assertEqual(str(context.exception), str(context.exception))
        print(str(context.exception))


if __name__ == "__main__":
    unittest.main()
