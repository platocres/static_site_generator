from markdown_utils import *
from htmlnode import *
from enum import Enum

# Enum to represent different types of inline text nodes
# As a Sum Type it will automatically error handle incorrect TextTypes
class TextType(Enum):
    NORMAL = "normal"   # Plain text
    BOLD = "bold"       # Bold text
    ITALIC = "italic"   # Italicized text
    CODE = "code"       # Inline code text
    LINK = "link"       # Hyperlink with anchor text
    IMAGE = "image"     # Image with alt text

# Class to represent a single inline text node
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        """
        Initialize a TextNode object.

        Args:
            text (str): The text content of the node.
            text_type (TextType): The type of text (e.g., NORMAL, BOLD, LINK).
            url (str, optional): The URL for links or images. Defaults to None.
        """

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
        """
        Check if two TextNode objects are equal.

        Args:
            other (TextNode): The other TextNode to compare.

        Returns:
            bool: True if all properties (text, text_type, url) are equal, False otherwise.
        """

    def __repr__(self):
        return f"TextNode({self.text!r}, {self.text_type!r}, {self.url!r})"
        """
        Return a string representation of the TextNode object.

        Returns:
            str: A string in the format TextNode(TEXT, TEXT_TYPE, URL).
        """