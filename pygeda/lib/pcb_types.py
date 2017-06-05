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

import decimal
import math


class flags(object):
    """Representation of PCB flags."""
    initial = None

    def __init__(self, initial):
        self.initial = initial


class distance(object):
    """Repreentation of PCB distance."""
    initial = 0

    def __init__(self, initial):
        self.initial = initial

    def raw(self):
        """RAW distance in 1/100 of a mil."""
        if type(self.initial) == type(1):
            return self.initial

        if type(self.initial) == type(1.0):
            return int(self.initial * 100)

        if self.initial[-2:] == "mm":
            return int(float(self.initial[:-2]) * 3937)

        if self.initial[-3:] == "mil":
            return int(float(self.initial[:-3]) * 100)

        try:
            float(self.initial)
            return int(float(self.initial))
        except:
            raise Exception('unknown value for distance {} ({})'
                            ''.format(self.initial, type(self.initial)))

    def __add__(self, other):
        return distance(self.raw()+other.raw())

    def __sub__(self, other):
        return distance(self.raw()-other.raw())

    def __div__(self, other):
        if type(other) == type(self):
            return distance(self.raw()/other.raw())
        return distance(self.raw()/other)

    def __mul__(self, other):
        if type(other) == type(self):
            return distance(self.raw()*other.raw())
        return distance(self.raw()*other)

    def __neg__(self):
        return distance(-self.raw())

    def __str__(self):
        return self.__repr__()

    def __json__(self):
        return self.__repr__()

    def __repr__(self):
        if self.raw() == 0:
            return "0.0000"
        if self.raw() % 100 == 0:
            return "%d.0mil" % (int(self.raw() / 100))
        dist = decimal.Decimal(float(self.raw()) / 3937)
        return "%smm" % round(dist, 3)
