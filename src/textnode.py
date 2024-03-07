import re
from enum import Enum

from htmlnode import LeafNode, ParentNode


class TextTypes(Enum):
    text_type_text = "text"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"
    text_type_link = "link"
    text_type_image = "image"


class BlockTypes(Enum):
    block_type_paragraph = ["paragraph", ""]
    block_type_heading = ["heading", "#"]
    block_type_code = ["code", "```"]
    block_type_quote = ["quote", ">"]
    block_type_unordered_list = ["ulist", "* |- "]
    block_type_ordered_list = ["olist", ". "]


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_text_none):
        return self.__dict__ == other_text_none.__dict__

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    if text_node.text_type == TextTypes.text_type_text:
        return LeafNode(None, text_node.text)

    if text_node.text_type == TextTypes.text_type_bold:
        return LeafNode("b", text_node.text)

    if text_node.text_type == TextTypes.text_type_italic:
        return LeafNode("i", text_node.text)

    if text_node.text_type == TextTypes.text_type_code:
        return LeafNode("code", text_node.text)

    if text_node.text_type == TextTypes.text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})

    if text_node.text_type == TextTypes.text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    raise ValueError("Text Node not valid")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextTypes.text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, bold section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextTypes.text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextTypes.text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for img in images:
            sections = original_text.split(f"![{img[0]}]({img[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextTypes.text_type_text))
            new_nodes.append(TextNode(img[0], TextTypes.text_type_image, img[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextTypes.text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextTypes.text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextTypes.text_type_text))
            new_nodes.append(TextNode(link[0], TextTypes.text_type_link, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextTypes.text_type_text))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextTypes.text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", TextTypes.text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", TextTypes.text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", TextTypes.text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    return [b.strip() for b in markdown.split("\n\n") if b != ""]


def block_to_block_type(block):
    lines = block.split("\n")
    if (
        block.startswith(BlockTypes.block_type_heading.value[1])
        or block.startswith(BlockTypes.block_type_heading.value[1] * 2)
        or block.startswith(BlockTypes.block_type_heading.value[1] * 3)
        or block.startswith(BlockTypes.block_type_heading.value[1] * 4)
        or block.startswith(BlockTypes.block_type_heading.value[1] * 5)
        or block.startswith(BlockTypes.block_type_heading.value[1] * 6)
    ):
        return BlockTypes.block_type_heading.value[0]
    if (
        len(lines) > 1
        and lines[0].startswith(BlockTypes.block_type_code.value[1])
        and lines[-1].startswith(BlockTypes.block_type_code.value[1])
    ):
        return BlockTypes.block_type_code.value[0]
    if block.startswith(BlockTypes.block_type_quote.value[1]):
        for line in lines:
            if not line.startswith(BlockTypes.block_type_quote.value[1]):
                return BlockTypes.block_type_paragraph.value[0]
        return BlockTypes.block_type_quote.value[0]
    if block.startswith(BlockTypes.block_type_unordered_list.value[1].split("|")[0]):
        for line in lines:
            if not line.startswith(
                BlockTypes.block_type_unordered_list.value[1].split("|")[0]
            ):
                return BlockTypes.block_type_paragraph.value[0]
        return BlockTypes.block_type_unordered_list.value[0]

    if block.startswith(BlockTypes.block_type_unordered_list.value[1].split("|")[1]):
        for line in lines:
            if not line.startswith(
                BlockTypes.block_type_unordered_list.value[1].split("|")[1]
            ):
                return BlockTypes.block_type_paragraph.value[0]
        return BlockTypes.block_type_unordered_list.value[0]
    if block.startswith(f"1{BlockTypes.block_type_ordered_list.value[1]}"):
        idx = 1
        for line in lines:
            if not line.startswith(f"{idx}. "):
                return BlockTypes.block_type_paragraph.value[0]
            idx += 1
        return BlockTypes.block_type_ordered_list.value[0]
    return BlockTypes.block_type_paragraph.value[0]


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockTypes.block_type_paragraph.value[0]:
        return paragraph_to_html_node(block)
    if block_type == BlockTypes.block_type_heading.value[0]:
        return heading_to_html_node(block)
    if block_type == BlockTypes.block_type_code.value[0]:
        return code_to_html_node(block)
    if block_type == BlockTypes.block_type_ordered_list.value[0]:
        return olist_to_html_node(block)
    if block_type == BlockTypes.block_type_unordered_list.value[0]:
        return ulist_to_html_node(block)
    if block_type == BlockTypes.block_type_quote.value[0]:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")
