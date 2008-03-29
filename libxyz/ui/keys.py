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

class Keys(object):
    """
    Keys abstractions
    """

    KEY_CONTROL = "ctrl"
    KEY_META = "meta"
    KEY_ESC = "esc"
    KEY_SHIFT = "shift"
    KEY_UP = 'up'
    KEY_DOWN = 'down'
    KEY_RIGHT = 'right'
    KEY_LEFT = 'left'
    KEY_END = 'end'
    KEY_HOME = 'home'
    KEY_INSERT = 'insert'
    KEY_DELETE = 'delete'
    KEY_PAGE_UP = 'page up'
    KEY_PAGE_DOWN = 'page down'
    KEY_ENTER = 'enter'
    KEY_TAB = 'tab'
    KEY_BACKSPACE = 'backspace'

    # F-keys
    KEY_F1 = 'f1'
    KEY_F2 = 'f2'
    KEY_F3 = 'f3'
    KEY_F4 = 'f4'
    KEY_F5 = 'f5'
    KEY_F1 = 'f1'
    KEY_F2 = 'f2'
    KEY_F3 = 'f3'
    KEY_F4 = 'f4'
    KEY_F5 = 'f5'
    KEY_F6 = 'f6'
    KEY_F7 = 'f7'
    KEY_F8 = 'f8'
    KEY_F9 = 'f9'
    KEY_F10 = 'f10'
    KEY_F11 = 'f11'
    KEY_F12 = 'f12'
    KEY_F13 = 'f13'
    KEY_F14 = 'f14'
    KEY_F15 = 'f15'
    KEY_F16 = 'f16'
    KEY_F17 = 'f17'
    KEY_F18 = 'f18'
    KEY_F19 = 'f19'
    KEY_F20 = 'f20'

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def shortcut(self, *keys):
        """
        Make a shortcut
        """

        _keys = []

        for key in keys:
            try:
                key = getattr(self, key)
            except AttributeError:
                pass

            _keys.append(key)

        return " ".join(_keys)
