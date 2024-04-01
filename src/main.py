import os.path
import shutil

from src.htmlnode import LeafNode
from textnode import TextNode
from os import path, mkdir, listdir


def delete_files(path_delete: str) -> None:
    pass


def check_dir(dir_path: str) -> bool:
    dir_state = False
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    else:
        dir_state = True
        if dir_path == "../static":
            if os.path.exists(f'../backup'):
                shutil.rmtree(f'../backup')
            else:
                os.mkdir(f'../backup')

            dir_copy(dir_path, f"../backup")

    return dir_state


def dir_copy(dir_copy_path: str, dir_moveto: str) -> None:
    items = os.listdir(dir_copy_path)
    for item in items:
        print(item)
        if os.path.isdir(f"{dir_copy_path}/{item}"):
            os.mkdir(f"{dir_moveto}/{item}")
            dir_copy(f"{dir_copy_path}/{item}", f"{dir_moveto}/{item}")
        else:
            shutil.copy(item, f"{dir_moveto}")


def main() -> None:
    check_dir("../static")

main()
