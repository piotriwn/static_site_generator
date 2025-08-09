from enum import Enum
from re import match, findall, DOTALL
from parentnode import ParentNode
from leafnode import LeafNode
from functions import text_to_html_nodes


class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "header"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


def markdown_to_blocks(markdown):
    return [element.strip() for element in markdown.split("\n\n") if element.strip()]


def block_to_block_type(block):
    if match(r"^#{1,6}", block):
        return BlockType.HEADING
    if match(r"^```.+```", block, DOTALL):
        return BlockType.CODE

    split_by_newline = block.split("\n")
    if all([line.startswith(">") for line in split_by_newline]):
        return BlockType.QUOTE

    if all([line.startswith("- ") for line in split_by_newline]):
        return BlockType.UNORDERED_LIST

    counter = 1
    matched_ol = False
    for line in split_by_newline:
        if match(rf"^{counter}\. .+", line):
            counter += 1
            matched_ol = True
            continue
        break

    if counter - 1 == len(split_by_newline) and matched_ol:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.CODE:
        matches = findall(r"```(.*)```", block, DOTALL)
        code_text = matches[0] if matches else block
        return ParentNode("pre", [LeafNode("code", code_text)])

    if block_type == BlockType.HEADING:
        level = len(match(r"^(#{1,6})", block).group(1))
        text = block[level:].strip()
        return ParentNode(f"h{level}", text_to_html_nodes(text))

    if block_type == BlockType.QUOTE:
        lines = [line[1:].strip() for line in block.split("\n")]
        text = " ".join(lines)
        return ParentNode("blockquote", text_to_html_nodes(text))

    if block_type == BlockType.UNORDERED_LIST:
        split_by_newline = block.split("\n")
        list_of_html_nodes = []
        for element in split_by_newline:
            list_el_content = findall(r"^- (.*)$", element)[0]
            list_of_html_nodes.append(ParentNode(
                "li", text_to_html_nodes(list_el_content)))
        return ParentNode(block_type.value, list_of_html_nodes)

    if block_type == BlockType.ORDERED_LIST:
        split_by_newline = block.split("\n")
        list_of_html_nodes = []
        for element in split_by_newline:
            list_el_content = findall(r"^[0-9]+\. (.*)$", element)[0]
            list_of_html_nodes.append(ParentNode(
                "li", text_to_html_nodes(list_el_content)))
        return ParentNode(block_type.value, list_of_html_nodes)

    return ParentNode(block_type.value, text_to_html_nodes(block))


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = [block_to_html_node(block) for block in blocks]
    parent = ParentNode("div", html_nodes)
    return parent
