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
from libxyz.ui import align

class Panel(lowui.WidgetWrap):
    """
    Panel is used to display filesystem hierarchy
    """

    resolution = (u"panel", u"widget")

    def __init__(self, xyz):
        self.xyz = xyz

        self._blank = lowui.Text("")
        self._xx0 = lowui.Text(" ..")
        self._xx1 = lowui.Text(" kernel")
        self._xx2 = lowui.AttrWrap(lowui.Text(" file2"), self._attr(u"cursor"))
        self._xx3 = lowui.Text(" file3")
        self._xx4 = lowui.Text(" file4")
        self._xx5 = lowui.Text(" file5")
        self._xx6 = lowui.Text(" file6")
        self._core = lowui.AttrWrap(lowui.Text(" xyzcmd.core"), self._attr(u"core"))

        _title1 = lowui.Text((self._attr(u"cwdtitle"), u" /var/lib/tmp/bin "), align.CENTER)
        _block1_mount = lowui.AttrWrap(lowui.Filler(_title1, align.TOP),
                                self._attr(u"mount"))
        self._block1 = lowui.AttrWrap(lowui.ListBox([self._xx0, self._xx1, self._xx4, self._xx3, self._core, self._xx2, self._xx5, self._xx6]), self._attr(u"panel"))
        self._block1 = lowui.BoxAdapter(lowui.Overlay(self._block1, _block1_mount, align.CENTER, 38, align.MIDDLE, 20), 22)


        _title2 = lowui.Text((self._attr(u"cwdtitle"), u" /boot/kernel "), align.CENTER)
        _block2_mount = lowui.AttrWrap(lowui.Filler(_title2, align.TOP),
                                self._attr(u"mount"))
        self._block2 = lowui.AttrWrap(lowui.ListBox([self._blank]), self._attr(u"panel"))
        self._block2 = lowui.BoxAdapter(lowui.Overlay(self._block2, _block2_mount, align.CENTER, 38, align.MIDDLE, 20), 22)

        columns = lowui.Columns([self._block1, self._block2], 0)
        self._widget = lowui.Pile([self._blank, columns, self._blank])

        super(Panel, self).__init__(self._widget)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _attr(self, name):
        """
        Find palette
        """

        return self.xyz.skin.attr(self.resolution, name)
