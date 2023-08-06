"""
General utility functions.
"""

import os
from random import choice
import importlib.resources
from rich import print as rprint

# CCUI Modules
from ccui.constants import (
    LINUX,
    WINDOWS,
)


def clear() -> None:
    """Clears the terminal."""
    os.system("cls" if WINDOWS else "clear")


def replace_chars(text: str, chars: str, replace: str) -> str:
    """
    Replace characters in string with others randomly selected.\n
    text    -- string to affect\n
    chars   -- collection of chars to randomly pick from\n
    replace -- substring to replace\n
    """
    list_of_chars = list(text)
    for index, char in enumerate(list_of_chars):
        if char == replace:
            list_of_chars[index] = choice(chars)
    return "".join(list_of_chars)


def output_file_content(filename: str, replace: str = None, replacement: str = None) -> None:
    """
    Outputs the text files to the terminal (supports colors).\n
    filename    -- example.txt\n
    replace     -- replace given substring with replacement\n
    replacement -- random.choice(replacement) will replace given replace string\n
    """
    file_content = ""

    with importlib.resources.open_text('ccui.utils', filename) as file:
        for line in file:
            file_content += replace_chars(line, replacement, replace) if replace else line

    rprint(file_content)
