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

from libxyz.ui import Keys

class Shortcut(object):
    """
    Keyboard shortcut abstraction class
    """

    def __init__(self, raw_shortcut):
        """
        @param raw_shortcut: Raw shortcut as read from config file
        """

        self.keys = Keys()

        _shortcut = []

        for _key in raw_shortcut.split("-"):
            try:
                _shortcut.append(getattr(self.keys, _key))
            except AttributeError, e:
                _shortcut.append(_key)

        self.shortcut = " ".join(_shortcut)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<Shortcut object: %s>" % self.shortcut

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()
