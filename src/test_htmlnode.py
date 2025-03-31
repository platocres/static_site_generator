import unittest
from htmlnode import *
from htmlnode import text_node_to_html_node  # Explicitly import the function

class TestHTMLNode(unittest.TestCase):
    def test_noteq(self):
        node1 = HTMLNode("p", "Hello, world!", None, {"class": "text"})
        node2 = HTMLNode("p", "Hello, world!", None, {"class": "text"})
        node3 = HTMLNode("p", "Hello, world!", None, {"class": "text"})
        node4 = HTMLNode("p", "Hello, world!", None, {"class": "text"})
        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node1, node4)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node = LeafNode("h1", "Hello, world!", {"class": "title"})
        self.assertEqual(node.to_html(), '<h1 class="title">Hello, world!</h1>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")





if __name__ == "__main__":
    unittest.main()