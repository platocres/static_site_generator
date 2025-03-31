import os
import shutil
import sys

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    # Get the base path from the first CLI argument, default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    if not basepath.endswith("/"):
        basepath += "/"

    print(f"Base path set to: {basepath}")

    print("Deleting public directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_docs)

    print("Generating pages...")
    generate_pages_recursive(
        dir_path_content,  # Pass the content directory
        template_path,
        dir_path_docs,  # Pass the docs directory as the destination
        basepath,  # Pass the base path
    )
    print("All pages generated successfully!")


main()