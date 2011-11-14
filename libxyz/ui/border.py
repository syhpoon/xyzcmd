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
from libxyz.ui import align

from libxyz.exceptions import UIError

class Border(lowui.BoxWidget):
    def __init__(self, widget, title=None, title_attr=None, attr=None):
        """
        Draw a line border around widget and set up a title
        @param widget: Widget to wrap
        @param title: Title
        @type title: libxyz.ui.lowui.Text object
        @param title_attr: Title attribute
        @param attr: Attribute of border
        """

        super(Border, self).__init__()

        self.widget = widget
        self.title = title
        self.title_attr = title_attr
        self.attr = attr
        self._attr = self.attr

        self.tline = self._get_attr(lowui.Divider("─".decode("utf-8")))
        self.bline = self._get_attr(lowui.Divider("─".decode("utf-8")))
        self.lline = self._get_attr(lowui.SolidFill("│".decode("utf-8")))
        self.rline = self._get_attr(lowui.SolidFill("│".decode("utf-8")))

        self.tlcorner = self._get_attr(lowui.Text("┌".decode("utf-8")))
        self.trcorner = self._get_attr(lowui.Text("┐".decode("utf-8")))
        self.blcorner = self._get_attr(lowui.Text("└".decode("utf-8")))
        self.brcorner = self._get_attr(lowui.Text("┘".decode("utf-8")))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def render(self, (maxcol, maxrow), focus=False):
        """
        Render widget
        """

        if self.title is not None:
            _len = lowui.util.calc_width(self.title, 0, len(self.title))

            if self.title_attr is not None:
                self._title = lowui.AttrWrap(lowui.Text(" %s " % self.title,
                                             align.CENTER), self.title_attr)
            else:
                self._title = lowui.Text(self.title, align.CENTER)

            _len += 2 # " text "

        tline_widgets = [('fixed', 1, self.tlcorner), self.tline]

        if self.title is not None:
            tline_widgets.append(("fixed", _len, self._title))

        tline_widgets.extend([self.tline, ("fixed", 1, self.trcorner)])

        self.top = lowui.Columns(tline_widgets)
        self.middle = lowui.Columns([('fixed', 1, self.lline),
                                    self.widget, ('fixed', 1, self.rline)],
                                    box_columns=[0,2], focus_column=1)

        self.bottom = lowui.Columns([('fixed', 1, self.blcorner),
                                    self.bline, ('fixed', 1, self.brcorner)])

        self.pile = lowui.Pile([('flow',self.top), self.middle,
                               ('flow', self.bottom)], focus_item=1)

        return self.pile.render((maxcol, maxrow), focus)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _get_attr(self, widget):
        if self.attr is None:
            return widget

        return lowui.AttrWrap(widget, self.attr)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_title_attr(self, attr):
        """
        Set title attribute
        """

        self.title_attr = attr
        self._invalidate()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_title(self, text):
        """
        Set title
        """

        self.title = text
        self._invalidate()
