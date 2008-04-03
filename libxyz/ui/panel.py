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
        #self.block1 = self._init_panel3()
        #self.block2 = self._init_panel3()
        self.block1 = Block(self._attr)
        self.block2 = Block(self._attr)

        #columns = lowui.Columns([self.block1, self.block2], 0)
        columns = lowui.Columns([self.block1.block, self.block2.block], 0)
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

#++++++++++++++++++++++++++++++++++++++++++++++++

class Block(object):
    """
    Single block
    """

    def __init__(self, attr_func):
        """
        @param res: Dictionary of defined resources
        """

        self.attr = attr_func

        self._xx0 = lowui.Text(" ..")
        self._xx1 = lowui.Text(" kernel")
        self._xx2 = lowui.AttrWrap(lowui.Text(" file2"), self.attr(u"cursor"))
        self._xx3 = lowui.Text(" file3")
        self._xx4 = lowui.Text(" file4")
        self._xx5 = lowui.Text(" file5")
        self._xx6 = lowui.Text(" file6")
        self._core = lowui.AttrWrap(lowui.Text(" xyzcmd.core"), self.attr(u"core"))

        self.title = lowui.Text((self.attr(u"cwdtitle"), u" ~ "), align.CENTER)

        self.info = lowui.Text(u"-rwx-rx-rx (1.5M) file2 ")
        self.info = lowui.Padding(self.info, align.LEFT, 38)
        self.info = lowui.AttrWrap(self.info, self.attr(u"info"))

        self.block_mount = lowui.Filler(lowui.Text(u""))
        self.block_mount = lowui.AttrWrap(self.block_mount, self.attr(u"mount"))

        self.block_cont = lowui.ListBox([self._xx0, self._xx1, self._xx4,
                                         self._xx3, self._core, self._xx2,
                                         self._xx5, self._xx6])

        self.block = lowui.AttrWrap(self.block_cont, self.attr(u"panel"))
        self.block = lowui.Frame(self.block, self.title, self.info)
        self.block = lowui.AttrWrap(self.block, self.attr(u"mount"))
        self.block = lowui.Overlay(self.block, self.block_mount,
                                   align.CENTER, 38, align.MIDDLE, 22)
        self.block = lowui.BoxAdapter(self.block, 22)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_block(self):
        return self.block
