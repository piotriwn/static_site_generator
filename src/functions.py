from textnode import TextNode, TextType
from leafnode import LeafNode
from re import findall

CHARS_ALLOWED_IN_ALT_TEXT = r"\w\s!?@#$%^&*+=\-_/;:<>,.'\""
CHARS_ALLOWED_IN_LINKS = r"\w!?@#$%^&*+=\-_/;:<>,.'\"()"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(
                "Incorrect text type, must be a member of TextType enum.")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_list.append(old_node)
            continue

        old_split_over_delimiter = old_node.text.split(delimiter)

        if len(old_split_over_delimiter) % 2 == 0:
            raise ValueError("Invalid markdown.")

        for i in range(len(old_split_over_delimiter)):
            text = old_split_over_delimiter[i]
            if text == "":
                continue
            if i % 2 == 0:
                new_list.append(TextNode(text, TextType.TEXT))
            else:
                new_list.append(TextNode(text, text_type))

    return new_list


def extract_markdown_images(text):
    return findall(fr"!\[([{CHARS_ALLOWED_IN_ALT_TEXT}]+)\]\(([{CHARS_ALLOWED_IN_LINKS}]+)\)", text)


def extract_markdown_links(text):
    return findall(fr"(?<!!)\[([{CHARS_ALLOWED_IN_ALT_TEXT}]+)\]\(([{CHARS_ALLOWED_IN_LINKS}]+)\)", text)


def split_nodes_image(old_nodes):
    new_list = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_list.append(old_node)
            continue

        extracted_images = extract_markdown_images(old_node.text)

        if extracted_images == []:
            new_list.append(old_node)
            continue

        for alt_text, link in extracted_images:
            splitted_over_full_regex = old_node.text.split(
                f"![{alt_text}]({link})", 1)
            text_before = splitted_over_full_regex[0]
            text_after = splitted_over_full_regex[1]

            if text_before:
                new_list.append(TextNode(text_before, TextType.TEXT))

            new_list.append(TextNode(alt_text, TextType.IMAGE, link))

            old_node = TextNode(text_after, TextType.TEXT)

        if old_node.text:
            new_list.append(old_node)

    return new_list


def split_nodes_link(old_nodes):
    new_list = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_list.append(old_node)
            continue

        extracted_links = extract_markdown_links(old_node.text)

        if extracted_links == []:
            new_list.append(old_node)
            continue

        for alt_text, link in extracted_links:
            splitted_over_full_regex = old_node.text.split(
                f"[{alt_text}]({link})", 1)
            text_before = splitted_over_full_regex[0]
            text_after = splitted_over_full_regex[1]

            if text_before:
                new_list.append(TextNode(text_before, TextType.TEXT))

            new_list.append(TextNode(alt_text, TextType.LINK, link))

            old_node = TextNode(text_after, TextType.TEXT)

        if old_node.text:
            new_list.append(old_node)

    return new_list


def text_to_textnodes(text):
    first_node = TextNode(text, TextType.TEXT)
    after_image_split = split_nodes_image([first_node])
    after_link_split = split_nodes_link(after_image_split)
    after_code_split = split_nodes_delimiter(
        after_link_split, "`", TextType.CODE)
    after_bold_split = split_nodes_delimiter(
        after_code_split, "**", TextType.BOLD)
    after_italic_split = split_nodes_delimiter(
        after_bold_split, "_", TextType.ITALIC)

    return after_italic_split
