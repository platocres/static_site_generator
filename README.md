# static_site_generator

Architecture
We'll dive into code in the next chapter, but first, I want to give you a high-level architecture for our static site generator.

![architecture diagram](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/UKCNg8E.png)

The flow of data through the full system is:

Markdown files are in the /content directory. A template.html file is in the root of the project.
The static site generator (the Python code in src/) reads the Markdown files and the template file.
The generator converts the Markdown files to a final HTML file for each page and writes them to the /public directory.
We start the built-in Python HTTP server (a separate program, unrelated to the generator) to serve the contents of the /public directory on http://localhost:8888 (our local machine).
We open a browser and navigate to http://localhost:8888 to view the rendered site.
How the SSG Works
The vast majority of our coding will happen in the src/ directory because almost all of the work is done in steps 2 and 3 above. Here's a rough outline of what the final program will do when it runs:

Delete everything in the /public directory.
Copy any static assets (HTML template, images, CSS, etc.) to the /public directory.
Generate an HTML file for each Markdown file in the /content directory. For each Markdown file:
Open the file and read its contents.
Split the markdown into "blocks" (e.g. paragraphs, headings, lists, etc.).
Convert each block into a tree of HTMLNode objects. For inline elements (like bold text, links, etc.) we will convert:
Raw markdown -> TextNode -> HTMLNode
Join all the HTMLNode blocks under one large parent HTMLNode for the pages.
Use a recursive to_html() method to convert the HTMLNode and all its nested nodes to a giant HTML string and inject it in the HTML template.
Write the full HTML string to a file for that page in the /public directory.
