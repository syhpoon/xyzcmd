#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <syhpoon@syhpoon.name> 2008
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

from libxyz.ui.display import is_lowui_ge_0_9_9

class InputWrapper(object):
    """
    Wrap get_input and seek in user-defined keycodes before return keys
    """

    WIN_RESIZE = 'window resize'
    
    def __init__(self, xyz):
        self.xyz = xyz
        self.plugin = xyz.pm.load(u":core:keycodes")
        self.keycodes = {}
        self._resized = False

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

    def get(self, allow_empty=False):
        """
        Get input from screen and search if it matches any user-defined
        keycodes

        @param allow_empty: If set, returns empty list if nothing was typed
        """

        _input = None

        if allow_empty:
            if is_lowui_ge_0_9_9():
                self.xyz.screen.set_input_timeouts(0)

        while True:
            _in = self.xyz.screen.get_input()

            if not _in:
                if allow_empty:
                    _input = _in
                    break
                else:
                    continue

            if self.WIN_RESIZE in _in:
                self._resized = True

            try:
                _input = [self.keycodes[tuple(_in)]]
            except KeyError:
                _input = _in

            break

        if allow_empty:
            if is_lowui_ge_0_9_9():
                self.xyz.screen.set_input_timeouts(None)

        return _input

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _resized_get(self):
        rval = self._resized

        if rval:
            self._resized = False

        return rval

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _resized_set(self, value):
        if value:
            self._resized = True
        else:
            self._resized = False
            
    resized = property(_resized_get, _resized_set)
