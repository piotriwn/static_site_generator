import unittest

from blocks import BlockType, markdown_to_blocks, block_to_block_type


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


if __name__ == "__main__":
    unittest.main()
