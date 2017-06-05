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

from cmdparse import Command

import pygeda.lib.schem
import pygeda.lib.pcb
from pygeda.lib.log import message


class Stat(Command):

    __cmd__ = "stat"
    __help__ = "display project statistics"

    def pcb_stat(self, path):
        message('File {}'.format(path))
        pcb = pygeda.lib.pcb.PCBFile(path)
        pcb.open()
        pcb.parse()
        pcb.close()
        # TODO: Read statitics

    def sch_stat(self, path):
        message('File {}'.format(path))
        sch = pygeda.lib.schem.Schematic(path)
        sch.open()
        sch.parse()
        sch.close()
        stat = {'unique': 0, 'rerdes':0}
        uids = []
        for component in sch.components:
            if component.refdes.is_set:
                stat['refdes'] = stat.get('refdes', 0) + 1
            uuid = component.uuid
            if uuid and uuid not in uids:
                stat['unique'] = stat.get('unique', 0) + 1
                uids.append(uuid)
            elif uuid:
                stat['duplicate'] = stat.get('duplicate', 0) + 1

        message("    Object Count   : {}".format(len(sch.objects)))
        message("    Components     : {}".format(len(sch.components)))
        message("        with refdes: {}".format(stat.get('refdes', 0)))
        message("        unique     : {}".format(stat.get('unique', 0)))
        message("        duplicate  : {}".format(stat.get('duplicate', 0)))
        message("    Net Fragments  : {}".format(len(sch.get_by_type('N'))))

    def print_stat(self, env):
        message("Statistics:")
        message("===========\n")

        for path in env.schematic_files:
            self.sch_stat(path)
        self.pcb_stat(env.pcb_file)

    def run(self, env=None):
        """Run command."""
        self.print_stat(env)
