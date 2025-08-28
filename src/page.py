from re import findall, MULTILINE
from blocks import markdown_to_html_node
from jinja2 import Template
import os


def extract_title(markdown):
    h1_headers = findall(r"^# (.+)$", markdown, flags=MULTILINE)
    if len(h1_headers) > 1:
        raise ValueError("There cannot be more than 1 h1 header.")
    if len(h1_headers) == 0:
        raise ValueError("There must be 1 h1 header.")
    return h1_headers[0].strip()


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        markdown = file.read()
    with open(template_path, 'r') as file:
        template = file.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    jinja_template = Template(template)
    rendered = jinja_template.render(Title=title, Content=html_string)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(rendered)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for child in os.listdir(dir_path_content):
        child_source = os.path.join(dir_path_content, child)
        child_dest = os.path.join(dest_dir_path, child)
        if os.path.isfile(child_source):
            child_dest = child_dest.replace(".md", ".html")
            generate_page(child_source, template_path, child_dest)
        else:
            generate_pages_recursive(child_source, template_path, child_dest)
