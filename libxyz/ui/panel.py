#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <syhpoon@syhpoon.name> 2008
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
import libxyz.core
import libxyz.const

from libxyz.ui import lowui
from libxyz.ui import align
from libxyz.ui import Separator
from libxyz.ui.utils import refresh
from libxyz.vfs.local import LocalVFSObject

class Panel(lowui.WidgetWrap):
    """
    Panel is used to display filesystem hierarchy
    """

    resolution = (u"panel", u"widget")
    context = u":sys:panel"

    def __init__(self, xyz):
        self.xyz = xyz
        self._attr = lambda x: self.xyz.skin.attr(self.resolution, x)

        _size = self.xyz.screen.get_cols_rows()
        _blocksize = libxyz.ui.Size(rows=_size[1] - 1, cols=_size[0] / 2 - 2)
        _enc = xyz.conf[u"xyz"][u"local_encoding"]

        self.block1 = Block(_blocksize, LocalVFSObject("/tmp"), self._attr,
                            _enc, active=True)
        self.block2 = Block(_blocksize, LocalVFSObject("/home/syhpoon"),
                            self._attr, _enc)

        columns = lowui.Columns([self.block1.block, self.block2.block], 0)

        self._cmd = libxyz.ui.Cmd(xyz)
        self._widget = lowui.Pile([columns, self._cmd])
        self._stop = False

        self._set_plugins()

        super(Panel, self).__init__(self._widget)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _get_active(self):
        if self.block1.active:
            return self.block1
        else:
            return self.block2

    active = property(_get_active)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def loop(self):
        """
        Start working loop
        """

        _dim = self.xyz.screen.get_cols_rows()

        while True:
            if self._stop:
                break

            self.xyz.screen.draw_screen(_dim, self.xyz.top.render(_dim, True))

            _input = self.xyz.input.get()

            if _input:
                _meth = self.xyz.km.process(_input, self.context)

                # No binds for PANEL context
                if _meth is None:
                    self._cmd.keypress(_dim, _input)
                else:
                    _meth()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _set_plugins(self):
        """
        Set virtual plugins
        """

        # :sys:run
        _run_plugin = libxyz.core.plugins.VirtualPlugin(self.xyz, u"run")
        _run_plugin.export(self.shutdown)

        _run_plugin.VERSION = u"0.1"
        _run_plugin.AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
        _run_plugin.BRIEF_DESCRIPTION = u"Run plugin"

        # :sys:panel
        _panel_plugin = libxyz.core.plugins.VirtualPlugin(self.xyz, u"panel")
        _panel_plugin.export(self.entry_next)
        _panel_plugin.export(self.entry_prev)
        _panel_plugin.export(self.entry_top)
        _panel_plugin.export(self.entry_bottom)
        _panel_plugin.export(self.switch_active)

        _panel_plugin.VERSION = u"0.1"
        _panel_plugin.AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
        _panel_plugin.BRIEF_DESCRIPTION = u"Panel plugin"

        self.xyz.pm.register(_run_plugin)
        self.xyz.pm.register(_panel_plugin)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def shutdown(self):
        """
        Quit program
        """

        _q = _(u"Really quit %s?" % libxyz.const.PROG)
        _title = libxyz.const.PROG

        if libxyz.ui.YesNoBox(self.xyz, self.xyz.top, _q, _title).show():
            self._stop = True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def entry_next(self):
        """
        Next entry
        """

        return self.active.next()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def entry_prev(self):
        """
        Previous entry
        """

        return self.active.prev()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def entry_top(self):
        """
        Top entry
        """

        return self.active.top()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def entry_bottom(self):
        """
        Bottom entry
        """

        return self.active.bottom()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def switch_active(self):
        """
        Switch active block
        """

        if self.block1.active:
            self.block1.deactivate()
            self.block2.activate()
        else:
            self.block2.deactivate()
            self.block1.activate()

#++++++++++++++++++++++++++++++++++++++++++++++++

