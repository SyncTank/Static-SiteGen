import os.path
import shutil
import datetime
from types import NotImplementedType

from textnode import TextNode, html_builder
from os import path, mkdir, listdir, read

def extract_title(markdown_file: str) -> bool:
    if len(markdown_file) < 0:
        return False
    try:
        with open(markdown_file) as file:
            first_line_check = file.readline()
    except Exception as e:
        print(e)
        return False
    if '#' in first_line_check:
        return True
    else:
        return False

def read_file_with_check(file_to_check: str):
    if len(file_to_check) < 0:
        raise Exception("No file is called")
    try:
        with open(file_to_check) as file:
            read_lines = file.read()
    except Exception as e:
        print(e)
        return

    markdown = ""
    if  read_lines is not None:
        for item in read_lines:
            markdown += item
        return markdown

def generate_page(from_page: str, template_page: str, dest_path: str) -> None:
    print(f"Generating Page from {from_page} to {dest_path} using {template_page}")
    markdown_file = read_file_with_check(from_page)
    template = read_file_with_check(template_page)
    print(html_builder([markdown_file] )) 

# Use your markdown_to_html_node function and .to_html() method to convert the markdown file to HTML.
# Use the extract_title function to grab the title of the page.
# Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
# Write the new HTML to a file at dest_path. Be sure to create any necessary directories if they don't exist.

def delete_files(path_delete: str) -> None:
    list_objs = os.listdir(path_delete)
    if len(list_objs) == 0:
        return
    else:
        for item in list_objs:
            file_path = f'{path_delete}/{item}'
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                delete_files(file_path)
                os.rmdir(file_path)


def load_dir(dir_copy: str, dir_path: str) -> None:
    if not os.path.exists(dir_copy):
        raise FileNotFoundError(dir_copy)
    if dir_path == "../public":
        versions = os.listdir("../backup")
        verison_backup = len(versions)
        date_backup = datetime.date.today()
        time_backup = datetime.datetime.today()
        if verison_backup > 4:
            to_del = ""
            for folder in versions:
                if len(to_del) == 0:
                    to_del = folder
                if os.path.getmtime(f"../backup/{folder}") < os.path.getmtime(f"../backup/{to_del}"):
                    to_del = folder
            delete_files(f"../backup/{to_del}")
            os.rmdir(f"../backup/{to_del}")
        load_dir(dir_path, f"../backup/backup_{verison_backup}_{date_backup}_{time_backup}")
    if not os.path.exists(dir_path):
        print(dir_copy, dir_path, "New folder created")
        os.mkdir(dir_path)
        dir_copy_files(dir_copy, dir_path)
    else:
        if not os.listdir(dir_path):
            print(dir_copy, dir_path, "Empty directory")
            dir_copy_files(dir_copy, dir_path)
        else:
            print(dir_copy, dir_path, "already exists")
            delete_files(dir_path)
            dir_copy_files(dir_copy, dir_path)


def dir_copy_files(dir_copy_path: str, dir_moveto: str) -> None:
    list_objs = os.listdir(dir_copy_path)
    if len(list_objs) == 0:
        return
    for item in list_objs:
        file_path = f'{dir_copy_path}/{item}'
        if os.path.isfile(file_path):
            shutil.copy(file_path, dir_moveto)
        else:
            os.mkdir(dir_moveto+"/"+item)
            dir_copy_files(file_path, dir_moveto+"/"+item)


def main() -> None:
    load_dir("../static", "../public")
    print(extract_title("../content/index.md")) 
    start_gen = extract_title("../content/index.md") 

    if start_gen:
        delete_files("../public")
        generate_page("../content/index.md", "../template.html", "../public/index.html")

main()
