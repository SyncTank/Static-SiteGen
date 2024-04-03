import os.path
import shutil

from src.htmlnode import LeafNode
from textnode import TextNode
from os import path, mkdir, listdir


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
        load_dir(dir_path, "../backup")
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


main()
