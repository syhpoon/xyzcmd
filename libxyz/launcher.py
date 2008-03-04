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

class Launcher(object):
    """
    Startup class
    """

    def __init__(self):
        """
        Initialization
        """

        self.screen = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def run(self):
        """
        Run commander
        """

        #self.parse_args()
        self.parse_configs()

        self.screen.run_wrapper(self.__run)

        self.screen = uilib.display.init_display()
        self.screen.register_palette([('box', 'white', 'dark red'),
                                      ('mount', 'yellow', 'dark green'),
                                      ('title', 'yellow', 'dark blue')])

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __run(self):
        _dim = self.screen.get_cols_rows()
        self._top = uilib.lowui.Filler(uilib.lowui.Text(""))

        _str = """XYZCommander"""
        _title = "KAGDILA?"

        _msg = uilib.MessageBox(self.screen, self._top, _str, _title)
        self.screen.draw_screen(_dim, _msg.render(_dim, True))

        while not self.screen.get_input():
            pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse_configs(self):
        """
        Parse configuration
        """

        # ... parsing configs

        self.skin_mgr = ???
