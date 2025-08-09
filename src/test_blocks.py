import unittest

from blocks import BlockType, markdown_to_blocks, block_to_block_type, block_to_html_node, markdown_to_html_node
from parentnode import ParentNode
from leafnode import LeafNode


class Test_markdown_to_blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class Test_block_to_block_type(unittest.TestCase):
    def block_to_block_type_heading(self):
        md = """
### This is a paragraph
"""
        self.assertEqual(
            BlockType.HEADING,
            block_to_block_type(md)
        )

    def block_to_block_type_code(self):
        md = """
```
print("Hello, world")
```
"""
        self.assertEqual(
            BlockType.CODE,
            block_to_block_type(md)
        )

    def block_to_block_type_quote(self):
        md = """
> Oh no!
> Anyway...
"""
        self.assertEqual(
            BlockType.QUOTE,
            block_to_block_type(md)
        )

    def block_to_block_type_unordered_list(self):
        md = """
- bla bla
- bla
"""
        self.assertEqual(
            BlockType.UNORDERED_LIST,
            block_to_block_type(md)
        )

    def block_to_block_type_ordered_list(self):
        md = """
1. Primo
2. Second primo
3.
"""
        self.assertEqual(
            BlockType.ORDERED_LIST,
            block_to_block_type(md)
        )

    def block_to_block_type_paragraph(self):
        md = """
Vanilla text
nothing fancy
"""
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type(md)
        )

    def block_to_block_type_ordered_list_incorrect_numbering(self):
        md = """
1. Primo
3. Third primo, who needs the second
"""
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type(md)
        )

    def block_to_block_type_ordered_list_incorrect_no_dot(self):
        md = """
1. Primo
2- No space here
"""
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type(md)
        )


class Test_block_to_html_node(unittest.TestCase):
    def test_block_to_html_node_simple(self):
        md = "This is **bolded** paragraph text in a p"
        expected_result = ParentNode("p", [
            LeafNode(None, "This is "),
            LeafNode("b", "bolded"),
            LeafNode(None, " paragraph text in a p"),
        ])
        self.assertEqual(
            block_to_html_node(md),
            expected_result
        )

    def test_block_to_html_node_ul(self):
        md = "- what the\n- heck is _that_"
        expected_result = ParentNode("ul", [
            ParentNode("li", [
                LeafNode(None, "what the"),
            ]),
            ParentNode("li", [
                LeafNode(None, "heck is "),
                LeafNode("i", "that"),
            ]),
        ])
        self.assertEqual(
            block_to_html_node(md),
            expected_result
        )


class Test_markdown_to_html_node(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()
