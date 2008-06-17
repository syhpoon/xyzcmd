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

        self._init_plugin()

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
        _cmd_plugin.export(u"clear", self.clear)

        self.xyz.pm.register(_cmd_plugin)

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

        return self.prompt.length() + len(self._data), 0

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
            self._data.extend(key)
            self._invalidate()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Public methods

    def del_char(self):
        """
        Delete single character
        """

        if self._data:
            del(self._data[-1])
            self._invalidate()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def clear(self):
        """
        Clear cmd line
        """

        self._data = []
        self._invalidate()
