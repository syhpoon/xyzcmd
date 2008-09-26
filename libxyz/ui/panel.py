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

import re
import os

import libxyz.ui
import libxyz.core
import libxyz.const

from libxyz.ui import lowui
from libxyz.ui import align
from libxyz.ui.utils import refresh
from libxyz.vfs.local import LocalVFSObject
from libxyz.vfs.types import *

class Panel(lowui.WidgetWrap):
    """
    Panel is used to display filesystem hierarchy
    """

    resolution = (u"panel", u"widget")
    context = u":sys:panel"

    def __init__(self, xyz):
        self.xyz = xyz

        _size = self.xyz.screen.get_cols_rows()
        _blocksize = libxyz.ui.Size(rows=_size[1] - 1, cols=_size[0] / 2 - 2)
        _enc = xyz.conf[u"xyz"][u"local_encoding"]

        self.block1 = Block(xyz, _blocksize,
                            LocalVFSObject("/tmp", _enc), _enc, active=True)

        self.block2 = Block(xyz, _blocksize,
                            LocalVFSObject("/home/syhpoon", _enc), _enc)

        self._stop = False
        columns = lowui.Columns([self.block1.block, self.block2.block], 0)

        self._cmd = libxyz.ui.Cmd(xyz)
        self._widget = lowui.Pile([columns, self._cmd])

        self._set_plugins()

        super(Panel, self).__init__(self._widget)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def render(self, (maxcol,), focus=False):
        """
        Render panel
        """

        columns = lowui.Columns([self.block1.block, self.block2.block], 0)

        self._widget = lowui.Pile([columns, self._cmd])

        return self._widget.render((maxcol,))

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
        _panel_plugin.export(self.block_next)
        _panel_plugin.export(self.block_prev)
        _panel_plugin.export(self.switch_active)
        _panel_plugin.export(self.get_selected)
        _panel_plugin.export(self.get_tagged)
        _panel_plugin.export(self.toggle_tag)
        _panel_plugin.export(self.tag_all)
        _panel_plugin.export(self.untag_all)
        _panel_plugin.export(self.tag_invert)
        _panel_plugin.export(self.tag_re)
        _panel_plugin.export(self.untag_re)
        _panel_plugin.export(self.swap_blocks)

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

        _q = _(u"Really quit %s?") % libxyz.const.PROG
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

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def block_next(self):
        """
        Next block
        """

        return self.active.block_next()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def block_prev(self):
        """
        Previous block
        """

        return self.active.block_prev()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_selected(self):
        """
        Get selected VFSFile instance
        """

        return self.active.get_selected()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_tagged(self):
        """
        Return list of tagged VFSFile instances
        """

        return self.active.get_tagged()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def toggle_tag(self):
        """
        Tag selected file
        """

        return self.active.toggle_tag()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def tag_all(self):
        """
        Tag every single object in current dir
        """

        return self.active.tag_all()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def untag_all(self):
        """
        Untag every single object in current dir
        """

        return self.active.untag_all()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def tag_invert(self):
        """
        Invert currently tagged files
        """

        return self.active.tag_invert()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def tag_re(self):
        """
        Tag files by regexp
        """

        return self.active.tag_re()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def untag_re(self):
        """
        Untag files by regexp
        """

        return self.active.untag_re()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def swap_blocks(self):
        """
        Swap panel blocks
        """

        xyzlog.log("CHANGED", xyzlog.loglevel.ERROR)
        self.block1, self.block2 = self.block2, self.block1

        self._invalidate()

#++++++++++++++++++++++++++++++++++++++++++++++++

