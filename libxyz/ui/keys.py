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

    CONTROL = "ctrl"
    CTRL = CONTROL
    META = "meta"
    ESCAPE = "esc"
    ESC = ESCAPE
    SHIFT = "shift"
    UP = 'up'
    DOWN = 'down'
    RIGHT = 'right'
    LEFT = 'left'
    END = 'end'
    HOME = 'home'
    INSERT = 'insert'
    DELETE = 'delete'
    PAGE_UP = 'page up'
    PAGE_DOWN = 'page down'
    ENTER = 'enter'
    TAB = 'tab'
    BACKSPACE = 'backspace'

    # F-keys
    F1 = 'f1'
    F2 = 'f2'
    F3 = 'f3'
    F4 = 'f4'
    F5 = 'f5'
    F1 = 'f1'
    F2 = 'f2'
    F3 = 'f3'
    F4 = 'f4'
    F5 = 'f5'
    F6 = 'f6'
    F7 = 'f7'
    F8 = 'f8'
    F9 = 'f9'
    F10 = 'f10'
    F11 = 'f11'
    F12 = 'f12'
    F13 = 'f13'
    F14 = 'f14'
    F15 = 'f15'
    F16 = 'f16'
    F17 = 'f17'
    F18 = 'f18'
    F19 = 'f19'
    F20 = 'f20'

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
