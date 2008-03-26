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

    KEY_SLASH = '/'
    KEY_ASTERISK = '*'
    KEY_MINUS = '-'
    KEY_PLUS = '+'

    KEY_SHIFT_TAB = 'shift tab'
    KEY_SHIFT_UP = 'shift up'
    KEY_SHIFT_DOWN = 'shift down'
    KEY_SHIFT_RIGHT = 'shift right'
    KEY_SHIFT_LEFT = 'shift left'
    KEY_SHIFT_END = 'shift end'
    KEY_SHIFT_HOME = 'shift home'

    KEY_CTRL_UP = 'ctrl up'
    KEY_CTRL_DOWN = 'ctrl down'
    KEY_CTRL_RIGHT = 'ctrl right'
    KEY_CTRL_LEFT = 'ctrl left'
    KEY_CTRL_END = 'ctrl end'
    KEY_CTRL_HOME = 'ctrl end'

    KEY_SHIFT_CTRL_UP = 'shift ctrl up'
    KEY_SHIFT_CTRL_DOWN = 'shift ctrl down'
    KEY_SHIFT_CTRL_RIGHT = 'shift ctrl right'
    KEY_SHIFT_CTRL_LEFT = 'shift ctrl left'
    KEY_SHIFT_CTRL_END = 'shift ctrl end'
    KEY_SHIFT_CTRL_HOME = 'shift ctrl home'

    KEY_SHIFT_F1 = 'shift f1'
    KEY_SHIFT_F2 = 'shift f2'
    KEY_SHIFT_F3 = 'shift f3'
    KEY_SHIFT_F4 = 'shift f4'
    KEY_SHIFT_F5 = 'shift f5'
    KEY_SHIFT_F6 = 'shift f6'
    KEY_SHIFT_F7 = 'shift f7'
    KEY_SHIFT_F8 = 'shift f8'
    KEY_SHIFT_F9 = 'shift f9'
    KEY_SHIFT_F10 = 'shift f10'
    KEY_SHIFT_F11 = 'shift f11'
    KEY_SHIFT_F12 = 'shift f12'
    KEY_SHIFT_F13 = 'shift f13'
    KEY_SHIFT_F14 = 'shift f14'
    KEY_SHIFT_F15 = 'shift f15'
    KEY_SHIFT_F16 = 'shift f16'
    KEY_SHIFT_F17 = 'shift f17'
    KEY_SHIFT_F18 = 'shift f18'
    KEY_SHIFT_F19 = 'shift f19'
    KEY_SHIFT_F20 = 'shift f20'

    KEY_CTRL_F1 = 'ctrl f1'
    KEY_CTRL_F2 = 'ctrl f2'
    KEY_CTRL_F3 = 'ctrl f3'
    KEY_CTRL_F4 = 'ctrl f4'
    KEY_CTRL_F5 = 'ctrl f5'
    KEY_CTRL_F6 = 'ctrl f6'
    KEY_CTRL_F7 = 'ctrl f7'
    KEY_CTRL_F8 = 'ctrl f8'
    KEY_CTRL_F9 = 'ctrl f9'
    KEY_CTRL_F10 = 'ctrl f10'
    KEY_CTRL_F11 = 'ctrl f11'
    KEY_CTRL_F12 = 'ctrl f12'
    KEY_CTRL_F13 = 'ctrl f13'
    KEY_CTRL_F14 = 'ctrl f14'
    KEY_CTRL_F15 = 'ctrl f15'
    KEY_CTRL_F16 = 'ctrl f16'
    KEY_CTRL_F17 = 'ctrl f17'
    KEY_CTRL_F18 = 'ctrl f18'
    KEY_CTRL_F19 = 'ctrl f19'
    KEY_CTRL_F20 = 'ctrl f20'

    KEY_SHIFT_CTRL_F1 = 'shift ctrl f1'
    KEY_SHIFT_CTRL_F2 = 'shift ctrl f2'
    KEY_SHIFT_CTRL_F3 = 'shift ctrl f3'
    KEY_SHIFT_CTRL_F4 = 'shift ctrl f4'
    KEY_SHIFT_CTRL_F5 = 'shift ctrl f5'
    KEY_SHIFT_CTRL_F6 = 'shift ctrl f6'
    KEY_SHIFT_CTRL_F7 = 'shift ctrl f7'
    KEY_SHIFT_CTRL_F8 = 'shift ctrl f8'
    KEY_SHIFT_CTRL_F9 = 'shift ctrl f9'
    KEY_SHIFT_CTRL_F10 = 'shift ctrl f10'
    KEY_SHIFT_CTRL_F11 = 'shift ctrl f11'
    KEY_SHIFT_CTRL_F12 = 'shift ctrl f12'
    KEY_SHIFT_CTRL_F13 = 'shift ctrl f13'
    KEY_SHIFT_CTRL_F14 = 'shift ctrl f14'
    KEY_SHIFT_CTRL_F15 = 'shift ctrl f15'
    KEY_SHIFT_CTRL_F16 = 'shift ctrl f16'
    KEY_SHIFT_CTRL_F17 = 'shift ctrl f17'
    KEY_SHIFT_CTRL_F18 = 'shift ctrl f18'
    KEY_SHIFT_CTRL_F19 = 'shift ctrl f19'
    KEY_SHIFT_CTRL_F20 = 'shift ctrl f20'
