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

from __future__ import print_function, absolute_import, division

from cmdparse import Command

import pygeda.lib.schem
from pygeda.lib.log import message
from pygeda.lib.schem_obj import Component

class Stat(Command):

    __cmd__ = "stat"
    __help__ = "display project statistics"

    def sch_stat(self, path):
        sch = pygeda.lib.schem.Schematic(path)
        sch.open()
        sch.parse()
        message("Object Count : {}".format(len(sch.objects)))
        message("Components   : {}".format(len(sch.get_by_class(Component))))
        message("Net Fragments: {}".format(len(sch.get_by_type('N'))))

    def print_stat(self, env):
        message("Statistics:")
        message('Schematic Files:')
        for path in env.schematic_files:
            message('File: {}'.format(path))
            self.sch_stat(path)

    def run(self, env=None):
        """Run command."""
        self.print_stat(env)
        pass
