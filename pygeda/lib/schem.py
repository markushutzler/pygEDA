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

from __future__ import print_function

from pygeda.lib.schem_obj import *
from pygeda.lib.log import message


class SchematicException(Exception):
    pass

class Schematic(object):
    """This class holds a schematic file."""

    def __init__(self, path=None):
        self.path = path
        self.objects = []

    def open(self):
        try:
            self.fh = open(self.path)
            message("File '{}' open.".format(self.path), 'D')
            return True
        except IOError:
            message("File '{}' doesn't exist.".format(self.path), 'E')
            return False

    @property
    def _next_line(self):
        line = self.fh.readline()
        line = line.strip()
        return line

    def _split(self, line):
        line = line.split(' ')
        line = map(str.strip, line)
        return line

    def parse(self):
        """Reads and parses a schematic file."""

        # check version
        try:
            line = self._next_line
            self.version = component_for_line(self._split(line))
            message("Schematic File Verion: {}".format(self.version.version), 'D')
            message("Schematic File Format: "
                    "{}".format(self.version.fileformat_version), 'D')
        except Exception as exception:
            raise exception

        if not self.version.fileformat_version == 2:
            message('File Version {} is not supported'.format(
                self.version.fileformat_version))
            raise SchematicException()

        lnr=0
        component = None
        parent = None
        line = self._next_line
        while line:
            if component and lnr < component.num_lines:
                component.append_text(line)
                lnr += 1

            elif line == '{':
                parent = component

            elif line == '}':
                parent = None

            elif parent:
                line = self._split(line)
                component = Attribute(line)
                lnr = 0
                parent.attributes.append(component)

            else:
                line = self._split(line)
                component = component_for_line(line)
                lnr = 0
                self.objects.append(component)

            line = self._next_line
