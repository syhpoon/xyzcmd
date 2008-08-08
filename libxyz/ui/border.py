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

class Border(lowui.WidgetWrap):
    def __init__(self, widget, title=None, attr=None):
        """
        Draw a line border around widget and set up a title
        @param widget: Widget to wrap
        @param title: (title, attribute) tuple or basestring
        @type title: libxyz.ui.lowui.Text object
        @param attr: Attribute of border
        """

        utf8decode = lowui.escape.utf8decode

        self._title = None

        if title is not None:
            if isinstance(title, tuple):
                _len = len(title[0])
                self._title = lowui.AttrWrap(lowui.Text(" %s " % title[0],
                                             align.CENTER), title[1])
            elif isinstance(title, basestring):
                _len = len(title)
                self._title = lowui.Text(title, align.CENTER)
            else:
                raise UIError(_(u"Invalid title type %s. "\
                                u"Tuple or basetring expected" %
                                type(self._title)))

            _len += 2 # " text "

        self.attr = attr

        self.tline = self._attr(lowui.Divider(utf8decode("─")))
        self.bline = self._attr(lowui.Divider(utf8decode("─")))
        self.lline = self._attr(lowui.SolidFill(utf8decode("│")))
        self.rline = self._attr(lowui.SolidFill(utf8decode("│")))

        self.tlcorner = self._attr(lowui.Text(utf8decode("┌")))
        self.trcorner = self._attr(lowui.Text(utf8decode("┐")))
        self.blcorner = self._attr(lowui.Text(utf8decode("└")))
        self.brcorner = self._attr(lowui.Text(utf8decode("┘")))

        tline_widgets = [('fixed', 1, self.tlcorner), self.tline]

        if title is not None:
            tline_widgets.append(("fixed", _len, self._title))

        tline_widgets.extend([self.tline, ("fixed", 1, self.trcorner)])

        self.top = lowui.Columns(tline_widgets)
        self.middle = lowui.Columns([('fixed', 1, self.lline),
                                    widget, ('fixed', 1, self.rline)],
                                    box_columns=[0,2], focus_column=1)

        self.bottom = lowui.Columns([('fixed', 1, self.blcorner),
                                    self.bline, ('fixed', 1, self.brcorner)])

        self.pile = lowui.Pile([('flow',self.top), self.middle,
                               ('flow', self.bottom)], focus_item=1)

        super(Border, self).__init__(self.pile)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _attr(self, widget):
        if self.attr is None:
            return widget

        return lowui.AttrWrap(widget, self.attr)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_title_attr(self, attr):
        """
        """

        self._title.set_attr(attr)
