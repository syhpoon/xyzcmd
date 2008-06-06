#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#
# This file is part of XYZCommander.
# XYZCommander is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# XYZCommander is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser Public License for more details.
# You should have received a copy of the GNU Lesser Public License
# along with XYZCommander. If not, see <http://www.gnu.org/licenses/>.

class LogLevel(object):
    """
    Available log levels
    """

    def __init__(self):
        self._levels = {"NONE": 0,
                        "ERROR": 1,
                        "WARNING": 2,
                        "INFO": 4,
                        "DEBUG": 8,
                        "UNKNOWN": 16,
                        "ALL": 31,
                        }

        self._str_levels = dict([(v, k) for k, v in self._levels.iteritems()])

        for _k, _v in self._levels.iteritems():
            setattr(self, _k, _v)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def str_level(self, level):
        """
        Return string level representation
        """

        return self._str_levels[level]
