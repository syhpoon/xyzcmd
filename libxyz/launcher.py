#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

"""
Launcher - all neccessary initialization
"""

import libxyz.ui.display as display
from libxyz.ui import uilib

class Launcher(object):
    """
    Startup class
    """

    def __init__(self):
        """
        Initialization
        """

        self.ui = display.init_display()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def run(self):
        """
        Run commander
        """

        self.ui.run_wrapper(self.__run)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __run(self):
        canvas = uilib.TextCanvas(["XYZ Commander"])
        self.ui.draw_screen((20, 1), canvas)

        while not self.ui.get_input():
            pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

