import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        text = "Hello, world"
        tag = "p"
        node = LeafNode(tag, text)
        expected_to_html = f"<p>{text}</p>"
        self.assertEqual(node.to_html(), expected_to_html)

    def test_leaf_to_html_a_with_props(self):
        text = "Click me!"
        tag = "a"
        props = {"href": "https://www.google.com"}
        node = LeafNode(tag, text, props)
        expected_to_html = "<a href=\"https://www.google.com\">Click me!</a>"
        self.assertEqual(node.to_html(), expected_to_html)

    def test_no_value(self):
        tag = "li"
        node = LeafNode(tag, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_repr(self):
        text = "Click me!"
        tag = "a"
        props = {"href": "https://www.google.com"}
        node = LeafNode(tag, text, props)
        expected_repr = f"tag = {tag}, value = {text}, children = None, props = {props}"
        self.assertEqual(expected_repr, node.__repr__())


if __name__ == "__main__":
    unittest.main()
