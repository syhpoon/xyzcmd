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

import libxyz.ui as uilib

from libxyz.core import Skin
from libxyz.core import XYZData

class Launcher(object):
    """
    Startup class
    """

    def __init__(self):
        """
        Initialization
        """

        import gettext
        gettext.install("xyzcmd")

        self.xyz = XYZData(
                            {
                            "screen": None,
                            "skin": None,
                            }
                          )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def run(self):
        """
        Run commander
        """

        #self.parse_args()
        self.parse_configs()

        self.xyz.screen = uilib.display.init_display()
        self.xyz.screen.register_palette(self.xyz.skin.get_palette_list())
        self.xyz.screen.run_wrapper(self._run)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _run(self):
        _dim = self.xyz.screen.get_cols_rows()
        self._top = uilib.lowui.Filler(uilib.lowui.Text(""))

        _str = "Welcome!\nAAAA\nBBBB\nCCCC"
        _title = "XYZCommander"

        _msg = uilib.YesNoBox(self.xyz, self._top, _str, _title)
        self.xyz.screen.draw_screen(_dim, _msg.render(_dim, True))

        while not self.xyz.screen.get_input():
            pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse_configs(self):
        """
        Parse configuration
        """

        # TODO: ... parsing configs

        self.xyz.skin = Skin("/tmp/skins/default")
