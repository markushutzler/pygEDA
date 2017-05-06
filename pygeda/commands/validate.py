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

import sys
import math

from cmdparse import Command

import pygeda.lib.schem
from pygeda.lib.log import  message


class Validate(Command):
    __cmd__ = 'validate'
    __help__ = 'validate schematic files'
    needed_tasks = []

    def run(self, env):
        for path in env.schematic_files:
            self.validate_file(path)
        message('=== DONE ===')
        order = 1
        if not self.needed_tasks:
            message('No issues found.')
            exit(0)

        message('Please fix all issues in the given order:')
        if 'manual' in self.needed_tasks:
            message('{}) fix issues marked as manually'.format(order))
            order += 1
        if 'unique' in self.needed_tasks:
            message('{}) run pygeda unique'.format(order))
            order += 1
        if 'refdes -f' in self.needed_tasks:
            message('{}) run pygeda refdes -f'.format(order))
            order += 1
        elif 'refdes' in self.needed_tasks:
            message('{}) run pygeda refdes'.format(order))
            order += 1
        exit(1)

    def validate_file(self, path):
        message('Checking file: %s' % path)
        sch = pygeda.lib.schem.Schematic(path)
        sch.open()
        sch.parse()
        sch.close()
        nets = sch.get_by_type('N')

        # Stats
        message('Found %d Components.' % len(sch.components))
        message('Found %d Unique Components.' % len(sch.unique_components))
        message('Found %d Nets.' % len(nets))

        # Check nets
        for net in nets:
            if math.hypot(abs(net.x1-net.x2), abs(net.y1-net.y2)) == 0.0:
                message('Net object with the length of 0.0 at ({}, {}). Fix '
                        'this issue manually.'.format(net.x1, net.y1), 'W')
                self.needed_tasks.append('manual')
            if abs(net.x1-net.x2) and abs(net.y1-net.y2):
                message('None orthogonal net at ({}, {}). Fix this issue '
                        'manually.'.format(net.x1, net.y1), 'W')
                self.needed_tasks.append('manual')

        # Check components
        refdes_list = []
        for comp in sch.components:
            if not comp.refdes.is_set:
                message('Designator of {} is not set.'.format(comp.refdes), 'E')
                self.needed_tasks.append('refdes')
            if not comp.uuid:
                message('UUID of {} is not unique.'.format(comp.refdes), 'E')
                self.needed_tasks.append('unique')
            if comp.refdes.string in refdes_list:
                message('Designator of {} is not unique.'.format(comp.refdes),
                        'E')
                self.needed_tasks.append('refdes -f')

            if comp.refdes.is_set:
                refdes_list.append(comp.refdes.string)
