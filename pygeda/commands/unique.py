#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    This file is part of pygEDA.
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
#    Copyright 2012 Markus Hutzler, spiderware gmbh


from __future__ import print_function, absolute_import, division

import uuid

from pygeda.lib.schem import Schematic, Attribute
from pygeda.lib.log import message
from cmdparse import Command


class Unique(Command):
    __cmd__ = 'unique'
    __help__ = 'generate or overwrite unique IDs in schematic files'

    uids = None
    env = None

    def _new_uid(self):
        uid = str(uuid.uuid1())
        if uid in self.uids:
            uid = self._new_uid()
        return uid

    def process_component(self, component):
        ret = 0
        unique_id = component.attribute('uid')
        if not unique_id:
            new = Attribute(['T', component.x, component.y,
                             0, 10, 0, 2, 0, 0, 1])
            uid = self._new_uid()
            new.key = 'uid'
            new.value = uid
            component.attributes.append(new)
            message('Adding UID {}. ({})'.format(
                str(component.attribute('uid').value),
                component.refdes(string=True)), 'I')
            ret = 1
        else:
            if unique_id.value in self.uids:
                new_uid = self._new_uid()
                message('Changing UID {} to {}. ({})'.format(
                    str(unique_id.value),
                    new_uid,
                    component.refdes(string=True)), 'W')
                unique_id.value = new_uid
                ret = 1
            else:
                self.uids.append(unique_id.value)
        return ret

    def process_file(self, path):
        message('Processing file: {}'.format(path))
        ret = 0
        sch = Schematic(path)
        sch.open()
        sch.parse()
        sch.close()
        self.uids = []
        for component in sch.components:
            ret += self.process_component(component)
        if ret == 0:
            message('All components are unique.', 'I')
        else:
            message('{} changes made.'.format(ret), 'I')
        if self.env.args.dry:
            message('Dry mode - not writing anything.', 'W')
            return ret
        fh = open(path, 'w')
        sch.write(fh)
        return ret

    def run(self, env):
        self.env = env
        for path in env.schematic_files:
            self.process_file(path)
