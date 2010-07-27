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

import libxyz.ui as uilib

from libxyz.ui import lowui
from libxyz.ui.utils import truncate
from libxyz.core.utils import ustring

class PluginEntry(lowui.FlowWidget):
    """
    Plugins list entry
    """

    def __init__(self, plugin, selected_attr, enter_cb):
        super(PluginEntry, self).__init__()

        self.plugin = plugin
        self.enter_cb = enter_cb

        self._keys = uilib.Keys()

        self._text = u"%s%*s - %s"

        self._attr = selected_attr
        self._content = lowui.Text(self._text)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def selectable(self):
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def rows(self, (maxcol,), focus=False):
        return 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def render(self, (maxcol,), focus=False):
        percent = lambda per, total: int((total / 100.0) * per)

        _pad = percent(35, maxcol) - len(self.plugin.ns)

        _text = self._text % (self.plugin.ns, _pad,
                              self.plugin.VERSION,
                              self.plugin.BRIEF_DESCRIPTION)

        if len(_text) >= maxcol:
            _text = truncate(_text, maxcol, xyzenc)

        if focus:
            self._content.set_text((self._attr, _text))
        else:
            self._content.set_text(_text)

        return self._content.render((maxcol,), focus)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def keypress(self, (maxcol,), key):
        if key == self._keys.ENTER:
            try:
                self.enter_cb()
            except Exception, e:
                xyzlog.error(_(u"Error in entry callback: %s" %
                           unicode(e)))
                xyzlog.debug(ustring(traceback.format_exc()))
        else:
            return key
