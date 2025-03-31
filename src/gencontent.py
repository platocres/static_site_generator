import os
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generate HTML pages for all markdown files in the content directory.

    Args:
        dir_path_content (str): The path to the content directory containing markdown files.
        template_path (str): The path to the HTML template file.
        dest_dir_path (str): The path to the destination directory where HTML files will be written.
    """
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):  # Process only markdown files
                # Compute the relative path and destination path
                relative_path = os.path.relpath(root, dir_path_content)
                dest_dir = os.path.join(dest_dir_path, relative_path)
                os.makedirs(dest_dir, exist_ok=True)  # Ensure the destination directory exists

                # Paths for the markdown file and the generated HTML file
                from_path = os.path.join(root, file)
                dest_path = os.path.join(dest_dir, file.replace(".md", ".html"))

                # Generate the HTML page
                print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'...")
                generate_page(from_path, template_path, dest_path)