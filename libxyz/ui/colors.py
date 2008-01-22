#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#


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

    default = None
    BOLD = 'bold'
    UNDERLINE = 'underline'
    STANDOUT = 'standout'
