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

"""Command script for refdes manipulation."""

from __future__ import print_function, absolute_import, division

from pygeda.lib.schem import Schematic, SchematicException
from pygeda.lib.log import message
from cmdparse import Command


class RefdesPool(object):
    """Pool to manage `schem_obj.Refdes` objects."""
    changes = 0
    pool = []

    def add(self, item, reset=False):
        """Add object to pool."""
        if not item:
            return
        if item.value in self.values(item.base):
            if reset:
                self.reset(item)
            else:
                message('Duplicate {}'.format(item.string), 'E')
                raise SchematicException('Duplicate Refdes')
        self.pool.append(item)

    def reset(self, item):
        """Reset refdes object."""
        if item.value == '?':
            return
        message('Resetting Component: {}'.format(item.string), 'I')
        item.value = '?'
        self.changes += 1

    def reset_all(self):
        """Reset all objects added to the pool."""
        map(self.reset, self.pool)

    def filter(self, base, remove_undefined=True):
        """Filter objects by base."""
        if not remove_undefined:
            return [x for x in self.pool if  x.base == base]
        return [x for x in self.pool if x.base == base and x.value != '?']

    def next_value(self, base):
        """Next possible value of a specific base."""
        ret = 1
        values = self.values(base)
        while str(ret) in values:
            ret += 1
        return ret

    def next_undefined(self):
        """Next undefined object in pool."""
        for refdes in self.pool:
            if refdes.value == '?':
                return refdes
        return None

    def values(self, base):
        """List of all values for a specific bae."""
        return [i.value for i in self.filter(base)]

    def enumerate(self):
        """Enumerate all objects."""
        while True:
            item = self.next_undefined()
            if not item:
                return
            value = self.next_value(item.base)
            item.value = str(value)
            message('Naming Component: {}'.format(item.string), 'I')
            self.changes += 1

class Refdes(Command):
    """Refdes command implementation."""
    __cmd__ = 'refdes'
    __help__ = 'enumerate components'

    env = None
    reflist = {}

    def process_file(self, path):
        """Process schematic file."""
        message('Processing file: {}'.format(path))
        sch = Schematic(path)
        sch.open()
        sch.parse()
        sch.close()
        ret = 0

        pool = RefdesPool()
        for component in sch.components:
            pool.add(component.refdes, reset=(self.env.args.reset or
                                              self.env.args.duplicates))

        if self.env.args.reset:
            pool.reset_all()
        if not self.env.args.no_enum:
            pool.enumerate()

        if pool.changes == 0:
            message('No references where changed.', 'I')
        else:
            message('{} changes made.'.format(pool.changes), 'I')
        if self.env.args.dry:
            message('Dry mode - not writing anything.', 'W')
            return ret
        fhandler = open(path, 'w')
        sch.write(fhandler)
        return ret

    def run(self, args=None):
        self.env = args

        for path in self.env.schematic_files:
            self.process_file(path)

    def add_arguments(self, parser):
        parser.add_argument('-r', dest='reset', action='store_true',
                            help="reset all references")
        parser.add_argument('-f', dest='duplicates', action='store_true',
                            help="rename duplicate objects")
        parser.add_argument('--no-enum', dest='no_enum', action='store_true',
                            help="do not enumerate")
