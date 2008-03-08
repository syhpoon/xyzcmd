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

import copy

from libxyz.exceptions import XYZValueError

class Color(object):
    """
    Base color
    """

    colors = {}
    ctype = "base"

    def __init__(self, color):
        if color not in self.colors:
            raise XYZValueError(_("Invalid %s color: %s" % \
            (self.ctype, str(color))))

        self.color = self.colors[color]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<%s color: %s>" % (self.ctype, str(self.color))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

#++++++++++++++++++++++++++++++++++++++++++++++++

class Foreground(Color):
    """
    Foreground color
    """

    colors = {
              "BLACK": "black",
              "BROWN": "brown",
              "YELLOW": "yellow",
              "WHITE": "white",
              "DEFAULT": "default",

              "DARK_BLUE": "dark blue",
              "DARK_MAGENTA": "dark magenta",
              "DARK_CYAN": "dark cyan",
              "DARK_RED": "dark red",
              "DARK_GREEN": "dark green",
              "DARK_GRAY": "dark gray",

              "LIGHT_GRAY": "light gray",
              "LIGHT_RED": "light red",
              "LIGHT_GREEN": "light green",
              "LIGHT_BLUE": "light blue",
              "LIGHT_MAGENTA": "light magenta",
              "LIGHT_CYAN": "light cyan",
              }

    ctype = "foreground"

#++++++++++++++++++++++++++++++++++++++++++++++++

class Background(Color):
    """
    Background color
    """

    colors = {
              "BLACK": "black",
              "BROWN": "brown",
              "DEFAULT": "default",

              "DARK_RED": "dark red",
              "DARK_GREEN": "dark green",
              "DARK_BLUE": "dark blue",
              "DARK_MAGENTA": "dark magenta",
              "DARK_CYAN": "dark cyan",

              "LIGHT_GRAY": "light gray",
              }

    ctype = "background"

#++++++++++++++++++++++++++++++++++++++++++++++++

class Monochrome(Color):
    """
    Monochrome color
    """

    colors = {
              "DEFAULT": None,
              "BOLD": "bold",
              "UNDERLINE": "underline",
              "STANDOUT": "standout",
              }

    ctype = "monochrome"

#++++++++++++++++++++++++++++++++++++++++++++++++

class Palette(object):
    """
    Wrapper for palette
    """

    def __init__(self, name, fg, bg, ma=None):
        self.name = name
        self.fg = fg
        self.bg = bg
        self.ma = ma

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_palette(self):
        """
        Return urwid-compatible palette tuple
        """

        return (self.name, self.fg.color, self.bg.color, self.ma.color)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def copy(self):
        """
        Return copy of Palette object
        """

        return copy.deepcopy(self)
