import os
import shutil
from textnode import *

PUBLIC_PATH = "public"
STATIC_PATH = "static"

def clear_public():
    if not os.path.exists(PUBLIC_PATH):
        raise Exception("File path does not exist")
    shutil.rmtree(PUBLIC_PATH)

def recursive_file_copy(current_file_path, dest_path):
    for file_object in os.listdir(current_file_path):
        full_object_path = os.path.join(STATIC_PATH, file_object)
        print(f"path: {full_object_path}")
        if os.path.isfile(full_object_path):
            shutil.copy(full_object_path, dest_path)
        else:
            print(f"object {file_object} is not a file")
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
    my_text_node = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.boot.dev")
    print(my_text_node)
    generate_new_public_dir()

if __name__ == "__main__":
    main()