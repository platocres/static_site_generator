# Static Site Generator 

## Use
This package can convert Markdown text into HTML and generate static websites on GitHub.io. To use it, you'll need to write up the content of your website in the form of markdown files (.MD) and place it into folders, representing different pages on your site, inside of the `content/` directory. Any image files stored locally should be kept inside of the `static/images` directory, and should be referenced inside your markdown files.

You can utilize `main.sh` for testing purposes if you want to generate the content locally and preview at http://localhost:8888. If you do not like the look of the generated site you will need to do the harder work of updating the CSS style sheet template to your liking. It can be found at `static/index.css`. Once your markdown files, static content, and folder structure is how you want it, run `build.sh` to generate the HTML content of your site for public viewing. The content will be generated in the `docs/` directory.

You will then need to commit the code to your own GitHub repository and set it to use the "pages" function. To do this:

- Open your repository's settings on GitHub and select the Pages section.
- Set the source to the main branch and the docs directory.
- Save the settings.
- Now the 'docs/' directory on your main branch will auto deploy to your GitHub Pages URL once something is in it.

Your static site will be viewable at: `https://USERNAME.github.io/REPO_NAME/`.

Example: https://platocres.github.io/static_site_generator/

## Requirements
This code requires Python3 in order to guarantee it will run as expected. It has not been tested in other versions of Python.

## Architecture
This is a high-level architecture for how the static site generator operates.

![architecture diagram](https://i.imgur.com/0VlW6Yt.png)

The flow of data through the full system is:

1. Markdown files are in the /content directory. A template.html file is in the root of the project.
2. The static site generator (the Python code in src/) reads the Markdown files and the template file.
3. The generator converts the Markdown files to a final HTML file for each page and writes them to the /docs directory.
4. The user initializes a GitHub repository with the same name as the website.
5. The user pushes the commits to the repository and sets the repository to serve as a static website on the main branch in the `docs/` directory.

## How the SSG Works
Here's a rough outline of what the program will do when it runs:

1. Delete everything in the /docs directory.
2. Copy any static assets (HTML template, images, CSS, etc.) to the /docs directory.
3. Generate an HTML file for each Markdown file in the /content directory. For each Markdown file:
    1. Open the file and read its contents.
    2. Split the markdown into "blocks" (e.g. paragraphs, headings, lists, etc.).
    3. Convert each block into a tree of HTMLNode objects. For inline elements (like bold text, links, etc.) we will convert:
        - Raw markdown -> TextNode -> HTMLNode
    4. Join all the HTMLNode blocks under one large parent HTMLNode for the pages.
    5. Use a recursive to_html() method to convert the HTMLNode and all its nested nodes to a giant HTML string and inject it in the HTML template.
    6. Write the full HTML string to a file for that page in the /docs directory.
