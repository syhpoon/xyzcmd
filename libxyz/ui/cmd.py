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

import copy

import libxyz.core

from libxyz.ui import lowui
from libxyz.ui import Prompt

class Cmd(lowui.FlowWidget):
    """
    Command line widget
    """

    resolution = (u"cmd",)
    context = u"CMD"

    def __init__(self, xyz, prompt=u""):
        """
        @param xyz: XYZData instance
        @param prompt: prompt text

        Resources used: text, prompt
        """

        super(Cmd, self).__init__()

        self.xyz = xyz
        self._attr = lambda x: xyz.skin.attr(self.resolution, x)

        self.prompt = Prompt(prompt, self._attr(u"prompt"))

        self._text_attr = self._attr(u"text")
        self._data = []
        self._index = 0

        self._plugin = self._init_plugin()

        try:
            _conf = self.xyz.conf[u"plugins"]
            self._undo_depth = _conf[self._plugin.ns.pfull][u"undo_depth"]
        except KeyError:
            # Default value
            self._undo_depth = 10

        self._undo = libxyz.core.Queue(self._undo_depth)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _init_plugin(self):
        """
        Init virtual plugin
        """

        _cmd_plugin = libxyz.core.plugins.VirtualPlugin(self.xyz, u"cmd")
        _cmd_plugin.AUTHOR = u"Max E. Kuznecov <mek@mek.uz.ua>"
        _cmd_plugin.VERSION = u"0.1"
        _cmd_plugin.BRIEF_DESCRIPTION = u"Command line plugin"

        _cmd_plugin.export(u"del_char", self.del_char)
        _cmd_plugin.export(u"del_char_left", self.del_char_left)
        _cmd_plugin.export(u"clear", self.clear)
        _cmd_plugin.export(u"clear_left", self.clear_left)
        _cmd_plugin.export(u"clear_right", self.clear_right)
        _cmd_plugin.export(u"cursor_begin", self.cursor_begin)
        _cmd_plugin.export(u"cursor_end", self.cursor_end)
        _cmd_plugin.export(u"cursor_left", self.cursor_left)
        _cmd_plugin.export(u"cursor_right", self.cursor_right)
        _cmd_plugin.export(u"cursor_word_left", self.cursor_word_left)
        _cmd_plugin.export(u"cursor_word_right", self.cursor_word_right)
        _cmd_plugin.export(u"is_empty", self.is_empty)
        _cmd_plugin.export(u"undo", self.undo)

        self.xyz.pm.register(_cmd_plugin)

        return _cmd_plugin

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def selectable(self):
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def rows(self, (maxcol,), focus=False):
        """
        Return the number of lines that will be rendered
        """

        return 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def render(self, (maxcol,), focus=False):
        """
        Render the command line
        """

        #TODO: cmd swap

        if self.prompt is not None:
            _canv_prompt = self.prompt.render((maxcol,))
        else:
            _canv_prompt = lowui.Text(u"").render((maxcol,))

        _totalsize = self.prompt.length() + len(self._data)

        if _totalsize > maxcol:
            _data = self._data[:maxcol]
        else:
            _data = self._data

        _text_len = maxcol - self.prompt.length()

        _canv_text = lowui.TextCanvas(text=["".join(_data)],
                                      attr=[[(self._text_attr, _text_len)]],
                                      maxcol=maxcol)

        canv = lowui.CanvasJoin(
                                [
                                 (_canv_prompt, None, False,
                                  self.prompt.length()),
                                 (_canv_text, 0, True, _text_len),
                                ]
                               )

        canv.cursor = self.get_cursor_coords((maxcol,))

        return canv

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_cursor_coords(self,(maxcol,)):
        """
        Return the (x,y) coordinates of cursor within widget.
        """

        return self.prompt.length() + self._index, 0

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def keypress(self, size, key):
        # First lookup for bind in own context
        _meth = self.xyz.km.process(key, self.context)

        if _meth is not None:
            _meth()
            return

        # Next in default one
        _meth = self.xyz.km.process(key)

        if _meth is not None:
            _meth()
            return
        else:
            # TODO: filter out control codes
            self._data.insert(self._index, *key)
            self._index += len(key)
            self._invalidate()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _save_undo(self):
        """
        Save undo data
        """

        self._undo.push((self._index, copy.copy(self._data)))

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _restore_undo(self):
        """
        Restore one undo level
        """

        if self._undo:
            self._index, self._data = self._undo.pop()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Public methods

    def del_char_left(self):
        """
        Delete single character left to the cursor
        """

        if self._index > 0:
            self._index -= 1
            del(self._data[self._index])
            self._invalidate()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def del_char(self):
        """
        Delete single character under the cursor
        """

        if self._index > 0 and self._index < len(self._data):
            del(self._data[self._index])
            self._invalidate()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def del_word_left(self):
        """
        Delete a word left to the cursor
        """

        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def del_word_right(self):
        """
        Delete a word right to the cursor
        """

        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def clear(self):
        """
        Clear the whole cmd line
        """

        self._save_undo()
        self._data = []
        self._index = 0
        self._invalidate()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def clear_left(self):
        """
        Clear the cmd line from the cursor to the left
        """

        self._save_undo()
        self._data = self._data[self._index:]
        self._index = 0
        self._invalidate()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def clear_right(self):
        """
        Clear the cmd line from the cursor to the right
        """

        self._save_undo()
        self._data = self._data[:self._index]
        self._invalidate()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def cursor_begin(self):
        """
        Move cursor to the beginning of the command line
        """

        self._index = 0
        self._invalidate()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def cursor_end(self):
        """
        Move cursor to the end of the command line
        """

        self._index = len(self._data)
        self._invalidate()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def cursor_left(self):
        """
        Move cursor left
        """

        if self._index > 0:
            self._index -= 1
            self._invalidate()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def cursor_right(self):
        """
        Move cursor right
        """

        if self._index < len(self._data):
            self._index += 1
            self._invalidate()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def cursor_word_left(self):
        """
        Move cursor one word left
        """

        for i in range(self._index - 1, 0, -1):
            if self._data[i].isspace():
                self._index = i
                self._invalidate()
                return

        return self.cursor_begin()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def cursor_word_right(self):
        """
        Move cursor one word right
        """

        for i in range(self._index + 1, len(self._data)):
            if self._data[i].isspace():
                self._index = i
                self._invalidate()
                return

        return self.cursor_end()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def execute(self):
        """
        Execute cmd contents
        """

        # TODO:
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def is_empty(self):
        """
        Return True if cmd is empty, i.e. has no contents
        """

        return self._data == []

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def undo(self):
        """
        Restore one level from undo buffer
        """

        self._restore_undo()
        self._invalidate()

    #TODO:
    #clear_word_left
    #clear_word_right
    #command-history
    #completion
