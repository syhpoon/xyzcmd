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

from libxyz.ui import lowui
from libxyz.ui.utils import term_width

class Separator(lowui.FlowWidget):
    """
    Horizontal separator widget
    """

    ignore_focus = True

    def __init__(self, title=None, div_char=None, title_attr=None,
                 div_attr=None, top=0, bottom=0):
        """
        @param title: Title
        @param div_char: Character to repeat across line
        @param title_attr: Attribute of title text
        @param div_attr: Attribute of divider line
        @param top: number of blank lines above
        @param bottom: number of blank lines below
        """

        super(Separator, self).__init__()

        self.set_text(title, title_attr)

        self.div_char = "─".decode("utf-8")
        self.div_attr = div_attr
        self.top = top
        self.bottom = bottom

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_text(self, title, title_attr=None):
        """
        Set some text in the middle of seprator
        """

        if title is not None:
            _title = " %s " % title
            self.title_len = term_width(_title)

            if title_attr is not None:
                self.text = lowui.Text((title_attr, _title))
            else:
                self.text = lowui.Text(_title)
        else:
            self.text = None
            self.title_len = 0

        self._invalidate()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def clear_text(self):
        """
        Remove text if any
        """

        self.text = None
        self.title_len = 0

        self._invalidate()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def rows(self, (maxcol,), focus=False):
        """
        Return the number of lines that will be rendered.
        """

        return self.top + 1 + self.bottom

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def render(self, (maxcol,), focus=False):
        """
        Render the separator as canvas and return it.
        """

        sep_len = (maxcol - self.title_len) / 2
        _len = sep_len * 2 + self.title_len

        if _len != maxcol:
            _offset = abs(maxcol - _len)
        else:
            _offset = 0

        _list = []

        canv_begin = lowui.Text((self.div_attr, self.div_char * sep_len))
        canv_begin = canv_begin.render((maxcol,))
        _list.append((canv_begin, None, False, sep_len))

        if self.text is not None:
            canv_text = self.text.render((maxcol,))
            _list.append((canv_text, None, False, self.title_len))

        canv_end = lowui.Text((self.div_attr, self.div_char *(sep_len+_offset)))
        canv_end = canv_end.render((maxcol,))
        _list.append((canv_end, None, False, sep_len + _offset))

        canv = lowui.CanvasJoin(_list)

        if self.top or self.bottom:
            canv.pad_trim_top_bottom(self.top, self.bottom)

        return canv
