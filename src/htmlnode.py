from main import *
from textnode import *


class HTMLNode:
    # tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
    # value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)
    # children - A list of HTMLNode objects representing the children of this node
    # props - A dictionary of key-value pairs representing the attributes of the HTML tag. 
    #   For example, a link (<a> tag) might have {"href": "https://www.google.com"}
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag              # An HTMLNode without a tag will just render as raw text
        self.value = value          # An HTMLNode without a value will be assumed to have children
        self.children = children    # An HTMLNode without children will be assumed to have a value
        self.props = props          # An HTMLNode without props will be assumed to have no attributes
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        return " ".join([f'{key}="{value}"' for key, value in self.props.items()])
        # Convert the props dictionary to a string of HTML attributes
        # For example, {"href": "https://www.google.com"} becomes 'href="https://www.google.com"'
        # If there are multiple props, they will be joined with a space
        # For example, {"href": "https://www.google.com", "target": "_blank"} becomes 'href="https://www.google.com" target="_blank"'
        # If there are no props, return an empty string
    
    def __repr__(self):
        return f"HTMLNode({self.tag!r}, {self.value!r}, {self.children!r}, {self.props!r})"
        # Return a string representation of the HTMLNode object
        # For example, HTMLNode("p", "Hello, world!", None, {"class": "text"}) becomes 'HTMLNode("p", "Hello, world!", None, {"class": "text"})'
        # If the node has no tag, value, children, or props, they will be represented as None

class LeafNode(HTMLNode):
    # A leaf node is a node that has no children
    # A leaf node will be rendered as a string
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
        # Call the parent constructor with no children
        # A leaf node will be rendered as a string
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        # If the node has a tag, render it as an HTML tag
        if self.tag:
            props_html = self.props_to_html()
            # Only add a space if there are attributes
            if props_html:
                return f"<{self.tag} {props_html}>{self.value}</{self.tag}>"
            return f"<{self.tag}>{self.value}</{self.tag}>"
        # If the node has no tag, render it as a string
        return self.value

class ParentNode(HTMLNode):
    # A parent node is a node that has children
    # A parent node will be rendered as a string
    def __init__(self, tag, children, props=None):
        """
        Initialize a ParentNode object.

        Args:
            tag (str): The HTML tag name (e.g., "p", "div").
            children (list): A list of child nodes (HTMLNode objects).
            props (dict, optional): A dictionary of HTML attributes. Defaults to None.
        """
        if tag is None:
            raise ValueError("ParentNode must have a tag")
        if children is None or not isinstance(children, list):
            raise ValueError("ParentNode must have a list of children")
        super().__init__(tag, None, children, props)

    def to_html(self):
        """
        Convert the ParentNode and its children to an HTML string.

        Returns:
            str: The HTML representation of the ParentNode and its children.

        Raises:
            ValueError: If the node does not have a tag or children.
        """
        # If the node has a tag, render it as an HTML tag
        props_html = self.props_to_html()
        # Recursively call to_html on all children and concatenate their results
        children_html = ''.join([child.to_html() for child in self.children])
        # Only add a space if there are attributes
        if props_html:
            return f"<{self.tag} {props_html}>{children_html}</{self.tag}>"
        return f"<{self.tag}>{children_html}</{self.tag}>"
    
def text_node_to_html_node(text_node):
    """
    Convert a TextNode to a corresponding LeafNode based on its TextType.

    Args:
        text_node (TextNode): The TextNode to convert.

    Returns:
        LeafNode: A new LeafNode object representing the HTML equivalent of the TextNode.

    Raises:
        ValueError: If the TextNode has an unsupported TextType.
    """
    # Map TextType.NORMAL to the behavior expected for TextType.TEXT
    if text_node.text_type == TextType.NORMAL:
        # Return a LeafNode with no tag, just raw text
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        # Return a LeafNode with a "b" tag
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        # Return a LeafNode with an "i" tag
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        # Return a LeafNode with a "code" tag
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        # Return a LeafNode with an "a" tag and "href" prop
        if not text_node.url:
            raise ValueError("TextNode of type LINK must have a URL")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        # Return a LeafNode with an "img" tag, "src" and "alt" props
        if not text_node.url:
            raise ValueError("TextNode of type IMAGE must have a URL")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        # Raise an exception for unsupported TextType
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")