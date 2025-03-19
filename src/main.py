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
        full_object_path = os.path.join(current_file_path, file_object)
        if os.path.isfile(full_object_path):
            shutil.copy(full_object_path, dest_path)
        else:
            full_destination_path = os.path.join(dest_path, file_object)
            os.mkdir(full_destination_path)
            recursive_file_copy(full_object_path,full_destination_path)

    #issue with .png not registering as file?

def generate_new_public_dir():
    try:
        clear_public()
    except Exception as e:
        print(e)
    os.mkdir(PUBLIC_PATH)
    recursive_file_copy(STATIC_PATH, PUBLIC_PATH)

def main():
    generate_new_public_dir()

if __name__ == "__main__":
    main()