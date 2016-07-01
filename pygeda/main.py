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

from __future__ import print_function, absolute_import

import cmdparse

if __name__ == "__main__":
    import sys
    import os
    path = os.path.abspath(os.path.dirname('__file__'))
    print("DEBUG: add module to sys-path %s" % path)
    sys.path.insert(0, path)

from pygeda.commands.template import Template
from pygeda.commands.validate import Validate


class Pygeda(object):
    def __init__(self):
        pass


def main():
    parser = cmdparse.ArgumentParser(description='Process some integers.')

    # Add commands
    parser.add_command(Template)
    parser.add_command(Validate)

    # Add global options
    parser.add_argument("-s", dest="sch", metavar="SCH", nargs='+',
                        help="schematic files")
    parser.add_argument("-p", dest="pcb", metavar="PCB", nargs="+",
                        help="pcb files")
    parser.add_argument("-c", dest="config", metavar="PCB",
                        help="project or config file")
    args = parser.parse_args()
    command = args.command()
    print("DEBUG: Running command: %s" % command.__cmd__)
    command.run()

if __name__ == "__main__":
    exit(main())
