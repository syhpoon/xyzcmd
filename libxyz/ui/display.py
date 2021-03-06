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

import urwid

def init_display(lib):
    """
    Initiate terminal driver

    @param lib: Driver lib: raw or curses
    """

    if lib == "curses":
        import urwid.curses_display as display
    else:
        import urwid.raw_display as display
        
    return display.Screen()

def is_lowui_ge_0_9_9():
    if hasattr(urwid, "VERSION") and urwid.VERSION >= (0, 9, 9):
        return True
    else:
        return False
