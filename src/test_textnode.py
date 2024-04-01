import unittest

from textnode import TextNode, inline_markdown_capture, markdown_block, html_builder


class TestTextNode(unittest.TestCase):
    def test_eq(self) -> None:
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_neg(self) -> None:
        node = TextNode("This is not a drill", "bold")
        node2 = TextNode("This is not a drill", "bold")
        self.assertEqual(node, node2)

    def test_eq_set(self) -> None:
        node = TextNode("This is not a drill", "Italic")
        node2 = TextNode("This is not a drill", "Italic", None)
        self.assertEqual(node, node2)

    def test_text_to_html_p(self) -> None:
        node = TextNode("This is not a drill", "text")
        self.assertIsNotNone(node.text_node_to_html_node(), print(node.text_node_to_html_node()))

    def test_text_to_html_bold(self) -> None:
        node = TextNode("This is not a drill", "bold")
        self.assertIsNotNone(node.text_node_to_html_node(), print(node.text_node_to_html_node()))

    def test_text_to_html_no_link(self) -> None:
        node = TextNode("This is not a drill", "link")
        self.assertIsNotNone(node.text_node_to_html_node(), print(node.text_node_to_html_node()))

    def test_text_to_html_link(self) -> None:
        node = TextNode("This is not a drill", "link", "https://www.google.com")
        self.assertIsNotNone(node.text_node_to_html_node(), print(node.text_node_to_html_node()))

    def test_text_to_html_image(self) -> None:
        node = TextNode("This is not a drill", "image", "url/of/image.jpg")
        self.assertIsNotNone(node.text_node_to_html_node(), print(node.text_node_to_html_node()))

    def test_nodes_delimiter_text(self) -> None:
        node = "This is not a drill"
        new_node = inline_markdown_capture(node, "text")
        self.assertIsNotNone(new_node, print(new_node))

    def test_nodes_delimiter_TextNode(self) -> None:
        node = TextNode("This is not a drill", "text", None)
        new_node = inline_markdown_capture(node, "text")
        self.assertIsNotNone(new_node, print(new_node))

    def test_nodes_delimiter_bold(self) -> None:
        node = "This is **not** a drill"
        new_node = inline_markdown_capture(node)
        self.assertIsNotNone(new_node, print(new_node))

    def test_nodes_delimiter_italic(self) -> None:
        node = "This is *not* a drill"
        new_node = inline_markdown_capture(node)
        self.assertIsNotNone(new_node, print(new_node))

    def test_nodes_delimiter_double_italic(self) -> None:
        node = "This is *not* a *drill* test"
        new_node = inline_markdown_capture(node)
        self.assertIsNotNone(new_node, print(new_node))

    def test_nodes_delimiter_code(self) -> None:
        node = "This is `not` a `drill` test"
        new_node = inline_markdown_capture(node)
        self.assertIsNotNone(new_node, print(new_node))

    def test_nodes_delimiter_two_types(self) -> None:
        node = "This is *not* a `drill` test"
        new_node = inline_markdown_capture(node)
        self.assertIsNotNone(new_node, print(new_node))

    def test_nodes_delimiter_link(self) -> None:  # review
        node = "This is [here sdfa](www.google.com) a drill"
        new_node = inline_markdown_capture(node)
        self.assertIsNotNone(new_node, print(new_node))

    def test_nodes_delimiter_link_italic(self) -> None:  # review
        node = "This is [here sdfa](www.google.com) *a* drill"
        new_node = inline_markdown_capture(node)
        self.assertIsNotNone(new_node, print(new_node))

    def test_nodes_delimiter_img(self) -> None:
        node = "This `is` ![alt text for image](url/of/image.jpg) a drill"
        new_node = inline_markdown_capture(node)
        self.assertIsNotNone(new_node, print(new_node))

    def test_nodes_delimiter_final(self) -> None:
        node =  "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        new_node = inline_markdown_capture(node)
        self.assertIsNotNone(new_node, print(new_node))

    def test_nodes_delimiter_final_comp(self) -> None:
        node = "This is **text** with an *italic* word and a `code block` and an ![image here is](https://i.imgur.com/zjjcJKZ.png) and a [new link founded](https://boot.dev)"
        new_node = inline_markdown_capture(node)
        for item in new_node:
            print(item)
        print()
        self.assertIsNotNone(new_node, print(new_node))

    def test_node_markdown_delimit_pattern(self) -> None:
        block = ("""# This is a heading

                This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                * This is a list item
                * This is another list item
                 """)
        read_block = markdown_block(block)
        self.assertIsNotNone(read_block, print(read_block))

    def test_node_markdown_delimit_pattern_dict(self) -> None:
        block = (""" 
                * This is a list
                * with items
                1. This is a list item
                - yes this is it
                - you will know

                1. that I will win
                2. in a battle of fonts

                > though 

                # we will 
                ## prevail
                ### against the evil of
                ##### man
                 """)
        read_block = markdown_block(block)
        self.assertIsNotNone(read_block, print(read_block))

    def test_node_markdown_delimit_pattern_two(self) -> None:
        block = ("""This is **bolded** paragraph

                This is another paragraph with *italic* text and `code` here
                This is the same paragraph on a new line
                
                ```
                print("heel")
                console.log("hello");
                std::cout << "hello" << std::endl;
                system.println("hello");
                ```
                

                * This is a list
                * with items
                
                - yes this is it
                - you will know
                
                1. that I will win
                2. in a battle of fonts
                
                > though 
                
                # we will 
                ## prevail
                ### against the evil of
                #### man
                 """)
        read_block = markdown_block(block)
        self.assertIsNotNone(read_block, print(read_block))

    def test_html_builder_node_block(self) -> None:
        block = [("""# This is a heading

                This is a paragraph of text. It has some **bold** and *italic* words inside of it.
                
                ```
                code block here
                test me please
                IEEE
                ```

                * This is a list item
                * This is another list item
                 """)]
        read_block = html_builder(block)
        self.assertIsNotNone(read_block, print(read_block))

    def test_html_builder_node_blocks(self) -> None:
        block = [("""# This is a heading

                This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                * This is a list item
                * This is another list item
                 """),
                 ("""This is **bolded** paragraph

                        This is another paragraph with *italic* text and `code` here
                        This is the same paragraph on a new line

                        ```
                        print("heel")
                        console.log("hello");
                        std::cout << "hello" << std::endl;
                        system.println("hello");
                        ```


                        * This is a list
                        * with items

                        - yes this is it
                        - you will know

                        1. that I will win
                        2. in a battle of fonts

                        > though 

                        # we will 
                        ## prevail
                        ### against the evil of
                        #### man
                         """)
                 ]
        read_block = html_builder(block)
        self.assertIsNotNone(read_block, print(read_block))

if __name__ == "__main__":
    unittest.main()
