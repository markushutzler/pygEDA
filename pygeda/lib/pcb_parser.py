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

"""This module handles PCB files."""

from __future__ import print_function, absolute_import, division

import re
import shlex


class PCBLineParser(object):
    """Parser class for a single line of a pcb file."""
    _info = None
    _type = None
    EMPTY = 0x01
    COMMENT = 0x02
    ERROR = 0x03
    OPEN = 0x10
    CLOSE = 0x20
    OLD = 0x40
    NEW = 0x41

    def __init__(self, line):
        self.line = line

    @property
    def type(self):
        if self._type:
            return self._type
        if self.line.startswith('#'):
            self._type = self.COMMENT
        elif self.line == '(':
            self._type = self.OPEN
        elif self.line == ')':
            self._type = self.CLOSE
        elif self.line == '' or not self.line:
            self._type = self.EMPTY
        else:
            obj = re.match(r'^\w+\(', self.line)
            if obj:
                self._type = self.OLD
            obj = re.match(r'^\w+\[', self.line)
            if obj:
                self._type = self.NEW
        if not self._type:
            self._type = self.ERROR
        return self._type

    @property
    def info(self):
        if self._info:
            return self._info
        obj = None
        if self.type == self.EMPTY:
            self._info = {'name': 'Comment', 'items': ''}
        elif self.type == self.COMMENT:
            self._info = {'name': 'Comment', 'items': self.line}
        elif self.type == self.NEW:
            obj = re.match(r'^(?P<name>\w+)\[(?P<items>.*)\]', self.line)
        elif self.type == self.OLD:
            obj = re.match(r'^(?P<name>\w+)\((?P<items>.*)\)', self.line)
        if obj:
            self._info = obj.groupdict()
        return self._info

    @property
    def items(self):
        info = self.info
        if not info:
            return []
        return shlex.split(info.get('items'))
