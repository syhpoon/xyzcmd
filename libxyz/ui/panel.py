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

import os
import sys
import traceback

import libxyz.ui
import libxyz.core
import libxyz.const
import libxyz.exceptions

from libxyz.core.utils import ustring, bstring, is_func
from libxyz.ui import lowui
from libxyz.ui import align
from libxyz.ui import Shortcut
from libxyz.ui import BlockEntries
from libxyz.ui.utils import refresh
from libxyz.ui.utils import truncate
from libxyz.vfs.types import VFSTypeFile
from libxyz.vfs.local import LocalVFSObject

class Panel(lowui.WidgetWrap):
    """
    Panel is used to display filesystem hierarchy
    """

    resolution = (u"panel", u"widget")
    context = u":sys:panel"

    EVENT_SHUTDOWN = u"event:shutdown"
    EVENT_BEFORE_SWITCH_TAB = u"event:sys:panel:before_switch_tab"
    EVENT_SWITCH_TAB = u"event:sys:panel:switch_tab"
    EVENT_NEW_TAB = u"event:sys:panel:new_tab"
    EVENT_DEL_TAB = u"event:sys:panel:del_tab"

    def __init__(self, xyz):
        self.xyz = xyz
        self.conf = self.xyz.conf[u"plugins"][u":sys:panel"]

        self._keys = libxyz.ui.Keys()

        _size = self.xyz.screen.get_cols_rows()
        _blocksize = libxyz.ui.Size(rows=_size[1] - 1, cols=_size[0] / 2 - 2)
        self._enc = xyzenc
        self._stop = False
        self._resize = False

        self._set_plugins()
        self._cmd = libxyz.ui.Cmd(xyz)
        _cwd = os.getcwd()

        self.filters = self._build_filters()
        self.xyz.hm.register("event:conf_update", self._update_conf_hook)

        self.block1 = Block(xyz, _blocksize, _cwd, self._enc, active=True)
        self.block2 = Block(xyz, _blocksize, _cwd, self._enc)
        self._compose()

        super(Panel, self).__init__(self._widget)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _update_conf_hook(self, var, val, sect):
        """
        Hook for update conf event
        """

        # Not ours
        if sect != "plugins" or var != ":sys:panel":
            return

        if "filters" in val or "filters_enabled" in val:
            self.filters = self._build_filters()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _compose(self):
        """
        Compose widgets
        """

        columns = lowui.Columns([self.block1, self.block2], 0)
        self._widget = lowui.Pile([columns, self._cmd])

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _build_filters(self):
        """
        Compile filters
        """

        filters = []

        # No need to compile
        if not self.conf[u"filters_enabled"]:
            return filters

        for f in self.conf[u"filters"]:
            try:
                rule = libxyz.core.FSRule(ustring(f))
            except libxyz.exceptions.ParseError, e:
                xyzlog.error(_(u"Error compiling filter: %s") % unicode(e))
                continue
            else:
                filters.append(rule)

        return filters

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @property
    def active(self):
        if self.block1.active:
            return self.block1
        else:
            return self.block2

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @property
    def inactive(self):
        if self.block1.active:
            return self.block2
        else:
            return self.block1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def loop(self):
        """
        Start working loop
        """

        _dim = self.xyz.screen.get_cols_rows()

        while True:
            if self._stop:
                break

            canv = self.xyz.top.render(_dim, True)
            self.xyz.screen.draw_screen(_dim, canv)

            _input = self.xyz.input.get()

            if _input:
                try:
                    self._cmd.keypress(_dim, _input)
                except Exception, e:
                    xyzlog.error(_(u"Error executing bind (%s): %s") %
                                 (Shortcut(_input), unicode(e)))
                    xyzlog.debug(ustring(traceback.format_exc(),
                                         self._enc))

                if self.xyz.input.resized:
                    self._resize = True

                if self._resize:
                    self._resize = False
                    _dim = self.xyz.screen.get_cols_rows()
                    _bsize = libxyz.ui.Size(rows=_dim[1] - 1,
                                            cols=_dim[0] / 2 - 2)

                    self.block1.size = _bsize
                    self.block2.size = _bsize
                    self._cmd._invalidate()
                    self.block1._invalidate()
                    self.block2._invalidate()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _set_plugins(self):
        """
        Set virtual plugins
        """

        # :sys:run
        _run_plugin = libxyz.core.plugins.VirtualPlugin(self.xyz, u"run")
        _run_plugin.export(self.shutdown)
        _run_plugin.export(self.repaint)

        _run_plugin.VERSION = u"0.1"
        _run_plugin.AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
        _run_plugin.BRIEF_DESCRIPTION = _(u"System runtime plugin")
        _run_plugin.HOMEPAGE = u"xyzcmd.syhpoon.name"

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
        _panel_plugin.export(self.get_untagged)
        _panel_plugin.export(self.get_current)
        _panel_plugin.export(self.get_all)
        _panel_plugin.export(self.get_active)
        _panel_plugin.export(self.toggle_tag)
        _panel_plugin.export(self.tag_all)
        _panel_plugin.export(self.untag_all)
        _panel_plugin.export(self.tag_invert)
        _panel_plugin.export(self.tag_rule)
        _panel_plugin.export(self.untag_rule)
        _panel_plugin.export(self.tag_diff)
        _panel_plugin.export(self.swap_blocks)
        _panel_plugin.export(self.reload)
        _panel_plugin.export(self.reload_all)
        _panel_plugin.export(self.action)
        _panel_plugin.export(self.chdir)
        _panel_plugin.export(self.search_forward)
        _panel_plugin.export(self.search_backward)
        _panel_plugin.export(self.search_cycle)
        _panel_plugin.export(self.show_tagged)
        _panel_plugin.export(self.select)
        _panel_plugin.export(self.cwd)
        _panel_plugin.export(self.vfs_driver)
        _panel_plugin.export(self.filter)
        _panel_plugin.export(self.sort)
        _panel_plugin.export(self.new_tab)
        _panel_plugin.export(self.del_tab)
        _panel_plugin.export(self.switch_tab)
        _panel_plugin.export(self.next_tab)
        _panel_plugin.export(self.prev_tab)
        _panel_plugin.export(self.get_tabs)
        _panel_plugin.export(self.active_tab)

        _panel_plugin.VERSION = u"0.1"
        _panel_plugin.AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
        _panel_plugin.BRIEF_DESCRIPTION = _(u"Panel plugin")
        _panel_plugin.HOMEPAGE = u"xyzcmd.syhpoon.name"
        _panel_plugin.DOC = _(u"""\
Configuration variables:
filters_enabled - Enable permanent filters. Default - False
filters_policy - Filters policy.
 If True - filter out objects matching the rule.
 If False - filter out objects which do not match the rule. Default - True
filters - List of permanent filters.
 Filters applied in defined order sequentially. Default - []
sorting_policy - Active sorting policy name or None. Default - None
sorting - Defined sorting policies. Each key corresponds to a policy name
 and value is either a function with two arguments (VFSObject) behaving
 like cmp() or a list of those functions. If value is a list, each function
 applied sequentially. Default - []""")

        _panel_plugin.EVENTS = [
            (u"before_switch_tab",
             _(u"Fires before switching to another tab. "\
               u"Arguments: Block instance and old tab index.")),

            (u"switch_tab",
             _(u"Fires when switching to another tab. "\
               u"Arguments: Block instance and new tab index.")),

            (u"new_tab",
             _(u"Fires when new tab is added. "\
               u"Arguments: Block instance and new tab index.")),

            (u"del_tab",
             _(u"Fires when tab is delete. "\
               u"Arguments: Block instance and deleted tab index.")),
            ]

        self.xyz.pm.register(_run_plugin)
        self.xyz.pm.register(_panel_plugin)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def shutdown(self, confirm=True):
        """
        Quit program
        """

        indeed = True

        if confirm:
            _q = _(u"Really quit %s?") % libxyz.const.PROG
            _title = libxyz.const.PROG

            indeed = libxyz.ui.YesNoBox(self.xyz, self.xyz.top, _q,
                                        _title).show()

        if indeed:
            self._stop = True
            self.xyz.hm.dispatch(self.EVENT_SHUTDOWN)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def repaint(self):
        """
        Repaint screen
        """

        self._resize = True
        self.xyz.screen.clear()

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

    def get_selected(self, active=True):
        """
        Get selected VFSObject instance
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.get_selected()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_tagged(self, active=True):
        """
        Return list of tagged VFSObject instances
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.get_tagged()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_untagged(self, active=True):
        """
        Return list of not tagged VFSObject instances
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.get_untagged()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_current(self, active=True):
        """
        Return VFSObject instance of selected entry
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.get_current()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_active(self):
        """
        Return list of tagged VFSObject instances or list of single selected
        object if none tagged
        """

        return self.get_tagged() or [self.get_selected()]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_all(self, active=True):
        """
        Return list of VFSObject instances in panel
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.get_all()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def toggle_tag(self, active=True):
        """
        Tag selected file
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.toggle_tag()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def tag_all(self, active=True):
        """
        Tag every single object in current dir
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.tag_all()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def untag_all(self, active=True):
        """
        Untag every single object in current dir
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.untag_all()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def tag_invert(self, active=True):
        """
        Invert currently tagged files
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.tag_invert()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def tag_rule(self, active=True):
        """
        Tag files by combined rule
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.tag_rule()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def untag_rule(self, active=True):
        """
        Untag files by combined rules
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.untag_rule()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def tag_diff(self, active=True):
        """
        Tag all the objects in active panel which are missing from the inactive
        one
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.tag_diff()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def swap_blocks(self):
        """
        Swap panel blocks
        """

        self.block1, self.block2 = self.block2, self.block1
        self._compose()

        if hasattr(self, "set_w"):
            self.set_w(self._widget)
        else:
            self._w = self._widget

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def reload(self, active=True):
        """
        Reload contents
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.reload()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def reload_all(self):
        """
        Reload both panels
        """

        self.active.reload()
        self.inactive.reload()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def action(self, active=True):
        """
        Perfrom action on selected object
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.action()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def chdir(self, path, active=True):
        """
        Change directory
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.chdir(path, active=active)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def search_forward(self):
        """
        Enable forward search-when-you-type mode
        """

        self.active.search_forward()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def search_backward(self):
        """
        Enable backward search-when-you-type mode
        """

        self.active.search_backward()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def search_cycle(self):
        """
        Enable cyclic search-when-you-type mode
        """

        self.active.search_cycle()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def show_tagged(self, active=True):
        """
        Show only tagged entries
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.show_tagged()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def select(self, name, active=True):
        """
        Select VFS object by given name in current directory
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.select(name)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def cwd(self, active=True):
        """
        Get current working directory
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.cwd

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def vfs_driver(self, active=True):
        """
        Return vfs driver used by object. None stands for LocalVFS
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.vfs_driver

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def filter(self, objects):
        """
        Filter objects
        """

        if not self.conf["filters_enabled"]:
            return objects

        policy = self.conf["filters_policy"]

        def policyf(res):
            if policy == True:
                result = not res
            else:
                result = res

            return result

        for f in self.filters:
            objects = [x for x in objects if policyf(f.match(x))]

        return objects

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def sort(self, objects):
        """
        Sort objects
        """

        policy = self.conf["sorting_policy"]

        if policy is None:
            return objects

        if policy not in self.conf["sorting"]:
            xyzlog.warning(_(u"Unable to find `%s` sorting policy") %
                           ustring(policy))
            return objects

        policy_data = self.conf["sorting"][policy]

        if is_func(policy_data):
            objects.sort(cmp=policy_data)
        elif isinstance(policy_data, list):
            for f in policy_data:
                objects.sort(cmp=f)

        return objects

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def new_tab(self, tabname=None, active=True):
        """
        Create new tab
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.tab_bar.new_tab(tabname)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def del_tab(self, index=None, active=True):
        """
        Delete tab. If index is None - delete current tab
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.tab_bar.del_tab(index)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def switch_tab(self, index, active=True):
        """
        Switch to tab
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.tab_bar.switch_tab(index)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def next_tab(self, active=True):
        """
        Switch to the next tab
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.tab_bar.next_tab()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def prev_tab(self, active=True):
        """
        Switch to the previous  tab
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.tab_bar.prev_tab()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_tabs(self, active=True):
        """
        Return list of tabs in format:
        [(path, selected_name)]
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.get_tabs()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def active_tab(self, active=True):
        """
        Get active tab index
        """

        if active:
            obj = self.active
        else:
            obj = self.inactive

        return obj.tab_bar.active_tab

#++++++++++++++++++++++++++++++++++++++++++++++++

class Block(lowui.FlowWidget):
    """
    Single panel block
    """

    def __init__(self, xyz, size, path, enc, active=False):
        """
        @param xyz: XYZData instance
        @param size: Block widget size
        @type size: L{libxyz.ui.Size}
        @param enc: Local encoding
        @param active: Boolean flag, True if block is active

        Required resources: cwdtitle, cwdtitleinact, panel, cursor, info
                            border, tagged
        """

        self.xyz = xyz
        self.size = size
        self.attr = lambda x: self.xyz.skin.attr(Panel.resolution, x)
        # Length of the string in terms of terminal columns
        self.term_width = lambda x: lowui.util.calc_width(x, 0, len(x))

        self.active = active
        self.selected = 0
        self.cwd = path

        self._display = []
        self._vindex = 0
        self._from = 0
        self._to = 0
        self._force_reload = False
        self.entries = BlockEntries(self.xyz, [])
        self._dir = None
        self._vfsobj = None
        self._title = u""
        self._tagged = []
        self._tab_data = []
        self._is_xterm = os.getenv("TERM", None) == "xterm"

        self._cursor_attr = None
        self._custom_info = None
        self._keys = libxyz.ui.Keys()
        self._cmd = self.xyz.pm.load(":sys:cmd")
        self._filter = self.xyz.pm.from_load(":sys:panel", "filter")
        self._sort = self.xyz.pm.from_load(":sys:panel", "sort")

        self._pending = libxyz.core.Queue(20)
        self._re_raw = r".*"
        self._rule_raw = ""
        self._enc = enc
        self.vfs_driver = None

        self.tab_bar = TabBar(self.xyz, self.attr, self)

        self._winfo = lowui.Text(u"")
        self._sep = libxyz.ui.Separator()

        _info = self._make_info()
        _title_attr = self._get_title_attr()

        self.frame = lowui.Frame(lowui.Filler(lowui.Text("")), footer=_info)

        self.border = libxyz.ui.Border(self.frame, self._title,
                                       _title_attr, self.attr(u"border"))
        self.block = lowui.Frame(
            lowui.AttrWrap(self.border, self.attr(u"panel")),
            header=self.tab_bar)

        self.xyz.hm.register(Panel.EVENT_BEFORE_SWITCH_TAB,
                             self._before_switch_tab_hook)
        self.xyz.hm.register(Panel.EVENT_SWITCH_TAB, self._switch_tab_hook)
        self.xyz.hm.register(Panel.EVENT_NEW_TAB, self._new_tab_hook)
        self.xyz.hm.register(Panel.EVENT_DEL_TAB, self._del_tab_hook)

        self.tab_bar.new_tab()

        self._setup(self.xyz.vfs.dispatch(path, self._enc))

        super(Block, self).__init__()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def rows(self, (maxcol,), focus=False):
        w = self.display_widget((maxcol,), focus)
        return w.rows((maxcol,), focus)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def display_widget(self, (maxcol,), focus):
        return lowui.BoxAdapter(self.block, self.size.rows)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _setup(self, vfsobj):
        _parent, _dir, _entries = vfsobj.walk()

        self._dir = _dir

        _entries = self._filter(_entries)
        _entries = self._sort(_entries)
        _entries.insert(0, _parent)

        self._title = truncate(_dir.full_path, self.size.cols - 4,
                               self._enc, True)

        if hasattr(self, "border"):
            self.border.set_title(self._title)

        self._tagged = []

        self.entries = _entries
        self._vfsobj = vfsobj
        self.vfs_driver = vfsobj.driver
        self._force_reload = True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def selectable(self):
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def render(self, (maxcol,), focus=False):
        """
        Render block
        """

        w = self.display_widget((maxcol,), focus)
        maxrow = w.rows((maxcol,), focus)

        # Reduce original sizes in order to fit into overlay
        maxcol_orig, maxcol = maxcol, maxcol - 2
        maxrow_orig, maxrow = maxrow, maxrow - 5

        # Search for pending action
        while True:
            try:
                _act = self._pending.pop()
            except IndexError:
                break
            else:
                _act(maxcol, maxrow)

        if self._custom_info is not None:
            self._set_custom_info(self._custom_info, maxcol)
        else:
            self._set_info(self.entries[self.selected], maxcol)

        _tlen = len(self._tagged)

        if _tlen > 0:
            _text = _(u"%s bytes (%d)") % (
                self._make_number_readable(
                    reduce(lambda x, y: x + y,
                           [self.entries[x].size for x in self._tagged
                            if isinstance(self.entries[x].ftype, VFSTypeFile)
                            ], 0)), _tlen)

            self._sep.set_text(bstring(_text, self._enc),
                               self.attr(u"tagged"))
        else:
            self._sep.clear_text()

        self._display = self._get_visible(maxrow, maxcol, self._force_reload)
        self._force_reload = False

        _len = len(self._display)

        canvases = []

        for i in xrange(0, _len):
            _text = self._display[i]
            _own_attr = None
            _abs_i = self._from + i

            if self._cursor_attr is not None and i == self._vindex:
                _own_attr = self._cursor_attr
            elif self.active and i == self._vindex:
                _own_attr = self.attr(u"cursor")
            elif _abs_i in self._tagged:
                _own_attr = self.attr(u"tagged")
            elif _abs_i in self.entries.palettes:
                _own_attr = self.entries.palettes[_abs_i]

            if _own_attr is not None:
                x = lowui.AttrWrap(lowui.Text(bstring(_text, self._enc)),
                                   _own_attr).render((maxcol,))
                canvases.append((x, i, False))
            else:
                canvases.append((lowui.Text(_text).render((maxcol,)),
                                 i, False))

        if _len < maxrow:
            _pad = lowui.AttrWrap(lowui.Text(" "), self.attr(u"panel"))
            canvases.append((_pad.render((maxcol,), focus), 0, False))

        _info = self._make_info()
        self.frame.set_footer(_info)

        combined = lowui.CanvasCombine(canvases)
        border = self.block.render((maxcol_orig, maxrow_orig), focus)

        if _len > maxrow:
            combined.trim_end(_len - maxrow)

        return lowui.CanvasOverlay(combined, border, 1, 2)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _make_info(self):
        _info = lowui.Padding(self._winfo, align.LEFT, self.size.cols)
        _info = lowui.AttrWrap(_info, self.attr(u"info"))
        _info = lowui.Pile([self._sep, _info])
        return _info

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

    def _get_visible(self, rows, cols, reload=False):
        """
        Get currently visible piece of entries
        """

        _from, _to, self._vindex = self._update_vindex(rows)

        if reload or ((_from, _to) != (self._from, self._to)):
            self._from, self._to = _from, _to
            self._display = []

            for _obj in self.entries[self._from:self._to]:
                _text = "%s%s "% (_obj.vtype, _obj.name)
                _text = truncate(_text, cols, self._enc)
                self._display.append(_text)

        return self._display

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
        _part1 = truncate(vfsobj.visual, cols - len(_part2) - 2, self._enc)

        _text = u"%s%s%s" % (_part1,
                             u" " * (cols - (self.term_width(_part1) +
                                             self.term_width(_part2)) -
                                     1), _part2)

        self._winfo.set_text(bstring(_text, self._enc))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _set_custom_info(self, custom_text, cols):
        """
        Set custom info text
        """

        _text = truncate(custom_text, cols, self._enc, True)
        self._winfo.set_text(bstring(_text, self._enc))

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
        self.chdir(self._dir.path, reload=False)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def next(self):
        """
        Next entry
        """

        if self.selected < self.entries.length - 1:
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

        self.selected = self.entries.length - 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def block_next(self):
        """
        One block down
        """

        def _do_next_block(cols, rows):
            if self.selected + rows >= self.entries.length:
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
        Get selected VFSObject instance
        """

        return self.entries[self.selected]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_current(self):
        """
        Get VFSObject instance of current directory
        """

        return self._vfsobj

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_all(self):
        """
        Return list of VFSObject instances in panel
        """

        return self.entries

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_tagged(self):
        """
        Return list of tagged VFSObject instances
        """

        return [self.entries[x] for x in self._tagged]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_untagged(self):
        """
        Return list of not tagged VFSObject instances
        """

        return [self.entries[x] for x in xrange(self.entries.length)
                if x not in self._tagged]

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
    def tag_rule(self):
        """
        Tag files by combined rule
        """

        self._tag_rule(tag=True)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def untag_rule(self):
        """
        Untag files by combined rule
        """

        self._tag_rule(tag=False)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _tag_rule(self, tag=True):
        """
        Tag engine
        """

        if tag:
            _title = _(u"Tag group")
        else:
            _title = _(u"Untag group")

        _input = libxyz.ui.InputBox(self.xyz, self.xyz.top,
                                    _("Type FS Rule"),
                                    title=_title, text=self._rule_raw)

        _raw = _input.show()

        if _raw is None:
            return
        else:
            self._rule_raw = _raw

        try:
            _rule = libxyz.core.FSRule(ustring(_raw, self._enc))
        except libxyz.exceptions.ParseError, e:
            xyzlog.error(unicode(e))
            return

        try:
            if tag:
                self._tagged = [i for i in xrange(self.entries.length) if
                                _rule.match(self.entries[i])]
            else:
                self._tagged = [i for i in self._tagged if not
                               _rule.match(self.entries[i])]
        except libxyz.exceptions.FSRuleError, e:
            self._tagged = []

            xyzlog.error(unicode(e))
            return

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def tag_invert(self):
        """
        Invert currently tagged files
        """

        self._tagged = [i for i in xrange(self.entries.length)
                        if i not in self._tagged]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def tag_all(self):
        """
        Tag every single object in current dir
        """

        self._tagged = [i for i in xrange(self.entries.length) if
                        self.entries[i].name != ".."]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def untag_all(self):
        """
        Untag every single object in current dir
        """

        self._tagged = []

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def tag_diff(self):
        """
        Tag all the objects in active panel which are missing from the inactive
        one
        """

        inactive_names = [x.name for x in
                          self.xyz.pm.from_load(":sys:panel", "get_all")(
                              active=False)]

        self._tagged = [i for i in xrange(self.entries.length) if
                        self.entries[i].name not in inactive_names]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def reload(self):
        """
        Reload contents
        """

        _selected = self.entries[self.selected]

        self._setup(self._vfsobj)

        if self.selected >= self.entries.length:
            self.selected = self.entries.length - 1

        # Try to find previously selected object
        if self.entries[self.selected].name != _selected.name:
            self.select(_selected.name)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def select(self, name):
        """
        Select VFS object by given name in current directory
        """

        for i in xrange(self.entries.length):
            if self.entries[i].name == name:
                self.selected = i
                break

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def action(self):
        """
        Perform action on selected file
        """

        _selected = self.entries[self.selected]
        _action = self.xyz.am.match(_selected)

        if _action is not None:
            try:
                _action(_selected)
            except Exception, e:
                xyzlog.error(_(u"Action error: %s") % (unicode(e)))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def chdir(self, path, reload=True, active=True):
        """
        Change directory
        If reload is not True only execute os.chdir, without reloading
        directory contents
        If active is False do not call os.chdir
        """

        try:
            old_selected = self.entries[self.selected].name
        except IndexError:
            old_selected = None

        if reload:
            _path = os.path.normpath(path)
            _parent = None
            _old_vfs = None

            if self.entries:
                _parent = os.path.normpath(self.entries[0].full_path)
                _old = self._dir.name
                _old_vfs = self._vfsobj

            try:
                _vfsobj = self.xyz.vfs.dispatch(path, self._enc)
            except libxyz.exceptions.VFSError, e:
                xyzlog.error(_(u"Unable to chdir to %s: %s") %
                             (ustring(path), ustring(e)))
                return

            try:
                self._setup(_vfsobj)
            except libxyz.exceptions.XYZRuntimeError, e:
                xyzlog.info(_(u"Unable to chdir to %s: %s") %
                            (ustring(path), ustring(e)))
                return

            self.selected = 0

            # We've just stepped out from dir, try to focus on it
            if _parent == _path:
                for x in xrange(self.entries.length):
                    if self.entries[x].name == _old:
                        self.selected = x
                        break

            if _old_vfs:
                del(_old_vfs)

        self.cwd = path
        self._tab_data[self.tab_bar.active_tab] = (path, old_selected)

        if path == os.path.sep:
            new_tab_name = path
        else:
            new_tab_name = os.path.basename(path)

        self.tab_bar.rename_tab(self.tab_bar.active_tab,
                                truncate(new_tab_name, 15, self._enc))

        # Call chdir only for local objects
        if isinstance(self._vfsobj, LocalVFSObject) and active:
            os.chdir(path)

        self._update_xterm_title(path)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def search_forward(self):
        """
        Search forward for matching object while user types
        """

        return self._search_engine(lambda x: (xrange(x, self.entries.length)))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def search_backward(self):
        """
        Search backward for matching object while user types
        """

        return self._search_engine(lambda x: (xrange(x, 0, -1)))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def search_cycle(self):
        """
        Search from current position downwards and then from top to
        currently selected
        """

        return self._search_engine(lambda x: range(x, self.entries.length) +
                                             range(0, x))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def show_tagged(self):
        """
        Show only tagged entries
        """

        if not self._tagged:
            return

        self.entries = BlockEntries(self.xyz,
                                    [self.entries[x] for x in self._tagged])
        self.selected = 0
        self._tagged = []

        _tagged = _(u"TAGGED")

        if not self._title.endswith(_tagged):
            self._title = truncate(u"%s:%s" % (self._title, _tagged),
                                   self.size.cols - 4, self._enc, True)

            if hasattr(self, "border"):
                self.border.set_title(self._title)

        self._force_reload = True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _search_engine(self, order, pattern=None):
        """
        Search for matching filenames while user types
        @param order: A function that returns generator for search order
        @param pattern: A search type pattern
        """

        self._cursor_attr = self.attr(u"search")

        if pattern is None:
            # Search everywhere in object name
            pattern = lambda pat, obj: ustring(pat) in ustring(obj)
            # Search from the beginning of object name
            #pattern = lambda pat, obj: obj.startswith(pat)

        _dim = self.xyz.screen.get_cols_rows()
        _collected = []

        _current_pos = self.selected
        _current_pos_orig = self.selected
        _skip = False

        # Starting internal read loop
        while True:
            self._custom_info = u"".join(_collected)

            self._invalidate()
            self.xyz.screen.draw_screen(_dim, self.xyz.top.render(_dim, True))

            try:
                _raw = self.xyz.input.get()

                if self.xyz.input.WIN_RESIZE in _raw:
                    _dim = self.xyz.screen.get_cols_rows()
                    continue

                if self._keys.ESCAPE in _raw or self._keys.ENTER in _raw:
                    self._invalidate()
                    break
                elif self._keys.BACKSPACE in _raw:
                    _current_pos = _current_pos_orig
                    if _collected:
                        _collected.pop()
                # Continue search
                elif self._keys.DOWN in _raw:
                    _skip = True

                _tmp = _collected[:]
                _tmp.extend([ustring(x, self._enc) for x in _raw
                             if len(x) == 1])
                _pattern = u"".join(_tmp)
            except Exception:
                break

            # Search
            for i in order(_current_pos):
                if pattern(_pattern, self.entries[i].name):
                    if _skip:
                        _skip = False
                        _current_pos  = i + 1
                        continue

                    self.selected = i
                    _collected = _tmp
                    break

        self._cursor_attr = None
        self._custom_info = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _before_switch_tab_hook(self, block, index):
        """
        Before switch tab hook
        """

        # It's for other block
        if block is not self:
            return

        try:
            # Save position
            path = self._tab_data[index][0]
            self._tab_data[index] = (path, self.entries[self.selected].name)

            self.chdir(path)
        except IndexError:
            pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _switch_tab_hook(self, block, index):
        """
        Switch tab hook
        """

        # It's for other block
        if block is not self:
            return

        try:
            path, name = self._tab_data[index]

            self.chdir(path)

            if name is not None:
                self.select(name)
        except IndexError:
            pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _new_tab_hook(self, block, _index):
        """
        New tab hook
        """

        # It's for other block
        if block is not self:
            return

        try:
            selected = self.entries[self.selected].name
        except IndexError:
            selected = None

        self._tab_data.append((self.cwd, selected))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _del_tab_hook(self, block, index):
        """
        Delete tab hook
        """

        # It's for other block
        if block is not self:
            return

        try:
            del(self._tab_data[index])
        except IndexError:
            pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_tabs(self):
        """
        Return list of open tabs
        """

        return self._tab_data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _update_xterm_title(self, title):
        """
        Update xterm title string
        """

        if self._is_xterm:
            sys.stdout.write("\33]2;%s\7" % title)

