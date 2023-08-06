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


class textColor:
    """
    Class containing ASCII codes, that
    in console making colored TEXT.

    Highlights have more opacity.
    """
    black        = "\u001b[30m"
    red          = "\u001b[31m"
    green        = "\u001b[32m"
    yellow       = "\u001b[33m"
    blue         = "\u001b[34m"
    magneta      = "\u001b[35m"
    cyan         = "\u001b[36m"
    white        = "\u001b[37m"
    reset        = "\u001b[39m"
    # -------Highlights-------
    black_ex     = "\u001b[90m"
    red_ex       = "\u001b[91m"
    greenm_ex    = "\u001b[92m"
    yellow_ex    = "\u001b[93m"
    blue_ex      = "\u001b[94m"
    magneta_ex   = "\u001b[95m"
    cyan_ex      = "\u001b[96m"
    white_ex     = "\u001b[97m"


class backColor:
    """
    Class containing ASCII codes, that
    in console making colored BACK and
    don't touch the text.

    Highlights have more opacity.
    """
    black        =  "\u001b[40m"
    red          =  "\u001b[41m"
    green        =  "\u001b[42m"
    yellow       =  "\u001b[43m"
    blue         =  "\u001b[44m"
    magneta      =  "\u001b[45m"
    cyan         =  "\u001b[46m"
    white        =  "\u001b[47m"
    reset        =  "\u001b[49m"
    # -------Highlights--------
    black_ex     = "\u001b[100m"
    red_ex       = "\u001b[101m"
    greenm_ex    = "\u001b[102m"
    yellow_ex    = "\u001b[103m"
    blue_ex      = "\u001b[104m"
    magneta_ex   = "\u001b[105m"
    cyan_ex      = "\u001b[106m"
    white_ex     = "\u001b[107m"


class styleColor:
    """
    Class containing ASCII codes, that
    in console change text font.
    """
    bright       = "\u001b[1m"
    dim          = "\u001b[2m"
    normal       = "\u001b[22m"
    reset        = "\u001b[0m"


color = textColor
back  = backColor
style = styleColor
