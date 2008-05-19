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

class InputWrapper(object):
    """
    Wrap get_input and seek in user-defined keycodes before return keys
    """

    def __init__(self, xyz):
        self.xyz = xyz
        self.plugin = xyz.pm.load(u":core:keycodes")
        self.keycodes = {}

        self.update()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def update(self, data=None):
        """
        Set/load keycodes data
        @param data: Keycodes data. If not provided load via get_keys()
        @type data: dict
        """

        if data is not None:
            self.keycodes = data
        else:
            self.keycodes = self.plugin.get_keys()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get(self):
        """
        Get input from screen and search if it matches any user-defined keycodes
        """

        _input = None

        while True:
            _in = self.xyz.screen.get_input()

            if not _in:
                continue

            try:
                _input = [self.keycodes[tuple(_in)]]
            except KeyError:
                _input = _in
            finally:
                break

        return _input
