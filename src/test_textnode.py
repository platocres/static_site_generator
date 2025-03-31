import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a different text node", TextType.NORMAL, "this is a url")
        node4 = TextNode("This is a text node", TextType.BOLD, None)
        node5 = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node, node2)
    # def test_not_eq(self):
        
    #     self.assertNotEqual()


if __name__ == "__main__":
    unittest.main()