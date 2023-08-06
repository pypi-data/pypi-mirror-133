"""
Helps to search for files and directories
"""
import os


def list_folder(dir_path="./"):
    """List all files and direcotires in the given path"""
    ignored = read_gitignore()
    lists = os.listdir(dir_path)

    non_match = []
    for i in lists:
        if i not in ignored:
            non_match.append(i)

    return non_match


def read_gitignore(dir_path="./"):
    """List all files and directories in the given .gititnore file"""
    file_lines = []

    with open(f"{dir_path}.gitignore", encoding="UTF-8") as ignore_file:
        lines = ignore_file.readlines()
        for line in lines:
            if not line.startswith("#"):
                line = str(line).rstrip("\n")
                file_lines.append(line)

    return file_lines
