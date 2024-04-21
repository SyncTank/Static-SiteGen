import os.path
import shutil
import datetime
from types import NotImplementedType

from textnode import TextNode, html_builder, inline_markdown_capture, markdown_block
from os import path, mkdir, listdir, read


def extract_title(markdown_file: str) -> str:
    if len(markdown_file) < 0:
        return ""
    try:
        with open(markdown_file) as file:
            first_line_check = file.readline()
    except Exception as e:
        print(e)
        return ""
    if '#' in first_line_check:
        return first_line_check
    else:
        return ""


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
    if read_lines is not None:
        for item in read_lines:
            markdown += item
        return markdown


def generate_page(from_page: str, template_page: str, dest_path: str) -> None:
    print(f"Generating Page from {from_page} to {dest_path} using {template_page}")
    try:
        template = read_file_with_check(template_page)

        markdown_file = read_file_with_check(from_page)
    except Exception:
        raise FileNotFoundError("Starter files not found")

    ext_title = extract_title(from_page).rstrip("\n")
    title = markdown_block(ext_title)[0].to_html()

    html_build = html_builder([markdown_file])
    content = ""

    for node in html_build:
        content += node

    template = template.replace(" {{ Title }} ", title)
    final_template = template.replace(" {{ Content }}", content)

    if os.path.exists(dest_path):
        delete_files(dest_path)
        f = open(dest_path, "w")
        f.write(final_template)
        f.close()
    else:
        f = open(dest_path, "w")
        f.write(final_template)
        f.close()


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


def check_path(file_to_check: str) -> bool:
    if not os.path.exists(file_to_check):
        raise FileNotFoundError(f"No file is called {file_to_check}")
    else:
        return True


def make_path(path_to_make: str) -> None:
    os.mkdir(path_to_make)


def make_backups(copy_path: str, backup_to_make: str) -> None:
    if not os.path.exists(backup_to_make):
        make_path(backup_to_make)
    dir_copy_files(copy_path, backup_to_make)


def backup_and_make(path_make: str) -> None:
    print(f"Making backup directory {path_make}")

    if path_make.count(".") > 0:
        path_make = path_make.replace(".", "")

    if not os.path.exists(f"../backups{path_make}"):
        make_path(f"../backups{path_make}")

    versions = os.listdir(f"../backups{path_make}")
    version_backups = len(versions)
    time_backup = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    if version_backups > 4:
        to_delete = ""
        for folder in versions:
            if len(to_delete) == 0:
                to_delete = folder
            if os.path.getmtime(f"../backups{path_make}/{folder}") < os.path.getmtime(
                    f"../backups{path_make}/{to_delete}"):
                to_delete = folder
        delete_files(f"../backups{path_make}/{to_delete}")
        os.rmdir(f"../backups{path_make}/{to_delete}")
        make_backups(f"..{path_make}", f"../backups{path_make}/backup_{version_backups}_{time_backup}")
    else:
        make_backups(f"..{path_make}", f"../backups{path_make}/backup_{version_backups}_{time_backup}")


def load_dir(dir_copy: str, dir_path: str) -> None:
    try:
        check_path(dir_copy)
    except Exception as e:
        print(e)

    if not os.path.exists(dir_path):
        print(f"Making directory {dir_path}")
        make_path(dir_path)

    if not os.path.exists("../backups"):
        print(f"Making backup directory Backup files")
        make_path("../backups")

    if len(os.listdir(dir_path)) > 0:
        backup_and_make(dir_path)
        delete_files(dir_path)
        dir_copy_files(dir_copy, dir_path)
    else:
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
            os.mkdir(dir_moveto + "/" + item)
            dir_copy_files(file_path, dir_moveto + "/" + item)


def main() -> None:
    load_dir("../static", "../public")
    print(extract_title("../content/index.md"))

    if bool(extract_title("../content/index.md")):
        #delete_files("../public")
        generate_page("../content/index.md", "../template.html", "../public/index.html")


if __name__ == '__main__':
    main()
