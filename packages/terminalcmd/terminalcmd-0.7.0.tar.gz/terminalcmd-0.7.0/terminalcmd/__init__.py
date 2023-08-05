# -*- coding: utf-8 -*-
"""
Betterconsole is a Python library which can help you to
make your own terminal program with high-intellegence instruments,
that will make your code "clear" and readable.

 * Note: Library is in beta-test now, so it will update very often.

Library is under the MIT License.

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
LIABILITY, WHETER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from .builtin import (
    log,
    prompt,
    clear,
    args,
    stream,
    citer
)
from .color_console import (
    color,
    back,
    style
)
from . import builder


__author__ = "Dallas"
__name__ = "terminalcmd"
__version__ = "0.7.1"
