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
from libxyz.ui import Prompt

class Cmd(lowui.FlowWidget):
    """
    Command line widget
    """

    resolution = (u"cmd",)

    def __init__(self, xyz, prompt=u""):
        """
        @param xyz: XYZData instance
        @param prompt: prompt text

        Resources used: text, prompt
        """

        super(Cmd, self).__init__()

        self._attr = lambda x: xyz.skin.attr(self.resolution, x)

        self.prompt = Prompt(prompt, self._attr(u"prompt"))

        self._text_attr = self._attr(u"text")
        self._data = []

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
        # First lookup for bind in default context
        _meth = self.xyz.km.process(key)

        if _meth is not None:
            _meth()
        else:
            self._data.extend(key)
            self._invalidate()
