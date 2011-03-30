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

import traceback

from libxyz.core.utils import ustring
from libxyz.ui import lowui
from libxyz.vfs import VFSObject

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

    text = property(lambda self: self._text)

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

        self.msg = msg
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
                xyzlog.error(_(u"Error in entry callback: %s") %
                             unicode(e))
                xyzlog.debug(ustring(traceback.format_exc()))

            return key
        elif key.isdigit():
            self._num.append(key)
        else:
            return key

#++++++++++++++++++++++++++++++++++++++++++++++++

class BlockEntries(list):
    """
    Wrapper for list of block entries
    """

    def __init__(self, xyz, data, trans=None):
        self.xyz = xyz
        self.length = len(data)
        self.palettes = {}

        if callable(trans):
            self.trans = trans
        else:
            self.trans = lambda x: x

        try:
            self._rules = self.xyz.skin["fs.rules"]
        except KeyError:
            self._rules = {}

        super(BlockEntries, self).__init__(data)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def insert(self, idx, obj):
        list.insert(self, idx, obj)
        self._set_palette(idx, obj)
        self.length = len(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __getslice__(self, i, j):
        if j > self.length:
            j = self.length

        return [self[x] for x in range(i, j)]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __getitem__(self, idx):
        item = list.__getitem__(self, idx)

        if not isinstance(item, VFSObject):
            item = self.xyz.vfs.dispatch(self.trans(item))

            self[idx] = item
            self._set_palette(idx, item)

        return item

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __iter__(self):
        for i in xrange(self.length):
            yield self[i]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _set_palette(self, idx, item):
        for _exp, _attr in self._rules.iteritems():
            if _exp.match(item):
                self.palettes[idx] = _attr.name
                break

