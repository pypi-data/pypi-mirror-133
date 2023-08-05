#!/usr/bin/env python3

#easy_user_input.easy_user_input - shortcut for easy_user_input.eui

#this module maps every function from the 'easy_user_input.eui'
#onto itself, allowing backwards compatibility with code using the longer name
#without having to maintain multiple copies of the same file.

#NOTE 1: this is a temporary feature to ease the transition into the new name
#it will not be maintained and it will be removed in the next major version

from typing import Tuple
from warnings import warn


def inputYesNo(promptText: str = "Choose yes or no", default: bool = None):
    from eui import inputYesNo
    warn("easy_user_input.easy_user_input has been renamed to easy_user_input.eui and this shortcut will be removed in the future.")
    return inputYesNo(promptText, default)

def inputChoice(
    choices:Tuple[str or Tuple[str, str]], 
    promptText:str = "Please select an option", 
    default: int = None
    ) -> int:
    from eui import inputChoice
    warn("easy_user_input.easy_user_input has been renamed to easy_user_input.eui and this shortcut will be removed in the future.")
    return inputChoice(choices,promptText,default)

def inputStrictString(promptText: str, allowedChars: str = None, default: str or None = None) -> str:
    from eui import inputStrictString
    warn("easy_user_input.easy_user_input has been renamed to easy_user_input.eui and this shortcut will be removed in the future.")
    return inputStrictString(promptText, allowedChars, default)


def inputPath(
        promptText: str = "Please input a valid path",
        existsBehavior: str = "reject",
        default: str or None = None
    ) -> str:
    from eui import inputPath
    warn("easy_user_input.easy_user_input has been renamed to easy_user_input.eui and this shortcut will be removed in the future.")
    return inputPath(promptText,existsBehavior,default)