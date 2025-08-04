from enum import Enum
from re import match


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    return [element.strip() for element in markdown.split("\n\n") if element]


def block_to_block_type(block):
    if match(block, r"$#{1,6}"):
        return BlockType.HEADING
    if match(block, r"^```.+```"):
        return BlockType.CODE

    split_by_newline = block.split("\n")
    if all([line.startswith(">") for line in split_by_newline]):
        return BlockType.QUOTE

    if all([line.startswith("- ") for line in split_by_newline]):
        return BlockType.UNORDERED_LIST

    counter = 1
    for line in split_by_newline:
        if match(line, rf"^{counter}\. .+"):
            counter += 1
            continue
        break
    if counter == len(split_by_newline):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

###


# def block_to_html_node(block):
#     block_type = block_to_block_type(block)
#     match block_type:
#         case BlockType.HEADING:
#             return LeafNode(None, text_node.text)
#         case TextType.BOLD:
#             return LeafNode("b", text_node.text)
#         case TextType.ITALIC:
#             return LeafNode("i", text_node.text)
#         case TextType.CODE:
#             return LeafNode("code", text_node.text)
#         case TextType.LINK:
#             return LeafNode("a", text_node.text, {"href": text_node.url})
#         case TextType.IMAGE:
#             return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
#         case _:
#             raise ValueError(
#                 "Incorrect text type, must be a member of TextType enum.")


# def markdown_to_html_node(markdown):
#     pass
