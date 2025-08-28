import unittest

from page import extract_title


class Test_extract_title(unittest.TestCase):
    def test_good_markdown(self):
        markdown = """
# Title 1 

It's just some markdown innit
"""
        self.assertEqual("Title 1", extract_title(markdown))

    def test_h1_not_at_top(self):
        markdown = """
Who said

# That h1

Needs to be on top?
"""
        self.assertEqual("That h1", extract_title(markdown))

    def test_no_h1(self):
        markdown = """
Way to forget

> Pretty

but no h1

## h2 though!
"""
        self.assertRaisesRegex(ValueError, "There must be 1 h1 header")

    def test_two_h1(self):
        markdown = """
# Hello

but I realy said

# HELLLO!11!! 
"""

        self.assertRaisesRegex(
            ValueError, "There cannot be more than 1 h1 header")


if __name__ == "__main__":
    unittest.main()
