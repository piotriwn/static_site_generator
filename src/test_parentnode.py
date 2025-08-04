import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_no_tag(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_complex_case(self):
        navigation_items = [
            LeafNode("b", "Bold Item"),
            LeafNode("a", "Link Text"),
            LeafNode("li", "List Item")
        ]
        article_content = ParentNode("p", [
            LeafNode("b", "Article Title"),
            ParentNode("div", [
                ParentNode("span", [
                    LeafNode(None, "Plain text content")
                ]),
                LeafNode("b", "Important note")
            ]),
            LeafNode("p", "Article paragraph"),
            ParentNode("div", navigation_items, props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
            )
        ])
        main_container = ParentNode("div", [
            article_content,
            LeafNode("p", "Footer text")
        ])
        self.assertEqual(
            main_container.to_html(),
            "<div><p><b>Article Title</b><div><span>Plain text content</span><b>Important note</b></div><p>Article paragraph</p><div href=\"https://www.google.com\" target=\"_blank\"><b>Bold Item</b><a>Link Text</a><li>List Item</li></div></p><p>Footer text</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
