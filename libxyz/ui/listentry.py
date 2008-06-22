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

class ListEntry(lowui.FlowWidget):
    """
    List entry
    """

    def __init__(self, msg, selected_attr, entry_attr=None):
        """
        @param msg: Message
        @param selected_attr: Atrribute of selected entry
        @param entry_attr: Entry text attribute
        @param write_time: Whether to write timestamp in entry
        """

        super(ListEntry, self).__init__()

        self._text = msg
        self._sel_attr = selected_attr
        self._entry_attr = entry_attr
        self._content = lowui.Text(self._text)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def selectable(self):
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def rows(self, (maxcol,), focus=False):
        return len(self._content.get_line_translation(maxcol))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def render(self, (maxcol,), focus=False):
        if focus:
            self._content.set_text((self._sel_attr, self._text))
        else:
            if self._entry_attr is not None:
                self._content.set_text((self._entry_attr, self._text))
            else:
                self._content.set_text(self._text)

        return self._content.render((maxcol,), focus)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def keypress(self, (maxcol,), key):
        return key
