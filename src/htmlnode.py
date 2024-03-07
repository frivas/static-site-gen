from typing import Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children=None,
        props=None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        html_attr = ""
        for prop in self.props:
            html_attr += f' {prop}="{self.props[prop]}"'
        return html_attr

    def __repr__(self):
        return f"Tag: {self.tag} Value: {self.value} Children: {self.children} Props: {self.fprops}"


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value is required")

        if self.tag is None:
            return str(self.value)

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNone({self.tag} {self.value} {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag should be provided")

        if self.children is None:
            raise ValueError("Children has to be provided")

        children_html = ""
        for c in self.children:
            children_html += c.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag} {self.children} {self.props})"
