#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    This file is part of pygeda.
#
#    pygEDA is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    pygEDA is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pygEDA.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright 2017 Markus Hutzler


from __future__ import print_function, absolute_import, division

from pygeda.lib.schem import Schematic
from pygeda.lib.log import message
from cmdparse import Command


class Refdes(Command):
    __cmd__ = 'refdes'
    __help__ = 'enumerate components'

    env = None

    def reset(self, component):
        refdes = component.refdes()
        if refdes["value"] == '?':
            return 0
        refdes["value"] = '?'
        message('Reseting Component: {}'.format(component.refdes(string=True)))
        component.set_refdes(refdes)
        return 1

    def process_file(self, path):
        message('Processing file: {}'.format(path))
        sch = Schematic(path)
        sch.open()
        sch.parse()
        sch.close()
        ret = 0

        # reset
        if self.env.args.reset:
            for component in sch.components:
                ret += self.reset(component)

        if ret == 0:
            message('No references where changed.', 'I')
        else:
            message('{} changes made.'.format(ret), 'I')
        if self.env.args.dry:
            message('Dry mode - not writing anything.', 'W')
            return ret
        fh = open(path, 'w')
        sch.write(fh)
        return ret

    def run(self, env=None):
        self.env = env

        for path in env.schematic_files:
            self.process_file(path)

    def add_arguments(self, parser):
        parser.add_argument('-r', dest='reset', action='store_true',
                            help="reset all references")
