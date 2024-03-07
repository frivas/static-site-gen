import unittest

from textnode import (
    BlockTypes,
    TextNode,
    TextTypes,
    block_to_block_type,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_html_node,
    split_nodes_delimiter,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextTypes.text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", TextTypes.text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextTypes.text_type_text),
                TextNode("bolded", TextTypes.text_type_bold),
                TextNode(" word", TextTypes.text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**",
            TextTypes.text_type_text,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextTypes.text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextTypes.text_type_text),
                TextNode("bolded", TextTypes.text_type_bold),
                TextNode(" word and ", TextTypes.text_type_text),
                TextNode("another", TextTypes.text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**",
            TextTypes.text_type_text,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextTypes.text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextTypes.text_type_text),
                TextNode("bolded word", TextTypes.text_type_bold),
                TextNode(" and ", TextTypes.text_type_text),
                TextNode("another", TextTypes.text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextTypes.text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", TextTypes.text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextTypes.text_type_text),
                TextNode("italic", TextTypes.text_type_italic),
                TextNode(" word", TextTypes.text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode(
            "This is text with a `code block` word", TextTypes.text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "`", TextTypes.text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextTypes.text_type_text),
                TextNode("code block", TextTypes.text_type_code),
                TextNode(" word", TextTypes.text_type_text),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(
            block_to_block_type(block), BlockTypes.block_type_heading.value[0]
        )
        block = "```\ncode\n```"
        self.assertEqual(
            block_to_block_type(block), BlockTypes.block_type_code.value[0]
        )
        block = "> quote\n> more quote"
        self.assertEqual(
            block_to_block_type(block), BlockTypes.block_type_quote.value[0]
        )
        block = "* list\n* items"
        self.assertEqual(
            block_to_block_type(block), BlockTypes.block_type_unordered_list.value[0]
        )
        block = "1. list\n2. items"
        self.assertEqual(
            block_to_block_type(block), BlockTypes.block_type_ordered_list.value[0]
        )
        block = "paragraph"
        self.assertEqual(
            block_to_block_type(block), BlockTypes.block_type_paragraph.value[0]
        )

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

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


if __name__ == "__main__":
    unittest.main()
