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
import libxyz.ui

class ListEntry(lowui.FlowWidget):
    """
    List entry
    """

    def __init__(self, msg, selected_attr, entry_attr=None):
        """
        @param msg: Message
        @param selected_attr: Atrribute of selected entry
        @param entry_attr: Entry text attribute
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class NumEntry(ListEntry):
    """
    Entry in list box which can be activated by pressing corresponding number
    """

    def __init__(self, msg, selected_attr, num_order, entry_attr=None,
                 enter_cb=None):
        """
        @param msg: Message
        @param selected_attr: Atrribute of selected entry
        @param entry_attr: Entry text attribute
        @param num_order: Entry number
        @param enter_cb: Callback to be executed upon ENTER pressed
        """

        self._num = []

        if callable(enter_cb):
            self._enter_cb = enter_cb
        else:
            self._enter_cb = None

        self.num_order = num_order
        self._keys = libxyz.ui.Keys()
        _msg = u"%d: %s" % (num_order, msg)

        super(NumEntry, self).__init__(_msg, selected_attr, entry_attr)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def keypress(self, (maxcol,), key):
        if key == self._keys.ENTER and callable(self._enter_cb):
            if self._num:
                _index = int("".join(self._num))
                self._num = []
            else:
                _index = self.num_order
            try:
                self._enter_cb(_index)
            except Exception, e:
                xyzlog.log(_(u"Error in entry callback: %s" %
                           str(e)), xyzlog.loglevel.ERROR)
                xyzlog.log(traceback.format_exc().decode(xyzenc),
                           xyzlog.loglevel.DEBUG)
            finally:
                return key
        elif key.isdigit():
            self._num.append(key)
        else:
            return key
