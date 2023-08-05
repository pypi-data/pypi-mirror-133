# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2021 Dallas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
import os
from typing import (
    Any,
    Union,
    Optional
)

from .color_console import (
    color,
    back,
    style
)


def log(
    *args,
    sep: str = " ",
    end: str = "\n"
) -> None:
    """
    Print given arguments to betterconsole.
    It's different to Python-builtin `print` only that it function
    reset color for every argument.

    :argument args: Any Something that will be shown in betterconsole.
    :argument sep: string Inserted between values, default a space.
    :argument end: string Appended after the last value, default a newline.
    """
    print(
        *args,
        sep=color.reset + back.reset + style.reset + sep,
        end=color.reset + back.reset + style.reset + end
    )


def prompt(*args) -> Optional[str]:
    """
    Read typed to betterconsole information.
    The prompt string, if given, is printed to standard output without a
    trailing newline before reading input.

    :argument args: Any Text that will be shown in betterconsole before input
    to make user know what's hapening.
    """
    return input(*args)


def clear() -> None:
    """Clear whole console by using system "clear" message."""
    if sys.platform == "win32":
        os.system("cls")
    elif sys.platform.startswith("linux"):
        os.system("clear")
    else:
        print(
            color.red + "Enable to work on your OS. "
            "Open issue on github page: https://github.com/DarkJoij/terminalcmd/issues" + color.reset
        )


def args(argument_index: Optional[int] = None) -> Union[str, list]:
    """
    Return system argument(s) from sys.argv.

    :argument argument_index: integer Return sys.argv[argument_index] that have such index.
    Or if not return full sys.argv list.
    """
    if argument_index:
        return sys.argv[argument_index]
    return sys.argv


def stream(
    stream_object: Union[list[Any], tuple[Any], dict[str, int]],
    sep: str = " ",
    end: str = "\n"
) -> None:
    """
    Print subobjects of given object.

     * In first version it was "iterating" with second "equal" parameter
     * (Important! It won't iterator!), but now not. Maybe later we'll fix it.

    :argument stream_object: Union[list, tuple, dict] Object that will be
    not full iterated.
    :argument sep: string Inserted between values, default a space.
    :argument end: string Appended after the last value, default a newline.
    """
    for i in stream_object:
        print(i, sep=sep, end=end)


def citer(
    iterable_object: Any,
    sentinel: Optional[Any] = None,
    sep: str = " ",
    end: str = "\n"
) -> None:
    """
    Iterating given object.

    :argument iterable_object: Any Object that will be FULL iterated using
    inserted or not sentinel. Iterator will print subobject of iterable_object
    until it return sentinel if sentinel! Elif not sentinel iterator will
    print subobject of iterable_object until iterable_object not end.
    :argument sentinel: Any Object (can be None). Iterator will print subobject
    of iterable_object if sentinel != subobject. Elif sentinel == subobject
    function will stop.
    :argument sep: string Inserted between values, default a space.
    :argument end: string Appended after the last value, default a newline."""
    if sentinel:
        for i in iter(iterable_object, sentinel):
            print(i, sep=sep, end=end)
    else:
        for i in iter(iterable_object):
            print(i, sep=sep, end=end)
