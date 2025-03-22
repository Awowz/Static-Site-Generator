import os
import shutil
import sys
from textnode import *
from blocknode import markdown_to_html_node

PUBLIC_PATH = "./doc"
STATIC_PATH = "./static"
CONTENT_PATH = "./content"
TEMPLET_FILE = "template.html"


def extract_title(markdown):
    lines = markdown.split("\n")
    if not lines[0].startswith("#"):
        raise Exception("file contiants no starter header")
    return lines[0][2:]

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path, 'r')
    file_contents = f.read()
    f1 = open(template_path, 'r')
    template_contents = f1.read()
    node = markdown_to_html_node(file_contents)
    html = node.to_html()
    title = extract_title(file_contents)
    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html)
    template_contents = template_contents.replace("href=\"/", f"href=\"{base_path}")
    template_contents = template_contents.replace("src=\"/", f"src=\"{base_path}")
    dest_path = dest_path.replace(".md", ".html")
    dest = open(dest_path, "w+")
    dest.write(template_contents)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for file_object in os.listdir(dir_path_content):
        full_object_path = os.path.join(dir_path_content, file_object)
        if os.path.isfile(full_object_path):
            generate_page(full_object_path, template_path, os.path.join(dest_dir_path, file_object), basepath)
        else:
            full_destination_path = os.path.join(dest_dir_path, file_object)
            os.mkdir(full_destination_path)
            generate_pages_recursive(full_object_path,template_path, full_destination_path, basepath)

def clear_public():
    if not os.path.exists(PUBLIC_PATH):
        raise Exception("File path does not exist")
    shutil.rmtree(PUBLIC_PATH)

def recursive_file_copy(current_file_path, dest_path):
    for file_object in os.listdir(current_file_path):
        full_object_path = os.path.join(current_file_path, file_object)
        if os.path.isfile(full_object_path):
            shutil.copy(full_object_path, dest_path)
        else:
            full_destination_path = os.path.join(dest_path, file_object)
            os.mkdir(full_destination_path)
            recursive_file_copy(full_object_path,full_destination_path)


def generate_new_public_dir():
    try:
        clear_public()
    except Exception as e:
        print(e)
    os.mkdir(PUBLIC_PATH)
    recursive_file_copy(STATIC_PATH, PUBLIC_PATH)

def main():
    basepath = "/"
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    print(f"basepath: {basepath}")
    generate_new_public_dir()
    generate_pages_recursive(CONTENT_PATH, TEMPLET_FILE, PUBLIC_PATH, basepath)
    

if __name__ == "__main__":
    main()