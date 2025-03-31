from textnode import *
from htmlnode import *
import re
from enum import Enum



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split text nodes in the input list by a delimiter and assign the specified text type to the split parts.

    Args:
        old_nodes (list): A list of TextNode objects to process.
        delimiter (str): The delimiter to split the text by.
        text_type (TextType): The TextType to assign to the split parts.

    Returns:
        list: A new list of TextNode objects, with split nodes based on the delimiter.
    """
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.NORMAL and delimiter in node.text:
            # Split the text by the delimiter
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                # Alternate between normal text and the specified text type
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.NORMAL))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            # If the node is not of type NORMAL or doesn't contain the delimiter, keep it as is
            new_nodes.append(node)

    return new_nodes

def extract_markdown_images(text):
    """
    Extract markdown image syntax and return a list of tuples containing alt text and URLs.

    Args:
        text (str): The raw markdown text.

    Returns:
        list: A list of tuples, where each tuple contains the alt text and URL of an image.
    """
    # Regex to match markdown image syntax: ![alt text](URL)
    image_pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(image_pattern, text)


def extract_markdown_links(text):
    """
    Extract markdown link syntax and return a list of tuples containing anchor text and URLs.

    Args:
        text (str): The raw markdown text.

    Returns:
        list: A list of tuples, where each tuple contains the anchor text and URL of a link.
    """
    # Regex to match markdown link syntax: [anchor text](URL)
    link_pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(link_pattern, text)

def text_to_textnodes(text):
    """
    Convert a raw markdown-flavored string into a list of TextNode objects.

    Args:
        text (str): The raw markdown text.

    Returns:
        list: A list of TextNode objects representing the parsed text.
    """
    # Start with a single TextNode containing the entire text as NORMAL
    nodes = [TextNode(text, TextType.NORMAL)]

    # Split nodes for bold (**), italic (_), and code (`) delimiters
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # Extract and replace markdown images
    for node in nodes[:]:  # Use a copy of the list to safely modify it
        if node.text_type == TextType.NORMAL:
            images = extract_markdown_images(node.text)
            if images:
                # Replace the node with new nodes for each image
                new_nodes = []
                remaining_text = node.text
                for alt_text, url in images:
                    # Split the text before the image
                    before, _, remaining_text = remaining_text.partition(f"![{alt_text}]({url})")
                    if before:
                        new_nodes.append(TextNode(before, TextType.NORMAL))
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
                # Replace the original node with the new nodes
                index = nodes.index(node)
                nodes[index:index + 1] = new_nodes

    # Extract and replace markdown links
    for node in nodes[:]:  # Use a copy of the list to safely modify it
        if node.text_type == TextType.NORMAL:
            links = extract_markdown_links(node.text)
            if links:
                # Replace the node with new nodes for each link
                new_nodes = []
                remaining_text = node.text
                for anchor_text, url in links:
                    # Split the text before the link
                    before, _, remaining_text = remaining_text.partition(f"[{anchor_text}]({url})")
                    if before:
                        new_nodes.append(TextNode(before, TextType.NORMAL))
                    new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
                # Replace the original node with the new nodes
                index = nodes.index(node)
                nodes[index:index + 1] = new_nodes

    return nodes

def markdown_to_blocks(markdown):
    """
    Split a raw Markdown string into a list of block strings.

    Args:
        markdown (str): The raw Markdown string.

    Returns:
        list: A list of block strings, with leading/trailing whitespace removed.
    """
    # Split the markdown string into blocks based on double newlines
    blocks = markdown.split("\n\n")
    
    # Strip leading/trailing whitespace from each block and remove empty blocks
    return [block.strip() for block in blocks if block.strip()]

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    """
    Determine the type of a markdown block.

    Args:
        block (str): A single block of markdown text.

    Returns:
        BlockType: The type of the markdown block.
    """
    # Check for heading (starts with 1-6 # characters followed by a space)
    if block.startswith("#"):
        parts = block.split(" ", 1)
        if len(parts) > 1 and 1 <= len(parts[0]) <= 6 and all(c == "#" for c in parts[0]):
            return BlockType.HEADING

    # Check for code block (starts and ends with 3 backticks)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Check for quote block (every line starts with >)
    if all(line.strip().startswith(">") for line in block.splitlines()):
        return BlockType.QUOTE

    # Check for unordered list block (every line starts with - followed by a space)
    if all(line.strip().startswith("- ") for line in block.splitlines()):
        return BlockType.UNORDERED_LIST

    # Check for ordered list block (every line starts with a number followed by . and a space)
    lines = block.splitlines()
    if all(line.strip().split(" ", 1)[0].isdigit() and line.strip().split(" ", 1)[0].endswith(".") for line in lines):
        numbers = [int(line.strip().split(" ", 1)[0][:-1]) for line in lines]
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.ORDERED_LIST

    # If none of the above, it's a paragraph
    return BlockType.PARAGRAPH