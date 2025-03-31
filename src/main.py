from textnode import *
from htmlnode import *

def main():
    # Create a new TextNode
    text_node = TextNode('This is some anchor text', 'link', 'https://www.boot.dev')
    # Display the text
    print(text_node)



if __name__ == "__main__":
    main()