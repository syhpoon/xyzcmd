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
    ctype = u"base"

    def __init__(self, color):
        if color not in self.colors:
            raise XYZValueError(_(u"Invalid %s color: %s" % \
            (self.ctype, str(color))))

        self.color = self.colors[color]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return u"<%s color: %s>" % (self.ctype, str(self.color))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

#++++++++++++++++++++++++++++++++++++++++++++++++

class Foreground(Color):
    """
    Foreground color
    """

    colors = {
              u"BLACK": u"black",
              u"BROWN": u"brown",
              u"YELLOW": u"yellow",
              u"WHITE": u"white",
              u"DEFAULT": u"default",

              u"DARK_BLUE": u"dark blue",
              u"DARK_MAGENTA": u"dark magenta",
              u"DARK_CYAN": u"dark cyan",
              u"DARK_RED": u"dark red",
              u"DARK_GREEN": u"dark green",
              u"DARK_GRAY": u"dark gray",

              u"LIGHT_GRAY": u"light gray",
              u"LIGHT_RED": u"light red",
              u"LIGHT_GREEN": u"light green",
              u"LIGHT_BLUE": u"light blue",
              u"LIGHT_MAGENTA": u"light magenta",
              u"LIGHT_CYAN": u"light cyan",
              }

    ctype = u"foreground"

#++++++++++++++++++++++++++++++++++++++++++++++++

class Background(Color):
    """
    Background color
    """

    colors = {
              u"BLACK": u"black",
              u"BROWN": u"brown",
              u"DEFAULT": u"default",

              u"DARK_RED": u"dark red",
              u"DARK_GREEN": u"dark green",
              u"DARK_BLUE": u"dark blue",
              u"DARK_MAGENTA": u"dark magenta",
              u"DARK_CYAN": u"dark cyan",

              u"LIGHT_GRAY": u"light gray",
              }

    ctype = u"background"

#++++++++++++++++++++++++++++++++++++++++++++++++

class Monochrome(Color):
    """
    Monochrome color
    """

    colors = {
              u"DEFAULT": None,
              u"BOLD": u"bold",
              u"UNDERLINE": u"underline",
              u"STANDOUT": u"standout",
              }

    ctype = u"monochrome"

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

        if self.ma is None:
            _ma = None
        elif isinstance(self.ma, tuple):
            _ma = tuple([x.color for x in self.ma])
        else: # Color object
            _ma = self.ma.color

        return (self.name, self.fg.color, self.bg.color, _ma)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def copy(self):
        """
        Return copy of Palette object
        """

        return copy.deepcopy(self)
