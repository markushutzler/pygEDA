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


class Refdes(Command):

    __cmd__ = "refdes"
    __help__ = "rearrange schematic references."

    def add_argumants(parser):
        """Add custom arguments."""
        parser.add_argument('-f', target='force', action="store_true",
                            help="overwrite duplicate")
        parser.add_argument('-r', target='reset', action="store_true",
                            help="reset old references")

    def run(self):
        """Run command."""
        pass
