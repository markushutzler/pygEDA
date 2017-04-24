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


class Path(Command):

    __cmd__ = "path"
    __help__ = "display used system path"

    def print_path(self, env):
        print()
        print('gEDA:', env.gEDA_path)
        print('PCB :', env.pcb_path)
        print('Symbols:')
        for path in  env.symbol_path:
            print('      ', path)
        print('Packages:')
        for path in  env.package_path:
            print('      ', path)
        print('Schematic Files:')
        for path in  env.schematic_files:
            print('      ', path)
        print('PCB File:')
        print('      ', env.pcb_file)
        print('Output Path:')
        print('      ', env.output_path)

    def run(self, env=None):
        """Run command."""
        self.print_path(env)
