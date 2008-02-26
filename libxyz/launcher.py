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

        self.ui = uilib.display.init_display()
        self.ui.register_palette([('bg', 'white', 'dark red')])

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def run(self):
        """
        Run commander
        """

        #self.parse_args()
        #self.parse_configs()
        self.ui.run_wrapper(self.__run)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __run(self):
        _dim = self.ui.get_cols_rows()
        self._top = uilib.lowui.Filler(uilib.lowui.Text(""))

        _msg = uilib.MessageBox(self.ui, self._top, "XYZCommander", "KAGDILA?")
        self.ui.draw_screen(_dim, _msg.render(_dim, True))

        while not self.ui.get_input():
            pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

