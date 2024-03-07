import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        output = ' href="https://www.google.com" target="_blank"'
        input = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(input.props_to_html(), output)


if __name__ == "__main__":
    unittest.main()