class Block(lowui.BoxWidget):
    """
    Single panel block
    """

    def __init__(self, xyz, size, vfsobj, enc, active=False):
        """
        @param xyz: XYZData instance
        @param size: Block widget size
        @type size: L{libxyz.ui.Size}
        @param vfsobj:
        @param enc: Local encoding
        @param active: Boolean flag, True if block is active

        Required resources: cwdtitle, cwdtitleinact, panel, cursor, info
                            border, tagged
        """

        self.xyz = xyz
        self.size = size
        self.attr = lambda x: self.xyz.skin.attr(Panel.resolution, x)

        self.active = active
        self.selected = 0

        self._display = []
        self._vindex = 0
        self._from = 0
        self._to = 0

        self._tagged = []

        self._enc = enc

        _dir, _dirs, _files = vfsobj.walk()

        _entries = [_dir]
        _entries.extend(_dirs)
        _entries.extend(_files)

        self.entries = _entries
        self._len = len(self.entries)

        self._palettes = self._process_skin_rulesets()

        self._winfo = lowui.Text(u"")
        self._sep = libxyz.ui.Separator()
        self._pending = libxyz.core.Queue(20)

        _info = lowui.Padding(self._winfo, align.LEFT, self.size.cols)
        _info = lowui.AttrWrap(_info, self.attr(u"info"))
        _info = lowui.Pile([self._sep, _info])

        self.block = lowui.Frame(self, footer=_info)

        _title_attr = self._get_title_attr()

        self.border = libxyz.ui.Border(self.block, (_dir.path, _title_attr),
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

        # Search for pending action
        while True:
            try:
                _act = self._pending.pop()
            except IndexError:
                break
            else:
                _act(maxcol, maxrow)

        self._set_info(self.entries[self.selected], maxcol)

        _tlen = len(self._tagged)

        if _tlen > 0:
            _text = _(u"%s bytes (%d)") % (
                    self._make_number_readable(
                        reduce(lambda x, y: x + y,
                           [self.entries[x].size for x in self._tagged
                            if isinstance(self.entries[x].ftype, VFSTypeFile)
                           ], 0)), _tlen)

            self._sep.set_text(_text.encode(self._enc), self.attr(u"tagged"))
        else:
            self._sep.clear_text()

        self._display = self._get_visible(maxrow, maxcol)
        _len = len(self._display)

        canvases = []

        for i in xrange(0, _len):
            _text = self._display[i]
            _own_attr = None
            _abs_i = self._from + i

            if self.active and i == self._vindex:
                _own_attr = self.attr(u"cursor")
            elif _abs_i in self._tagged:
                _own_attr = self.attr(u"tagged")
            elif _abs_i in self._palettes:
                _own_attr = self._palettes[_abs_i]

            if _own_attr is not None:
                x = lowui.TextCanvas(text=[_text.encode(self._enc)],
                                     attr=[[(_own_attr, maxcol)]],
                                     maxcol=maxcol)
                canvases.append((x, i, False))
            else:
                canvases.append((lowui.Text(_text).render((maxcol,)), i, False))

        combined = lowui.CanvasCombine(canvases)

        if _len < maxrow:
            combined.pad_trim_top_bottom(0, maxrow - _len)
        elif _len > maxrow:
            combined.trim_end(_len - maxrow)

        return combined

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _make_number_readable(self, num):
        _res = []

        i = 0
        _sep = False

        for x in reversed(unicode(num)):
            if _sep:
                _res.append(u"_")
                _sep = False

            _res.append(x)

            if i > 0 and (i + 1) % 3 == 0:
                _sep = True

            i += 1

        _res.reverse()

        return u"".join(_res)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _get_visible(self, rows, cols):
        """
        Get currently visible piece of entries
        """

        _len = self._len
        _from, _to, self._vindex = self._update_vindex(rows)

        if (_from, _to) != (self._from, self._to):
            self._from, self._to = _from, _to
            self._display = []

            for _obj in self.entries[self._from:self._to]:
                _text = u"%s%s "% (_obj.vtype, _obj.name)
                _text = self._truncate(_text, cols)
                self._display.append(_text)

        return self._display

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_skin_rulesets(self):
        """
        Process defined fs.* rulesets
        """

        _result = {}

        try:
            _rules = self.xyz.skin["fs.rules"]
        except KeyError:
            return _result

        for i in xrange(self._len):
            for _exp, _attr in _rules.iteritems():
                if _exp.match(self.entries[i]):
                    _result[i] = _attr.name
                    break

        return _result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _truncate(self, text, cols):
        """
        Truncate text if its length exceeds cols
        """

        _len = len(text)

        if _len < cols:
            return text
        else:
            return u"%s~" % text[:cols - 1]

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

        _part2 = vfsobj.info
        _part1 = self._truncate(vfsobj.visual, cols - len(_part2) - 2)

        _text = u"%s%s%s" % (_part1, u" " * (cols - (len(_part1) +
                             len(_part2)) - 1), _part2)

        self._winfo.set_text(_text.encode(self._enc))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _update_vindex(self, rows):
        """
        Calculate vindex according to selected position
        """

        pos = self.selected

        _from = pos / rows * rows
        _to = _from + rows
        _vindex = pos - (rows * (pos / rows))

        return (_from, _to, _vindex)

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

        if self.selected < self._len - 1:
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

        self.selected = self._len - 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def block_next(self):
        """
        One block down
        """

        def _do_next_block(cols, rows):
            if self.selected + rows >= self._len:
                return self.bottom()
            else:
                self.selected += rows

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # As we aren't aware of how many rows are in a single
        # block at this moment, postpone jumping until render is called

        self._pending.push(_do_next_block)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def block_prev(self):
        """
        One block up
        """

        def _do_prev_block(cols, rows):
            if self.selected - rows < 0:
                return self.top()
            else:
                self.selected -= rows

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self._pending.push(_do_prev_block)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_selected(self):
        """
        Get selected VFSFile instance
        """

        return self.entries[self.selected]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_tagged(self):
        """
        Return list of tagged VFSFile instances
        """

        return [self.entries[x] for x in self._tagged]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def toggle_tag(self):
        """
        Toggle tagged selected file
        """

        if self.selected in self._tagged:
            self._tagged.remove(self.selected)
        else:
            self._tagged.append(self.selected)

        self.next()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def tag_re(self):
        """
        Tag files by regexp
        """

        _input = libxyz.ui.InputBox(self.xyz, self.xyz.top, "",
                                    title=_(u"Tag group"), text=r".*")
        
        _raw = _input.show()

        if _raw is None:
            return
        else:
            _re = re.compile(_raw, re.U)

        self._tagged = [i for i in xrange(self._len) if
                        _re.search(self.entries[i].name.encode(self._enc))]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def untag_re(self):
        """
        Untag files by regexp
        """
        
        _input = libxyz.ui.InputBox(self.xyz, self.xyz.top, "",
                                    title=_(u"Untag group"), text=r".*")
        
        _raw = _input.show()

        if _raw is None:
            return
        else:
            _re = re.compile(_raw, re.U)

        self._tagged = [i for i in self._tagged if not
                        _re.search(self.entries[i].name.encode(self._enc))]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def tag_invert(self):
        """
        Invert currently tagged files
        """

        self._tagged = [i for i in xrange(self._len)
                        if i not in self._tagged]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def tag_all(self):
        """
        Tag every single object in current dir
        """

        self._tagged = [i for i in xrange(self._len)]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def untag_all(self):
        """
        Untag every single object in current dir
        """

        self._tagged = []
