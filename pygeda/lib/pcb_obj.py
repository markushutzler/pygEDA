#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pygeda - Support tool for Electonic Design Automation
# Copyright (C) 2017  Markus Hutzler
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

from __future__ import print_function, absolute_import, division

from pygeda.lib.pcb_types import distance, flags

_POOL = {}


def register(cls):
    """Register PCB Object class to pool."""
    _POOL[cls.__name__] = cls


def get_class(name):
    """Retrieve class bu name."""
    if name == 'Comment':
        name = 'PCBComment'
    return _POOL.get(name)


class PCBObject(object):
    """PCB Object base class."""
    fields = []
    children = []
    has_children = False
    old_style = False

    def __init__(self, line=None):
        self.line = line
        self.children = []
        if not line:
            return
        items = line.items
        idx = 0
        if isinstance(self, get_class('Comment')):
            self.comment = line.line
            return
        for field in self.fields:
            setattr(self, field[0], field[1](items[idx]))
            idx += 1


class PCBBase(PCBObject):
    """Root PCB class."""
    has_children = True


@register
class PCBComment(PCBObject):
    """Special PCB Object."""
    fields = [['comment', str], ]


@register
class Arc(PCBObject):
    """PCB Object."""
    fields = [
        ['x', distance], ['y', distance], ['width', distance],
        ['height', distance], ['thickness', distance],
        ['clearance', distance], ['startangle', int], ['deltaangle', int],
        ['nflags', str]
    ]

@register
class Attribute(PCBObject):
    """PCB Object."""
    fields = [['name', str], ['value', str], ]
    old_style = True


@register
class Connect(PCBObject):
    """PCB Object."""
    fields = [['pinpad', str], ]
    old_style = True


@register
class Cursor(PCBObject):
    """PCB Object."""
    fields = [['x', int], ['y', int], ['zoom', float], ]
    old_style = True


@register
class DRC(PCBObject):
    """PCB Object."""
    fields = [
        ['bloat', distance], ['shrink', distance], ['line', distance],
        ['silk', distance], ['drill', distance], ['ring', distance]
    ]


@register
class Element(PCBObject):
    """PCB Object."""
    fields = [
        ['sflags', flags], ['desc', str], ['name', str], ['value', str],
        ['mx', distance], ['my', distance], ['tx', distance],
        ['ty', distance], ['tdir', int], ['tscale', int], ['tsflags', flags]
    ]
    has_children = True


@register
class ElementArc(PCBObject):
    """PCB Object."""
    fields = [
        ['x', distance], ['y', distance], ['width', distance],
        ['height', distance], ['startAngle', int], ['seltaAngle', int],
        ['thickness', distance]
    ]


@register
class ElementLine(PCBObject):
    """PCB Object."""
    fields = [
        ['x1', distance], ['y1', distance], ['x2', distance], ['y2', distance],
        ['thickness', distance]
    ]


@register
class FileVersion(PCBObject):
    """PCB Object."""
    fields = [['version', int], ]


@register
class Flags(PCBObject):
    """PCB Object."""
    fields = [['number', str], ]
    old_style = True


@register
class Grid(PCBObject):
    """PCB Object."""
    fields = [
        ['step', distance], ['offsetx', distance], ['offsety', distance],
        ['visible', int]
    ]


@register
class Groups(PCBObject):
    """PCB Object."""
    fields = [['string', str], ]
    old_style = True


@register
class Layer(PCBObject):
    """PCB Object."""
    fields = [['layerNum', int], ['name', str]]
    old_style = True
    has_children = True


@register
class Line(PCBObject):
    """PCB Object."""
    fields = [
        ['x1', distance], ['y1', distance], ['x2', distance], ['y2', distance],
        ['thickness', distance], ['clearance', distance], ['sflags', flags]
    ]


@register
class Mark(PCBObject):
    """PCB Object."""
    fields = [['x', int], ['y', int]]


@register
class Net(PCBObject):
    """PCB Object."""
    fields = [['name', str], ['style', str]]
    old_style = True
    has_children = True


@register
class NetList(PCBObject):
    """PCB Object."""
    fields = []
    old_style = True


@register
class Pad(PCBObject):
    """PCB Object."""
    fields = [
        ['rx1', distance], ['ry1', distance], ['rx2', distance],
        ['ry2', distance], ['thickness', distance], ['clearance', distance],
        ['mask', distance], ['name', str], ['number', str], ['sflags', flags]
    ]


@register
class PCB(PCBObject):
    """PCB Object."""
    fields = [['name', str], ['width', distance], ['height', distance]]


@register
class Pin(PCBObject):
    """PCB Object."""
    fields = [
        ['rx', distance], ['ry', distance], ['thickness', distance],
        ['clearance', distance], ['mask', distance], ['drill', distance],
        ['name', str], ['number', str], ['sflags', flags]
    ]


@register
class PolyArea(PCBObject):
    """PCB Object."""
    fields = [['area', float], ]


@register
class Polygon(PCBObject):
    """PCB Object."""
    fields = [['sflags', flags], ]
    old_style = True


@register
class Rat(PCBObject):
    """PCB Object."""
    fields = [
        ['x1', distance], ['y1', distance], ['group1', int],
        ['x2', distance], ['y2', distance], ['group2', int],
        ['sflags', flags]
    ]


@register
class Styles(PCBObject):
    """PCB Object."""
    fields = [['string', str], ]
    old_style = True


@register
class Symbol(PCBObject):
    """PCB Object."""
    fields = [['char', str], ['delta', distance]]
    has_children = True


@register
class SymbolLine(PCBObject):
    """PCB Object."""
    fields = [
        ['x1', distance], ['y1', distance], ['x2', distance], ['y2', distance],
        ['thickness', distance]
    ]


@register
class Text(PCBObject):
    """PCB Object."""
    fields = [
        ['x', distance], ['y', distance], ['direction', int], ['scale', float],
        ['string', str], ['sflags', flags]
    ]


@register
class Thermal(PCBObject):
    """PCB Object."""
    fields = [['scale', float], ]


@register
class Via(PCBObject):
    """PCB Object."""
    fields = [
        ['x', distance], ['y', distance], ['thickness', distance],
        ['clearance', distance], ['mask', distance], ['drill', distance],
        ['name', str], ['sflags', flags]
    ]
