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
    path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    print("DEBUG: add module to sys-path {}".format(path))
    sys.path.insert(0, path)


from pygeda.commands.path import Path
from pygeda.commands.stat import Stat
import pygeda.lib.env


class Pygeda(object):
    def __init__(self):
        pass


def main():
    parser = cmdparse.ArgumentParser(description='pygeda')

    # Add commands
    parser.add_command(Path)
    parser.add_command(Stat)

    # Add global options
    parser.add_argument("-c", dest="config", metavar="cfg",
                        help="project or config file", default="pygedarc")
    args = parser.parse_args()
    command = args.command()
    env = pygeda.lib.env.Env()
    try:
        env.check_project_file(args.config)
    except IOError as error:
        parser.error(error)
    command.run(env)

if __name__ == "__main__":
    exit(main())
