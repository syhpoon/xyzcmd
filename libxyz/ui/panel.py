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

        self._block1 = self._init_panel3()
        self._block2 = self._init_panel3()

        columns = lowui.Columns([self._block1, self._block2], 0)
        _status = lowui.Text("Status bar")
        _cmd = lowui.Text("# uname -a")
        self._widget = lowui.Pile([columns, _status, _cmd])

        super(Panel, self).__init__(self._widget)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _attr(self, name):
        """
        Find palette
        """

        return self.xyz.skin.attr(self.resolution, name)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _init_panel(self):
        _title = lowui.Text((self._attr(u"cwdtitle"), u" ~ "), align.CENTER)
        _title = lowui.Filler(_title, align.TOP)
        _info = lowui.Text((self._attr(u"cwdtitle"), u" -rwx-r-x-r-x "),
                           align.LEFT)
        _info = lowui.Filler(_info)

        _block_mount = lowui.AttrWrap(_title, self._attr(u"mount"))

        _block_cont = lowui.ListBox([self._xx0, self._xx1, self._xx4,
                                     self._xx3, self._core, self._xx2,
                                     self._xx5, self._xx6])
        _block = lowui.AttrWrap(_block_cont, self._attr(u"panel"))

        _block = lowui.Overlay(_block, _block_mount, align.CENTER, 38,
                               align.MIDDLE, 20)
        _block = lowui.BoxAdapter(_block, 22)

        return _block

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _init_panel3(self):
        _title = lowui.Text((self._attr(u"cwdtitle"), u" ~ "), align.CENTER)
        _info = lowui.Text((self._attr(u"cwdtitle"), u" -rwx-r-x-r-x "),
                           align.LEFT)

        _block_mount = lowui.AttrWrap(lowui.Filler(lowui.Text(u"")), self._attr(u"mount"))

        _block_cont = lowui.ListBox([self._xx0, self._xx1, self._xx4,
                                     self._xx3, self._core, self._xx2,
                                     self._xx5, self._xx6])
        _block = lowui.AttrWrap(_block_cont, self._attr(u"panel"))

        #_block = lowui.Overlay(_block, _block_mount, align.CENTER, 38,
        #                       align.MIDDLE, 20)
        #_block = lowui.BoxAdapter(_block, 22)

        _block = lowui.AttrWrap(lowui.Frame(_block, _title, _info), self._attr(u"mount"))
        _block = lowui.Overlay(_block, _block_mount, align.CENTER, 38,
                               align.MIDDLE, 22)
        _block = lowui.BoxAdapter(_block, 22)

        return _block
