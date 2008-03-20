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
Launcher - all neccessary initialization
"""

import gettext

import libxyz.ui as uilib

from libxyz.core import Skin
from libxyz.core import XYZData
from libxyz.core.plugins import PluginManager

class Launcher(object):
    """
    Startup class
    """

    def __init__(self):
        """
        Initialization
        """

        gettext.install(u"xyzcmd")

        self.xyz = XYZData(
                            {
                            u"screen": None,
                            u"skin": None,
                            u"pm": None,
                            }
                          )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def run(self):
        """
        Run commander
        """

        self.parse_args()
        self.parse_configs()
        # TODO: real plugins path from config
        self.xyz.pm = PluginManager(self.xyz, ['/tmp/plugins',])

        self.xyz.screen = uilib.display.init_display()
        self.xyz.screen.register_palette(self.xyz.skin.get_palette_list())
        self.xyz.screen.run_wrapper(self._run)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _run(self):
        _dim = self.xyz.screen.get_cols_rows()
        self._top = uilib.lowui.Filler(uilib.lowui.Text(""))

        _str = u"Welcome!\nAAAA\nBBBB\nCCCC"
        _title = u"XYZCommander"

        #_msg = uilib.YesNoBox(self.xyz, self._top, _str, _title)
        #self.xyz.screen.draw_screen(_dim, _msg.render(_dim, True))

        #say_hello = self.xyz.pm.from_load(u":misc:hello", u"SayHello")
        hello = self.xyz.pm.load(u":misc:hello")
        hello.say_hello(self._top)

        while not self.xyz.screen.get_input():
            pass

        self.finalize()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse_args(self):
        """
        Parse command line arguments
        """

        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse_configs(self):
        """
        Parse configuration
        """

        # TODO: ... parsing configs

        # TODO: real skin path from configs
        self.xyz.skin = Skin(u"/tmp/skins/default")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def finalize(self):
        """
        Perform shutdown procedures
        """

        self.xyz.pm.shutdown()
