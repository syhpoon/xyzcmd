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


"""
Define colors as constants
"""

class Foreground(object):
    """
    Foreground colors
    """

    BLACK = 'black'
    BROWN = 'brown'
    YELLOW = 'yellow'
    WHITE = 'white'
    DEFAULT = 'default'

    DARK_BLUE = 'dark blue'
    DARK_MAGENTA = 'dark magenta'
    DARK_CYAN = 'dark cyan'
    DARK_RED = 'dark red'
    DARK_GREEN = 'dark green',
    DARK_GRAY = 'dark gray'

    LIGHT_GRAY = 'light gray'
    LIGHT_RED = 'light red'
    LIGHT_GREEN = 'light green'
    LIGHT_BLUE = 'light blue'
    LIGHT_MAGENTA = 'light magenta'
    LIGHT_CYAN = 'light cyan'

#++++++++++++++++++++++++++++++++++++++++++++++++

class Background(object):
    """
    Background colors
    """

    BLACK = 'black'
    BROWN = 'brown'
    DEFAULT = 'default'

    DARK_RED = 'dark red',
    DARK_GREEN = 'dark green'
    DARK_BLUE = 'dark blue'
    DARK_MAGENTA = 'dark magenta'
    DARK_CYAN = 'dark cyan'

    LIGHT_CYAN = 'light gray'

#++++++++++++++++++++++++++++++++++++++++++++++++

class Monochrome(object):
    """
    Monochrome colors
    """

    DEFAULT = None
    BOLD = 'bold'
    UNDERLINE = 'underline'
    STANDOUT = 'standout'

#++++++++++++++++++++++++++++++++++++++++++++++++

class Palette(object):
    """
    Wrapper for palette
    """

    def __init__(self, fg, bg, ma=None):
        pass
