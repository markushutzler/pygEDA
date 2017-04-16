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

"""This module handles schematic objects."""

FORMAT_XY = [['x', int], ['y', int], ]


class SchematicObject(object):
    """Base class for Schematic objects."""
    has_lines = False

    def __init__(self, d):
        self.attributes = []
        self.data = d
        self.text = []
        self.ctype = d[0]
        idx = 1
        for field in self.fields:
            # print(self,field[0],field[1](d[idx]))
            setattr(self, field[0], field[1](d[idx]))
            idx += 1

    def append_text(self, text):
        self.text.append(text)


class Version(SchematicObject):
    ctype = 'v'
    fields = [['version', int], ['fileformat_version', int] ]
    pos = None

class Text(SchematicObject):
    has_lines = True
    ctype = 'T'
    fields = FORMAT_XY + [['color',int],['size',int],['visibility',int],
                          ['show_name_value',int],['angle',int],
                          ['alignment',int],['num_lines',int]]


class Attribute(Text):
    def append_text(self, text):
        super(Attribute, self).append_text(text)
        self.set(text)

    def set(self, s, parent=None):
        self.key = s.split('=')[0]
        self.value = "".join(s.split('=')[1:])


class UndefinedObject(SchematicObject):
    ctype = '-'
    fields = []


def component_for_line(l):
    object_types = [
            Version, Text,
    ]
    for cls in object_types:
        if cls.ctype == l[0]:
            return cls(l)
    ret = UndefinedObject(l)
    return ret
