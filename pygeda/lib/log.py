#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pygeda - Support tools for gEDA
# Copyright (C) 2016  Markus Hutzler
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

DEBUG = False

def _color(level):
    if level == "W":
        return u"\033[33m"
    if level == "E":
        return u"\033[31m"
    return ""


def _color_end(level):
    if level == "W":
        return u"\033[0m"
    if level == "E":
        return u"\033[0m"
    return ""


def message(message, level="R"):
    if level.startswith('D') and not DEBUG:
        return
    line = _color(level)
    if level == "I":
        line += "I: "
    elif level == "W":
        line += "W: "
    elif level == "D":
        line += "D: "
    elif level == "E":
        line += "E: "
    else:
        pass
    line += message
    line += _color_end(level)
    print(line)