class Block(lowui.BoxWidget):
    """
    Single block
    """

    def __init__(self, size, vfsobj, attr_func, enc, active=False):
        """
        @param size: Block widget size
        @type size: L{libxyz.ui.Size}
        @param vfsobj:
        @param attr_func: Skin attribute access function
        @param enc: Local encoding
        @param active: Boolean flag, True if block is active
        """

        self.size = size
        self.attr = attr_func

        self.active = active
        self.selected = 0

        self._enc = enc

        _dir, _dirs, _files = vfsobj.walk()

        _entries = []

        _entries.extend(_dirs)
        _entries.extend(_files)

        self.entries = _entries

        self._len = len(self.entries)

        self._winfo = lowui.Text(u"")
        self._sep = Separator()

        _info = lowui.Padding(self._winfo, align.LEFT, self.size.cols)
        _info = lowui.AttrWrap(_info, self.attr(u"info"))
        _info = lowui.Pile([self._sep, _info])

        self.block = lowui.Frame(self, footer=_info)

        _title_attr = self._get_title_attr()

        self.border = libxyz.ui.Border(self.block, (_dir, _title_attr),
                                      self.attr(u"border"))
        self.block = lowui.AttrWrap(self.border, self.attr(u"panel"))

        self.block = lowui.BoxAdapter(self.block, self.size.rows)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def selectable(self):
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def render(self, (maxcol, maxrow), focus=False):
        """
        Render block
        """

        self._set_info(self.entries[self.selected], maxcol)

        if self.selected >= maxrow:
            _from = self.selected - maxrow + 1
        else:
            _from = 0

        # We have less entries then maxrow
        if self._len <= maxrow:
            _to = self._len
        else:
            _to = maxrow + _from

        _len = self._len - _from

        canvases = []

        for i in range(_from, len(self.entries)):
            _obj = self.entries[i]
            _text = u"%s%s "% (_obj.visual, _obj.name.decode(self._enc))
            _text = self._truncate(_text, maxcol)

            if self.active and i == self.selected:
                x = lowui.TextCanvas(text=[_text.encode(self._enc)],
                                     attr=[[(self.attr(u"cursor"), maxcol)]],
                                     maxcol=maxcol)
                canvases.append((x, i, False))
            else:
                canvases.append((lowui.Text(_text).render((maxcol,)),i,False))

        combined = lowui.CanvasCombine(canvases)

        if _len < maxrow:
            combined.pad_trim_top_bottom(0, maxrow - _len)
        elif _len > maxrow:
            combined.trim_end(_len - maxrow)

        return combined

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _truncate(self, text, cols):
        """
        Truncate text if its length exceeds cols
        """

        _len = len(text)

        if _len < cols:
            return text
        else:
            return "%s~" % text[:cols - 1]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _get_title_attr(self):
        """
        Return title attr
        """

        if self.active:
            return self.attr(u"cwdtitle")
        else:
            return self.attr(u"cwdtitleinact")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _set_info(self, vfsobj, cols):
        """
        Set info text
        """

        _part2 = u"%s %s" % (vfsobj.size, vfsobj.mode)
        _part1 = u"%s%s" % (vfsobj.visual, vfsobj.name.decode(self._enc))
        _part1 = self._truncate(_part1, cols - len(_part2) - 2)

        _text = u"%s%s%s" % (_part1, u" " * (cols - (len(_part1) +
                             len(_part2)) - 1), _part2)

        self._winfo.set_text(_text.encode(self._enc))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def deactivate(self):
        """
        Deactivate block
        """

        self.active = False
        self.border.set_title_attr(self._get_title_attr())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def activate(self):
        """
        Activate block
        """

        self.active = True
        self.border.set_title_attr(self._get_title_attr())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def next(self):
        """
        Next entry
        """

        if self.selected < len(self.entries) - 1:
            self.selected += 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def prev(self):
        """
        Previous entry
        """

        if self.selected > 0:
            self.selected -= 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def top(self):
        """
        Top entry
        """

        self.selected = 0

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def bottom(self):
        """
        Bottom entry
        """

        self.selected = len(self.entries) - 1
