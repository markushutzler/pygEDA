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

import cmdparse

if __name__ == "__main__":
    import sys
    import os
    path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    print("DEBUG: add module to sys-path {}".format(path))
    sys.path.insert(0, path)


import pygeda.lib.env
from pygeda.commands.path import Path
from pygeda.commands.stat import Stat
from pygeda.commands.unique import Unique
from pygeda.commands.refdes import Refdes


class Pygeda(object):
    def __init__(self):
        pass


def main():
    parser = cmdparse.ArgumentParser(description='pygeda')

    # Add commands
    parser.add_command(Path)
    parser.add_command(Stat)
    parser.add_command(Unique)
    parser.add_command(Refdes)

    # Add global options
    parser.add_argument("-c", dest="config", metavar="cfg",
                        help="project or config file", default="pygedarc")
    parser.add_argument("-d", dest="dry", action="store_true", default=False,
                        help="dry mode, do not write anything")
    args = parser.parse_args()
    command = args.command()
    env = pygeda.lib.env.Env()
    env.args = args
    try:
        env.check_project_file(args.config)
    except IOError as error:
        parser.error(error)
    command.run(env)

if __name__ == "__main__":
    exit(main())
