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

from libxyz.ui import lowui

class Panel(lowui.WidgetWrap):
    """
    Panel is used to display filesystem hierarchy
    """

    resolution = (u"box", u"widget")
    #resolution = (u"panel", u"widget")

    def __init__(self, xyz):
        self.xyz = xyz

        self._blank = lowui.Text("")
        self._block = lowui.AttrWrap(lowui.BoxAdapter(lowui.ListBox([self._blank]), 15), self._attr(u"box"))

        self._block.box_widget.body = lowui.Button("AAA")
        self._widget = lowui.Pile([self._blank, self._block, self._blank])

        super(Panel, self).__init__(self._widget)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _attr(self, name):
        """
        Find palette
        """

        return self.xyz.skin.attr(self.resolution, name)
