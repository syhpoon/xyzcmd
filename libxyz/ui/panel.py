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

import libxyz.ui

from libxyz.ui import lowui
from libxyz.ui import align
from libxyz.vfs.local import LocalVFSObject

class Panel(lowui.WidgetWrap):
    """
    Panel is used to display filesystem hierarchy
    """

    resolution = (u"panel", u"widget")

    def __init__(self, xyz):
        self.xyz = xyz

        self._blank = lowui.Text("")
        _blocksize = libxyz.ui.Size(rows=22, cols=38)
        self.block1 = Block(_blocksize, LocalVFSObject("/tmp"), self._attr)
        self.block2 = Block(_blocksize, LocalVFSObject("/"), self._attr)

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

    def __init__(self, size, vfsobj, attr_func):
        """
        @param size: Block widget size
        @type size: L{libxyz.ui.Size}
        @param vfsobj:
        @param attr_func:
        """

        self.size = size
        self.attr = attr_func

        _dir, _dirs, _files = vfsobj.walk()

        _entries = [lowui.Text(u"..")]
        _entries.extend([lowui.Text(u"%s%s "% (x.visual, x.name))
                         for x in _dirs])
        _entries.extend([lowui.Text(u"%s%s " % (x.visual, x.name))
                         for x in _files])

        self.info = lowui.Text(u"-rwx-rx-rx (1.5M) file2 ")
        self.info = lowui.Padding(self.info, align.LEFT, self.size.cols)
        self.info = lowui.AttrWrap(self.info, self.attr(u"info"))

        self.block_cont = lowui.ListBox(_entries)

        self.block = lowui.Frame(self.block_cont, footer=self.info)
        self.block = libxyz.ui.Border(self.block,
                                      (_dir, self.attr(u"cwdtitle")),
                                      self.attr(u"border"))
        self.block = lowui.AttrWrap(self.block, self.attr(u"panel"))

        self.block = lowui.BoxAdapter(self.block, self.size.rows)
