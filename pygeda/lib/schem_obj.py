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

import re


FORMAT_LINE = [
        ['color', int],
        ['line_width', int],
        ['capstyle', int],
        ['dashstyle',int],
        ['dashlength', int],
        ['dashspace', int]
]

FORMAT_XY = [
        ['x', int],
        ['y', int],
]

FORMAT_2XY = [
        ['x1', int],
        ['y1', int],
        ['x2', int],
        ['y2', int],
]

FORMAT_FILL =  [
        ['filltype', int],
        ['fillwidth', int],
        ['angle1', int],
        ['pitch1', int],
        ['angle2', int],
        ['pitch2', int]
]


class SchematicObject(object):
    """Base class for Schematic objects."""
    num_lines = 0

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

    def attribute(self, key):
        """Returns the first attribute for a key."""
        for i in self.attributes:
            if i.key == key:
                return i

    def write(self, fh):
        line = [self.ctype, ]
        for field in self.fields:
            line.append(str(getattr(self, field[0])))
        fh.write(' '.join(line))
        fh.write('\n')
        for line in self.text:
            fh.write(line)
            fh.write('\n')
        if not self.attributes:
            return
        fh.write('{\n')
        for attr in self.attributes:
            attr.write(fh)
        fh.write('}\n')


class Component(SchematicObject):
    ctype = 'C'
    fields = FORMAT_XY + [['selectable',int],['angle',int],['mirror',int],
                          ['basename',str] ]

    refdes_re = re.compile(r"^(?P<base_ref>[a-zA-Z_]+?)(?P<value>[0-9?]+?)"
                            "(?P<postfix>[a-zA-Z]*?)$")

    def refdes(self, string=False):
        """Returns the refdes of the Component.

        If string=True, a string like C3 or U5a will be retuned. Otherwise, a
        dict (see refdes_re) + error state  will be returned."""

        attribute = self.attribute('refdes')
        if attribute:
            if string:
                return attribute.value
            x = self.refdes_re.match(attribute.value)
            if x:
                ret = x.groupdict()
                ret['error'] = None
                return ret
            else:
                return {'postfix': '', 'base_ref': '', 'value': '',
                        'error': 'Refdes not well formated.'}


class Version(SchematicObject):
    ctype = 'v'
    fields = [['version', int], ['fileformat_version', int] ]


class Line(SchematicObject):
    ctype = 'L'
    fields = FORMAT_2XY  + FORMAT_LINE


class Box(SchematicObject):
    ctype = 'B'
    _EXTRA = [['width', int], ['height',int], ]
    fields = FORMAT_XY + _EXTRA + FORMAT_LINE + FORMAT_FILL


class Circle(SchematicObject):
    ctype = 'V'
    fields = FORMAT_XY + [['radius', int], ] + FORMAT_LINE + FORMAT_FILL


class Arc(SchematicObject):
    ctype = 'A'
    fields = FORMAT_XY + [['radius', int], ['startangle', int],
                          ['sweepangle', int], ] + FORMAT_LINE


class Text(SchematicObject):
    ctype = 'T'
    fields = FORMAT_XY + [['color',int],['size',int],['visibility',int],
                          ['show_name_value',int],['angle',int],
                          ['alignment',int],['num_lines',int]]


class Net(SchematicObject):
    ctype = 'N'
    fields = FORMAT_2XY + [['color', int], ]


class Bus(SchematicObject):
    ctype = 'U'
    fields = FORMAT_2XY + [['color', int], ['ripperdir', int], ]


class Pin(SchematicObject):
    ctype = 'P'
    fields = FORMAT_2XY + [['color', int], ['pintype', int],
                           ['whichend', int], ]


class Path(SchematicObject):
    has_lines = True
    ctype = 'H'
    fields = FORMAT_LINE + FORMAT_FILL + [['num_lines', int], ]


class Attribute(Text):
    key = None
    value = None

    def append_text(self, text):
        super(Attribute, self).append_text(text)
        self._set(text)

    def write(self, fh):
        self.text = ['='.join([self.key, self.value]), ]
        super(Attribute, self).write(fh)

    def _set(self, s):
        self.key = s.split('=')[0]
        self.value = "=".join(s.split('=')[1:])


class UndefinedObject(SchematicObject):
    ctype = '-'
    fields = []


def component_for_line(l):
    object_types = [
        Version, Component, Text, Box, Net, Line, Circle, Arc, Bus, Pin, Path,
    ]
    for cls in object_types:
        if cls.ctype == l[0]:
            return cls(l)
    ret = UndefinedObject(l)
    return ret