#++++++++++++++++++++++++++++++++++++++++++++++++

class TabBar(lowui.FlowWidget):
    """
    Tabs bar
    """

    def __init__(self, xyz, attr, block):
        self.xyz = xyz
        self.block = block
        self._attr = attr
        self.term_width = lambda x: lowui.util.calc_width(x, 0, len(x))

        self._active_tab = 0
        self._tabs = []

        super(TabBar, self).__init__()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    active_tab = property(lambda self: self._active_tab)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def new_tab(self, tabname=None):
        """
        Add new tab
        """

        if tabname is None:
            tabname = "Tab"

        self._tabs.append(tabname)
        newidx = len(self._tabs) - 1

        self.xyz.hm.dispatch(Panel.EVENT_NEW_TAB, self.block, newidx)
        self.switch_tab(newidx)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def del_tab(self, index=None):
        """
        Delete tab by index
        """

        if index is None:
            index = self._active_tab

        _len = len(self._tabs)

        if _len > 1 and index < _len:
            del(self._tabs[index])

            if self._active_tab >= len(self._tabs):
                self._active_tab -= 1

            self.xyz.hm.dispatch(Panel.EVENT_DEL_TAB, self.block, index)

            self.switch_tab(self._active_tab)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def switch_tab(self, index):
        """
        Switch to tab by index
        """

        if index < len(self._tabs):
            self.xyz.hm.dispatch(Panel.EVENT_BEFORE_SWITCH_TAB, self.block,
                                 self._active_tab)
            self._active_tab = index
            self.xyz.hm.dispatch(Panel.EVENT_SWITCH_TAB, self.block,
                                 self._active_tab)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def next_tab(self):
        """
        Switch to the next tab
        """

        index = self._active_tab + 1

        if index >= len(self._tabs):
            index = 0

        self.switch_tab(index)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def prev_tab(self):
        """
        Switch to the previous  tab
        """

        index = self._active_tab - 1

        if index < 0:
            index = len(self._tabs) - 1

        self.switch_tab(index)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @refresh
    def rename_tab(self, index, new_name):
        """
        Rename tab at index
        """

        if index >= len(self._tabs):
            return
        else:
            self._tabs[index] = new_name

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def render(self, (maxcol,), focus=False):
        """
        Render the tab bar
        """

        make_c = lambda text, at: lowui.AttrWrap(
            lowui.Text(text), self._attr(at)).render((maxcol,))

        canvases = []
        length = 0

        for idx in xrange(len(self._tabs)):
            tabname = self._gen_tab_name(self._tabs[idx], idx)
            length += self.term_width(tabname)

            if idx == self._active_tab:
                canv = make_c(tabname, "tabact")
            else:
                canv = make_c(tabname, "tabbar")

            canvases.append((canv, None, False, self.term_width(tabname)))

        if length < maxcol:
            canvases.append((make_c("", "tabbar"), None, False,
                             maxcol - length))

        combined = lowui.CanvasJoin(canvases)

        if length > maxcol:
            more = lowui.AttrWrap(
                lowui.Text(" >>"),
                self._attr("tabbar")).render((3,))

            combined.pad_trim_left_right(0, -(length - maxcol))
            combined.overlay(more, maxcol - 3, 0)

        return combined

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def rows(self, (maxcol,), focus=False):
        """
        Return the number of lines that will be rendered
        """

        return 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _gen_tab_name(self, tab, idx):
        return "{%d %s} " % (idx, tab)
