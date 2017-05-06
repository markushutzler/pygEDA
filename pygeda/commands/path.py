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

from pygeda.lib.log import message

class Path(Command):

    __cmd__ = "path"
    __help__ = "display used system path"

    def message_path(self, env):
        message('gEDA: {}'.format(env.gEDA_path))
        message('PCB : {}'.format(env.pcb_path))
        message('Symbols:')
        for path in env.symbol_path:
            message('    {}'.format(path))
        message('Packages:')
        for path in env.package_path:
            message('    {}'.format(path))
        message('Schematic Files:')
        for path in env.schematic_files:
            message('    {}'.format(path))
        message('PCB File:')
        message('    {}'.format(env.pcb_file))
        message('Output Path:')
        message('    {}'.format(env.output_path))

    def run(self, env=None):
        """Run command."""
        self.message_path(env)
