"""
Indicate of the static project structures through a list of files
"""

import re
from ..files import file_dir


def indicate_python_structure():
    """Provide a list of well-known files and directories in a Python based context"""
    python_specific_files = [
        "setup.(py|cfg)",
        "conftest.py",
        "pyproject([.]?txt|cfg|ini|toml)",
        "(.*)?.egg-info",
        "(.*)?pycache(.*)?",
        "requirements([.]?txt|cfg|ini|toml)?",
        "makefile",
        "([.])?pylint(rc|[.]?y(a)?ml|json|cfg|ini|toml)?",
        "([.])?bandit(rc|[.]?y(a)?ml|json|cfg|ini|toml)?",
        "([.])?mypy(rc|[.]?y(a)?ml|json|cfg|ini|toml)?",
        ".*.py(i)?",
    ]
    return python_specific_files


def indicate_git_structure():
    """Provide a list of well-known files and directories in a Git based context"""
    git_specific_files = [
        "README([.]?md|markdown)?",
        "VERSION([.]?md|markdown)?",
        "LICENSE([.]?md|markdown)?",
        ".gitignore",
        ".gitlab-ci(rc|[.]?y(a)?ml|json)?",
    ]
    return git_specific_files


def indicate_node_structure():
    """Provide a list of well-known files and directories in a Nodejs based context"""
    node_specific_files = ["package([.]?json)?", "package-lock([.]?json)?", "node_modules", "yarn.lock"]
    return node_specific_files


def compare_structure(origin_structure, matches_structure):
    """Compare two given structures and return a list of matches entries"""
    match_list = []
    for origin_entry in origin_structure:
        for matches_entry in matches_structure:
            match = re.match(matches_entry, origin_entry)
            if match is not None:
                match_list.append(origin_structure)

    return list(dict.fromkeys(match_list))


def indicate_structure(dir_path="./"):
    """Tests various indications for structured directories"""

    origin = file_dir.list_folder(dir_path)

    list_python_matches = {"python": compare_structure(origin, indicate_python_structure())}
    list_node_matches = {"node": compare_structure(origin, indicate_node_structure())}
    list_git_matches = {"git": compare_structure(origin, indicate_git_structure())}

    return list_python_matches | list_node_matches | list_git_matches
