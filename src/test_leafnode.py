import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        output_p = "<p>This is a paragraph of text.</p>"
        input = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(input.to_html(), output_p)

    def test_render_a(self):
        output_a = '<a href="https://www.google.com">Click me!</a>'
        input = LeafNode(
            "a",
            "Click me!",
            props={"href": "https://www.google.com"},
        )
        self.assertEqual(input.to_html(), output_a)


if __name__ == "__main__":
    unittest.main()
