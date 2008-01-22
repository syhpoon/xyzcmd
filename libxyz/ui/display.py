#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

import urwid.raw_display
import urwid

def init_display():
    """
    Create main ui object
    """

    return urwid.raw_display.Screen()
