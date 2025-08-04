import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr_all_none(self):
        node = HTMLNode()
        expected_repr = "tag = None, value = None, children = None, props = None"
        self.assertEqual(expected_repr, node.__repr__())

    def test_repr_children_none(self):
        tag = "p"
        value = "va1u3."
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(tag, value, props=props)
        expected_repr = f"tag = {tag}, value = {value}, children = None, props = {props}"
        self.assertEqual(expected_repr, node.__repr__())

    def test_repr_children(self):
        tag = "a"
        value = "va1u3."
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        children = [
            HTMLNode(tag="nice tag")
        ]
        node = HTMLNode(tag, value, children, props)
        expected_repr = f"tag = {tag}, value = {value}, children = {children}, props = {props}"
        self.assertEqual(expected_repr, node.__repr__())

    def test_props_to_html(self):
        tag = "a"
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(tag, props=props)
        expected_props_to_html = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(expected_props_to_html, node.props_to_html())


if __name__ == "__main__":
    unittest.main()
