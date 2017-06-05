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

"""Module to manage PCB files."""

from __future__ import print_function, absolute_import, division

import pygeda.lib.pcb_obj
from pygeda.lib.pcb_parser import PCBLineParser
from pygeda.lib.log import message


class PCBFile(object):
    """This class holds a schematic file."""

    def __init__(self, path=None):
        self.path = path
        self.objects = None

    def open(self):
        try:
            self.fh = open(self.path)
            message("File '{}' open.".format(self.path), 'D')
            return True
        except IOError:
            message("File '{}' doesn't exist.".format(self.path), 'E')
            return False

    def close(self):
        self.fh.close()

    def parse(self):
        """Reads and parses a pcb file."""
        current = None
        target = pygeda.lib.pcb_obj.PCBBase()
        stack = [target, ]
        lines = self.fh.readlines()
        for line in lines:
            line = line.strip()
            line = PCBLineParser(line)
            if line.info:
                cls = pygeda.lib.pcb_obj.get_class(line.info.get('name'))
                current = cls(line)
                target.children.append(current)
            elif line.type == PCBLineParser.OPEN:
                stack.append(current)
                target = current
            elif line.type == PCBLineParser.CLOSE:
                stack.pop()
                target = stack[-1]
        if len(stack) != 1:
            raise Exception("Format Error")
        self.objects = target.children

    def write(self, fh):
        """Write to a schematic file."""
        for obj in self.objects:
            obj.write(fh)
