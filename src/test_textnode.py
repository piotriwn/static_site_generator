import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "some_url")
        self.assertNotEqual(node, node2)

    def test_url(self):
        text = "1 tEst/"
        type = TextType.LINK
        url = ":crazy url"
        node = TextNode(text, type, url)
        expected_repr = f"TextNode({text}, {type.value}, {url})"
        self.assertEqual(node.__repr__(), expected_repr)

    def test_repr(self):
        text = "FAANCY node 1"
        type = TextType.LINK
        node = TextNode(text, type)
        repr_str = node.__repr__()
        expected_repr = f"TextNode({text}, {type.value}, {None})"
        self.assertEqual(repr_str, expected_repr)


if __name__ == "__main__":
    unittest.main()
